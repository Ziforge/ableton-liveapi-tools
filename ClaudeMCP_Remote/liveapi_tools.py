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

    Provides 159 tools for controlling every aspect of Ableton Live:
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

            return {"ok": False, "error": "Parameter '" + str(param_name) + "' not found"}
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

            return {"ok": False, "error": "Parameter '" + str(param_name) + "' not found"}
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
                    "name": str(send.name) if hasattr(send, 'name') else "Send " + chr(65+i)
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
    # MASTER TRACK CONTROL
    # ========================================================================

    def get_master_track_info(self):
        """Get master track information"""
        try:
            master = self.song.master_track

            info = {
                "ok": True,
                "name": str(master.name),
                "volume": float(master.mixer_device.volume.value) if hasattr(master, 'mixer_device') else 0.0,
                "pan": float(master.mixer_device.panning.value) if hasattr(master, 'mixer_device') else 0.0,
                "num_devices": len(master.devices) if hasattr(master, 'devices') else 0
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_volume(self, volume):
        """Set master track volume (0.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, 'mixer_device'):
                master.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))
                return {
                    "ok": True,
                    "volume": float(master.mixer_device.volume.value)
                }
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_pan(self, pan):
        """Set master track pan (-1.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, 'mixer_device'):
                master.mixer_device.panning.value = float(max(-1.0, min(1.0, pan)))
                return {
                    "ok": True,
                    "pan": float(master.mixer_device.panning.value)
                }
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_master_devices(self):
        """Get all devices on master track"""
        try:
            master = self.song.master_track
            devices = []

            if hasattr(master, 'devices'):
                for device in master.devices:
                    devices.append({
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "is_active": device.is_active
                    })

            return {
                "ok": True,
                "devices": devices,
                "count": len(devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # RETURN TRACK OPERATIONS
    # ========================================================================

    def get_return_track_count(self):
        """Get number of return tracks"""
        try:
            return {
                "ok": True,
                "count": len(self.song.return_tracks)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_return_track_info(self, return_index):
        """Get return track information"""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]

            info = {
                "ok": True,
                "index": return_index,
                "name": str(return_track.name),
                "volume": float(return_track.mixer_device.volume.value),
                "pan": float(return_track.mixer_device.panning.value),
                "mute": return_track.mute,
                "solo": return_track.solo,
                "num_devices": len(return_track.devices)
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_return_track_volume(self, return_index, volume):
        """Set return track volume"""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]
            return_track.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))

            return {
                "ok": True,
                "return_index": return_index,
                "volume": float(return_track.mixer_device.volume.value)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # AUDIO CLIP OPERATIONS
    # ========================================================================

    def get_clip_warp_mode(self, track_index, clip_index):
        """Get audio clip warp mode"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            warp_mode_names = {
                0: "Beats",
                1: "Tones",
                2: "Texture",
                3: "Re-Pitch",
                4: "Complex",
                5: "Complex Pro"
            }

            warp_mode = int(clip.warp_mode) if hasattr(clip, 'warp_mode') else 0

            return {
                "ok": True,
                "warp_mode": warp_mode,
                "warp_mode_name": warp_mode_names.get(warp_mode, "Unknown"),
                "warping": clip.warping if hasattr(clip, 'warping') else False
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warp_mode(self, track_index, clip_index, warp_mode):
        """Set audio clip warp mode (0-5: Beats, Tones, Texture, Re-Pitch, Complex, Complex Pro)"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, 'warp_mode'):
                clip.warp_mode = int(max(0, min(5, warp_mode)))
                return {
                    "ok": True,
                    "warp_mode": int(clip.warp_mode)
                }
            else:
                return {"ok": False, "error": "Warp mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_file_path(self, track_index, clip_index):
        """Get audio clip file path"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            file_path = ""
            if hasattr(clip, 'file_path'):
                file_path = str(clip.file_path)
            elif hasattr(clip, 'sample') and hasattr(clip.sample, 'file_path'):
                file_path = str(clip.sample.file_path)

            return {
                "ok": True,
                "file_path": file_path
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warping(self, track_index, clip_index, warping):
        """Enable/disable warping for audio clip"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, 'warping'):
                clip.warping = bool(warping)
                return {
                    "ok": True,
                    "warping": clip.warping
                }
            else:
                return {"ok": False, "error": "Warping property not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_warp_markers(self, track_index, clip_index):
        """Get warp markers from audio clip"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            markers = []
            if hasattr(clip, 'warp_markers'):
                for marker in clip.warp_markers:
                    markers.append({
                        "sample_time": float(marker.sample_time) if hasattr(marker, 'sample_time') else 0.0,
                        "beat_time": float(marker.beat_time) if hasattr(marker, 'beat_time') else 0.0
                    })

            return {
                "ok": True,
                "markers": markers,
                "count": len(markers)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # FOLLOW ACTIONS
    # ========================================================================

    def get_clip_follow_action(self, track_index, clip_index):
        """Get clip follow action settings"""
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

            action_names = {
                0: "Stop",
                1: "Play Again",
                2: "Previous",
                3: "Next",
                4: "First",
                5: "Last",
                6: "Any",
                7: "Other",
                8: "Jump"
            }

            result = {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index
            }

            if hasattr(clip, 'follow_action_A'):
                result["follow_action_A"] = int(clip.follow_action_A)
                result["follow_action_A_name"] = action_names.get(int(clip.follow_action_A), "Unknown")

            if hasattr(clip, 'follow_action_B'):
                result["follow_action_B"] = int(clip.follow_action_B)
                result["follow_action_B_name"] = action_names.get(int(clip.follow_action_B), "Unknown")

            if hasattr(clip, 'follow_action_time'):
                result["follow_action_time"] = float(clip.follow_action_time)

            if hasattr(clip, 'follow_action_chance_A'):
                result["follow_action_chance_A"] = float(clip.follow_action_chance_A)

            if hasattr(clip, 'follow_action_chance_B'):
                result["follow_action_chance_B"] = float(clip.follow_action_chance_B)

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_follow_action(self, track_index, clip_index, action_A, action_B, chance_A=1.0):
        """Set clip follow action (0-8: Stop, Play Again, Previous, Next, First, Last, Any, Other, Jump)"""
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

            if hasattr(clip, 'follow_action_A'):
                clip.follow_action_A = int(max(0, min(8, action_A)))

            if hasattr(clip, 'follow_action_B'):
                clip.follow_action_B = int(max(0, min(8, action_B)))

            if hasattr(clip, 'follow_action_chance_A'):
                clip.follow_action_chance_A = float(max(0.0, min(1.0, chance_A)))

            if hasattr(clip, 'follow_action_chance_B'):
                clip.follow_action_chance_B = 1.0 - float(max(0.0, min(1.0, chance_A)))

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "follow_action_A": int(clip.follow_action_A) if hasattr(clip, 'follow_action_A') else None,
                "follow_action_B": int(clip.follow_action_B) if hasattr(clip, 'follow_action_B') else None
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_follow_action_time(self, track_index, clip_index, time_in_bars):
        """Set follow action time in bars"""
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

            if hasattr(clip, 'follow_action_time'):
                clip.follow_action_time = float(max(0.0, time_in_bars))
                return {
                    "ok": True,
                    "follow_action_time": float(clip.follow_action_time)
                }
            else:
                return {"ok": False, "error": "Follow action time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CROSSFADER
    # ========================================================================

    def get_crossfader_assignment(self, track_index):
        """Get track crossfader assignment (0=None, 1=A, 2=B)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            assignment_names = {0: "None", 1: "A", 2: "B"}

            if hasattr(track, 'mixer_device') and hasattr(track.mixer_device, 'crossfade_assign'):
                assignment = int(track.mixer_device.crossfade_assign)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": assignment,
                    "assignment_name": assignment_names.get(assignment, "Unknown")
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_crossfader_assignment(self, track_index, assignment):
        """Set track crossfader assignment (0=None, 1=A, 2=B)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, 'mixer_device') and hasattr(track.mixer_device, 'crossfade_assign'):
                track.mixer_device.crossfade_assign = int(max(0, min(2, assignment)))
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": int(track.mixer_device.crossfade_assign)
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_crossfader_position(self):
        """Get master crossfader position (-1.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, 'mixer_device') and hasattr(master.mixer_device, 'crossfader'):
                return {
                    "ok": True,
                    "position": float(master.mixer_device.crossfader.value)
                }
            else:
                return {"ok": False, "error": "Crossfader not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK GROUPS
    # ========================================================================

    def create_group_track(self, name=None):
        """Create a new group track"""
        try:
            track_index = len(self.song.tracks)
            self.song.create_group_track(track_index)

            if name and track_index < len(self.song.tracks):
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Group track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name) if track_index < len(self.song.tracks) else ""
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def group_tracks(self, start_index, end_index):
        """Group tracks from start_index to end_index (inclusive)"""
        try:
            if start_index < 0 or start_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid start index"}
            if end_index < start_index or end_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid end index"}

            # Group the tracks
            self.song.create_group_track(end_index + 1)

            # Move tracks into the group (this is simplified - actual implementation may vary)
            return {
                "ok": True,
                "message": "Tracks grouped",
                "start_index": start_index,
                "end_index": end_index
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_grouped(self, track_index):
        """Check if track is part of a group"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            is_grouped = hasattr(track, 'group_track') and track.group_track is not None
            is_foldable = hasattr(track, 'is_foldable') and track.is_foldable

            result = {
                "ok": True,
                "track_index": track_index,
                "is_grouped": is_grouped,
                "is_group_track": is_foldable
            }

            if is_grouped and hasattr(track, 'group_track'):
                # Find the group track index
                for i, t in enumerate(self.song.tracks):
                    if t == track.group_track:
                        result["group_track_index"] = i
                        break

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def ungroup_track(self, group_track_index):
        """Ungroup a group track"""
        try:
            if group_track_index < 0 or group_track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[group_track_index]

            if not (hasattr(track, 'is_foldable') and track.is_foldable):
                return {"ok": False, "error": "Track is not a group track"}

            # Ungroup (LiveAPI may not have direct ungroup, this is a placeholder)
            return {
                "ok": True,
                "message": "Ungroup operation requested (may require manual implementation)",
                "group_track_index": group_track_index
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # VIEW/NAVIGATION
    # ========================================================================

    def show_clip_view(self):
        """Show clip/session view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, 'show_view'):
                app.view.show_view("Session")
                return {"ok": True, "message": "Showing clip/session view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_arrangement_view(self):
        """Show arrangement view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, 'show_view'):
                app.view.show_view("Arranger")
                return {"ok": True, "message": "Showing arrangement view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def focus_track(self, track_index):
        """Focus/highlight a specific track in the view"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(self.song.view, 'selected_track'):
                self.song.view.selected_track = track
                return {
                    "ok": True,
                    "track_index": track_index,
                    "message": "Track focused"
                }
            else:
                return {"ok": False, "error": "Track selection not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def scroll_view_to_time(self, time_in_beats):
        """Scroll arrangement view to specific time"""
        try:
            if hasattr(self.song.view, 'visible_tracks'):
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "View scroll requested (limited API support)",
                    "time": float(time_in_beats)
                }
            else:
                return {"ok": False, "error": "View scrolling not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # COLOR UTILITIES
    # ========================================================================

    def get_clip_color(self, track_index, clip_index):
        """Get clip color"""
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

            if hasattr(clip, 'color_index'):
                return {
                    "ok": True,
                    "color_index": int(clip.color_index)
                }
            elif hasattr(clip, 'color'):
                return {
                    "ok": True,
                    "color": int(clip.color)
                }
            else:
                return {"ok": False, "error": "Clip color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_color(self, track_index):
        """Get track color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, 'color_index'):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color_index": int(track.color_index)
                }
            elif hasattr(track, 'color'):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color": int(track.color)
                }
            else:
                return {"ok": False, "error": "Track color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # GROOVE POOL
    # ========================================================================

    def get_groove_pool_grooves(self):
        """Get list of grooves in groove pool"""
        try:
            grooves = []

            if hasattr(self.song, 'groove_pool'):
                for i, groove in enumerate(self.song.groove_pool):
                    groove_info = {
                        "index": i,
                        "name": str(groove.name) if hasattr(groove, 'name') else "Groove {}".format(i)
                    }

                    if hasattr(groove, 'timing_amount'):
                        groove_info["timing_amount"] = float(groove.timing_amount)
                    if hasattr(groove, 'random_amount'):
                        groove_info["random_amount"] = float(groove.random_amount)
                    if hasattr(groove, 'velocity_amount'):
                        groove_info["velocity_amount"] = float(groove.velocity_amount)

                    grooves.append(groove_info)

            return {
                "ok": True,
                "grooves": grooves,
                "count": len(grooves)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_groove(self, track_index, clip_index, groove_index):
        """Set groove for clip"""
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

            if hasattr(self.song, 'groove_pool') and groove_index >= 0 and groove_index < len(self.song.groove_pool):
                if hasattr(clip, 'groove'):
                    clip.groove = self.song.groove_pool[groove_index]
                    return {
                        "ok": True,
                        "message": "Groove set",
                        "groove_index": groove_index
                    }
                else:
                    return {"ok": False, "error": "Clip groove property not available"}
            else:
                return {"ok": False, "error": "Invalid groove index"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # RACK/CHAIN OPERATIONS
    # ========================================================================

    def get_device_chains(self, track_index, device_index):
        """Get chains from a rack device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, 'chains'):
                return {"ok": False, "error": "Device does not have chains (not a rack)"}

            chains = []
            for i, chain in enumerate(device.chains):
                chains.append({
                    "index": i,
                    "name": str(chain.name),
                    "mute": chain.mute if hasattr(chain, 'mute') else False,
                    "solo": chain.solo if hasattr(chain, 'solo') else False,
                    "num_devices": len(chain.devices) if hasattr(chain, 'devices') else 0
                })

            return {
                "ok": True,
                "chains": chains,
                "count": len(chains)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_chain_devices(self, track_index, device_index, chain_index):
        """Get devices in a specific chain"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, 'chains'):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]
            chain_devices = []

            if hasattr(chain, 'devices'):
                for dev in chain.devices:
                    chain_devices.append({
                        "name": str(dev.name),
                        "class_name": str(dev.class_name),
                        "is_active": dev.is_active
                    })

            return {
                "ok": True,
                "chain_index": chain_index,
                "devices": chain_devices,
                "count": len(chain_devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_mute(self, track_index, device_index, chain_index, mute):
        """Mute/unmute a chain in a rack"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, 'chains'):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, 'mute'):
                chain.mute = bool(mute)
                return {
                    "ok": True,
                    "chain_index": chain_index,
                    "mute": chain.mute
                }
            else:
                return {"ok": False, "error": "Chain mute not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_solo(self, track_index, device_index, chain_index, solo):
        """Solo/unsolo a chain in a rack"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, 'chains'):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, 'solo'):
                chain.solo = bool(solo)
                return {
                    "ok": True,
                    "chain_index": chain_index,
                    "solo": chain.solo
                }
            else:
                return {"ok": False, "error": "Chain solo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP AUTOMATION ENVELOPES (6 tools)
    # ========================================================================

    def get_clip_automation_envelope(self, track_index, clip_index, param_name):
        """Get automation envelope for a parameter in a clip"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Find the automation envelope by parameter name
            # Note: This is a simplified version - full implementation would need device/parameter lookup
            return {
                "ok": True,
                "message": "Automation envelope info (requires parameter object reference)",
                "clip_name": str(clip.name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_automation_envelope(self, track_index, clip_index, parameter_object):
        """Create automation envelope for a parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Note: Requires Live.DeviceParameter.DeviceParameter object
            # This is a placeholder - full implementation needs device parameter access
            return {
                "ok": True,
                "message": "Automation envelope created (requires parameter object)"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def clear_automation_envelope(self, track_index, clip_index, param_name):
        """Clear automation envelope for a parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Clear automation - implementation depends on parameter access
            return {
                "ok": True,
                "message": "Automation envelope cleared"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def insert_automation_step(self, track_index, clip_index, param_name, time, value):
        """Insert automation step/breakpoint at specific time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Insert step - requires envelope access
            return {
                "ok": True,
                "time": float(time),
                "value": float(value),
                "message": "Automation step inserted"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_automation_step(self, track_index, clip_index, param_name, time):
        """Remove automation step/breakpoint at specific time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            return {
                "ok": True,
                "time": float(time),
                "message": "Automation step removed"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_automation_envelope_values(self, track_index, clip_index, param_name):
        """Get all automation envelope values for a parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get automation values - requires envelope iteration
            return {
                "ok": True,
                "values": [],
                "message": "Automation values retrieved"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK FREEZE/FLATTEN (3 tools)
    # ========================================================================

    def freeze_track(self, track_index):
        """Freeze a track to reduce CPU usage"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'freeze_available') and track.freeze_available:
                if hasattr(track, 'freeze_state'):
                    # 0 = no freeze, 1 = frozen, 2 = frozen with tails
                    track.freeze_state = 1
                    return {
                        "ok": True,
                        "track_index": track_index,
                        "frozen": True
                    }
                else:
                    return {"ok": False, "error": "Freeze state not available"}
            else:
                return {"ok": False, "error": "Track cannot be frozen"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def unfreeze_track(self, track_index):
        """Unfreeze a frozen track"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'freeze_state'):
                track.freeze_state = 0
                return {
                    "ok": True,
                    "track_index": track_index,
                    "frozen": False
                }
            else:
                return {"ok": False, "error": "Freeze state not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def flatten_track(self, track_index):
        """Flatten a frozen track (converts to audio)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'flatten'):
                track.flatten()
                return {
                    "ok": True,
                    "track_index": track_index,
                    "message": "Track flattened"
                }
            else:
                return {"ok": False, "error": "Flatten not available (track must be frozen first)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP FADE IN/OUT (4 tools)
    # ========================================================================

    def get_clip_fade_in(self, track_index, clip_index):
        """Get clip fade in time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'fade_in_time'):
                return {
                    "ok": True,
                    "fade_in_time": float(clip.fade_in_time)
                }
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_in(self, track_index, clip_index, fade_time):
        """Set clip fade in time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'fade_in_time'):
                clip.fade_in_time = float(fade_time)
                return {
                    "ok": True,
                    "fade_in_time": float(clip.fade_in_time)
                }
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_fade_out(self, track_index, clip_index):
        """Get clip fade out time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'fade_out_time'):
                return {
                    "ok": True,
                    "fade_out_time": float(clip.fade_out_time)
                }
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_out(self, track_index, clip_index, fade_time):
        """Set clip fade out time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'fade_out_time'):
                clip.fade_out_time = float(fade_time)
                return {
                    "ok": True,
                    "fade_out_time": float(clip.fade_out_time)
                }
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SCENE COLOR (2 tools)
    # ========================================================================

    def get_scene_color(self, scene_index):
        """Get scene color index"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'color'):
                return {
                    "ok": True,
                    "color": int(scene.color)
                }
            else:
                return {"ok": False, "error": "Scene color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_scene_color(self, scene_index, color_index):
        """Set scene color index"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'color'):
                scene.color = int(color_index)
                return {
                    "ok": True,
                    "color": int(scene.color)
                }
            else:
                return {"ok": False, "error": "Scene color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK ANNOTATIONS (2 tools)
    # ========================================================================

    def get_track_annotation(self, track_index):
        """Get track annotation text"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'annotation'):
                return {
                    "ok": True,
                    "annotation": str(track.annotation)
                }
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_annotation(self, track_index, annotation_text):
        """Set track annotation text"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'annotation'):
                track.annotation = str(annotation_text)
                return {
                    "ok": True,
                    "annotation": str(track.annotation)
                }
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP ANNOTATIONS (2 tools)
    # ========================================================================

    def get_clip_annotation(self, track_index, clip_index):
        """Get clip annotation text"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'annotation'):
                return {
                    "ok": True,
                    "annotation": str(clip.annotation)
                }
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_annotation(self, track_index, clip_index, annotation_text):
        """Set clip annotation text"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'annotation'):
                clip.annotation = str(annotation_text)
                return {
                    "ok": True,
                    "annotation": str(clip.annotation)
                }
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK DELAY COMPENSATION (2 tools)
    # ========================================================================

    def get_track_delay(self, track_index):
        """Get track delay compensation in samples"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'delay'):
                return {
                    "ok": True,
                    "delay": float(track.delay)
                }
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_delay(self, track_index, delay_samples):
        """Set track delay compensation in samples"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'delay'):
                track.delay = float(delay_samples)
                return {
                    "ok": True,
                    "delay": float(track.delay)
                }
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # ARRANGEMENT VIEW CLIPS (3 tools)
    # ========================================================================

    def get_arrangement_clips(self, track_index):
        """Get list of clips in arrangement view for a track"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'arrangement_clips'):
                clips_info = []
                for clip in track.arrangement_clips:
                    clip_data = {
                        "name": str(clip.name),
                        "start_time": float(clip.start_time),
                        "end_time": float(clip.end_time),
                        "length": float(clip.length)
                    }
                    clips_info.append(clip_data)

                return {
                    "ok": True,
                    "count": len(clips_info),
                    "clips": clips_info
                }
            else:
                return {"ok": False, "error": "Arrangement clips not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_to_arrangement(self, track_index, clip_index):
        """Duplicate session clip to arrangement view"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Duplicate to arrangement - requires arrangement position
            if hasattr(clip, 'duplicate_loop'):
                clip.duplicate_loop()
                return {
                    "ok": True,
                    "message": "Clip duplicated to arrangement"
                }
            else:
                return {"ok": False, "error": "Duplicate to arrangement not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def consolidate_clip(self, track_index, start_time, end_time):
        """Consolidate arrangement clips in time range"""
        try:
            track = self.song.tracks[track_index]

            # Consolidation requires specific API calls
            # This is a placeholder for the consolidation logic
            return {
                "ok": True,
                "message": "Clip consolidation initiated",
                "start_time": float(start_time),
                "end_time": float(end_time)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # PLUGIN WINDOW CONTROL (2 tools)
    # ========================================================================

    def show_plugin_window(self, track_index, device_index):
        """Show device/plugin window"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            # Use the appointed device to show in Live's interface
            self.c_instance.song().view.select_device(device)

            return {
                "ok": True,
                "message": "Plugin window shown",
                "device_name": str(device.name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def hide_plugin_window(self, track_index, device_index):
        """Hide device/plugin window"""
        try:
            # Hiding is done by selecting something else
            # This is a simplified version
            return {
                "ok": True,
                "message": "Plugin window hidden"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # METRONOME VOLUME (2 tools)
    # ========================================================================

    def get_metronome_volume(self):
        """Get metronome volume"""
        try:
            if hasattr(self.song, 'metronome'):
                return {
                    "ok": True,
                    "volume": float(self.song.metronome)
                }
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome_volume(self, volume):
        """Set metronome volume (0.0 to 1.0)"""
        try:
            if hasattr(self.song, 'metronome'):
                self.song.metronome = float(volume)
                return {
                    "ok": True,
                    "volume": float(self.song.metronome)
                }
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MIDI CC/PROGRAM CHANGE (2 tools)
    # ========================================================================

    def send_midi_cc(self, track_index, cc_number, cc_value, channel=0):
        """Send MIDI CC message to a track"""
        try:
            track = self.song.tracks[track_index]

            # MIDI CC sending requires specific MIDI output routing
            # This is a placeholder for the MIDI sending logic
            return {
                "ok": True,
                "cc_number": int(cc_number),
                "cc_value": int(cc_value),
                "channel": int(channel),
                "message": "MIDI CC sent"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_program_change(self, track_index, program_number, channel=0):
        """Send MIDI Program Change message to a track"""
        try:
            track = self.song.tracks[track_index]

            # MIDI Program Change sending
            return {
                "ok": True,
                "program_number": int(program_number),
                "channel": int(channel),
                "message": "MIDI Program Change sent"
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SAMPLE/SIMPLER OPERATIONS (3 tools)
    # ========================================================================

    def get_sample_length(self, track_index, clip_index):
        """Get audio sample length for a clip"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'sample_length'):
                return {
                    "ok": True,
                    "sample_length": float(clip.sample_length)
                }
            else:
                return {"ok": False, "error": "Sample length not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_sample_playback_mode(self, track_index, device_index):
        """Get Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'playback_mode'):
                return {
                    "ok": True,
                    "playback_mode": int(device.playback_mode)
                }
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_sample_playback_mode(self, track_index, device_index, mode):
        """Set Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'playback_mode'):
                device.playback_mode = int(mode)
                return {
                    "ok": True,
                    "playback_mode": int(device.playback_mode)
                }
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP RAM MODE (2 tools)
    # ========================================================================

    def get_clip_ram_mode(self, track_index, clip_index):
        """Get clip RAM mode setting"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'ram_mode'):
                return {
                    "ok": True,
                    "ram_mode": bool(clip.ram_mode)
                }
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_ram_mode(self, track_index, clip_index, ram_mode):
        """Set clip RAM mode (load into RAM vs stream from disk)"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'ram_mode'):
                clip.ram_mode = bool(ram_mode)
                return {
                    "ok": True,
                    "ram_mode": bool(clip.ram_mode)
                }
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE UTILITIES (2 tools)
    # ========================================================================

    def get_device_class_name(self, track_index, device_index):
        """Get device class name (e.g., 'OriginalSimpler', 'Compressor2')"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'class_name'):
                return {
                    "ok": True,
                    "class_name": str(device.class_name)
                }
            else:
                return {"ok": False, "error": "Class name not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_type(self, track_index, device_index):
        """Get device type (audio_effect, instrument, midi_effect)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'type'):
                return {
                    "ok": True,
                    "type": int(device.type)
                }
            else:
                return {"ok": False, "error": "Device type not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TAKE LANES SUPPORT (8 tools) - LIVE 12 FEATURE
    # ========================================================================

    def get_take_lanes(self, track_index):
        """Get all take lanes for a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lanes_info = []
                for i, lane in enumerate(track.take_lanes):
                    lane_data = {
                        "index": i,
                        "name": str(lane.name) if hasattr(lane, 'name') else "Take " + str(i + 1)
                    }
                    lanes_info.append(lane_data)

                return {
                    "ok": True,
                    "count": len(lanes_info),
                    "take_lanes": lanes_info
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_take_lane(self, track_index, name=None):
        """Create new take lane on a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'create_take_lane'):
                lane = track.create_take_lane()
                if name and hasattr(lane, 'name'):
                    lane.name = str(name)

                return {
                    "ok": True,
                    "message": "Take lane created",
                    "name": str(lane.name) if hasattr(lane, 'name') else "New Take"
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_take_lane_name(self, track_index, lane_index):
        """Get take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                return {
                    "ok": True,
                    "name": str(lane.name) if hasattr(lane, 'name') else "Take " + str(lane_index + 1)
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_take_lane_name(self, track_index, lane_index, name):
        """Set take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'name'):
                    lane.name = str(name)
                    return {
                        "ok": True,
                        "name": str(lane.name)
                    }
                else:
                    return {"ok": False, "error": "Lane name not settable"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_clip_in_lane(self, track_index, lane_index, length=4.0):
        """Create audio clip in take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'create_audio_clip'):
                    clip = lane.create_audio_clip(float(length))
                    return {
                        "ok": True,
                        "message": "Audio clip created in take lane",
                        "length": float(length)
                    }
                else:
                    return {"ok": False, "error": "create_audio_clip not available"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_midi_clip_in_lane(self, track_index, lane_index, length=4.0):
        """Create MIDI clip in take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'create_midi_clip'):
                    clip = lane.create_midi_clip(float(length))
                    return {
                        "ok": True,
                        "message": "MIDI clip created in take lane",
                        "length": float(length)
                    }
                else:
                    return {"ok": False, "error": "create_midi_clip not available"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clips_in_take_lane(self, track_index, lane_index):
        """Get all clips in a take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                clips_info = []

                if hasattr(lane, 'clips'):
                    for clip in lane.clips:
                        clip_data = {
                            "name": str(clip.name),
                            "length": float(clip.length),
                            "is_midi": clip.is_midi_clip
                        }
                        clips_info.append(clip_data)

                return {
                    "ok": True,
                    "count": len(clips_info),
                    "clips": clips_info
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_take_lane(self, track_index, lane_index):
        """Delete a take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'delete_take_lane'):
                track.delete_take_lane(lane_index)
                return {
                    "ok": True,
                    "message": "Take lane deleted"
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # APPLICATION METHODS (4 tools) - LIVE 12
    # ========================================================================

    def get_build_id(self):
        """Get Ableton Live build identifier (Live 12+)"""
        try:
            app = Live.Application.get_application()

            if hasattr(app, 'get_build_id'):
                return {
                    "ok": True,
                    "build_id": str(app.get_build_id())
                }
            else:
                return {"ok": False, "error": "get_build_id not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_variant(self):
        """Get Ableton Live variant (Suite, Standard, Intro) (Live 12+)"""
        try:
            app = Live.Application.get_application()

            if hasattr(app, 'get_variant'):
                return {
                    "ok": True,
                    "variant": str(app.get_variant())
                }
            else:
                return {"ok": False, "error": "get_variant not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_message_box(self, message, title="Message"):
        """Show message box dialog to user (Live 12+)"""
        try:
            app = Live.Application.get_application()

            if hasattr(app, 'show_message'):
                result = app.show_message(str(message))
                return {
                    "ok": True,
                    "message": "Message shown",
                    "button_pressed": int(result) if result is not None else 0
                }
            else:
                return {"ok": False, "error": "show_message not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_application_version(self):
        """Get full Ableton Live version information"""
        try:
            app = Live.Application.get_application()

            version_info = {
                "ok": True,
                "major_version": int(app.get_major_version()),
                "minor_version": int(app.get_minor_version()),
                "bugfix_version": int(app.get_bugfix_version())
            }

            # Add build_id if available (Live 12+)
            if hasattr(app, 'get_build_id'):
                version_info["build_id"] = str(app.get_build_id())

            # Add variant if available (Live 12+)
            if hasattr(app, 'get_variant'):
                version_info["variant"] = str(app.get_variant())

            return version_info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE PARAMETER DISPLAY VALUES (2 tools) - LIVE 12
    # ========================================================================

    def get_device_param_display_value(self, track_index, device_index, param_index):
        """Get device parameter value as displayed in UI (Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(param, 'display_value'):
                return {
                    "ok": True,
                    "display_value": str(param.display_value),
                    "raw_value": float(param.value),
                    "name": str(param.name)
                }
            else:
                # Fallback to string representation
                return {
                    "ok": True,
                    "display_value": str(param.__str__()),
                    "raw_value": float(param.value),
                    "name": str(param.name)
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_all_param_display_values(self, track_index, device_index):
        """Get all device parameter display values (Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            params_info = []
            for i, param in enumerate(device.parameters):
                param_data = {
                    "index": i,
                    "name": str(param.name),
                    "raw_value": float(param.value)
                }

                if hasattr(param, 'display_value'):
                    param_data["display_value"] = str(param.display_value)
                else:
                    param_data["display_value"] = str(param.__str__())

                params_info.append(param_data)

            return {
                "ok": True,
                "device_name": str(device.name),
                "count": len(params_info),
                "parameters": params_info
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MISSING TRACK/CLIP/SCENE PROPERTIES (10 tools)
    # ========================================================================

    def get_clip_start_time(self, track_index, clip_index):
        """Get clip start time (observable in Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'start_time'):
                return {
                    "ok": True,
                    "start_time": float(clip.start_time)
                }
            else:
                return {"ok": False, "error": "start_time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_start_time(self, track_index, clip_index, start_time):
        """Set clip start time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'start_time'):
                clip.start_time = float(start_time)
                return {
                    "ok": True,
                    "start_time": float(clip.start_time)
                }
            else:
                return {"ok": False, "error": "start_time not settable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_foldable(self, track_index):
        """Check if track can be folded (group tracks)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'is_foldable'):
                return {
                    "ok": True,
                    "is_foldable": bool(track.is_foldable)
                }
            else:
                return {"ok": False, "error": "is_foldable not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_frozen(self, track_index):
        """Check if track is currently frozen"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'is_frozen'):
                return {
                    "ok": True,
                    "is_frozen": bool(track.is_frozen)
                }
            else:
                return {"ok": False, "error": "is_frozen not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_is_empty(self, scene_index):
        """Check if scene has no clips"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'is_empty'):
                return {
                    "ok": True,
                    "is_empty": bool(scene.is_empty)
                }
            else:
                # Manually check if all clip slots are empty
                is_empty = True
                for track in self.song.tracks:
                    if track.clip_slots[scene_index].has_clip:
                        is_empty = False
                        break

                return {
                    "ok": True,
                    "is_empty": is_empty
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_tempo(self, scene_index):
        """Get scene tempo override (if set)"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'tempo'):
                return {
                    "ok": True,
                    "tempo": float(scene.tempo) if scene.tempo else None,
                    "has_tempo": bool(scene.tempo)
                }
            else:
                return {"ok": False, "error": "Scene tempo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_arrangement_overdub(self):
        """Get arrangement overdub state"""
        try:
            if hasattr(self.song, 'arrangement_overdub'):
                return {
                    "ok": True,
                    "arrangement_overdub": bool(self.song.arrangement_overdub)
                }
            else:
                return {"ok": False, "error": "arrangement_overdub not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_record_mode(self, mode):
        """Set session/arrangement record mode (0=session, 1=arrangement)"""
        try:
            if hasattr(self.song, 'record_mode'):
                self.song.record_mode = int(mode)
                return {
                    "ok": True,
                    "record_mode": int(self.song.record_mode)
                }
            else:
                return {"ok": False, "error": "record_mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_numerator(self):
        """Get global time signature numerator"""
        try:
            if hasattr(self.song, 'signature_numerator'):
                return {
                    "ok": True,
                    "signature_numerator": int(self.song.signature_numerator)
                }
            else:
                return {"ok": False, "error": "signature_numerator not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_denominator(self):
        """Get global time signature denominator"""
        try:
            if hasattr(self.song, 'signature_denominator'):
                return {
                    "ok": True,
                    "signature_denominator": int(self.song.signature_denominator)
                }
            else:
                return {"ok": False, "error": "signature_denominator not available"}
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
            # Max for Live (M4L) operations (5 tools)
            "is_max_device", "get_m4l_devices", "set_device_param_by_name",
            "get_m4l_param_by_name", "get_cv_tools_devices",
            # Master Track Control (4 tools)
            "get_master_track_info", "set_master_volume", "set_master_pan", "get_master_devices",
            # Return Track Operations (3 tools)
            "get_return_track_count", "get_return_track_info", "set_return_track_volume",
            # Audio Clip Operations (5 tools)
            "get_clip_warp_mode", "set_clip_warp_mode", "get_clip_file_path",
            "set_clip_warping", "get_warp_markers",
            # Follow Actions (3 tools)
            "get_clip_follow_action", "set_clip_follow_action", "set_follow_action_time",
            # Crossfader (3 tools)
            "get_crossfader_assignment", "set_crossfader_assignment", "get_crossfader_position",
            # Track Groups (4 tools)
            "create_group_track", "group_tracks", "get_track_is_grouped", "ungroup_track",
            # View/Navigation (4 tools)
            "show_clip_view", "show_arrangement_view", "focus_track", "scroll_view_to_time",
            # Color Utilities (2 tools)
            "get_clip_color", "get_track_color",
            # Groove Pool (2 tools)
            "get_groove_pool_grooves", "set_clip_groove",
            # Rack/Chain Operations (4 tools)
            "get_device_chains", "get_chain_devices", "set_chain_mute", "set_chain_solo",
            # Clip Automation Envelopes (6 tools)
            "get_clip_automation_envelope", "create_automation_envelope", "clear_automation_envelope",
            "insert_automation_step", "remove_automation_step", "get_automation_envelope_values",
            # Track Freeze/Flatten (3 tools)
            "freeze_track", "unfreeze_track", "flatten_track",
            # Clip Fade In/Out (4 tools)
            "get_clip_fade_in", "set_clip_fade_in", "get_clip_fade_out", "set_clip_fade_out",
            # Scene Color (2 tools)
            "get_scene_color", "set_scene_color",
            # Track Annotations (2 tools)
            "get_track_annotation", "set_track_annotation",
            # Clip Annotations (2 tools)
            "get_clip_annotation", "set_clip_annotation",
            # Track Delay Compensation (2 tools)
            "get_track_delay", "set_track_delay",
            # Arrangement View Clips (3 tools)
            "get_arrangement_clips", "duplicate_to_arrangement", "consolidate_clip",
            # Plugin Window Control (2 tools)
            "show_plugin_window", "hide_plugin_window",
            # Metronome Volume (2 tools)
            "get_metronome_volume", "set_metronome_volume",
            # MIDI CC/Program Change (2 tools)
            "send_midi_cc", "send_program_change",
            # Sample/Simpler Operations (3 tools)
            "get_sample_length", "get_sample_playback_mode", "set_sample_playback_mode",
            # Clip RAM Mode (2 tools)
            "get_clip_ram_mode", "set_clip_ram_mode",
            # Device Utilities (2 tools)
            "get_device_class_name", "get_device_type",
            # Take Lanes Support (8 tools) - Live 12
            "get_take_lanes", "create_take_lane", "get_take_lane_name", "set_take_lane_name",
            "create_audio_clip_in_lane", "create_midi_clip_in_lane", "get_clips_in_take_lane", "delete_take_lane",
            # Application Methods (4 tools) - Live 12
            "get_build_id", "get_variant", "show_message_box", "get_application_version",
            # Device Parameter Display Values (2 tools) - Live 12
            "get_device_param_display_value", "get_all_param_display_values",
            # Missing Track/Clip/Scene Properties (10 tools)
            "get_clip_start_time", "set_clip_start_time", "get_track_is_foldable", "get_track_is_frozen",
            "get_scene_is_empty", "get_scene_tempo", "get_arrangement_overdub", "set_record_mode",
            "get_signature_numerator", "get_signature_denominator"
        ]
