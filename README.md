# FaderPort 16 Emulator with AI Voice Control

An intelligent voice-controlled DAW controller that emulates the PreSonus FaderPort 16, combining AI-powered speech recognition with MIDI control for seamless music production workflows.

## Features

- **Dual Mode Operation**
  - Music Theory Chat Mode - AI-powered music theory discussion and assistance
  - DAW Control Mode - Voice commands for transport, tracks, and faders

- **Voice Control**
  - Natural language processing for intuitive commands
  - Google Speech Recognition with PocketSphinx offline fallback
  - iOS-compatible audio recording via Gradio interface

- **16-Track MIDI Control**
  - Virtual faders with real-time MIDI output
  - Individual track mute/solo controls
  - Transport controls (play, stop, record)
  - Session state persistence

- **Cross-Platform Interface**
  - Web-based Gradio UI accessible from PC and iPad
  - Real-time visual feedback for all controls
  - Responsive design for mobile devices

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Windows 11 (for LoopMIDI support)
- DAW software (Ableton Live, Logic Pro, etc.)
- Microphone access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AudioCommandController.git
cd AudioCommandController
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt

# Windows-specific PyAudio installation
pip install pipwin
pipwin install pyaudio
```

4. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your preferences
```

### Running the Application

```bash
python app.py
```

Access the interface at:
- Local: http://localhost:7860
- Network: http://[your-ip]:7860 (for iPad/mobile access)

## Voice Commands

### DAW Control Mode

**Transport Controls:**
- "play" - Start playback
- "stop" - Stop playback
- "record" - Enable recording

**Track Controls:**
- "solo track 3" - Solo track 3, unsolo all others
- "mute track 5" - Mute track 5
- "unmute track 2" - Unmute track 2

**Fader Controls:**
- "set fader 1 to 75" - Set track 1 volume to 75%
- "fader 3 to 50" - Set track 3 volume to 50%

### Music Theory Chat Mode

Switch to "Music Theory Chat" mode and ask questions like:
- "What's a good chord progression for jazz?"
- "Explain the circle of fifths"
- "How do I modulate from C major to A minor?"
- "What scales work over a G7 chord?"

## Hardware Setup

See [SETUP.md](SETUP.md) for detailed hardware configuration instructions including:
- LoopMIDI virtual MIDI port setup
- FaderPort 16 HUI mode configuration
- DAW MIDI routing (Ableton Live, Logic Pro, etc.)
- Windows Firewall and network access
- Microphone permissions

## System Architecture

```
┌─────────────────┐
│  Voice Input    │
│  (Microphone)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Speech Recognition│
│ Google API/Sphinx │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│   NLP Engine    │───────│  Music Theory   │
│  (Transformers) │       │   Chatbot       │
└────────┬────────┘       └─────────────────┘
         │
         ▼
┌─────────────────┐
│  DAW Commands   │
│    Parser       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│  MIDI Output    │───────│   LoopMIDI      │
│     (Mido)      │       │  Virtual Port   │
└─────────────────┘       └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │   DAW Software  │
                          │ (Ableton/Logic) │
                          └─────────────────┘
```

## Configuration

### MIDI Settings

By default, the application tries to connect to these MIDI ports:
1. "LoopMIDI Port 1"
2. "LoopMIDI Port"
3. "loopMIDI Port 1"

Configure your preferred port in `.env`:
```
MIDI_PORT_NAME=LoopMIDI Port 1
```

### Audio Settings

Default audio configuration:
```
AUDIO_SAMPLE_RATE=44100
AUDIO_BUFFER_SIZE=512
RECORD_DURATION=5
```

### Network Settings

For iPad/mobile access:
```
SERVER_PORT=7860
SERVER_HOST=0.0.0.0
```

## Troubleshooting

### MIDI Not Working
- Verify LoopMIDI is running and port name matches
- Check DAW MIDI preferences
- Restart the application and DAW

### Audio Recording Silent
- Check Windows microphone permissions (Settings → Privacy → Microphone)
- Test microphone in Windows Sound settings
- Try different browsers (Chrome recommended for best compatibility)
- Ensure PocketSphinx is installed for offline recognition

### iPad Can't Connect
- Verify devices are on the same WiFi network
- Check Windows Firewall allows port 7860
- Use direct IP address instead of hostname
- Clear browser cache

### AI Chat Not Responding
- Check internet connection (required for Google Speech API)
- Verify Hugging Face model download completed
- Try smaller transformer models for low-memory systems
- Check transformers library compatibility

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## Project Structure

```
AudioCommandController/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── SETUP.md              # Detailed hardware setup
├── faderport_data.json   # Session state (auto-generated)
└── chat_history.json     # Chat logs (auto-generated)
```

## Dependencies

- **gradio** - Web UI framework
- **transformers** - AI models for chatbot
- **torch** - PyTorch for ML models
- **speechrecognition** - Voice recognition
- **pyaudio** - Audio I/O
- **mido** - MIDI communication
- **python-rtmidi** - MIDI backend
- **pandas** - Data management
- **python-dotenv** - Environment configuration
- **pocketsphinx** - Offline speech recognition
- **numpy** - Numerical operations

## Advanced Features

### Session Persistence

All track settings, fader positions, and mute/solo states are automatically saved to `faderport_data.json` and restored on application restart.

### Chat History

Music theory conversations are logged to `chat_history.json` for review and learning.

### Multiple AI Models

The application tries multiple transformer models in order of preference:
1. facebook/blenderbot-400M-distill
2. microsoft/DialoGPT-medium
3. microsoft/DialoGPT-small

### iOS Compatibility

Enhanced Gradio audio settings ensure compatibility with iOS Safari and Chrome browsers for iPad control.

## Performance Tips

- Close unused browser tabs to free memory for AI models
- Use smaller transformer models on systems with limited RAM
- Disable chat history logging for faster performance
- Reduce audio buffer size for lower latency

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- PreSonus for FaderPort 16 hardware inspiration
- Gradio team for the excellent web UI framework
- Hugging Face for transformer models
- Speech Recognition library contributors

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check [SETUP.md](SETUP.md) for detailed configuration help
- Review troubleshooting section above

## Version History

### v1.0.0 (Current)
- Initial release
- Dual-mode voice control (Chat + DAW)
- 16-track MIDI control
- iOS-compatible web interface
- Session persistence
- Multi-model AI fallbacks

---

**Happy Music Making!**
