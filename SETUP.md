# FaderPort 16 Emulator - Detailed Setup Guide

This guide provides step-by-step instructions for setting up the FaderPort 16 Emulator with all required hardware and software components.

## Table of Contents

- [System Requirements](#system-requirements)
- [Software Installation](#software-installation)
- [LoopMIDI Configuration](#loopmidi-configuration)
- [FaderPort 16 Hardware Setup](#faderport-16-hardware-setup)
- [DAW Configuration](#daw-configuration)
- [Network and Firewall Setup](#network-and-firewall-setup)
- [Microphone Permissions](#microphone-permissions)
- [Testing and Verification](#testing-and-verification)
- [Advanced Configuration](#advanced-configuration)

## System Requirements

### Minimum Requirements
- **OS**: Windows 11, macOS 10.15+, or Linux
- **CPU**: Intel i5 / AMD Ryzen 5 or better
- **RAM**: 8GB (16GB recommended for AI models)
- **Python**: 3.10 or higher
- **Storage**: 5GB free space for dependencies and models
- **Internet**: Required for initial setup and Google Speech API

### Recommended Setup
- **OS**: Windows 11 Pro
- **CPU**: Intel i7 / AMD Ryzen 7 or better
- **RAM**: 16GB+
- **SSD**: For faster model loading
- **Network**: Gigabit Ethernet or 5GHz WiFi for iPad access

## Software Installation

### 1. Python Installation

**Windows:**
1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```bash
python --version
pip --version
```

**macOS:**
```bash
brew install python@3.10
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

### 2. Visual Studio Build Tools (Windows Only)

Required for PyAudio compilation:

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Run installer
3. Select "Desktop development with C++"
4. Install (requires ~7GB)

Alternative: Use pipwin (easier method):
```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/AudioCommandController.git
cd AudioCommandController

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Windows PyAudio installation (if not using pipwin)
pip install pipwin
pipwin install pyaudio
```

## LoopMIDI Configuration

LoopMIDI creates virtual MIDI ports for routing between the application and your DAW.

### Installation (Windows)

1. Download LoopMIDI from [Tobias Erichsen](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Run installer (loopMIDISetup_xxx.exe)
3. Launch LoopMIDI
4. Create a new virtual port:
   - Click the "+" button
   - Name: `LoopMIDI Port 1`
   - Click "OK"
5. Verify port appears in the list
6. Optional: Enable "Start minimized" in Settings

### Alternative: Virtual MIDI Ports (macOS)

macOS has built-in IAC Driver:

1. Open "Audio MIDI Setup" (/Applications/Utilities/)
2. Window → Show MIDI Studio
3. Double-click "IAC Driver"
4. Check "Device is online"
5. Click "+" to add a port
6. Name it "IAC Driver Bus 1"

### Alternative: ALSA MIDI (Linux)

```bash
# Install required packages
sudo apt-get install vmpk
# Or use a2jmidid for ALSA-to-JACK MIDI bridge
sudo apt-get install a2jmidid

# Create virtual MIDI port
sudo modprobe snd-virmidi
```

## FaderPort 16 Hardware Setup

### Switching to HUI Mode

The FaderPort 16 must be in HUI (Human User Interface) mode to work with most DAWs.

**Steps:**

1. **Power Off** the FaderPort 16
2. **Hold SELECT buttons 1 & 2** simultaneously
3. While holding, **power on** the unit
4. Display shows mode selection menu
5. Use **SELECT buttons** to navigate to "HUI" mode
6. Press **SELECT under "EXIT"** to confirm
7. Unit will **restart** in HUI mode
8. LED indicators will show HUI mode active

**Mode Indicators:**
- Native Mode: Standard operation
- HUI Mode: Mackie HUI emulation (recommended)
- MCU Mode: Mackie Control Universal emulation

**Reverting to Native Mode:**
Repeat the process above and select "Native" instead of "HUI".

### USB Connection

1. Connect FaderPort 16 to PC via USB cable
2. Windows will auto-install drivers
3. Verify in Device Manager:
   - Sound, video and game controllers → "FaderPort 16"
   - Universal Serial Bus controllers → "USB Composite Device"

## DAW Configuration

### Ableton Live Setup

1. **Open Preferences** (Ctrl+, / Cmd+,)
2. Navigate to **Link/Tempo/MIDI**
3. In **Control Surface** section:
   - Control Surface: **Mackie Control**
   - Input: **LoopMIDI Port 1**
   - Output: **LoopMIDI Port 1**
4. In **MIDI Ports** section:
   - Enable **Track** for LoopMIDI Port 1
   - Enable **Remote** for LoopMIDI Port 1
5. Click **OK** to save

### Blue Cat PatchWork Integration

For multi-channel MIDI routing in Ableton:

1. Add **Blue Cat PatchWork** to a MIDI track
2. Right-click → **Configure**
3. **MIDI Input**: LoopMIDI Port 1
4. Enable **MIDI Thru**
5. Add instruments to each slot (1-16 for 16 tracks)
6. Configure each slot's MIDI channel (1-16)

### Logic Pro X Setup

1. **Open Preferences** → **Control Surfaces** → **Setup**
2. Click **New** → **Install**
3. Select **Mackie Designs** → **Mackie Control**
4. Click **Add**
5. Set **MIDI Input**: LoopMIDI Port 1 (or IAC Driver)
6. Set **MIDI Output**: LoopMIDI Port 1 (or IAC Driver)
7. Click **Done**

### Pro Tools Setup

1. **Setup** → **Peripherals** → **MIDI Controllers**
2. Click **Add**
3. **Type**: HUI
4. **Receive From**: LoopMIDI Port 1
5. **Send To**: LoopMIDI Port 1
6. Click **OK**

### Reaper Setup

1. **Options** → **Preferences** → **Control/OSC/web**
2. Click **Add**
3. **Mode**: Mackie Control
4. **MIDI Input**: LoopMIDI Port 1
5. **MIDI Output**: LoopMIDI Port 1
6. Click **OK**

## Network and Firewall Setup

### Windows Firewall Configuration

To allow iPad/mobile access:

**Method 1: Windows Defender Firewall GUI**

1. Open **Windows Security**
2. Click **Firewall & network protection**
3. Click **Advanced settings**
4. Click **Inbound Rules** → **New Rule**
5. **Rule Type**: Port → Next
6. **Protocol**: TCP
7. **Specific local ports**: `7860` → Next
8. **Action**: Allow the connection → Next
9. **Profile**: Check all (Domain, Private, Public) → Next
10. **Name**: "FaderPort AI Controller" → Finish

**Method 2: PowerShell (Administrator)**

```powershell
New-NetFirewallRule -DisplayName "FaderPort AI Controller" -Direction Inbound -Protocol TCP -LocalPort 7860 -Action Allow
```

**Method 3: Command Prompt (Administrator)**

```cmd
netsh advfirewall firewall add rule name="FaderPort AI Controller" dir=in action=allow protocol=TCP localport=7860
```

### Verify Firewall Rule

```powershell
Get-NetFirewallRule -DisplayName "FaderPort AI Controller"
```

### Finding Your IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your active network adapter.

**macOS/Linux:**
```bash
ifconfig
# or
ip addr show
```

### Router Configuration (Optional)

For external network access:

1. Log into your router admin panel
2. Find **Port Forwarding** settings
3. Add new rule:
   - Service Name: FaderPort
   - External Port: 7860
   - Internal Port: 7860
   - Internal IP: [Your PC's IP address]
   - Protocol: TCP

## Microphone Permissions

### Windows 11

1. Open **Settings** (Win + I)
2. Navigate to **Privacy & Security** → **Microphone**
3. Enable **Microphone access**
4. Enable **Let apps access your microphone**
5. Enable **Let desktop apps access your microphone**
6. Scroll down and ensure your browser is enabled

### macOS

1. Open **System Preferences** → **Security & Privacy**
2. Click **Privacy** tab
3. Select **Microphone** from left sidebar
4. Check the box next to your browser
5. May require restarting the browser

### Linux

```bash
# Check microphone access
arecord -l

# Test recording
arecord -d 5 test.wav
aplay test.wav
```

### Browser Permissions

When first accessing the Gradio interface:

1. Browser will prompt for microphone permission
2. Click **Allow**
3. If blocked, click the lock icon in address bar
4. Change microphone permission to **Allow**
5. Refresh the page

## Testing and Verification

### 1. Test Python Installation

```bash
python --version
# Should show Python 3.10 or higher
```

### 2. Test Dependencies

```bash
python -c "import gradio; print(gradio.__version__)"
python -c "import mido; print(mido.version_info)"
python -c "import speech_recognition; print('Speech Recognition OK')"
```

### 3. Test MIDI Ports

```bash
python -c "import mido; print(mido.get_output_names())"
# Should show LoopMIDI Port 1 in the list
```

### 4. Test Microphone

```bash
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('Mic OK')"
```

### 5. Run Application

```bash
python app.py
```

Expected output:
```
INFO:__main__:PyAudio initialized successfully
INFO:__main__:MIDI port 'LoopMIDI Port 1' connected successfully
INFO:__main__:Transformer model 'facebook/blenderbot-400M-distill' loaded successfully
Running on local URL:  http://0.0.0.0:7860
```

### 6. Test Web Interface

**From PC:**
1. Open browser: http://localhost:7860
2. Should see FaderPort interface

**From iPad (same WiFi):**
1. Find PC IP address (e.g., 192.168.1.100)
2. Open browser: http://192.168.1.100:7860
3. Should see FaderPort interface

### 7. Test Voice Recognition

1. Click microphone icon
2. Say "play"
3. Check "Recognized Text" field shows "play"
4. Check "Response" field shows "Transport: Playing"
5. Verify MIDI message sent to DAW

### 8. Test MIDI Communication

In your DAW:
1. Create a MIDI track
2. Set input to LoopMIDI Port 1
3. Enable monitoring
4. Move a fader in the web interface
5. Should see MIDI activity in DAW

## Advanced Configuration

### Custom MIDI Port Names

Edit `.env`:
```
MIDI_PORT_NAME=My Custom MIDI Port
```

Or modify `app.py`:
```python
port_names = ['My Custom Port', 'LoopMIDI Port 1', 'Another Port']
```

### Audio Configuration

Edit `.env`:
```
AUDIO_SAMPLE_RATE=48000
AUDIO_BUFFER_SIZE=256
RECORD_DURATION=10
```

### Network Configuration

Edit `.env`:
```
SERVER_PORT=8080
SERVER_HOST=127.0.0.1  # Local only
# or
SERVER_HOST=0.0.0.0    # Network accessible
```

### SSL/HTTPS Setup (Advanced)

For secure connections:

```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    ssl_keyfile="path/to/key.pem",
    ssl_certfile="path/to/cert.pem"
)
```

### Multi-Client Support

Gradio supports multiple simultaneous connections by default. Each client gets their own session.

### Custom AI Models

Edit `app.py` to use different models:

```python
models = [
    "facebook/blenderbot-1B-distill",  # Larger, better quality
    "microsoft/DialoGPT-large",        # Larger DialoGPT
    "your-custom-model"                # Your fine-tuned model
]
```

### Offline Mode

For completely offline operation:

1. Download models beforehand:
```python
from transformers import pipeline
pipeline("conversational", model="facebook/blenderbot-400M-distill")
```

2. Use PocketSphinx exclusively:
```python
# Remove Google recognition, use only Sphinx
text = r.recognize_sphinx(audio).lower()
```

3. Disable internet requirement in code

### Performance Tuning

**Low-Memory Systems:**
```python
# Use smaller model
models = ["microsoft/DialoGPT-small"]

# Reduce Gradio queue size
demo.queue(concurrency_count=1)
```

**High-Performance Systems:**
```python
# Use larger models
models = ["facebook/blenderbot-1B-distill"]

# Increase concurrency
demo.queue(concurrency_count=4)

# Use GPU acceleration
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
self.chatbot = pipeline("conversational", model=model, device=device)
```

## Troubleshooting

### Port Already in Use

```bash
# Windows: Find process using port 7860
netstat -ano | findstr :7860
taskkill /PID [PID] /F

# macOS/Linux
lsof -ti:7860 | xargs kill -9
```

### MIDI Port Not Found

1. Verify LoopMIDI is running
2. Check port name exactly matches
3. Restart LoopMIDI
4. Restart application

### Model Download Fails

```bash
# Set Hugging Face cache directory
export HF_HOME=/path/to/cache

# Pre-download models
python -c "from transformers import pipeline; pipeline('conversational', model='facebook/blenderbot-400M-distill')"
```

### Microphone Not Working

1. Test in Windows Sound Settings
2. Check browser permissions
3. Try different browser (Chrome recommended)
4. Check privacy settings
5. Restart browser

### iPad Can't Connect

1. Verify same WiFi network
2. Check firewall rule
3. Ping PC from iPad
4. Use IP address not hostname
5. Clear browser cache
6. Try different browser

### Audio Processing Errors

```bash
# Reinstall PyAudio
pip uninstall pyaudio
pip install pipwin
pipwin install pyaudio

# Or build from source
pip install --upgrade pyaudio
```

## Support Resources

- **Project GitHub**: [Issues](https://github.com/yourusername/AudioCommandController/issues)
- **LoopMIDI**: https://www.tobias-erichsen.de/software/loopmidi.html
- **Gradio Docs**: https://www.gradio.app/docs
- **Mido Docs**: https://mido.readthedocs.io
- **Speech Recognition**: https://github.com/Uberi/speech_recognition

## Next Steps

After completing setup:

1. Test all voice commands
2. Configure your DAW project
3. Customize fader mappings
4. Explore music theory chat mode
5. Create custom voice commands
6. Set up automatic startup

---

**Setup Complete!** You're ready to control your DAW with voice commands.
