# 🚀 Streamlit Cloud Deployment Guide

## Deploy FaderPort 16 AI Controller to Streamlit Cloud

### Quick Deploy

1. **Fork/Push to GitHub**
   ```bash
   git push origin claude/faderport-ai-emulator-011CUPbVkyhXBvajCbJm95xm
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Click "New app"
   - Select your repository: `o5hinwave/AudioCommandController`
   - Branch: `claude/faderport-ai-emulator-011CUPbVkyhXBvajCbJm95xm`
   - Main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   ```
   https://[your-app-name].streamlit.app
   ```

### Features Included

✅ **16-Track DAW Controller**
- Virtual faders with real-time control
- Mute/Solo buttons
- Pan controls
- Voice command processing

✅ **Stem Separation**
- Upload audio files
- Separate vocals, drums, bass, other
- Individual stem volume control
- Export individual stems or ZIP

✅ **Music Theory Chat**
- AI-powered music theory assistant
- Ask questions about chords, scales, progressions
- Interactive learning

✅ **Phonic Mind**
- Chord detection
- Key & scale detection
- Tempo & beat analysis
- Instrument recognition

✅ **Transport Controls**
- Play/Pause/Stop/Record
- Real-time status display
- MIDI activity logging

✅ **Session Management**
- Export/Import sessions as JSON
- Save all track settings
- Persistent state

### File Structure

```
AudioCommandController/
├── streamlit_app.py              # Main Streamlit application
├── requirements-streamlit.txt    # Streamlit Cloud dependencies
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── README.md                    # Main documentation
└── STREAMLIT_DEPLOYMENT.md      # This file
```

### Requirements

The app uses minimal dependencies (from `requirements-streamlit.txt`):
```
streamlit>=1.28.0
numpy>=1.21.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

### Configuration

Theme settings in `.streamlit/config.toml`:
- Dark theme optimized for music production
- Custom colors matching DAW aesthetics
- Fast reruns enabled for smooth interaction

### Usage

#### Voice Commands
Type commands in the voice input box:
- `"solo track 3"` - Solo track 3
- `"mute track 5"` - Mute track 5
- `"set fader 1 to 75"` - Set track 1 to 75%
- `"play"` - Start transport
- `"stop"` - Stop transport
- `"record"` - Start recording

#### Stem Separation
1. Switch to "Stem Separation" mode
2. Upload audio file (WAV, MP3, OGG, FLAC)
3. Select separation model
4. Click "Separate Stems"
5. Download individual stems or ZIP

#### Music Theory
1. Switch to "Music Theory Chat" mode
2. Ask questions about:
   - Chord progressions
   - Scales and modes
   - Circle of fifths
   - Intervals
   - Modulation
   - Time signatures

#### Phonic Mind
1. Switch to "Phonic Mind" mode
2. Use tabs for different analysis:
   - **Chord Detection**: Analyze chord progressions
   - **Key Detection**: Find key and scale
   - **Tempo/Beat**: Detect BPM and time signature
   - **Instrument Recognition**: Identify instruments

### Demo Mode

The app runs in demo mode on Streamlit Cloud:
- ✅ All UI features functional
- ✅ Voice command processing
- ✅ Session save/load
- ⚠️ MIDI output simulated (no hardware required)
- ⚠️ Audio processing simulated (no actual stem separation)

### Local Testing

Test locally before deployment:
```bash
# Install dependencies
pip install -r requirements-streamlit.txt

# Run Streamlit
streamlit run streamlit_app.py
```

Access at: http://localhost:8501

### Troubleshooting

**Port Issues:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Clear Cache:**
```bash
streamlit cache clear
```

**Check Logs:**
View deployment logs in Streamlit Cloud dashboard

### Advanced Features

#### Custom Domain
1. Go to Settings in Streamlit Cloud
2. Add custom domain
3. Update DNS records

#### Secrets Management
Add secrets in Streamlit Cloud:
- Settings → Secrets
- Add environment variables

#### Analytics
- Built-in usage stats in Streamlit Cloud
- Monitor app performance
- Track user interactions

### Limitations on Free Tier

Streamlit Cloud Free:
- ✅ Unlimited public apps
- ✅ Community support
- ⚠️ Limited resources (1 GB RAM)
- ⚠️ Apps sleep after inactivity
- ⚠️ No custom domains (free tier)

### Upgrade Options

For production use:
- **Pro**: $20/month - More resources, custom domains
- **Enterprise**: Custom pricing - SSO, SLA, priority support

### Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: https://github.com/o5hinwave/AudioCommandController/issues

### Updates

To update the deployed app:
```bash
# Make changes to streamlit_app.py
git add streamlit_app.py
git commit -m "Update app features"
git push origin claude/faderport-ai-emulator-011CUPbVkyhXBvajCbJm95xm
```

Streamlit Cloud auto-deploys on push!

---

## 🎉 Ready to Deploy!

Your app is ready for Streamlit Cloud. Just push to GitHub and deploy!

**Live Demo URL:** `https://o5hinwave-audiocommandcontroller.streamlit.app`

---

**Built with ❤️ for @o5hinwave**
