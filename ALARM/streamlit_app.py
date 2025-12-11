import streamlit as st
import datetime
import time

# ===============================
# IMAGE ICONS (Guaranteed Visible)
# ===============================
ICON_ALARM = "https://raw.githubusercontent.com/google/material-design-icons/master/png/device/access_alarm/materialicons/48dp/2x/baseline_access_alarm_black_48dp.png"
ICON_CLOCK = "https://raw.githubusercontent.com/google/material-design-icons/master/png/device/access_time/materialicons/48dp/2x/baseline_access_time_black_48dp.png"
ICON_REPEAT = "https://raw.githubusercontent.com/google/material-design-icons/master/png/av/repeat/materialicons/48dp/2x/baseline_repeat_black_48dp.png"
ICON_LOG = "https://raw.githubusercontent.com/google/material-design-icons/master/png/action/history/materialicons/48dp/2x/baseline_history_black_48dp.png"
HEADER_BANNER = "https://raw.githubusercontent.com/google/material-design-icons/master/png/device/access_alarm/materialicons/48dp/2x/baseline_access_alarm_black_48dp.png"

# ===============================
# Models
# ===============================
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

# ===============================
# Utils
# ===============================
def format_duration(seconds):
    mins = seconds // 60
    sec = seconds % 60
    return f"{mins}m {sec}s"

# ===============================
# Session
# ===============================
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "triggered" not in st.session_state:
    st.session_state.triggered = None

# ===============================
# Header
# ===============================
st.image(HEADER_BANNER, width=80)
st.markdown("<h1 style='text-align:center;'>Alarm App</h1>", unsafe_allow_html=True)

# ===============================
# Sidebar - Add Alarm
# ===============================
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Label")
time_str = st.sidebar.time_input("Time", datetime.time(7, 0)).strftime("%H:%M")
repeat = st.sidebar.multiselect("Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

if st.sidebar.button("Add"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat))
    st.sidebar.success("Alarm added")

# ===============================
# List Alarms
# ===============================
st.subheader("Active Alarms")

if not st.session_state.alarms:
    st.info("No alarms yet.")
else:
    for idx, alarm in enumerate(st.session_state.alarms):

        with st.container():
            col1, col2, col3, col4 = st.columns([1, 4, 2, 2])

            with col1:
                st.image(ICON_ALARM, width=40)

            with col2:
                st.write(f"**{alarm.label}**")
                st.write(f"⏰ {alarm.time_str}")
                st.write(f"🔁 {', '.join(alarm.repeat) if alarm.repeat else 'No Repeat'}")

            with col3:
                if st.button("Toggle", key=f"tgl{idx}"):
                    alarm.enabled = not alarm.enabled

            with col4:
                if st.button("Delete", key=f"del{idx}"):
                    st.session_state.alarms.pop(idx)
                    st.experimental_rerun()

# ===============================
# Trigger logic
# ===============================
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
current_day = now.strftime("%a")

for alarm in st.session_state.alarms:
    if alarm.enabled:
        match_time = alarm.time_str == current_time
        match_day = (not alarm.repeat) or (current_day in alarm.repeat)

        if match_time and match_day:
            st.session_state.triggered = {
                "label": alarm.label,
                "start": time.time()
            }

# ===============================
# Alarm Ringing UI
# ===============================
if st.session_state.triggered:
    st.error("⏰ Alarm ringing!")
    st.write(f"Alarm: **{st.session_state.triggered['label']}**")

    if st.button("Stop Alarm"):
        duration = int(time.time() - st.session_state.triggered['start'])
        st.session_state.logs.append(AlarmLog(st.session_state.triggered['label'], duration))
        st.session_state.triggered = None
        st.success("Stopped")

# ===============================
# Logs
# ===============================
st.subheader("History Logs")

if not st.session_state.logs:
    st.info("No logs available.")
else:
    for log in st.session_state.logs:
        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.image(ICON_LOG, width=35)
            with col2:
                st.write(f"**{log.label}**")
                st.write(f"🕒 {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"Duration: {format_duration(log.duration)}")
