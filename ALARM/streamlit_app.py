import streamlit as st
import datetime
import time

# --------------------------------------------------------------------
#  Image URLs (Open-source icons)
# --------------------------------------------------------------------
ICON_ALARM = "https://cdn-icons-png.flaticon.com/512/1827/1827370.png"
ICON_TIME = "https://cdn-icons-png.flaticon.com/512/1827/1827375.png"
ICON_REPEAT = "https://cdn-icons-png.flaticon.com/512/1827/1827393.png"
ICON_LOG = "https://cdn-icons-png.flaticon.com/512/2099/2099199.png"
HEADER_BANNER = "https://cdn.pixabay.com/photo/2017/08/30/07/45/alarm-clock-2691564_1280.jpg"

# --------------------------------------------------------------------
#  Models
# --------------------------------------------------------------------
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

# --------------------------------------------------------------------
# Utility
# --------------------------------------------------------------------
def format_duration(seconds):
    minutes = seconds // 60
    second = seconds % 60
    return f"{minutes}m {second}s"

# --------------------------------------------------------------------
# State init
# --------------------------------------------------------------------
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "triggered" not in st.session_state:
    st.session_state.triggered = None

# --------------------------------------------------------------------
# HEADER WITH IMAGE
# --------------------------------------------------------------------
st.image(HEADER_BANNER, use_column_width=True)
st.markdown(
    "<h1 style='text-align:center; margin-top: -20px;'>Modern Alarm App</h1>",
    unsafe_allow_html=True
)

# --------------------------------------------------------------------
# Sidebar - Create Alarm
# --------------------------------------------------------------------
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Alarm Label")
time_str = st.sidebar.time_input("Time", value=datetime.time(7, 0)).strftime("%H:%M")
repeat_days = st.sidebar.multiselect("Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

if st.sidebar.button("Add Alarm"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat_days))
    st.sidebar.success("Alarm added successfully")

# --------------------------------------------------------------------
# Display Alarms
# --------------------------------------------------------------------
st.subheader("Active Alarms")

if len(st.session_state.alarms) == 0:
    st.info("No alarms added.")
else:
    for idx, alarm in enumerate(st.session_state.alarms):

        st.markdown("""
            <div style="
                border:1px solid #ddd; 
                padding:15px; 
                border-radius:10px; 
                margin-bottom:12px;
                background-color:#fafafa;">
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])

        with col1:
            st.image(ICON_ALARM, width=40)

        with col2:
            st.write(f"**{alarm.label}**")
            st.write(f"<img src='{ICON_TIME}' width='18'> {alarm.time_str}", unsafe_allow_html=True)

            repeat_label = ", ".join(alarm.repeat) if alarm.repeat else "No Repeat"
            st.write(
                f"<img src='{ICON_REPEAT}' width='18'> {repeat_label}",
                unsafe_allow_html=True
            )

        with col3:
            if st.button("Enable/Disable", key=f"enable_{idx}"):
                alarm.enabled = not alarm.enabled

        with col4:
            if st.button("Delete", key=f"delete_{idx}"):
                st.session_state.alarms.pop(idx)
                st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------
# Alarm Trigger
# --------------------------------------------------------------------
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
current_day = now.strftime("%a")

for alarm in st.session_state.alarms:
    if alarm.enabled:
        should_trigger = alarm.time_str == current_time
        if alarm.repeat:
            should_trigger = should_trigger and (current_day in alarm.repeat)

        if should_trigger:
            st.session_state.triggered = {
                "label": alarm.label,
                "start_time": time.time()
            }

# Trigger UI
if st.session_state.triggered:
    st.error("Alarm is ringing!")
    st.write(f"Alarm: **{st.session_state.triggered['label']}**")

    if st.button("Stop Alarm"):
        duration = int(time.time() - st.session_state.triggered["start_time"])
        st.session_state.logs.append(AlarmLog(st.session_state.triggered["label"], duration))
        st.session_state.triggered = None
        st.success("Alarm stopped")

# --------------------------------------------------------------------
# Logs
# --------------------------------------------------------------------
st.subheader("Alarm Logs")

if len(st.session_state.logs) == 0:
    st.info("No logs yet.")
else:
    for log in st.session_state.logs:

        st.markdown("""
            <div style="
                border:1px solid #e1e1e1; 
                padding:15px; 
                border-radius:10px;
                margin-bottom:10px;">
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 6])

        with col1:
            st.image(ICON_LOG, width=40)
        with col2:
            st.write(f"**{log.label}**")
            st.write(f"Time: {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"Duration: {format_duration(log.duration)}")

        st.markdown("</div>", unsafe_allow_html=True)
