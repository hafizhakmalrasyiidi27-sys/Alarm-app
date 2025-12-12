import streamlit as st
import datetime
import time

# -----------------------------------------------------------
# Model data untuk alarm & log
# -----------------------------------------------------------
class Alarm:
    def __init__(self, label, time_str, repeat):
        self.label = label
        self.time_str = time_str
        self.repeat = repeat  # list of days
        self.enabled = True

class AlarmLog:
    def __init__(self, label, duration):
        self.label = label
        self.duration = duration
        self.timestamp = datetime.datetime.now()

# -----------------------------------------------------------
# Utility
# -----------------------------------------------------------
def format_duration(seconds):
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
    st.session_state.triggered = None

# -----------------------------------------------------------
# Sidebar - Create Alarm
# -----------------------------------------------------------
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Label", "")
time_str = st.sidebar.time_input("Alarm Time", value=datetime.time(7, 0)).strftime("%H:%M")
repeat_days = st.sidebar.multiselect("Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

if st.sidebar.button("Add Alarm"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat_days))
    st.sidebar.success("Alarm added successfully.")

# -----------------------------------------------------------
# Main Layout
# -----------------------------------------------------------
st.title("Alarm App")

# -----------------------------------------------------------
# Display Active Alarms
# -----------------------------------------------------------
st.subheader("Active Alarms")

if len(st.session_state.alarms) == 0:
    st.info("No alarms available.")
else:
    for idx, alarm in enumerate(st.session_state.alarms):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.write(f"{alarm.label} — {alarm.time_str}")
        with col2:
            st.write(", ".join(alarm.repeat) if alarm.repeat else "No Repeat")
        with col3:
            if st.button("Toggle", key=f"toggle_{idx}"):
                alarm.enabled = not alarm.enabled
        with col4:
            if st.button("Delete", key=f"delete_{idx}"):
                st.session_state.alarms.pop(idx)
                st.experimental_rerun()

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
            st.session_state.triggered = {
                "label": alarm.label,
                "start_time": time.time()
            }

# -----------------------------------------------------------
# Triggered Alarm Interface
# -----------------------------------------------------------
if st.session_state.triggered:
    st.warning(f"Alarm: {st.session_state.triggered['label']} is ringing!")

    if st.button("Stop Alarm"):
        start = st.session_state.triggered["start_time"]
        duration = int(time.time() - start)

        st.session_state.logs.append(
            AlarmLog(st.session_state.triggered["label"], duration)
        )

        st.session_state.triggered = None
        st.success("Alarm stopped.")

# -----------------------------------------------------------
# Alarm Logs
# -----------------------------------------------------------
st.subheader("Alarm Logs")

if len(st.session_state.logs) == 0:
    st.info("No logs available.")
else:
    for log in st.session_state.logs:
        timestamp_str = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        duration_str = format_duration(log.duration)

        st.write(f"{timestamp_str} - {log.label} - {duration_str}")
