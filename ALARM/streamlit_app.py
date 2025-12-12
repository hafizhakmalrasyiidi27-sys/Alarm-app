import streamlit as st
import datetime
import time
import uuid

# -----------------------------------------------------------
# OPTIONAL: Auto Refresh (agar alarm bisa trigger)
# -----------------------------------------------------------
# Membuat query param dinamis agar Streamlit rerun setiap detik.
# Jika ingin mematikan auto-refresh, komentar atau hapus baris di bawah.
st.experimental_set_query_params(_refresh=str(int(time.time())))

# -----------------------------------------------------------
# Model data untuk alarm & log
# -----------------------------------------------------------
class Alarm:
    def __init__(self, label, time_str, repeat):
        self.label = label
        self.time_str = time_str
        self.repeat = repeat  # list of days (e.g. ["Mon","Tue"])
        self.enabled = True

class AlarmLog:
    def __init__(self, label, duration):
        self.label = label
        self.duration = duration
        self.timestamp = datetime.datetime.now()

# -----------------------------------------------------------
# Utility
# -----------------------------------------------------------
def format_duration(seconds: int) -> str:
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds}s"

# -----------------------------------------------------------
# Initialize State
# -----------------------------------------------------------
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "triggered" not in st.session_state:
    st.session_state.triggered = None  # {"label":..., "start_time":..., "id":...}

# -----------------------------------------------------------
# Background (TAMBAHAN)
# -----------------------------------------------------------
page_bg = """
<style>
/* background gradient + subtle pattern */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f6f8fb 0%, #d7e1ea 50%, #b9c6d3 100%);
    background-attachment: fixed;
}
.stCard {
    background: rgba(255,255,255,0.6) !important;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(22, 40, 62, 0.08);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------------------------------------
# Sidebar - Create Alarm
# -----------------------------------------------------------
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Label", value="My Alarm")
time_input = st.sidebar.time_input("Alarm Time", value=datetime.time(7, 0))
time_str = time_input.strftime("%H:%M")  # store as "HH:MM"
repeat_days = st.sidebar.multiselect("Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

if st.sidebar.button("Add Alarm"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat_days))
    st.sidebar.success("Alarm added successfully.")

# Optional: choose alarm sound URL or upload (we use a safe public sound by default)
DEFAULT_ALARM_SOUND = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"

# Allow user to test sound
st.sidebar.markdown("---")
if st.sidebar.button("Test Sound"):
    # Render a short audio tag that plays once
    st.sidebar.markdown(
        f"""
        <audio autoplay>
            <source src="{DEFAULT_ALARM_SOUND}" type="audio/ogg">
            Your browser does not support the audio element.
        </audio>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------
# Main Layout
# -----------------------------------------------------------
st.title("Alarm App")

# Gambar jam modern (tanpa caption)
st.image("https://cdn-icons-png.flaticon.com/512/992/992700.png", width=140)

# -----------------------------------------------------------
# Display Active Alarms
# -----------------------------------------------------------
st.subheader("Active Alarms")

if len(st.session_state.alarms) == 0:
    st.info("No alarms available.")
else:
    # Iterate by index to keep keys stable for buttons
    for idx in range(len(st.session_state.alarms)):
        # guard in case list length changed
        if idx >= len(st.session_state.alarms):
            break

        alarm = st.session_state.alarms[idx]

        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        with col1:
            st.markdown(f"**{alarm.label}** — `{alarm.time_str}`")
        with col2:
            st.markdown(f"{', '.join(alarm.repeat) if alarm.repeat else 'No Repeat'}")
        with col3:
            toggle_key = f"toggle_{idx}"
            if st.button("Toggle", key=toggle_key):
                if 0 <= idx < len(st.session_state.alarms):
                    st.session_state.alarms[idx].enabled = not st.session_state.alarms[idx].enabled
        with col4:
            delete_key = f"delete_{idx}"
            if st.button("Delete", key=delete_key):
                # Safe removal: rebuild list without the selected index
                if 0 <= idx < len(st.session_state.alarms):
                    st.session_state.alarms = [a for i, a in enumerate(st.session_state.alarms) if i != idx]
                # no st.experimental_rerun() here

# -----------------------------------------------------------
# Alarm Trigger Check
# -----------------------------------------------------------
current_time = datetime.datetime.now().strftime("%H:%M")
current_day = datetime.datetime.now().strftime("%a")

for alarm in st.session_state.alarms:
    if alarm.enabled:
        should_trigger = (alarm.time_str == current_time)
        if alarm.repeat:
            should_trigger = should_trigger and (current_day in alarm.repeat)
        if should_trigger:
            # Only set triggered if none currently triggered
            if not st.session_state.triggered:
                # unique id to help JS selectors if needed
                trig_id = str(uuid.uuid4())
                st.session_state.triggered = {
                    "label": alarm.label,
                    "start_time": time.time(),
                    "id": trig_id,
                    "sound_url": DEFAULT_ALARM_SOUND
                }

# -----------------------------------------------------------
# Triggered Alarm Interface + Sound
# -----------------------------------------------------------
if st.session_state.triggered:
    trig = st.session_state.triggered
    st.warning(f"⏰ Alarm: **{trig['label']}** is ringing!")

    # Play looping audio via HTML audio tag (autoplay + loop)
    # audio element has fixed id so we can pause it later
    st.markdown(
        f"""
        <div id="alarm_container">
            <audio id="alarm_audio" autoplay loop>
                <source src="{trig['sound_url']}" type="audio/ogg">
                Your browser does not support the audio element.
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Button to stop alarm and create log
    if st.button("Stop Alarm"):
        # Pause audio using JS before clearing triggered (this markup will run on the rerun)
        st.markdown(
            """
            <script>
            try {{
                var a = document.getElementById('alarm_audio');
                if (a) {{ a.pause(); a.currentTime = 0; }}
            }} catch(e){{ console.log(e) }}
            </script>
            """.format(),
            unsafe_allow_html=True
        )

        start = trig["start_time"]
        duration = int(time.time() - start)

        st.session_state.logs.append(
            AlarmLog(trig["label"], duration)
        )

        # clear triggered
        st.session_state.triggered = None
        st.success("Alarm stopped and logged.")

# -----------------------------------------------------------
# Alarm Logs
# -----------------------------------------------------------
st.subheader("Alarm Logs")

if len(st.session_state.logs) == 0:
    st.info("No logs available.")
else:
    # show newest first
    for log in reversed(st.session_state.logs):
        timestamp_str = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        duration_str = format_duration(log.duration)
        st.write(f"{timestamp_str} — **{log.label}** — {duration_str}")

# -----------------------------------------------------------
# OPTIONAL: quick instructions / footer
# -----------------------------------------------------------
st.markdown("---")
st.markdown(
)
