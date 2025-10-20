"""
ClaudeMCP Remote Script - Thread-Safe Socket Server for LiveAPI Communication
Ableton Live Remote Script that receives commands via TCP port 9004
and executes LiveAPI operations in the main thread using a queue-based approach.

Author: Claude Code
License: MIT
"""

import Live
import socket
import threading
import json
import sys
import traceback
try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3
from .liveapi_tools import LiveAPITools


class ClaudeMCP:
    """
    Main Remote Script class loaded by Ableton Live

    Uses a queue-based approach to ensure thread safety:
    1. Socket threads receive commands and add them to command_queue
    2. update_display() (main thread) processes commands from queue
    3. Results are put in response_queue for socket threads to retrieve
    """

    def __init__(self, c_instance):
        """
        Initialize the Remote Script

        Args:
            c_instance: The ControlSurface instance provided by Live
        """
        self.c_instance = c_instance
        self.song = c_instance.song()

        # Initialize LiveAPI tools
        self.tools = LiveAPITools(self.song, self.c_instance)

        # Thread-safe queues for command processing
        self.command_queue = queue.Queue()  # Commands from socket threads
        self.response_queues = {}  # {request_id: Queue} for responses
        self.request_counter = 0
        self.request_lock = threading.Lock()

        # Socket server state
        self.socket_server = None
        self.socket_thread = None
        self.running = False

        # Start socket server
        self.start_socket_server()

        self.log("ClaudeMCP Remote Script initialized (Queue-based, Thread-Safe)")
        self.log("Socket server listening on port 9004")

    def log(self, message):
        """Log message to Ableton's Log.txt"""
        self.c_instance.log_message("[ClaudeMCP] " + str(message))

    def start_socket_server(self):
        """Start the socket server in a background thread"""
        try:
            self.running = True
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_server.bind(('127.0.0.1', 9004))
            self.socket_server.listen(5)

            # Start listening thread
            self.socket_thread = threading.Thread(target=self._socket_listener)
            self.socket_thread.daemon = True
            self.socket_thread.start()

            self.log("Socket server started successfully on port 9004")
        except Exception as e:
            self.log("ERROR starting socket server: " + str(e))
            self.log(traceback.format_exc())

    def _socket_listener(self):
        """Background thread that listens for client connections"""
        while self.running:
            try:
                client_socket, address = self.socket_server.accept()
                self.log("Client connected from " + str(address))

                # Spawn a new thread for each client
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()

            except Exception as e:
                if self.running:
                    self.log("Socket listener error: " + str(e))

    def _handle_client(self, client_socket):
        """
        Handle commands from a connected client (runs in socket thread)

        This method DOES NOT call LiveAPI directly - instead it:
        1. Receives commands from socket
        2. Puts them in command_queue
        3. Waits for response from response_queue
        4. Sends response back to socket
        """
        buffer = ""

        try:
            client_socket.settimeout(30.0)  # Increased timeout

            while self.running:
                try:
                    # Read data from socket
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    # Decode data
                    decoded = data.decode('utf-8')
                    buffer += decoded

                    # Process complete messages (terminated by newline)
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        message = message.strip()

                        if message:
                            # Generate unique request ID
                            with self.request_lock:
                                request_id = self.request_counter
                                self.request_counter += 1
                                # Create response queue for this request
                                self.response_queues[request_id] = queue.Queue()

                            try:
                                # Parse command
                                command = json.loads(message)

                                # Put command in queue for main thread to process
                                self.command_queue.put((request_id, command))

                                # Wait for response from main thread (with timeout)
                                try:
                                    response = self.response_queues[request_id].get(timeout=25.0)
                                except queue.Empty:
                                    response = {
                                        "ok": False,
                                        "error": "Command processing timeout - main thread may be busy"
                                    }

                                # Clean up response queue
                                with self.request_lock:
                                    if request_id in self.response_queues:
                                        del self.response_queues[request_id]

                                # Send response back to client
                                response_str = json.dumps(response) + '\n'
                                client_socket.sendall(response_str.encode('utf-8'))

                            except Exception as e:
                                error_resp = {"ok": False, "error": str(e)}
                                try:
                                    client_socket.sendall((json.dumps(error_resp) + '\n').encode('utf-8'))
                                except:
                                    pass

                except socket.timeout:
                    continue  # Client might be idle
                except Exception as e:
                    self.log("Receive error: " + str(e))
                    break

        except Exception as e:
            self.log("Client handler error: " + str(e))
        finally:
            try:
                client_socket.close()
            except:
                pass

    def _process_command(self, command):
        """
        Process a JSON command and return JSON response
        THIS RUNS IN THE MAIN THREAD (called from update_display)

        Args:
            command: dict with {"action": "...", "param": "value", ...}

        Returns:
            dict: Response with {"ok": True/False, ...}
        """
        try:
            action = command.get('action', '')

            # Dispatch to appropriate tool
            if action == 'ping':
                return {"ok": True, "message": "pong (queue-based, thread-safe)", "script": "ClaudeMCP_Remote"}

            elif action == 'health_check':
                return {
                    "ok": True,
                    "message": "ClaudeMCP Remote Script running (thread-safe)",
                    "tool_count": len(self.tools.get_available_tools()),
                    "ableton_version": str(Live.Application.get_application().get_major_version()),
                    "queue_size": self.command_queue.qsize()
                }

            # Session control
            elif action == 'start_playback':
                return self.tools.start_playback()
            elif action == 'stop_playback':
                return self.tools.stop_playback()
            elif action == 'start_recording':
                return self.tools.start_recording()
            elif action == 'stop_recording':
                return self.tools.stop_recording()
            elif action == 'continue_playing':
                return self.tools.continue_playing()
            elif action == 'get_session_info':
                return self.tools.get_session_info()
            elif action == 'set_tempo':
                return self.tools.set_tempo(command.get('bpm', 120))
            elif action == 'set_time_signature':
                return self.tools.set_time_signature(command.get('numerator', 4), command.get('denominator', 4))
            elif action == 'set_loop_start':
                return self.tools.set_loop_start(command.get('position', 0.0))
            elif action == 'set_loop_length':
                return self.tools.set_loop_length(command.get('length', 4.0))
            elif action == 'set_metronome':
                return self.tools.set_metronome(command.get('enabled', True))
            elif action == 'tap_tempo':
                return self.tools.tap_tempo()
            elif action == 'undo':
                return self.tools.undo()
            elif action == 'redo':
                return self.tools.redo()

            # Track management
            elif action == 'create_midi_track':
                return self.tools.create_midi_track(command.get('name', None))
            elif action == 'create_audio_track':
                return self.tools.create_audio_track(command.get('name', None))
            elif action == 'create_return_track':
                return self.tools.create_return_track()
            elif action == 'delete_track':
                return self.tools.delete_track(command.get('track_index', 0))
            elif action == 'duplicate_track':
                return self.tools.duplicate_track(command.get('track_index', 0))
            elif action == 'rename_track':
                return self.tools.rename_track(command.get('track_index', 0), command.get('name', ''))
            elif action == 'set_track_volume':
                return self.tools.set_track_volume(command.get('track_index', 0), command.get('volume', 0.85))
            elif action == 'set_track_pan':
                return self.tools.set_track_pan(command.get('track_index', 0), command.get('pan', 0.0))
            elif action == 'arm_track':
                return self.tools.arm_track(command.get('track_index', 0), command.get('armed', True))
            elif action == 'solo_track':
                return self.tools.solo_track(command.get('track_index', 0), command.get('solo', True))
            elif action == 'mute_track':
                return self.tools.mute_track(command.get('track_index', 0), command.get('mute', True))
            elif action == 'get_track_info':
                return self.tools.get_track_info(command.get('track_index', 0))
            elif action == 'set_track_color':
                return self.tools.set_track_color(command.get('track_index', 0), command.get('color_index', 0))

            # Clip operations
            elif action == 'create_midi_clip':
                return self.tools.create_midi_clip(command.get('track_index', 0), command.get('scene_index', 0), command.get('length', 4.0))
            elif action == 'delete_clip':
                return self.tools.delete_clip(command.get('track_index', 0), command.get('scene_index', 0))
            elif action == 'duplicate_clip':
                return self.tools.duplicate_clip(command.get('track_index', 0), command.get('scene_index', 0))
            elif action == 'launch_clip':
                return self.tools.launch_clip(command.get('track_index', 0), command.get('scene_index', 0))
            elif action == 'stop_clip':
                return self.tools.stop_clip(command.get('track_index', 0), command.get('scene_index', 0))
            elif action == 'stop_all_clips':
                return self.tools.stop_all_clips()
            elif action == 'get_clip_info':
                return self.tools.get_clip_info(command.get('track_index', 0), command.get('scene_index', 0))
            elif action == 'set_clip_name':
                return self.tools.set_clip_name(command.get('track_index', 0), command.get('scene_index', 0), command.get('name', ''))

            # MIDI notes
            elif action == 'add_notes':
                return self.tools.add_notes(command.get('track_index', 0), command.get('scene_index', 0), command.get('notes', []))
            elif action == 'get_clip_notes':
                return self.tools.get_clip_notes(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'remove_notes':
                return self.tools.remove_notes(
                    command.get('track_index', 0),
                    command.get('clip_index', 0),
                    command.get('pitch_from', 0),
                    command.get('pitch_to', 127),
                    command.get('time_from', 0.0),
                    command.get('time_to', 999.0)
                )

            # Devices
            elif action == 'add_device':
                return self.tools.add_device(command.get('track_index', 0), command.get('device_name', ''))
            elif action == 'get_track_devices':
                return self.tools.get_track_devices(command.get('track_index', 0))
            elif action == 'set_device_param':
                return self.tools.set_device_param(
                    command.get('track_index', 0),
                    command.get('device_index', 0),
                    command.get('param_index', 0),
                    command.get('value', 0.0)
                )

            # Scene operations
            elif action == 'create_scene':
                return self.tools.create_scene(command.get('name', None))
            elif action == 'delete_scene':
                return self.tools.delete_scene(command.get('scene_index', 0))
            elif action == 'duplicate_scene':
                return self.tools.duplicate_scene(command.get('scene_index', 0))
            elif action == 'launch_scene':
                return self.tools.launch_scene(command.get('scene_index', 0))
            elif action == 'rename_scene':
                return self.tools.rename_scene(command.get('scene_index', 0), command.get('name', ''))
            elif action == 'get_scene_info':
                return self.tools.get_scene_info(command.get('scene_index', 0))

            # Transport operations
            elif action == 'jump_to_time':
                return self.tools.jump_to_time(command.get('time_in_beats', 0.0))
            elif action == 'get_current_time':
                return self.tools.get_current_time()
            elif action == 'set_arrangement_overdub':
                return self.tools.set_arrangement_overdub(command.get('enabled', True))
            elif action == 'set_back_to_arranger':
                return self.tools.set_back_to_arranger(command.get('enabled', True))
            elif action == 'set_punch_in':
                return self.tools.set_punch_in(command.get('enabled', True))
            elif action == 'set_punch_out':
                return self.tools.set_punch_out(command.get('enabled', True))
            elif action == 'nudge_up':
                return self.tools.nudge_up()
            elif action == 'nudge_down':
                return self.tools.nudge_down()

            # Automation operations
            elif action == 're_enable_automation':
                return self.tools.re_enable_automation()
            elif action == 'get_session_automation_record':
                return self.tools.get_session_automation_record()
            elif action == 'set_session_automation_record':
                return self.tools.set_session_automation_record(command.get('enabled', True))
            elif action == 'get_session_record':
                return self.tools.get_session_record()
            elif action == 'set_session_record':
                return self.tools.set_session_record(command.get('enabled', True))
            elif action == 'capture_midi':
                return self.tools.capture_midi()

            # Track extras
            elif action == 'set_track_fold_state':
                return self.tools.set_track_fold_state(command.get('track_index', 0), command.get('folded', True))
            elif action == 'set_track_input_routing':
                return self.tools.set_track_input_routing(command.get('track_index', 0), command.get('routing_type_name', ''))
            elif action == 'set_track_output_routing':
                return self.tools.set_track_output_routing(command.get('track_index', 0), command.get('routing_type_name', ''))

            # Send operations
            elif action == 'set_track_send':
                return self.tools.set_track_send(command.get('track_index', 0), command.get('send_index', 0), command.get('value', 0.0))
            elif action == 'get_track_sends':
                return self.tools.get_track_sends(command.get('track_index', 0))

            # Clip extras
            elif action == 'set_clip_looping':
                return self.tools.set_clip_looping(command.get('track_index', 0), command.get('clip_index', 0), command.get('looping', True))
            elif action == 'set_clip_loop_start':
                return self.tools.set_clip_loop_start(command.get('track_index', 0), command.get('clip_index', 0), command.get('loop_start', 0.0))
            elif action == 'set_clip_loop_end':
                return self.tools.set_clip_loop_end(command.get('track_index', 0), command.get('clip_index', 0), command.get('loop_end', 4.0))
            elif action == 'set_clip_start_marker':
                return self.tools.set_clip_start_marker(command.get('track_index', 0), command.get('clip_index', 0), command.get('start_marker', 0.0))
            elif action == 'set_clip_end_marker':
                return self.tools.set_clip_end_marker(command.get('track_index', 0), command.get('clip_index', 0), command.get('end_marker', 4.0))
            elif action == 'set_clip_muted':
                return self.tools.set_clip_muted(command.get('track_index', 0), command.get('clip_index', 0), command.get('muted', True))
            elif action == 'set_clip_gain':
                return self.tools.set_clip_gain(command.get('track_index', 0), command.get('clip_index', 0), command.get('gain', 1.0))
            elif action == 'set_clip_pitch_coarse':
                return self.tools.set_clip_pitch_coarse(command.get('track_index', 0), command.get('clip_index', 0), command.get('semitones', 0))
            elif action == 'set_clip_pitch_fine':
                return self.tools.set_clip_pitch_fine(command.get('track_index', 0), command.get('clip_index', 0), command.get('cents', 0))
            elif action == 'set_clip_signature_numerator':
                return self.tools.set_clip_signature_numerator(command.get('track_index', 0), command.get('clip_index', 0), command.get('numerator', 4))

            # MIDI note extras
            elif action == 'select_all_notes':
                return self.tools.select_all_notes(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'deselect_all_notes':
                return self.tools.deselect_all_notes(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'replace_selected_notes':
                return self.tools.replace_selected_notes(command.get('track_index', 0), command.get('clip_index', 0), command.get('notes', []))
            elif action == 'get_notes_extended':
                return self.tools.get_notes_extended(
                    command.get('track_index', 0),
                    command.get('clip_index', 0),
                    command.get('start_time', 0.0),
                    command.get('time_span', 999.0),
                    command.get('start_pitch', 0),
                    command.get('pitch_span', 128)
                )

            # Groove & quantization
            elif action == 'set_clip_groove_amount':
                return self.tools.set_clip_groove_amount(command.get('track_index', 0), command.get('clip_index', 0), command.get('amount', 0.0))
            elif action == 'quantize_clip':
                return self.tools.quantize_clip(command.get('track_index', 0), command.get('clip_index', 0), command.get('quantize_to', 0.25))
            elif action == 'quantize_clip_pitch':
                return self.tools.quantize_clip_pitch(command.get('track_index', 0), command.get('clip_index', 0), command.get('pitch', 60))
            elif action == 'get_groove_amount':
                return self.tools.get_groove_amount()
            elif action == 'set_groove_amount':
                return self.tools.set_groove_amount(command.get('amount', 0.0))

            # Monitoring & input
            elif action == 'set_track_current_monitoring_state':
                return self.tools.set_track_current_monitoring_state(command.get('track_index', 0), command.get('state', 1))
            elif action == 'get_track_available_input_routing_types':
                return self.tools.get_track_available_input_routing_types(command.get('track_index', 0))
            elif action == 'get_track_available_output_routing_types':
                return self.tools.get_track_available_output_routing_types(command.get('track_index', 0))
            elif action == 'get_track_input_routing_type':
                return self.tools.get_track_input_routing_type(command.get('track_index', 0))

            # Device extras
            elif action == 'set_device_on_off':
                return self.tools.set_device_on_off(command.get('track_index', 0), command.get('device_index', 0), command.get('enabled', True))
            elif action == 'get_device_parameters':
                return self.tools.get_device_parameters(command.get('track_index', 0), command.get('device_index', 0))
            elif action == 'get_device_parameter_by_name':
                return self.tools.get_device_parameter_by_name(command.get('track_index', 0), command.get('device_index', 0), command.get('param_name', ''))
            elif action == 'set_device_parameter_by_name':
                return self.tools.set_device_parameter_by_name(
                    command.get('track_index', 0),
                    command.get('device_index', 0),
                    command.get('param_name', ''),
                    command.get('value', 0.0)
                )
            elif action == 'delete_device':
                return self.tools.delete_device(command.get('track_index', 0), command.get('device_index', 0))
            elif action == 'get_device_presets':
                return self.tools.get_device_presets(command.get('track_index', 0), command.get('device_index', 0))
            elif action == 'set_device_preset':
                return self.tools.set_device_preset(command.get('track_index', 0), command.get('device_index', 0), command.get('preset_index', 0))
            elif action == 'randomize_device_parameters':
                return self.tools.randomize_device_parameters(command.get('track_index', 0), command.get('device_index', 0))

            # Project & arrangement
            elif action == 'get_project_root_folder':
                return self.tools.get_project_root_folder()
            elif action == 'trigger_session_record':
                return self.tools.trigger_session_record()
            elif action == 'get_can_jump_to_next_cue':
                return self.tools.get_can_jump_to_next_cue()
            elif action == 'get_can_jump_to_prev_cue':
                return self.tools.get_can_jump_to_prev_cue()
            elif action == 'jump_to_next_cue':
                return self.tools.jump_to_next_cue()
            elif action == 'jump_to_prev_cue':
                return self.tools.jump_to_prev_cue()

            # Browser operations
            elif action == 'browse_devices':
                return self.tools.browse_devices()
            elif action == 'browse_plugins':
                return self.tools.browse_plugins(command.get('plugin_type', 'vst'))
            elif action == 'load_device_from_browser':
                return self.tools.load_device_from_browser(command.get('track_index', 0), command.get('device_name', ''))
            elif action == 'get_browser_items':
                return self.tools.get_browser_items(command.get('category', 'devices'))

            # Loop & Locator operations
            elif action == 'set_loop_enabled':
                return self.tools.set_loop_enabled(command.get('enabled', True))
            elif action == 'get_loop_enabled':
                return self.tools.get_loop_enabled()
            elif action == 'create_locator':
                return self.tools.create_locator(command.get('time_in_beats', 0.0), command.get('name', 'Locator'))
            elif action == 'delete_locator':
                return self.tools.delete_locator(command.get('locator_index', 0))
            elif action == 'get_locators':
                return self.tools.get_locators()
            elif action == 'jump_by_amount':
                return self.tools.jump_by_amount(command.get('amount_in_beats', 0.0))

            # Clip color
            elif action == 'set_clip_color':
                return self.tools.set_clip_color(command.get('track_index', 0), command.get('clip_index', 0), command.get('color_index', 0))

            # Track routing extras
            elif action == 'get_track_output_routing':
                return self.tools.get_track_output_routing(command.get('track_index', 0))
            elif action == 'set_track_input_sub_routing':
                return self.tools.set_track_input_sub_routing(command.get('track_index', 0), command.get('sub_routing', ''))
            elif action == 'set_track_output_sub_routing':
                return self.tools.set_track_output_sub_routing(command.get('track_index', 0), command.get('sub_routing', ''))

            # Device extras - missing tool
            elif action == 'randomize_device':
                return self.tools.randomize_device(command.get('track_index', 0), command.get('device_index', 0))

            # Max for Live (M4L) operations
            elif action == 'is_max_device':
                return self.tools.is_max_device(command.get('track_index', 0), command.get('device_index', 0))
            elif action == 'get_m4l_devices':
                return self.tools.get_m4l_devices(command.get('track_index', 0))
            elif action == 'set_device_param_by_name':
                return self.tools.set_device_param_by_name(command.get('track_index', 0), command.get('device_index', 0), command.get('param_name', ''), command.get('value', 0.0))
            elif action == 'get_m4l_param_by_name':
                return self.tools.get_m4l_param_by_name(command.get('track_index', 0), command.get('device_index', 0), command.get('param_name', ''))
            elif action == 'get_cv_tools_devices':
                return self.tools.get_cv_tools_devices(command.get('track_index', 0))

            # Master Track Control
            elif action == 'get_master_track_info':
                return self.tools.get_master_track_info()
            elif action == 'set_master_volume':
                return self.tools.set_master_volume(command.get('volume', 0.85))
            elif action == 'set_master_pan':
                return self.tools.set_master_pan(command.get('pan', 0.0))
            elif action == 'get_master_devices':
                return self.tools.get_master_devices()

            # Return Track Operations
            elif action == 'get_return_track_count':
                return self.tools.get_return_track_count()
            elif action == 'get_return_track_info':
                return self.tools.get_return_track_info(command.get('return_index', 0))
            elif action == 'set_return_track_volume':
                return self.tools.set_return_track_volume(command.get('return_index', 0), command.get('volume', 0.85))

            # Audio Clip Operations
            elif action == 'get_clip_warp_mode':
                return self.tools.get_clip_warp_mode(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'set_clip_warp_mode':
                return self.tools.set_clip_warp_mode(command.get('track_index', 0), command.get('clip_index', 0), command.get('warp_mode', 0))
            elif action == 'get_clip_file_path':
                return self.tools.get_clip_file_path(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'set_clip_warping':
                return self.tools.set_clip_warping(command.get('track_index', 0), command.get('clip_index', 0), command.get('warping', True))
            elif action == 'get_warp_markers':
                return self.tools.get_warp_markers(command.get('track_index', 0), command.get('clip_index', 0))

            # Follow Actions
            elif action == 'get_clip_follow_action':
                return self.tools.get_clip_follow_action(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'set_clip_follow_action':
                return self.tools.set_clip_follow_action(command.get('track_index', 0), command.get('clip_index', 0), command.get('action_A', 0), command.get('action_B', 0), command.get('chance_A', 1.0))
            elif action == 'set_follow_action_time':
                return self.tools.set_follow_action_time(command.get('track_index', 0), command.get('clip_index', 0), command.get('time_in_bars', 1.0))

            # Crossfader
            elif action == 'get_crossfader_assignment':
                return self.tools.get_crossfader_assignment(command.get('track_index', 0))
            elif action == 'set_crossfader_assignment':
                return self.tools.set_crossfader_assignment(command.get('track_index', 0), command.get('assignment', 0))
            elif action == 'get_crossfader_position':
                return self.tools.get_crossfader_position()

            # Track Groups
            elif action == 'create_group_track':
                return self.tools.create_group_track(command.get('name'))
            elif action == 'group_tracks':
                return self.tools.group_tracks(command.get('start_index', 0), command.get('end_index', 0))
            elif action == 'get_track_is_grouped':
                return self.tools.get_track_is_grouped(command.get('track_index', 0))
            elif action == 'ungroup_track':
                return self.tools.ungroup_track(command.get('group_track_index', 0))

            # View/Navigation
            elif action == 'show_clip_view':
                return self.tools.show_clip_view()
            elif action == 'show_arrangement_view':
                return self.tools.show_arrangement_view()
            elif action == 'focus_track':
                return self.tools.focus_track(command.get('track_index', 0))
            elif action == 'scroll_view_to_time':
                return self.tools.scroll_view_to_time(command.get('time_in_beats', 0.0))

            # Color Utilities
            elif action == 'get_clip_color':
                return self.tools.get_clip_color(command.get('track_index', 0), command.get('clip_index', 0))
            elif action == 'get_track_color':
                return self.tools.get_track_color(command.get('track_index', 0))

            # Groove Pool
            elif action == 'get_groove_pool_grooves':
                return self.tools.get_groove_pool_grooves()
            elif action == 'set_clip_groove':
                return self.tools.set_clip_groove(command.get('track_index', 0), command.get('clip_index', 0), command.get('groove_index', 0))

            # Rack/Chain Operations
            elif action == 'get_device_chains':
                return self.tools.get_device_chains(command.get('track_index', 0), command.get('device_index', 0))
            elif action == 'get_chain_devices':
                return self.tools.get_chain_devices(command.get('track_index', 0), command.get('device_index', 0), command.get('chain_index', 0))
            elif action == 'set_chain_mute':
                return self.tools.set_chain_mute(command.get('track_index', 0), command.get('device_index', 0), command.get('chain_index', 0), command.get('mute', True))
            elif action == 'set_chain_solo':
                return self.tools.set_chain_solo(command.get('track_index', 0), command.get('device_index', 0), command.get('chain_index', 0), command.get('solo', True))

            # Unknown action
            else:
                return {
                    "ok": False,
                    "error": "Unknown action: " + action,
                    "available_actions": self.tools.get_available_tools()
                }

        except Exception as e:
            self.log("ERROR processing command: " + str(e))
            self.log(traceback.format_exc())
            return {
                "ok": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def update_display(self):
        """
        Called by Ableton Live on each tick to update displays
        RUNS IN MAIN THREAD - safe to call LiveAPI here

        We process commands from the queue here to ensure thread safety
        """
        # Process up to 5 commands per tick to avoid blocking the UI
        commands_processed = 0
        max_commands_per_tick = 5

        while commands_processed < max_commands_per_tick:
            try:
                # Try to get a command from queue (non-blocking)
                request_id, command = self.command_queue.get_nowait()

                # Process command in main thread (safe for LiveAPI)
                response = self._process_command(command)

                # Put response in the request's response queue
                if request_id in self.response_queues:
                    self.response_queues[request_id].put(response)

                commands_processed += 1

            except queue.Empty:
                # No more commands in queue
                break
            except Exception as e:
                self.log("Error in update_display: " + str(e))
                break

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by Live to connect this script with other scripts
        Required by Ableton's Remote Script API
        """
        pass

    def can_lock_to_devices(self):
        """
        Called by Live to check if this script can lock to devices
        Required by Ableton's Remote Script API
        """
        return False

    def refresh_state(self):
        """
        Called by Live to refresh the script's state
        Required by Ableton's Remote Script API
        """
        pass

    def build_midi_map(self, midi_map_handle):
        """
        Called by Live to build MIDI mapping
        Required by Ableton's Remote Script API
        """
        pass

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log("Shutting down ClaudeMCP Remote Script...")

        # Stop socket server
        self.running = False

        if self.socket_server:
            try:
                self.socket_server.close()
            except:
                pass

        self.log("ClaudeMCP Remote Script stopped")


# Required entry points for Ableton
def create_instance(c_instance):
    """Factory function called by Live to create the script instance"""
    return ClaudeMCP(c_instance)
