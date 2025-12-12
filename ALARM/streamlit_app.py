import streamlit as st
import datetime
import time
import uuid

# -----------------------------------------------------------
# AUTO REFRESH (agar alarm bisa trigger tepat waktu)
# -----------------------------------------------------------
st.experimental_set_query_params(_refresh=str(int(time.time())))

# -----------------------------------------------------------
# MODEL DATA
# -----------------------------------------------------------
class Alarm:
    def __init__(self, label, time_str, repeat):
        self.label = label
        self.time_str = time_str
        self.repeat = repeat
        self.enabled = True

class AlarmLog:
    def __init__(self, label, duration):
        self.label = label
        self.duration = duration
        self.timestamp = datetime.datetime.now()

# -----------------------------------------------------------
# UTIL
# -----------------------------------------------------------
def format_duration(seconds: int) -> str:
    m = seconds // 60
    s = seconds % 60
    return f"{m}m {s}s"

# -----------------------------------------------------------
# STATE
# -----------------------------------------------------------
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "triggered" not in st.session_state:
    st.session_state.triggered = None

# -----------------------------------------------------------
# PAGE BACKGROUND
# -----------------------------------------------------------
page_bg = """
<style>
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
# SIDEBAR – ADD ALARM
# -----------------------------------------------------------
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Label", value="My Alarm")
time_input = st.sidebar.time_input("Alarm Time", value=datetime.time(7, 0))
time_str = time_input.strftime("%H:%M")
repeat_days = st.sidebar.multiselect(
    "Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)

if st.sidebar.button("Add Alarm"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat_days))
    st.sidebar.success("Alarm added successfully!")

# Test Sound button
DEFAULT_ALARM_SOUND = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"

if st.sidebar.button("Test Sound"):
    st.sidebar.markdown(
        f"""
        <audio autoplay>
            <source src="{DEFAULT_ALARM_SOUND}" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------
st.title("Alarm App")

# Gambar jam modern
st.image("https://cdn-icons-png.flaticon.com/512/992/992700.png", width=140)

# -----------------------------------------------------------
# ACTIVE ALARMS
# -----------------------------------------------------------
st.subheader("Active Alarms")

if len(st.session_state.alarms) == 0:
    st.info("No alarms available.")
else:
    for idx in range(len(st.session_state.alarms)):
        if idx >= len(st.session_state.alarms):
            break

        alarm = st.session_state.alarms[idx]

        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        with col1:
            st.markdown(f"**{alarm.label}** — `{alarm.time_str}`")
        with col2:
            st.markdown(
                ", ".join(alarm.repeat) if alarm.repeat else "No Repeat"
            )
        with col3:
            if st.button("Toggle", key=f"toggle_{idx}"):
                st.session_state.alarms[idx].enabled = not alarm.enabled
        with col4:
            if st.button("Delete", key=f"delete_{idx}"):
                st.session_state.alarms = [
                    a for i, a in enumerate(st.session_state.alarms)
                    if i != idx
                ]

# -----------------------------------------------------------
# CHECK ALARM TRIGGER
# -----------------------------------------------------------
now_time = datetime.datetime.now().strftime("%H:%M")
now_day = datetime.datetime.now().strftime("%a")

for alarm in st.session_state.alarms:
    if alarm.enabled:
        match = alarm.time_str == now_time
        if alarm.repeat:
            match = match and (now_day in alarm.repeat)

        if match:
            if not st.session_state.triggered:
                st.session_state.triggered = {
                    "label": alarm.label,
                    "start_time": time.time(),
                    "sound_url": DEFAULT_ALARM_SOUND,
                    "id": str(uuid.uuid4())
                }

# -----------------------------------------------------------
# ALARM RINGING UI + SOUND
# -----------------------------------------------------------
if st.session_state.triggered:
    trig = st.session_state.triggered

    st.warning(f"⏰ Alarm: **{trig['label']}** is ringing!")

    # Play looping alarm sound
    st.markdown(
        f"""
        <audio id="alarm_audio" autoplay loop>
            <source src="{trig['sound_url']}" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True
    )

    if st.button("Stop Alarm"):
        # Stop sound
        st.markdown(
            """
            <script>
            var a = document.getElementById("alarm_audio");
            if (a) { a.pause(); a.currentTime = 0; }
            </script>
            """,
            unsafe_allow_html=True
        )

        # Save log
        duration = int(time.time() - trig["start_time"])
        st.session_state.logs.append(AlarmLog(trig["label"], duration))

        # Clear triggered
        st.session_state.triggered = None

        st.success("Alarm stopped and logged.")

# -----------------------------------------------------------
# LOGS
# -----------------------------------------------------------
st.subheader("Alarm Logs")

if len(st.session_state.logs) == 0:
    st.info("No logs available.")
else:
    for log in reversed(st.session_state.logs):
        ts = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        dur = format_duration(log.duration)
        st.write(f"{ts} — **{log.label}** — {dur}")
