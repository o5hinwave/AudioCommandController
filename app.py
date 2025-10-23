# app.py - Enhanced FaderPort 16 Emulator
import gradio as gr
import mido
import pyaudio
import speech_recognition as sr
from transformers import pipeline
import pandas as pd
import json
import os
import wave
import threading
import time
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class FaderPortEmulator:
    def __init__(self):
        self.audio_initialized = False
        self.midi_initialized = False
        self.transformer_initialized = False
        self.initialize_components()
        self.load_session_state()
        self.chat_history = pd.DataFrame(columns=['user_input', 'bot_response', 'timestamp'])

    def initialize_components(self):
        """Initialize all components with error handling"""
        # Initialize PyAudio
        try:
            self.p = pyaudio.PyAudio()
            self.audio_initialized = True
            logger.info("PyAudio initialized successfully")
        except Exception as e:
            logger.error(f"PyAudio initialization failed: {e}")
            self.p = None

        # Initialize MIDI output
        try:
            # Try multiple common LoopMIDI port names
            port_names = ['LoopMIDI Port 1', 'LoopMIDI Port', 'loopMIDI Port 1']
            for port_name in port_names:
                try:
                    self.midi_out = mido.open_output(port_name)
                    self.midi_initialized = True
                    logger.info(f"MIDI port '{port_name}' connected successfully")
                    break
                except:
                    continue
            if not self.midi_initialized:
                raise Exception("No LoopMIDI ports found")
        except Exception as e:
            logger.error(f"MIDI initialization failed: {e}")
            self.midi_out = None

        # Initialize Transformers
        try:
            # Try multiple models for robustness
            models = [
                "facebook/blenderbot-400M-distill",
                "microsoft/DialoGPT-medium",
                "microsoft/DialoGPT-small"
            ]
            for model in models:
                try:
                    self.chatbot = pipeline("conversational", model=model)
                    self.transformer_initialized = True
                    logger.info(f"Transformer model '{model}' loaded successfully")
                    break
                except:
                    continue
            if not self.transformer_initialized:
                raise Exception("No suitable transformer models available")
        except Exception as e:
            logger.error(f"Transformer initialization failed: {e}")
            self.chatbot = None

    def load_session_state(self):
        """Load or create session state"""
        if not os.path.exists('faderport_data.json'):
            self.session_state = {
                'tracks': [{'name': f'Track {i+1}', 'fader': 0.5, 'muted': False, 'solo': False}
                          for i in range(16)],
                'plugins': ['Blue Cat PatchWork'],
                'transport': {'playing': False, 'recording': False},
                'settings': {'audio_sample_rate': 44100, 'buffer_size': 512}
            }
            self.save_state()
        else:
            with open('faderport_data.json', 'r') as f:
                self.session_state = json.load(f)

    def save_state(self):
        """Save session state to file"""
        try:
            with open('faderport_data.json', 'w') as f:
                json.dump(self.session_state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def save_chat(self, user_input, bot_response):
        """Save chat history"""
        try:
            new_row = pd.DataFrame({
                'user_input': [user_input],
                'bot_response': [bot_response],
                'timestamp': [pd.Timestamp.now()]
            })
            self.chat_history = pd.concat([self.chat_history, new_row], ignore_index=True)
            self.chat_history.to_json('chat_history.json', orient='records', lines=True)
        except Exception as e:
            logger.error(f"Failed to save chat: {e}")

    def record_voice_gradio(self, audio_data):
        """Process audio from Gradio component"""
        if audio_data is None:
            return "No audio received"

        try:
            # Handle Gradio audio format (sample_rate, audio_array)
            if isinstance(audio_data, tuple):
                sample_rate, audio_array = audio_data

                # Convert to appropriate format for speech recognition
                import numpy as np

                # Normalize audio
                if audio_array.dtype != np.int16:
                    audio_array = (audio_array * 32767).astype(np.int16)

                # Save temporary WAV file
                temp_filename = "temp_gradio_audio.wav"
                with wave.open(temp_filename, 'wb') as wf:
                    wf.setnchannels(1)  # Mono
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_array.tobytes())

                # Use speech recognition
                r = sr.Recognizer()
                with sr.AudioFile(temp_filename) as source:
                    audio = r.record(source)

                # Try Google first, fallback to Sphinx
                try:
                    text = r.recognize_google(audio).lower()
                    logger.info(f"Google recognition: {text}")
                except (sr.UnknownValueError, sr.RequestError):
                    try:
                        text = r.recognize_sphinx(audio).lower()
                        logger.info(f"Sphinx recognition: {text}")
                    except:
                        text = "Could not understand audio"

                # Clean up temp file
                try:
                    os.remove(temp_filename)
                except:
                    pass

                return text
            else:
                return "Invalid audio format"

        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return f"Audio processing error: {e}"

    def record_voice_pyaudio(self):
        """Fallback PyAudio recording method"""
        if not self.audio_initialized:
            return "Audio system not initialized"

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "input.wav"

        try:
            stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                               input=True, frames_per_buffer=CHUNK)
            frames = []

            logger.info("Recording...")
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()

            # Save audio file
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Speech recognition
            r = sr.Recognizer()
            with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
                audio = r.record(source)

            try:
                return r.recognize_google(audio).lower()
            except (sr.UnknownValueError, sr.RequestError):
                try:
                    return r.recognize_sphinx(audio).lower()
                except:
                    return "Could not understand audio"

        except Exception as e:
            logger.error(f"PyAudio recording error: {e}")
            return f"Recording error: {e}"

    def music_theory_chat(self, voice_input):
        """Handle music theory chat mode"""
        if not self.transformer_initialized:
            return "Chatbot not available - check transformer installation"

        if voice_input.startswith("Error") or "could not understand" in voice_input.lower():
            return voice_input

        try:
            response = self.chatbot(voice_input)[0]['generated_text']
            self.save_chat(voice_input, response)
            return response
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Chat processing error: {e}"

    def daw_control(self, voice_input):
        """Handle DAW control commands"""
        if voice_input.startswith("Error") or "could not understand" in voice_input.lower():
            return voice_input

        if not self.midi_initialized:
            return "MIDI not available - check LoopMIDI configuration"

        try:
            # Transport controls
            if "play" in voice_input:
                self.midi_out.send(mido.Message('start'))
                self.session_state['transport']['playing'] = True
                self.save_state()
                return "Transport: Playing"

            elif "stop" in voice_input:
                self.midi_out.send(mido.Message('stop'))
                self.session_state['transport']['playing'] = False
                self.save_state()
                return "Transport: Stopped"

            elif "record" in voice_input:
                self.midi_out.send(mido.Message('control_change', control=95, value=127))
                self.session_state['transport']['recording'] = True
                self.save_state()
                return "Transport: Recording"

            # Track controls
            elif "solo track" in voice_input:
                try:
                    track_num = int(voice_input.split("track")[-1].strip()) - 1
                    if 0 <= track_num < 16:
                        # Clear all solos first
                        for i in range(16):
                            self.session_state['tracks'][i]['solo'] = False
                            self.midi_out.send(mido.Message('control_change', control=i + 32, value=0))

                        # Solo selected track
                        self.session_state['tracks'][track_num]['solo'] = True
                        self.midi_out.send(mido.Message('control_change', control=track_num + 32, value=127))
                        self.save_state()
                        return f"Soloed Track {track_num + 1}"
                    else:
                        return "Invalid track number (1-16)"
                except (ValueError, IndexError):
                    return "Invalid solo command format"

            elif "mute track" in voice_input:
                try:
                    track_num = int(voice_input.split("track")[-1].strip()) - 1
                    if 0 <= track_num < 16:
                        self.session_state['tracks'][track_num]['muted'] = True
                        self.midi_out.send(mido.Message('control_change', control=track_num + 16, value=127))
                        self.save_state()
                        return f"Muted Track {track_num + 1}"
                    else:
                        return "Invalid track number (1-16)"
                except (ValueError, IndexError):
                    return "Invalid mute command format"

            elif "unmute track" in voice_input:
                try:
                    track_num = int(voice_input.split("track")[-1].strip()) - 1
                    if 0 <= track_num < 16:
                        self.session_state['tracks'][track_num]['muted'] = False
                        self.midi_out.send(mido.Message('control_change', control=track_num + 16, value=0))
                        self.save_state()
                        return f"Unmuted Track {track_num + 1}"
                    else:
                        return "Invalid track number (1-16)"
                except (ValueError, IndexError):
                    return "Invalid unmute command format"

            elif "set fader" in voice_input or "fader" in voice_input:
                try:
                    parts = voice_input.split()
                    track_idx = None
                    value = None

                    # Parse track number
                    for i, part in enumerate(parts):
                        if part.isdigit():
                            if track_idx is None:
                                track_idx = int(part) - 1
                            else:
                                value = int(part) / 100

                    if track_idx is not None and value is not None and 0 <= track_idx < 16 and 0 <= value <= 1:
                        self.session_state['tracks'][track_idx]['fader'] = value
                        midi_value = int(value * 127)
                        self.midi_out.send(mido.Message('control_change', control=track_idx, value=midi_value))
                        self.save_state()
                        return f"Set Track {track_idx + 1} fader to {int(value * 100)}%"
                    else:
                        return "Invalid fader command format. Try 'set fader 1 to 75'"
                except (ValueError, IndexError):
                    return "Invalid fader command format"

            else:
                return f"Command not recognized: '{voice_input}'. Try: play, stop, record, solo track [1-16], mute track [1-16], set fader [1-16] to [0-100]"

        except Exception as e:
            logger.error(f"DAW control error: {e}")
            return f"DAW control error: {e}"

    def create_interface(self):
        """Create the Gradio interface"""
        with gr.Blocks(title="FaderPort 16 Emulator", theme=gr.themes.Soft()) as demo:
            gr.Markdown("# FaderPort 16 Emulator with AI Voice Control")
            gr.Markdown("### Two-mode voice controller: Music Theory Chat + DAW Control")

            with gr.Row():
                with gr.Column(scale=1):
                    mode = gr.Radio(
                        ["Music Theory Chat", "DAW Control"],
                        label="Control Mode",
                        value="DAW Control"
                    )

                    # Audio input with iOS compatibility
                    audio_input = gr.Audio(
                        label="Voice Input",
                        sources=["microphone"],
                        type="numpy",
                        format="wav"
                    )

                    voice_text = gr.Textbox(
                        label="Recognized Text",
                        placeholder="Your voice command will appear here...",
                        interactive=False
                    )

                    response = gr.Textbox(
                        label="Response",
                        placeholder="AI response will appear here...",
                        interactive=False,
                        lines=3
                    )

                with gr.Column(scale=2):
                    gr.Markdown("### Virtual FaderPort 16 Controls")

                    # Transport controls
                    with gr.Row():
                        transport_status = gr.Textbox(
                            label="Transport Status",
                            value="Stopped",
                            interactive=False
                        )

                    # Track controls in 4x4 grid
                    track_components = []
                    for row in range(4):
                        with gr.Row():
                            for col in range(4):
                                track_idx = row * 4 + col
                                with gr.Column():
                                    track_name = gr.Textbox(
                                        label=f"Track {track_idx + 1}",
                                        value=self.session_state['tracks'][track_idx]['name'],
                                        interactive=True
                                    )

                                    fader = gr.Slider(
                                        0, 1,
                                        value=self.session_state['tracks'][track_idx]['fader'],
                                        label="Volume",
                                        interactive=True
                                    )

                                    with gr.Row():
                                        mute_btn = gr.Checkbox(
                                            value=self.session_state['tracks'][track_idx]['muted'],
                                            label="Mute"
                                        )
                                        solo_btn = gr.Checkbox(
                                            value=self.session_state['tracks'][track_idx].get('solo', False),
                                            label="Solo"
                                        )

                                    track_components.append({
                                        'name': track_name,
                                        'fader': fader,
                                        'mute': mute_btn,
                                        'solo': solo_btn,
                                        'index': track_idx
                                    })

            # System status
            with gr.Row():
                system_status = gr.Textbox(
                    label="System Status",
                    value=f"Audio: {'✅' if self.audio_initialized else '❌'} | "
                          f"MIDI: {'✅' if self.midi_initialized else '❌'} | "
                          f"AI: {'✅' if self.transformer_initialized else '❌'}",
                    interactive=False
                )

            def process_voice_command(audio_data, mode_selection):
                """Process voice command based on mode"""
                if audio_data is None:
                    return "No audio received", "Please record some audio first"

                # Process audio to text
                voice_text = self.record_voice_gradio(audio_data)

                # Generate response based on mode
                if mode_selection == "Music Theory Chat":
                    response = self.music_theory_chat(voice_text)
                else:
                    response = self.daw_control(voice_text)

                return voice_text, response

            def update_fader(track_idx, value):
                """Update fader value"""
                if self.midi_initialized:
                    self.session_state['tracks'][track_idx]['fader'] = value
                    midi_value = int(value * 127)
                    try:
                        self.midi_out.send(mido.Message('control_change', control=track_idx, value=midi_value))
                        self.save_state()
                    except Exception as e:
                        logger.error(f"MIDI fader update failed: {e}")
                return value

            def update_mute(track_idx, muted):
                """Update mute status"""
                if self.midi_initialized:
                    self.session_state['tracks'][track_idx]['muted'] = muted
                    try:
                        self.midi_out.send(mido.Message('control_change', control=track_idx + 16, value=127 if muted else 0))
                        self.save_state()
                    except Exception as e:
                        logger.error(f"MIDI mute update failed: {e}")
                return muted

            def update_solo(track_idx, soloed):
                """Update solo status"""
                if self.midi_initialized:
                    self.session_state['tracks'][track_idx]['solo'] = soloed
                    try:
                        self.midi_out.send(mido.Message('control_change', control=track_idx + 32, value=127 if soloed else 0))
                        self.save_state()
                    except Exception as e:
                        logger.error(f"MIDI solo update failed: {e}")
                return soloed

            # Event handlers
            audio_input.change(
                process_voice_command,
                inputs=[audio_input, mode],
                outputs=[voice_text, response]
            )

            # Bind track control events
            for track_comp in track_components:
                track_comp['fader'].change(
                    lambda val, idx=track_comp['index']: update_fader(idx, val),
                    inputs=[track_comp['fader']],
                    outputs=[track_comp['fader']]
                )

                track_comp['mute'].change(
                    lambda val, idx=track_comp['index']: update_mute(idx, val),
                    inputs=[track_comp['mute']],
                    outputs=[track_comp['mute']]
                )

                track_comp['solo'].change(
                    lambda val, idx=track_comp['index']: update_solo(idx, val),
                    inputs=[track_comp['solo']],
                    outputs=[track_comp['solo']]
                )

            # Add help section
            with gr.Accordion("Voice Commands Help", open=False):
                gr.Markdown("""
                ### DAW Control Commands:
                - **Transport**: "play", "stop", "record"
                - **Track Control**: "solo track 1", "mute track 2", "unmute track 3"
                - **Fader Control**: "set fader 1 to 75", "fader 3 to 50"

                ### Music Theory Chat:
                - Switch to "Music Theory Chat" mode
                - Ask questions like: "What's a good chord progression for jazz?"
                - Discuss scales, harmony, composition, etc.

                ### Troubleshooting:
                - Ensure LoopMIDI is running with "LoopMIDI Port 1"
                - Check Windows microphone permissions
                - Verify Blue Cat PatchWork is loaded in Ableton
                """)

        return demo

    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.midi_out:
                self.midi_out.close()
            if self.p:
                self.p.terminate()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

# Initialize and run the application
if __name__ == "__main__":
    app = FaderPortEmulator()
    demo = app.create_interface()

    try:
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        app.cleanup()
