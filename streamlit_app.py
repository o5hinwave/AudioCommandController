import streamlit as st
import numpy as np
import pandas as pd
import json
from datetime import datetime
import io

# Configure page
st.set_page_config(
    page_title="FaderPort 16 AI Controller",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'tracks' not in st.session_state:
    st.session_state.tracks = [
        {'name': f'Track {i+1}', 'fader': 0.5, 'muted': False, 'solo': False, 'pan': 0.5}
        for i in range(16)
    ]

if 'transport' not in st.session_state:
    st.session_state.transport = {'playing': False, 'recording': False, 'loop': False}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'midi_log' not in st.session_state:
    st.session_state.midi_log = []

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .transport-btn {
        background-color: #4CAF50;
    }
    .track-container {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .midi-log {
        background-color: #0d1117;
        color: #58a6ff;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        max-height: 200px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def log_midi(message):
    """Log MIDI messages"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    st.session_state.midi_log.append(f"[{timestamp}] {message}")
    if len(st.session_state.midi_log) > 50:
        st.session_state.midi_log.pop(0)

def save_session():
    """Save session to JSON"""
    session_data = {
        'tracks': st.session_state.tracks,
        'transport': st.session_state.transport,
        'timestamp': datetime.now().isoformat()
    }
    return json.dumps(session_data, indent=2)

def load_session(json_data):
    """Load session from JSON"""
    try:
        data = json.loads(json_data)
        st.session_state.tracks = data.get('tracks', st.session_state.tracks)
        st.session_state.transport = data.get('transport', st.session_state.transport)
        st.success("Session loaded successfully!")
    except Exception as e:
        st.error(f"Error loading session: {e}")

# Main App Layout
st.title("🎛️ FaderPort 16 AI Controller")
st.markdown("**Professional DAW Control with AI Voice Commands & Stem Separation**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Control Panel")

    mode = st.radio(
        "🎵 Mode",
        ["DAW Control", "Music Theory Chat", "Stem Separation", "Phonic Mind"],
        help="Select control mode"
    )

    st.divider()

    # Transport Controls
    st.subheader("🎮 Transport")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶️" if not st.session_state.transport['playing'] else "⏸️", key="play_btn"):
            st.session_state.transport['playing'] = not st.session_state.transport['playing']
            status = "Playing" if st.session_state.transport['playing'] else "Paused"
            log_midi(f"Transport: {status}")
            st.rerun()

    with col2:
        if st.button("⏹️", key="stop_btn"):
            st.session_state.transport['playing'] = False
            st.session_state.transport['recording'] = False
            log_midi("Transport: Stopped")
            st.rerun()

    with col3:
        if st.button("⏺️" if not st.session_state.transport['recording'] else "⏹️", key="rec_btn"):
            st.session_state.transport['recording'] = not st.session_state.transport['recording']
            status = "Recording" if st.session_state.transport['recording'] else "Stopped"
            log_midi(f"Transport: {status}")
            st.rerun()

    # Transport status
    if st.session_state.transport['playing']:
        st.success("▶️ Playing")
    if st.session_state.transport['recording']:
        st.error("⏺️ Recording")

    st.divider()

    # Session Management
    st.subheader("💾 Session")

    if st.button("📥 Export Session"):
        session_json = save_session()
        st.download_button(
            label="Download JSON",
            data=session_json,
            file_name=f"faderport_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    uploaded_file = st.file_uploader("📤 Import Session", type=['json'])
    if uploaded_file:
        load_session(uploaded_file.read().decode())

    st.divider()

    # System Status
    st.subheader("🔧 System Status")
    st.info("✅ Streamlit Cloud Ready")
    st.success("✅ Demo Mode Active")
    st.warning("⚠️ MIDI: Simulated")

# Main Content Area
if mode == "DAW Control":
    st.header("🎚️ 16-Track Mixer")

    # Voice Command Input
    with st.expander("🎤 Voice Commands", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            voice_input = st.text_input(
                "Enter voice command or use speech input",
                placeholder="e.g., 'solo track 3', 'mute track 5', 'set fader 1 to 75'",
                key="voice_input"
            )
        with col2:
            if st.button("🎤 Process", key="process_voice"):
                if voice_input:
                    # Process voice commands
                    cmd = voice_input.lower()

                    if "solo track" in cmd:
                        try:
                            track_num = int(''.join(filter(str.isdigit, cmd))) - 1
                            if 0 <= track_num < 16:
                                # Clear all solos
                                for track in st.session_state.tracks:
                                    track['solo'] = False
                                st.session_state.tracks[track_num]['solo'] = True
                                log_midi(f"CC{track_num+32}: 127 (Solo Track {track_num+1})")
                                st.success(f"✅ Soloed Track {track_num+1}")
                                st.rerun()
                        except:
                            st.error("Invalid track number")

                    elif "mute track" in cmd:
                        try:
                            track_num = int(''.join(filter(str.isdigit, cmd))) - 1
                            if 0 <= track_num < 16:
                                st.session_state.tracks[track_num]['muted'] = True
                                log_midi(f"CC{track_num+16}: 127 (Mute Track {track_num+1})")
                                st.success(f"✅ Muted Track {track_num+1}")
                                st.rerun()
                        except:
                            st.error("Invalid track number")

                    elif "unmute track" in cmd:
                        try:
                            track_num = int(''.join(filter(str.isdigit, cmd))) - 1
                            if 0 <= track_num < 16:
                                st.session_state.tracks[track_num]['muted'] = False
                                log_midi(f"CC{track_num+16}: 0 (Unmute Track {track_num+1})")
                                st.success(f"✅ Unmuted Track {track_num+1}")
                                st.rerun()
                        except:
                            st.error("Invalid track number")

                    elif "set fader" in cmd or "fader" in cmd:
                        try:
                            nums = [int(s) for s in cmd.split() if s.isdigit()]
                            if len(nums) >= 2:
                                track_num = nums[0] - 1
                                value = nums[1] / 100
                                if 0 <= track_num < 16 and 0 <= value <= 1:
                                    st.session_state.tracks[track_num]['fader'] = value
                                    midi_val = int(value * 127)
                                    log_midi(f"CC{track_num}: {midi_val} (Fader {track_num+1})")
                                    st.success(f"✅ Set Track {track_num+1} fader to {int(value*100)}%")
                                    st.rerun()
                        except:
                            st.error("Invalid fader command")

                    elif "play" in cmd:
                        st.session_state.transport['playing'] = True
                        log_midi("Transport: Play")
                        st.success("✅ Playing")
                        st.rerun()

                    elif "stop" in cmd:
                        st.session_state.transport['playing'] = False
                        st.session_state.transport['recording'] = False
                        log_midi("Transport: Stop")
                        st.success("✅ Stopped")
                        st.rerun()

                    elif "record" in cmd:
                        st.session_state.transport['recording'] = True
                        log_midi("Transport: Record")
                        st.success("✅ Recording")
                        st.rerun()

                    else:
                        st.warning("Command not recognized. Try: 'solo track 3', 'mute track 5', 'set fader 1 to 75'")

        # Command help
        with st.expander("💡 Command Examples"):
            st.markdown("""
            **Transport:**
            - "play" - Start playback
            - "stop" - Stop playback
            - "record" - Start recording

            **Track Control:**
            - "solo track 3" - Solo track 3
            - "mute track 5" - Mute track 5
            - "unmute track 2" - Unmute track 2

            **Fader Control:**
            - "set fader 1 to 75" - Set track 1 to 75%
            - "fader 3 to 50" - Set track 3 to 50%
            """)

    st.divider()

    # Track Controls (4x4 grid)
    for row in range(4):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            track_idx = row * 4 + col_idx
            track = st.session_state.tracks[track_idx]

            with col:
                st.markdown(f"### 🎚️ {track['name']}")

                # Fader
                new_fader = st.slider(
                    "Volume",
                    0.0, 1.0,
                    track['fader'],
                    0.01,
                    key=f"fader_{track_idx}",
                    label_visibility="collapsed"
                )

                if new_fader != track['fader']:
                    track['fader'] = new_fader
                    midi_val = int(new_fader * 127)
                    log_midi(f"CC{track_idx}: {midi_val}")

                st.caption(f"🔊 {int(track['fader']*100)}%")

                # Pan
                new_pan = st.slider(
                    "Pan",
                    0.0, 1.0,
                    track['pan'],
                    0.01,
                    key=f"pan_{track_idx}",
                    label_visibility="collapsed"
                )

                if new_pan != track['pan']:
                    track['pan'] = new_pan
                    log_midi(f"Pan{track_idx}: {int(new_pan*127)}")

                pan_text = "L" if new_pan < 0.45 else "R" if new_pan > 0.55 else "C"
                st.caption(f"↔️ {pan_text}")

                # Mute/Solo buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "M" if not track['muted'] else "🔇",
                        key=f"mute_{track_idx}",
                        type="primary" if track['muted'] else "secondary",
                        use_container_width=True
                    ):
                        track['muted'] = not track['muted']
                        log_midi(f"CC{track_idx+16}: {127 if track['muted'] else 0}")
                        st.rerun()

                with col2:
                    if st.button(
                        "S" if not track['solo'] else "🎯",
                        key=f"solo_{track_idx}",
                        type="primary" if track['solo'] else "secondary",
                        use_container_width=True
                    ):
                        track['solo'] = not track['solo']
                        log_midi(f"CC{track_idx+32}: {127 if track['solo'] else 0}")
                        st.rerun()

elif mode == "Music Theory Chat":
    st.header("🎼 Music Theory Assistant")

    # Chat interface
    st.markdown("### Ask me anything about music theory!")

    user_input = st.text_input(
        "Your question:",
        placeholder="e.g., What's a good chord progression for jazz?",
        key="theory_input"
    )

    if st.button("💬 Ask", key="ask_theory"):
        if user_input:
            st.session_state.chat_history.append({
                'user': user_input,
                'bot': None,
                'timestamp': datetime.now()
            })

            # Simple music theory responses
            response = get_music_theory_response(user_input.lower())

            st.session_state.chat_history[-1]['bot'] = response
            st.rerun()

    # Display chat history
    st.divider()
    for chat in reversed(st.session_state.chat_history[-10:]):
        with st.container():
            st.markdown(f"**You:** {chat['user']}")
            st.info(f"**Assistant:** {chat['bot']}")
            st.caption(chat['timestamp'].strftime("%H:%M:%S"))
            st.divider()

elif mode == "Stem Separation":
    st.header("🎵 Stem Separation")

    st.info("🎸 **Separate audio into individual stems** - Vocals, Drums, Bass, Other")

    # File upload
    uploaded_audio = st.file_uploader(
        "Upload audio file",
        type=['wav', 'mp3', 'ogg', 'flac'],
        help="Upload an audio file to separate into stems"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        model_type = st.selectbox(
            "Separation Model",
            ["2stems (Vocals/Accompaniment)", "4stems (Vocals/Drums/Bass/Other)", "5stems (with Piano)"],
            help="Choose separation quality"
        )

    with col2:
        quality = st.select_slider(
            "Quality",
            options=["Fast", "Balanced", "High Quality"],
            value="Balanced"
        )

    if uploaded_audio:
        st.success(f"✅ File uploaded: {uploaded_audio.name}")

        with st.expander("⚙️ Advanced Settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                sample_rate = st.select_slider("Sample Rate", options=[22050, 44100, 48000], value=44100)
                normalize = st.checkbox("Normalize output", value=True)
            with col2:
                fade_in = st.slider("Fade in (ms)", 0, 1000, 50)
                fade_out = st.slider("Fade out (ms)", 0, 1000, 50)

        if st.button("🚀 Separate Stems", type="primary", use_container_width=True):
            with st.spinner("🎵 Separating stems... This may take a few minutes..."):
                # Simulate stem separation process
                progress_bar = st.progress(0)
                status_text = st.empty()

                steps = [
                    ("Loading audio file...", 20),
                    ("Analyzing frequency spectrum...", 40),
                    ("Extracting vocals...", 60),
                    ("Extracting instruments...", 80),
                    ("Finalizing stems...", 100)
                ]

                for step, progress in steps:
                    status_text.text(step)
                    progress_bar.progress(progress)
                    import time
                    time.sleep(0.5)

                st.success("✅ Stem separation complete!")

                # Display results
                st.markdown("### 🎧 Separated Stems")

                stems = ["Vocals", "Drums", "Bass", "Other"]
                cols = st.columns(4)

                for idx, (stem_name, col) in enumerate(zip(stems, cols)):
                    with col:
                        st.markdown(f"#### {stem_name}")
                        st.markdown("🎵 Audio Player")
                        st.caption("(Demo mode - no actual audio)")

                        # Volume control for each stem
                        vol = st.slider(
                            "Volume",
                            0, 100, 100,
                            key=f"stem_vol_{idx}",
                            label_visibility="collapsed"
                        )

                        if st.button(f"💾 Export {stem_name}", key=f"export_{idx}"):
                            st.success(f"✅ {stem_name} exported!")

                st.divider()

                # Batch export
                if st.button("📦 Export All Stems (ZIP)", use_container_width=True):
                    st.success("✅ All stems exported as ZIP file!")

elif mode == "Phonic Mind":
    st.header("🧠 Phonic Mind - AI Audio Analysis")

    st.markdown("### 🎯 Intelligent Audio Processing & Learning")

    tab1, tab2, tab3, tab4 = st.tabs(["🎼 Chord Detection", "🎵 Key Detection", "🥁 Tempo/Beat", "🎸 Instrument Recognition"])

    with tab1:
        st.subheader("Chord Progression Analyzer")

        uploaded_audio = st.file_uploader("Upload audio", type=['wav', 'mp3'], key="chord_upload")

        if uploaded_audio or st.button("🎹 Analyze Demo Track"):
            with st.spinner("Analyzing chords..."):
                # Simulated chord detection
                chords = [
                    ("C Major", "0:00", 0.95),
                    ("G Major", "0:02", 0.92),
                    ("A Minor", "0:04", 0.88),
                    ("F Major", "0:06", 0.91),
                    ("C Major", "0:08", 0.94),
                    ("G Major", "0:10", 0.89),
                    ("F Major", "0:12", 0.87),
                    ("G Major", "0:14", 0.93)
                ]

                st.success("✅ Chord analysis complete!")

                # Display chord progression
                st.markdown("#### Detected Chord Progression:")

                cols = st.columns(4)
                for idx, (chord, time, confidence) in enumerate(chords):
                    with cols[idx % 4]:
                        st.metric(
                            label=f"{time}",
                            value=chord,
                            delta=f"{confidence*100:.0f}% confidence"
                        )

                st.divider()

                # Chord sequence
                st.markdown("#### Simplified Progression:")
                st.code("C - G - Am - F  (I - V - vi - IV)", language="text")

                st.info("💡 This is a common pop progression (I-V-vi-IV)")

    with tab2:
        st.subheader("Key & Scale Detector")

        if st.button("🔍 Detect Key", use_container_width=True):
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Detected Key", "C Major", delta="98% confidence")
                st.metric("Secondary Key", "A Minor", delta="87% confidence")

            with col2:
                st.metric("Scale Type", "Major Scale")
                st.metric("Mode", "Ionian")

            st.divider()

            st.markdown("#### Scale Notes:")
            notes = ["C", "D", "E", "F", "G", "A", "B"]
            cols = st.columns(7)
            for note, col in zip(notes, cols):
                with col:
                    st.button(note, use_container_width=True)

            st.markdown("#### Recommended Chords:")
            st.info("**Diatonic chords:** C, Dm, Em, F, G, Am, Bdim")

    with tab3:
        st.subheader("Tempo & Beat Detection")

        if st.button("⏱️ Detect Tempo", use_container_width=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("BPM", "120", delta="Allegro")

            with col2:
                st.metric("Time Signature", "4/4", delta="Common time")

            with col3:
                st.metric("Rhythm Style", "Straight", delta="Rock/Pop")

            st.divider()

            # Beat visualization
            st.markdown("#### Beat Grid:")
            beats = st.columns(16)
            for i, beat in enumerate(beats):
                with beat:
                    if i % 4 == 0:
                        st.button("▼", key=f"beat_{i}", use_container_width=True)
                    else:
                        st.button("•", key=f"beat_{i}", use_container_width=True)

            st.caption("▼ = Downbeat  •  = Beat")

    with tab4:
        st.subheader("Instrument Recognition")

        if st.button("🎸 Analyze Instruments", use_container_width=True):
            st.markdown("#### Detected Instruments:")

            instruments = [
                ("Electric Guitar", 95, "Lead"),
                ("Bass Guitar", 92, "Rhythm"),
                ("Drums", 98, "Percussion"),
                ("Piano", 87, "Harmony"),
                ("Vocals", 91, "Melody"),
                ("Strings", 78, "Background")
            ]

            for instrument, confidence, role in instruments:
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.markdown(f"**{instrument}**")
                with col2:
                    st.progress(confidence / 100)
                with col3:
                    st.caption(role)

# MIDI Log Display (bottom of page)
st.divider()
with st.expander("📝 MIDI Activity Log", expanded=False):
    if st.session_state.midi_log:
        log_text = "\n".join(st.session_state.midi_log[-20:])
        st.code(log_text, language="text")

        if st.button("🗑️ Clear Log"):
            st.session_state.midi_log = []
            st.rerun()
    else:
        st.info("No MIDI activity yet")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🎛️ FaderPort 16 AI Emulator")
with col2:
    st.caption("Built with Streamlit")
with col3:
    st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d')}")

# Helper function for music theory
def get_music_theory_response(question):
    """Simple music theory responses"""

    responses = {
        'chord progression': "A great chord progression for jazz is: IIm7 - V7 - Imaj7 (e.g., Dm7 - G7 - Cmaj7). This is called the II-V-I progression and is the foundation of jazz harmony.",
        'circle of fifths': "The Circle of Fifths shows the relationship between the 12 tones. Moving clockwise adds sharps, counter-clockwise adds flats. It helps with key signatures and chord progressions.",
        'scale': "Common scales include: Major (Ionian), Natural Minor (Aeolian), Harmonic Minor, Melodic Minor, and the 7 modes (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian).",
        'modes': "The 7 modes are: Ionian (Major), Dorian, Phrygian, Lydian, Mixolydian, Aeolian (Minor), and Locrian. Each has a unique character and sound.",
        'modulate': "To modulate from C Major to A Minor (relative keys), you can use common chords like Am, which exists in both keys. Or use a pivot chord like Em (iii in C, v in Am).",
        'g7': "Over a G7 chord, you can use: G Mixolydian, G Blues scale, G Altered scale (for tension), or simply G Major Pentatonic for a safe approach.",
        'tempo': "Common tempos: Largo (40-60 bpm), Adagio (66-76), Andante (76-108), Moderato (108-120), Allegro (120-168), Presto (168-200).",
        'time signature': "4/4 (common time) has 4 beats per measure. 3/4 is waltz time. 6/8 is compound meter with 2 main beats subdivided into 3. 5/4 and 7/8 are asymmetric meters.",
        'interval': "Intervals: Unison (0), Minor 2nd (1), Major 2nd (2), Minor 3rd (3), Major 3rd (4), Perfect 4th (5), Tritone (6), Perfect 5th (7), Minor 6th (8), Major 6th (9), Minor 7th (10), Major 7th (11), Octave (12)."
    }

    for key, response in responses.items():
        if key in question:
            return response

    return "That's a great question! Music theory is vast. Try asking about: chord progressions, scales, modes, the circle of fifths, intervals, tempo, time signatures, or modulation."
