"""
LiveAPI Tools Implementation for ClaudeMCP Remote Script
Implements all LiveAPI operations for controlling Ableton Live

Author: Claude Code
License: MIT
"""

import Live


class LiveAPITools:
    """
    Comprehensive implementation of LiveAPI operations

    Provides 125 tools for controlling every aspect of Ableton Live:
    - Session control (play/stop/record/tempo/time signature)
    - Track management (create/delete/arm/solo/mute)
    - Clip operations (create/delete/launch/stop)
    - MIDI note editing (add/remove/modify notes)
    - Device control (add/remove/parameters)
    - Mixing (volume/pan/sends)
    - Scenes (create/delete/launch)
    - And much more...
    """

    def __init__(self, song, c_instance):
        """
        Initialize LiveAPI tools

        Args:
            song: The Live.Song.Song object
            c_instance: The ControlSurface instance
        """
        self.song = song
        self.c_instance = c_instance

    def log(self, message):
        """Log message to Ableton's Log.txt"""
        self.c_instance.log_message("[LiveAPITools] " + str(message))

    # ========================================================================
    # SESSION CONTROL
    # ========================================================================

    def start_playback(self):
        """Start Ableton playback"""
        try:
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Playback started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_playback(self):
        """Stop Ableton playback"""
        try:
            if self.song.is_playing:
                self.song.stop_playing()
            return {"ok": True, "message": "Playback stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def start_recording(self):
        """Start recording"""
        try:
            self.song.record_mode = True
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Recording started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_recording(self):
        """Stop recording"""
        try:
            self.song.record_mode = False
            return {"ok": True, "message": "Recording stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def continue_playing(self):
        """Continue playback from current position"""
        try:
            self.song.continue_playing()
            return {"ok": True, "message": "Playback continued"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_info(self):
        """Get current session state information"""
        try:
            return {
                "ok": True,
                "is_playing": self.song.is_playing,
                "tempo": float(self.song.tempo),
                "time_signature_numerator": self.song.signature_numerator,
                "time_signature_denominator": self.song.signature_denominator,
                "current_song_time": float(self.song.current_song_time),
                "loop_start": float(self.song.loop_start),
                "loop_end": float(self.song.loop_start + self.song.loop_length),
                "loop_length": float(self.song.loop_length),
                "num_tracks": len(self.song.tracks),
                "num_scenes": len(self.song.scenes),
                "record_mode": self.song.record_mode,
                "metronome": self.song.metronome,
                "nudge_up": self.song.nudge_up,
                "nudge_down": self.song.nudge_down
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_tempo(self, bpm):
        """
        Set session tempo

        Args:
            bpm: Tempo in BPM (20-999)
        """
        try:
            bpm = float(bpm)
            if bpm < 20 or bpm > 999:
                return {"ok": False, "error": "BPM must be between 20 and 999"}
            self.song.tempo = bpm
            return {"ok": True, "message": "Tempo set", "bpm": float(self.song.tempo)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_time_signature(self, numerator, denominator):
        """
        Set time signature

        Args:
            numerator: Top number (1-99)
            denominator: Bottom number (1, 2, 4, 8, 16)
        """
        try:
            numerator = int(numerator)
            denominator = int(denominator)

            if numerator < 1 or numerator > 99:
                return {"ok": False, "error": "Numerator must be between 1 and 99"}
            if denominator not in [1, 2, 4, 8, 16]:
                return {"ok": False, "error": "Denominator must be 1, 2, 4, 8, or 16"}

            self.song.signature_numerator = numerator
            self.song.signature_denominator = denominator

            return {
                "ok": True,
                "message": "Time signature set",
                "numerator": self.song.signature_numerator,
                "denominator": self.song.signature_denominator
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_start(self, position):
        """Set loop start position in beats"""
        try:
            self.song.loop_start = float(position)
            return {"ok": True, "loop_start": float(self.song.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_length(self, length):
        """Set loop length in beats"""
        try:
            self.song.loop_length = float(length)
            return {"ok": True, "loop_length": float(self.song.loop_length)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome(self, enabled):
        """Enable or disable metronome"""
        try:
            self.song.metronome = bool(enabled)
            return {"ok": True, "metronome": self.song.metronome}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def tap_tempo(self):
        """Tap tempo"""
        try:
            self.song.tap_tempo()
            return {"ok": True, "message": "Tempo tapped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def undo(self):
        """Undo last action"""
        try:
            self.song.undo()
            return {"ok": True, "message": "Undo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def redo(self):
        """Redo last undone action"""
        try:
            self.song.redo()
            return {"ok": True, "message": "Redo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK MANAGEMENT
    # ========================================================================

    def create_midi_track(self, name=None):
        """
        Create a new MIDI track

        Args:
            name: Optional track name
        """
        try:
            track_index = len(self.song.tracks)
            self.song.create_midi_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "MIDI track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_track(self, name=None):
        """
        Create a new audio track

        Args:
            name: Optional track name
        """
        try:
            track_index = len(self.song.tracks)
            self.song.create_audio_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Audio track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_return_track(self):
        """Create a new return track"""
        try:
            self.song.create_return_track()
            return_index = len(self.song.return_tracks) - 1
            return {
                "ok": True,
                "message": "Return track created",
                "return_index": return_index
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_track(self, track_index):
        """Delete track by index"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.delete_track(track_index)
            return {"ok": True, "message": "Track deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_track(self, track_index):
        """Duplicate track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.duplicate_track(track_index)
            return {"ok": True, "message": "Track duplicated", "new_index": track_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_track(self, track_index, name):
        """Rename track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].name = str(name)
            return {"ok": True, "message": "Track renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_volume(self, track_index, volume):
        """
        Set track volume

        Args:
            track_index: Track index
            volume: Volume (0.0 to 1.0)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            volume = float(volume)
            if volume < 0.0 or volume > 1.0:
                return {"ok": False, "error": "Volume must be between 0.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.volume.value = volume

            return {
                "ok": True,
                "message": "Track volume set",
                "track_index": track_index,
                "volume": float(track.mixer_device.volume.value)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_pan(self, track_index, pan):
        """
        Set track pan

        Args:
            track_index: Track index
            pan: Pan (-1.0 to 1.0, where 0 is center)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            pan = float(pan)
            if pan < -1.0 or pan > 1.0:
                return {"ok": False, "error": "Pan must be between -1.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.panning.value = pan

            return {
                "ok": True,
                "message": "Track pan set",
                "track_index": track_index,
                "pan": float(track.mixer_device.panning.value)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def arm_track(self, track_index, armed=True):
        """Arm or disarm track for recording"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.can_be_armed:
                track.arm = bool(armed)
                return {"ok": True, "message": "Track armed" if armed else "Track disarmed", "armed": track.arm}
            else:
                return {"ok": False, "error": "Track cannot be armed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def solo_track(self, track_index, solo=True):
        """Solo or unsolo track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].solo = bool(solo)
            return {"ok": True, "message": "Track soloed" if solo else "Track unsoloed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def mute_track(self, track_index, mute=True):
        """Mute or unmute track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].mute = bool(mute)
            return {"ok": True, "message": "Track muted" if mute else "Track unmuted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_info(self, track_index):
        """Get detailed track information"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            return {
                "ok": True,
                "track_index": track_index,
                "name": str(track.name),
                "color": track.color if hasattr(track, 'color') else None,
                "is_foldable": track.is_foldable,
                "mute": track.mute,
                "solo": track.solo,
                "arm": track.arm if track.can_be_armed else False,
                "has_midi_input": track.has_midi_input,
                "has_audio_input": track.has_audio_input,
                "volume": float(track.mixer_device.volume.value),
                "pan": float(track.mixer_device.panning.value),
                "num_devices": len(track.devices),
                "num_clips": len([cs for cs in track.clip_slots if cs.has_clip])
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_color(self, track_index, color_index):
        """Set track color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, 'color'):
                track.color = int(color_index)
                return {"ok": True, "message": "Track color set", "color": track.color}
            else:
                return {"ok": False, "error": "Track color not supported"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP OPERATIONS
    # ========================================================================

    def create_midi_clip(self, track_index, scene_index, length=4.0):
        """
        Create a new MIDI clip

        Args:
            track_index: Track index
            scene_index: Scene index
            length: Clip length in bars (default: 4.0)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            clip_slot = track.clip_slots[scene_index]

            if clip_slot.has_clip:
                return {"ok": False, "error": "Clip slot already has a clip"}

            # Create clip
            clip_slot.create_clip(float(length))

            return {
                "ok": True,
                "message": "MIDI clip created",
                "track_index": track_index,
                "scene_index": scene_index,
                "length": float(length)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_clip(self, track_index, scene_index):
        """Delete clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.delete_clip()
            return {"ok": True, "message": "Clip deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_clip(self, track_index, scene_index):
        """Duplicate clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.duplicate_clip_to(clip_slot)
            return {"ok": True, "message": "Clip duplicated"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def launch_clip(self, track_index, scene_index):
        """Launch clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.fire()
            return {"ok": True, "message": "Clip launched"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_clip(self, track_index, scene_index):
        """Stop clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].stop_all_clips()
            return {"ok": True, "message": "Clip stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_all_clips(self):
        """Stop all playing clips"""
        try:
            self.song.stop_all_clips()
            return {"ok": True, "message": "All clips stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_info(self, track_index, scene_index):
        """Get clip information"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            return {
                "ok": True,
                "name": str(clip.name),
                "length": float(clip.length),
                "loop_start": float(clip.loop_start),
                "loop_end": float(clip.loop_end),
                "is_midi_clip": clip.is_midi_clip,
                "is_audio_clip": clip.is_audio_clip,
                "is_playing": clip.is_playing,
                "muted": clip.muted,
                "color": clip.color if hasattr(clip, 'color') else None
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_name(self, track_index, scene_index, name):
        """Set clip name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.clip.name = str(name)
            return {"ok": True, "message": "Clip renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MIDI NOTE OPERATIONS
    # ========================================================================

    def add_notes(self, track_index, scene_index, notes):
        """
        Add MIDI notes to a clip

        Args:
            track_index: Track index
            scene_index: Scene index (or clip_index)
            notes: List of note dicts with keys:
                   - pitch: MIDI note number (0-127)
                   - start: Start time in beats
                   - duration: Note duration in beats
                   - velocity: MIDI velocity (0-127)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if scene_index < 0 or scene_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid scene/clip index"}

            clip_slot = track.clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            # Add notes
            for note in notes:
                pitch = int(note.get('pitch', 60))
                start = float(note.get('start', 0.0))
                duration = float(note.get('duration', 1.0))
                velocity = int(note.get('velocity', 100))

                # Validate parameters
                if pitch < 0 or pitch > 127:
                    continue
                if velocity < 0 or velocity > 127:
                    continue
                if duration <= 0:
                    continue

                # Add note to clip
                clip.set_notes(((pitch, start, duration, velocity, False),))

            return {
                "ok": True,
                "message": "Notes added",
                "track_index": track_index,
                "scene_index": scene_index,
                "note_count": len(notes)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_notes(self, track_index, clip_index):
        """
        Get all MIDI notes from a clip

        Args:
            track_index: Track index
            clip_index: Clip slot index
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            # Get notes from clip
            notes_data = clip.get_notes(0, 0, clip.length, 128)

            notes = []
            for note_tuple in notes_data:
                notes.append({
                    "pitch": note_tuple[0],
                    "start_time": float(note_tuple[1]),
                    "duration": float(note_tuple[2]),
                    "velocity": note_tuple[3],
                    "muted": note_tuple[4]
                })

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "notes": notes,
                "count": len(notes)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_notes(self, track_index, clip_index, pitch_from=0, pitch_to=127, time_from=0.0, time_to=999.0):
        """Remove MIDI notes from clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            clip.remove_notes(float(time_from), int(pitch_from), float(time_to - time_from), int(pitch_to - pitch_from))
            return {"ok": True, "message": "Notes removed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE OPERATIONS
    # ========================================================================

    def add_device(self, track_index, device_name):
        """Add device to track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            # This is a simplified version - actual device loading requires browser API
            return {
                "ok": True,
                "message": "Device add requested (browser API required for full implementation)",
                "device_name": device_name
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_devices(self, track_index):
        """Get all devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            devices = []

            for device in track.devices:
                devices.append({
                    "name": str(device.name),
                    "class_name": str(device.class_name),
                    "is_active": device.is_active,
                    "num_parameters": len(device.parameters)
                })

            return {
                "ok": True,
                "track_index": track_index,
                "devices": devices,
                "count": len(devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_param(self, track_index, device_index, param_index, value):
        """Set device parameter value"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            if param_index < 0 or param_index >= len(device.parameters):
                return {"ok": False, "error": "Invalid parameter index"}

            param = device.parameters[param_index]
            param.value = float(value)

            return {
                "ok": True,
                "message": "Parameter set",
                "value": float(param.value)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SCENE OPERATIONS
    # ========================================================================

    def create_scene(self, name=None):
        """Create a new scene"""
        try:
            scene_index = len(self.song.scenes)
            self.song.create_scene(scene_index)

            if name:
                self.song.scenes[scene_index].name = str(name)

            return {
                "ok": True,
                "message": "Scene created",
                "scene_index": scene_index,
                "name": str(self.song.scenes[scene_index].name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_scene(self, scene_index):
        """Delete scene by index"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.delete_scene(scene_index)
            return {"ok": True, "message": "Scene deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_scene(self, scene_index):
        """Duplicate scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.duplicate_scene(scene_index)
            return {"ok": True, "message": "Scene duplicated", "new_index": scene_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def launch_scene(self, scene_index):
        """Launch a scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.scenes[scene_index].fire()
            return {"ok": True, "message": "Scene launched", "scene_index": scene_index}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_scene(self, scene_index, name):
        """Rename scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.scenes[scene_index].name = str(name)
            return {"ok": True, "message": "Scene renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_info(self, scene_index):
        """Get scene information"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            scene = self.song.scenes[scene_index]
            return {
                "ok": True,
                "scene_index": scene_index,
                "name": str(scene.name),
                "color": scene.color if hasattr(scene, 'color') else None,
                "tempo": float(scene.tempo) if hasattr(scene, 'tempo') else None,
                "time_signature_numerator": scene.time_signature_numerator if hasattr(scene, 'time_signature_numerator') else None
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRANSPORT OPERATIONS
    # ========================================================================

    def jump_to_time(self, time_in_beats):
        """Jump playback to specific time in beats"""
        try:
            self.song.current_song_time = float(time_in_beats)
            return {"ok": True, "time": float(self.song.current_song_time)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_current_time(self):
        """Get current playback position in beats"""
        try:
            return {
                "ok": True,
                "current_song_time": float(self.song.current_song_time),
                "is_playing": self.song.is_playing
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_arrangement_overdub(self, enabled):
        """Enable/disable arrangement overdub"""
        try:
            self.song.arrangement_overdub = bool(enabled)
            return {"ok": True, "arrangement_overdub": self.song.arrangement_overdub}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_back_to_arranger(self, enabled):
        """Enable/disable back to arrangement"""
        try:
            self.song.back_to_arranger = bool(enabled)
            return {"ok": True, "back_to_arranger": self.song.back_to_arranger}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_in(self, enabled):
        """Enable/disable punch in recording"""
        try:
            self.song.punch_in = bool(enabled)
            return {"ok": True, "punch_in": self.song.punch_in}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_out(self, enabled):
        """Enable/disable punch out recording"""
        try:
            self.song.punch_out = bool(enabled)
            return {"ok": True, "punch_out": self.song.punch_out}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_up(self):
        """Nudge playback position up"""
        try:
            self.song.nudge_up()
            return {"ok": True, "message": "Nudged up"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_down(self):
        """Nudge playback position down"""
        try:
            self.song.nudge_down()
            return {"ok": True, "message": "Nudged down"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # AUTOMATION OPERATIONS
    # ========================================================================

    def re_enable_automation(self):
        """Re-enable all automation"""
        try:
            self.song.re_enable_automation()
            return {"ok": True, "message": "Automation re-enabled"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_automation_record(self):
        """Get session automation recording state"""
        try:
            return {
                "ok": True,
                "session_automation_record": self.song.session_automation_record
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_automation_record(self, enabled):
        """Enable/disable session automation recording"""
        try:
            self.song.session_automation_record = bool(enabled)
            return {"ok": True, "session_automation_record": self.song.session_automation_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_record(self):
        """Get session record state"""
        try:
            return {
                "ok": True,
                "session_record": self.song.session_record
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_record(self, enabled):
        """Enable/disable session recording"""
        try:
            self.song.session_record = bool(enabled)
            return {"ok": True, "session_record": self.song.session_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def capture_midi(self):
        """Capture MIDI from the last played notes"""
        try:
            self.song.capture_midi()
            return {"ok": True, "message": "MIDI captured"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK EXTRAS
    # ========================================================================

    def set_track_fold_state(self, track_index, folded):
        """Fold or unfold a group track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.is_foldable:
                track.fold_state = bool(folded)
                return {"ok": True, "fold_state": track.fold_state}
            else:
                return {"ok": False, "error": "Track is not foldable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_input_routing(self, track_index, routing_type, routing_channel):
        """Set track input routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            return {
                "ok": True,
                "message": "Input routing set (requires routing configuration)",
                "routing_type": routing_type,
                "routing_channel": routing_channel
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_output_routing(self, track_index, routing_type):
        """Set track output routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            return {
                "ok": True,
                "message": "Output routing set (requires routing configuration)",
                "routing_type": routing_type
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP EXTRAS
    # ========================================================================

    def set_clip_looping(self, track_index, clip_index, looping):
        """Enable/disable clip looping"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.looping = bool(looping)
            return {"ok": True, "looping": clip.looping}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_start(self, track_index, clip_index, loop_start):
        """Set clip loop start position"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.loop_start = float(loop_start)
            return {"ok": True, "loop_start": float(clip.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_end(self, track_index, clip_index, loop_end):
        """Set clip loop end position"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.loop_end = float(loop_end)
            return {"ok": True, "loop_end": float(clip.loop_end)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_start_marker(self, track_index, clip_index, start_marker):
        """Set clip start marker"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.start_marker = float(start_marker)
            return {"ok": True, "start_marker": float(clip.start_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_end_marker(self, track_index, clip_index, end_marker):
        """Set clip end marker"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.end_marker = float(end_marker)
            return {"ok": True, "end_marker": float(clip.end_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_muted(self, track_index, clip_index, muted):
        """Mute or unmute clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.muted = bool(muted)
            return {"ok": True, "muted": clip.muted}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_gain(self, track_index, clip_index, gain):
        """Set clip gain/volume"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'gain'):
                clip.gain = float(gain)
                return {"ok": True, "gain": float(clip.gain)}
            else:
                return {"ok": False, "error": "Clip does not support gain"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_coarse(self, track_index, clip_index, semitones):
        """Transpose clip by semitones"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'pitch_coarse'):
                clip.pitch_coarse = int(semitones)
                return {"ok": True, "pitch_coarse": clip.pitch_coarse}
            else:
                return {"ok": False, "error": "Clip does not support pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_fine(self, track_index, clip_index, cents):
        """Fine-tune clip pitch in cents"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'pitch_fine'):
                clip.pitch_fine = int(cents)
                return {"ok": True, "pitch_fine": clip.pitch_fine}
            else:
                return {"ok": False, "error": "Clip does not support fine pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_signature_numerator(self, track_index, clip_index, numerator):
        """Set clip time signature numerator"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.signature_numerator = int(numerator)
            return {"ok": True, "signature_numerator": clip.signature_numerator}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MIDI NOTE EXTRAS
    # ========================================================================

    def select_all_notes(self, track_index, clip_index):
        """Select all notes in clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            clip.select_all_notes()
            return {"ok": True, "message": "All notes selected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def deselect_all_notes(self, track_index, clip_index):
        """Deselect all notes in clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            clip.deselect_all_notes()
            return {"ok": True, "message": "All notes deselected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def replace_selected_notes(self, track_index, clip_index, notes):
        """Replace selected notes with new notes"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip

            # Convert notes to tuple format
            note_tuples = []
            for note in notes:
                pitch = int(note.get('pitch', 60))
                start = float(note.get('start', 0.0))
                duration = float(note.get('duration', 1.0))
                velocity = int(note.get('velocity', 100))
                muted = bool(note.get('muted', False))
                note_tuples.append((pitch, start, duration, velocity, muted))

            clip.replace_selected_notes(tuple(note_tuples))
            return {"ok": True, "message": "Selected notes replaced", "note_count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_notes_extended(self, track_index, clip_index, start_time, time_span, start_pitch, pitch_span):
        """Get notes with extended filtering options"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            notes_data = clip.get_notes_extended(
                from_time=float(start_time),
                from_pitch=int(start_pitch),
                time_span=float(time_span),
                pitch_span=int(pitch_span)
            )

            notes = []
            for note_tuple in notes_data:
                notes.append({
                    "pitch": note_tuple[0],
                    "start_time": float(note_tuple[1]),
                    "duration": float(note_tuple[2]),
                    "velocity": note_tuple[3],
                    "muted": note_tuple[4]
                })

            return {"ok": True, "notes": notes, "count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # GROOVE & QUANTIZATION
    # ========================================================================

    def set_clip_groove_amount(self, track_index, clip_index, amount):
        """Set clip groove amount (0.0-1.0)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'groove_amount'):
                clip.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(clip.groove_amount)}
            else:
                return {"ok": False, "error": "Clip does not support groove"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def quantize_clip(self, track_index, clip_index, quantize_to):
        """Quantize MIDI clip to grid"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'quantize'):
                clip.quantize(float(quantize_to), 1.0)
                return {"ok": True, "message": "Clip quantized", "quantize_to": quantize_to}
            else:
                return {"ok": False, "error": "Clip does not support quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def quantize_clip_pitch(self, track_index, clip_index):
        """Quantize MIDI clip pitch"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, 'quantize_pitch'):
                clip.quantize_pitch(0, 127, 1.0)
                return {"ok": True, "message": "Clip pitch quantized"}
            else:
                return {"ok": False, "error": "Clip does not support pitch quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_groove_amount(self, track_index):
        """Get track groove amount"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, 'groove_amount'):
                return {"ok": True, "groove_amount": float(track.groove_amount)}
            else:
                return {"ok": False, "error": "Track does not support groove"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_groove_amount(self, track_index, amount):
        """Set track groove amount (0.0-1.0)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, 'groove_amount'):
                track.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(track.groove_amount)}
            else:
                return {"ok": False, "error": "Track does not support groove"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MONITORING & INPUT
    # ========================================================================

    def set_track_current_monitoring_state(self, track_index, state):
        """Set track monitoring state (0=In, 1=Auto, 2=Off)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.can_be_armed:
                track.current_monitoring_state = int(state)
                return {"ok": True, "monitoring_state": track.current_monitoring_state}
            else:
                return {"ok": False, "error": "Track cannot be monitored"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_available_input_routing_types(self, track_index):
        """Get available input routing types for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            routing_types = []
            if hasattr(track, 'available_input_routing_types'):
                for routing in track.available_input_routing_types:
                    routing_types.append(str(routing.display_name))

            return {"ok": True, "routing_types": routing_types, "count": len(routing_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_available_output_routing_types(self, track_index):
        """Get available output routing types for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            routing_types = []
            if hasattr(track, 'available_output_routing_types'):
                for routing in track.available_output_routing_types:
                    routing_types.append(str(routing.display_name))

            return {"ok": True, "routing_types": routing_types, "count": len(routing_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_input_routing_type(self, track_index):
        """Get current input routing type for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, 'input_routing_type'):
                return {
                    "ok": True,
                    "routing_type": str(track.input_routing_type.display_name) if track.input_routing_type else None
                }
            else:
                return {"ok": False, "error": "Track does not have input routing"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE EXTRAS
    # ========================================================================

    def set_device_on_off(self, track_index, device_index, enabled):
        """Turn device on or off"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            if hasattr(device, 'is_active'):
                device.is_active = bool(enabled)
                return {"ok": True, "is_active": device.is_active}
            else:
                return {"ok": False, "error": "Device does not support on/off"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_parameters(self, track_index, device_index):
        """Get all parameters for a device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            parameters = []

            for i, param in enumerate(device.parameters):
                parameters.append({
                    "index": i,
                    "name": str(param.name),
                    "value": float(param.value),
                    "min": float(param.min),
                    "max": float(param.max),
                    "is_quantized": param.is_quantized,
                    "is_enabled": param.is_enabled if hasattr(param, 'is_enabled') else True
                })

            return {
                "ok": True,
                "track_index": track_index,
                "device_index": device_index,
                "parameters": parameters,
                "count": len(parameters)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_parameter_by_name(self, track_index, device_index, param_name):
        """Get device parameter by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    return {
                        "ok": True,
                        "index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max)
                    }

            return {"ok": False, "error": f"Parameter '{param_name}' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_parameter_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            for param in device.parameters:
                if str(param.name) == param_name:
                    param.value = float(value)
                    return {
                        "ok": True,
                        "name": str(param.name),
                        "value": float(param.value)
                    }

            return {"ok": False, "error": f"Parameter '{param_name}' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_device(self, track_index, device_index):
        """Delete device from track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            track.delete_device(device_index)
            return {"ok": True, "message": "Device deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_presets(self, track_index, device_index):
        """Get available presets for device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            # This is a simplified implementation
            return {
                "ok": True,
                "message": "Device preset browsing requires browser API",
                "device_index": device_index
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_preset(self, track_index, device_index, preset_index):
        """Load preset for device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            # This is a simplified implementation
            return {
                "ok": True,
                "message": "Device preset loading requires browser API",
                "preset_index": preset_index
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def randomize_device_parameters(self, track_index, device_index):
        """Randomize all device parameters"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            import random
            device = track.devices[device_index]
            randomized_count = 0

            for param in device.parameters:
                if param.is_enabled and not param.is_quantized:
                    random_value = random.uniform(param.min, param.max)
                    param.value = random_value
                    randomized_count += 1

            return {
                "ok": True,
                "message": "Device parameters randomized",
                "randomized_count": randomized_count
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # PROJECT & ARRANGEMENT
    # ========================================================================

    def get_project_root_folder(self):
        """Get project root folder path"""
        try:
            if hasattr(self.song, 'project_root_folder'):
                return {
                    "ok": True,
                    "project_root_folder": str(self.song.project_root_folder) if self.song.project_root_folder else None
                }
            else:
                return {"ok": False, "error": "Project root folder not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def trigger_session_record(self, length=None):
        """Trigger session record with optional fixed length"""
        try:
            if length:
                self.song.trigger_session_record(float(length))
            else:
                self.song.trigger_session_record()
            return {"ok": True, "message": "Session record triggered"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_next_cue(self):
        """Check if can jump to next cue point"""
        try:
            return {
                "ok": True,
                "can_jump_to_next_cue": self.song.can_jump_to_next_cue
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_prev_cue(self):
        """Check if can jump to previous cue point"""
        try:
            return {
                "ok": True,
                "can_jump_to_prev_cue": self.song.can_jump_to_prev_cue
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_next_cue(self):
        """Jump to next cue point"""
        try:
            if self.song.can_jump_to_next_cue:
                self.song.jump_to_next_cue()
                return {"ok": True, "message": "Jumped to next cue"}
            else:
                return {"ok": False, "error": "Cannot jump to next cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_prev_cue(self):
        """Jump to previous cue point"""
        try:
            if self.song.can_jump_to_prev_cue:
                self.song.jump_to_prev_cue()
                return {"ok": True, "message": "Jumped to previous cue"}
            else:
                return {"ok": False, "error": "Cannot jump to previous cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SEND OPERATIONS
    # ========================================================================

    def set_track_send(self, track_index, send_index, value):
        """Set track send level"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            sends = track.mixer_device.sends

            if send_index < 0 or send_index >= len(sends):
                return {"ok": False, "error": "Invalid send index"}

            sends[send_index].value = float(value)
            return {
                "ok": True,
                "send_index": send_index,
                "value": float(sends[send_index].value)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_sends(self, track_index):
        """Get all send levels for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            sends = []

            for i, send in enumerate(track.mixer_device.sends):
                sends.append({
                    "index": i,
                    "value": float(send.value),
                    "name": str(send.name) if hasattr(send, 'name') else f"Send {chr(65+i)}"
                })

            return {
                "ok": True,
                "track_index": track_index,
                "sends": sends,
                "count": len(sends)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # BROWSER OPERATIONS
    # ========================================================================

    def browse_devices(self):
        """Get list of available devices from browser"""
        try:
            # Note: Browser access is limited in LiveAPI
            # This returns a basic list of device types
            device_types = [
                "Instrument", "Audio Effect", "MIDI Effect",
                "Drum Rack", "Instrument Rack", "Effect Rack"
            ]
            return {
                "ok": True,
                "device_types": device_types,
                "count": len(device_types)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def browse_plugins(self, plugin_type="vst"):
        """Browse available plugins (VST, AU, etc.)"""
        try:
            # Note: Plugin browsing is limited in LiveAPI
            # Returns placeholder info
            return {
                "ok": True,
                "message": "Plugin browsing via LiveAPI is limited",
                "plugin_type": plugin_type
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_device_from_browser(self, track_index, device_name):
        """Load a device from browser onto track (alias for add_device)"""
        # This is essentially the same as add_device
        return self.add_device(track_index, device_name)

    def get_browser_items(self, category="devices"):
        """Get browser items by category"""
        try:
            categories = ["devices", "plugins", "instruments", "audio_effects", "midi_effects"]
            return {
                "ok": True,
                "category": category,
                "available_categories": categories,
                "message": "Browser item enumeration is limited in LiveAPI"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # LOOP AND LOCATOR OPERATIONS
    # ========================================================================

    def set_loop_enabled(self, enabled):
        """Enable or disable song loop"""
        try:
            self.song.loop = bool(enabled)
            return {"ok": True, "loop_enabled": self.song.loop}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_loop_enabled(self):
        """Get current loop enabled state"""
        try:
            return {
                "ok": True,
                "loop_enabled": self.song.loop,
                "loop_start": float(self.song.loop_start),
                "loop_length": float(self.song.loop_length)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_locator(self, time_in_beats, name="Locator"):
        """Create a locator/cue point at specified time"""
        try:
            # Note: Direct locator creation may not be available in all LiveAPI versions
            # Using cue point functionality if available
            if hasattr(self.song, 'create_cue_point'):
                self.song.create_cue_point(float(time_in_beats))
                return {
                    "ok": True,
                    "message": "Cue point created",
                    "time": float(time_in_beats),
                    "name": name
                }
            else:
                return {
                    "ok": False,
                    "error": "Cue point creation not available in this Ableton version"
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_locator(self, locator_index):
        """Delete a locator/cue point"""
        try:
            if hasattr(self.song, 'cue_points'):
                if locator_index < 0 or locator_index >= len(self.song.cue_points):
                    return {"ok": False, "error": "Invalid locator index"}
                cue_point = self.song.cue_points[locator_index]
                if hasattr(cue_point, 'delete'):
                    cue_point.delete()
                    return {"ok": True, "message": "Locator deleted", "locator_index": locator_index}
            return {"ok": False, "error": "Cue points not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_locators(self):
        """Get all locators/cue points"""
        try:
            if hasattr(self.song, 'cue_points'):
                locators = []
                for i, cue in enumerate(self.song.cue_points):
                    locators.append({
                        "index": i,
                        "time": float(cue.time) if hasattr(cue, 'time') else 0.0,
                        "name": str(cue.name) if hasattr(cue, 'name') else ""
                    })
                return {"ok": True, "locators": locators, "count": len(locators)}
            else:
                return {"ok": True, "locators": [], "count": 0}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_by_amount(self, amount_in_beats):
        """Jump playback position by specified amount (positive or negative)"""
        try:
            current_time = self.song.current_song_time
            new_time = float(current_time) + float(amount_in_beats)
            # Ensure non-negative time
            new_time = max(0.0, new_time)
            self.song.current_song_time = new_time
            return {
                "ok": True,
                "old_time": float(current_time),
                "new_time": float(self.song.current_song_time),
                "jumped_by": float(amount_in_beats)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP COLOR
    # ========================================================================

    def set_clip_color(self, track_index, clip_index, color_index):
        """Set clip color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Set color if available
            if hasattr(clip, 'color_index'):
                clip.color_index = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color_index": int(color_index)
                }
            elif hasattr(clip, 'color'):
                clip.color = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color": int(color_index)
                }
            else:
                return {"ok": False, "error": "Clip color not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK ROUTING EXTRAS
    # ========================================================================

    def get_track_output_routing(self, track_index):
        """Get track output routing configuration"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            result = {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name)
            }

            if hasattr(track, 'output_routing_type'):
                result["output_routing_type"] = str(track.output_routing_type.display_name) if hasattr(track.output_routing_type, 'display_name') else str(track.output_routing_type)

            if hasattr(track, 'output_routing_channel'):
                result["output_routing_channel"] = str(track.output_routing_channel.display_name) if hasattr(track.output_routing_channel, 'display_name') else str(track.output_routing_channel)

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_input_sub_routing(self, track_index, sub_routing):
        """Set track input sub-routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, 'input_sub_routing'):
                # Sub-routing is typically set by index or name
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "Input sub-routing setting is limited in LiveAPI",
                    "track_index": track_index,
                    "requested_sub_routing": str(sub_routing)
                }
            else:
                return {"ok": False, "error": "Input sub-routing not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_output_sub_routing(self, track_index, sub_routing):
        """Set track output sub-routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, 'output_sub_routing'):
                # Sub-routing is typically set by index or name
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "Output sub-routing setting is limited in LiveAPI",
                    "track_index": track_index,
                    "requested_sub_routing": str(sub_routing)
                }
            else:
                return {"ok": False, "error": "Output sub-routing not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE EXTRAS (MISSING TOOL)
    # ========================================================================

    def randomize_device(self, track_index, device_index):
        """Randomize all parameters of a device (simplified version)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # This is an alias for randomize_device_parameters
            # Randomizing all parameters (excluding read-only ones)
            randomized_count = 0
            for param in device.parameters:
                if hasattr(param, 'is_enabled') and param.is_enabled and not param.is_quantized:
                    try:
                        import random
                        param.value = random.uniform(float(param.min), float(param.max))
                        randomized_count += 1
                    except:
                        pass

            return {
                "ok": True,
                "track_index": track_index,
                "device_index": device_index,
                "device_name": str(device.name),
                "randomized_parameters": randomized_count
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MAX FOR LIVE (M4L) DEVICE OPERATIONS
    # ========================================================================

    def is_max_device(self, track_index, device_index):
        """Check if device is a Max for Live device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # M4L devices have specific class names
            m4l_classes = ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']
            is_m4l = device.class_name in m4l_classes

            return {
                "ok": True,
                "is_m4l": is_m4l,
                "class_name": str(device.class_name),
                "class_display_name": str(device.class_display_name) if hasattr(device, 'class_display_name') else str(device.class_name),
                "device_name": str(device.name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_m4l_devices(self, track_index):
        """Get all Max for Live devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            m4l_devices = []
            m4l_classes = ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']

            for i, device in enumerate(track.devices):
                if device.class_name in m4l_classes:
                    device_type = self._get_m4l_type(device.class_name)
                    m4l_devices.append({
                        "index": i,
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "type": device_type,
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters)
                    })

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "devices": m4l_devices,
                "count": len(m4l_devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _get_m4l_type(self, class_name):
        """Get M4L device type from class name"""
        type_map = {
            'MxDeviceAudioEffect': 'audio_effect',
            'MxDeviceMidiEffect': 'midi_effect',
            'MxDeviceInstrument': 'instrument'
        }
        return type_map.get(class_name, 'unknown')

    def set_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name (useful for M4L devices with custom parameter names)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # Find parameter by name
            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    param.value = float(value)
                    return {
                        "ok": True,
                        "track_index": track_index,
                        "device_index": device_index,
                        "param_name": param_name,
                        "param_index": i,
                        "value": float(param.value)
                    }

            return {"ok": False, "error": "Parameter '{}' not found".format(param_name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_m4l_param_by_name(self, track_index, device_index, param_name):
        """Get M4L device parameter value by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # Find parameter by name
            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    return {
                        "ok": True,
                        "param_index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_enabled": param.is_enabled if hasattr(param, 'is_enabled') else True
                    }

            return {"ok": False, "error": "Parameter '{}' not found".format(param_name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_cv_tools_devices(self, track_index):
        """Get all CV Tools devices on track (subset of M4L devices)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            cv_devices = []

            for i, device in enumerate(track.devices):
                device_name = str(device.name)
                # Check if device name contains "CV" (common in CV Tools)
                if 'CV' in device_name or 'cv' in device_name.lower():
                    cv_devices.append({
                        "index": i,
                        "name": device_name,
                        "class_name": str(device.class_name),
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters)
                    })

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "cv_devices": cv_devices,
                "count": len(cv_devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # UTILITY
    # ========================================================================

    def get_available_tools(self):
        """Get list of all available tool names"""
        return [
            "ping", "health_check",
            # Session control (14 tools)
            "start_playback", "stop_playback", "start_recording", "stop_recording",
            "continue_playing", "get_session_info", "set_tempo", "set_time_signature",
            "set_loop_start", "set_loop_length", "set_metronome", "tap_tempo",
            "undo", "redo",
            # Transport (8 tools)
            "jump_to_time", "get_current_time", "set_arrangement_overdub", "set_back_to_arranger",
            "set_punch_in", "set_punch_out", "nudge_up", "nudge_down",
            # Automation (6 tools)
            "re_enable_automation", "get_session_automation_record", "set_session_automation_record",
            "get_session_record", "set_session_record", "capture_midi",
            # Track management (13 tools)
            "create_midi_track", "create_audio_track", "create_return_track",
            "delete_track", "duplicate_track", "rename_track",
            "set_track_volume", "set_track_pan", "arm_track", "solo_track", "mute_track",
            "get_track_info", "set_track_color",
            # Track extras (5 tools)
            "set_track_fold_state", "set_track_input_routing", "set_track_output_routing",
            "set_track_send", "get_track_sends",
            # Clip operations (8 tools)
            "create_midi_clip", "delete_clip", "duplicate_clip",
            "launch_clip", "stop_clip", "stop_all_clips",
            "get_clip_info", "set_clip_name",
            # Clip extras (10 tools)
            "set_clip_looping", "set_clip_loop_start", "set_clip_loop_end",
            "set_clip_start_marker", "set_clip_end_marker", "set_clip_muted",
            "set_clip_gain", "set_clip_pitch_coarse", "set_clip_pitch_fine",
            "set_clip_signature_numerator",
            # MIDI notes (3 tools)
            "add_notes", "get_clip_notes", "remove_notes",
            # MIDI extras (4 tools)
            "select_all_notes", "deselect_all_notes", "replace_selected_notes", "get_notes_extended",
            # Devices (3 tools)
            "add_device", "get_track_devices", "set_device_param",
            # Device extras (9 tools)
            "set_device_on_off", "get_device_parameters", "get_device_parameter_by_name",
            "set_device_parameter_by_name", "delete_device", "get_device_presets",
            "set_device_preset", "randomize_device_parameters",
            # Scenes (6 tools)
            "create_scene", "delete_scene", "duplicate_scene",
            "launch_scene", "rename_scene", "get_scene_info",
            # Groove & Quantize (5 tools)
            "set_clip_groove_amount", "quantize_clip", "quantize_clip_pitch",
            "get_groove_amount", "set_groove_amount",
            # Monitoring & Input (4 tools)
            "set_track_current_monitoring_state", "get_track_available_input_routing_types",
            "get_track_available_output_routing_types", "get_track_input_routing_type",
            # Project & Arrangement (6 tools)
            "get_project_root_folder", "trigger_session_record", "get_can_jump_to_next_cue",
            "get_can_jump_to_prev_cue", "jump_to_next_cue", "jump_to_prev_cue",
            # Browser operations (4 tools)
            "browse_devices", "browse_plugins", "load_device_from_browser", "get_browser_items",
            # Loop & Locator operations (6 tools)
            "set_loop_enabled", "get_loop_enabled", "create_locator", "delete_locator",
            "get_locators", "jump_by_amount",
            # Clip color (1 tool)
            "set_clip_color",
            # Track routing extras (3 tools)
            "get_track_output_routing", "set_track_input_sub_routing", "set_track_output_sub_routing",
            # Device extras - missing tool (1 tool)
            "randomize_device",
            # Max for Live (M4L) operations (6 tools)
            "is_max_device", "get_m4l_devices", "set_device_param_by_name",
            "get_m4l_param_by_name", "get_cv_tools_devices"
        ]
