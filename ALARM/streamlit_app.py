import streamlit as st
import datetime
import time

# ======================================
# Modern Icons (Heroicons – guaranteed)
# ======================================
ICON_ALARM = "https://unpkg.com/heroicons@2.1.1/24/solid/bell-alert.svg"
ICON_CLOCK = "https://unpkg.com/heroicons@2.1.1/24/solid/clock.svg"
ICON_REPEAT = "https://unpkg.com/heroicons@2.1.1/24/solid/arrow-path.svg"
ICON_LOG = "https://unpkg.com/heroicons@2.1.1/24/solid/book-open.svg"
HEADER_BANNER = "https://unpkg.com/heroicons@2.1.1/24/solid/bell.svg"

# ======================================
# Models
# ======================================
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

# ======================================
# Utils
# ======================================
def format_duration(seconds):
    mins = seconds // 60
    sec = seconds % 60
    return f"{mins}m {sec}s"

# ======================================
# Init State
# ======================================
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "triggered" not in st.session_state:
    st.session_state.triggered = None

# ======================================
# Modern Header
# ======================================
st.markdown(
    """
    <div style="text-align:center; padding:10px 0 0 0;">
        <img src='https://unpkg.com/heroicons@2.1.1/24/solid/bell.svg' width='60'>
        <h1 style="margin-top:10px; font-size:32px; font-weight:700;">Modern Alarm App</h1>
        <p style="color:#777; margin-top:-10px;">Minimalist • Clean • Modern UI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================
# Sidebar – Add Alarm
# ======================================
st.sidebar.title("Create Alarm")

label = st.sidebar.text_input("Label")
time_str = st.sidebar.time_input("Time", datetime.time(7, 0)).strftime("%H:%M")
repeat = st.sidebar.multiselect("Repeat", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

if st.sidebar.button("Add Alarm"):
    st.session_state.alarms.append(Alarm(label, time_str, repeat))
    st.sidebar.success("Alarm added")

# ======================================
# Alarm List
# ======================================
st.subheader("Active Alarms")

if not st.session_state.alarms:
    st.info("No alarms added yet.")
else:
    for idx, alarm in enumerate(st.session_state.alarms):

        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:16px;
                background:rgba(255,255,255,0.7);
                margin-bottom:14px;
                border:1px solid #eee;
                box-shadow:0 4px 12px rgba(0,0,0,0.05);
            ">
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns([1, 4, 2, 2])

        with col1:
            st.image(ICON_ALARM, width=42)

        with col2:
            st.write(f"**{alarm.label}**")
            st.write(f"🕒 {alarm.time_str}")
            st.write(f"🔁 {', '.join(alarm.repeat) if alarm.repeat else 'No repeat'}")

        with col3:
            if st.button("Enable" if not alarm.enabled else "Disable", key=f"toggle{idx}"):
                alarm.enabled = not alarm.enabled

        with col4:
            if st.button("Delete", key=f"delete{idx}"):
                st.session_state.alarms.pop(idx)
                st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# Alarm Trigger Logic
# ======================================
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
current_day = now.strftime("%a")

for alarm in st.session_state.alarms:
    if alarm.enabled:
        match_time = current_time == alarm.time_str
        match_day = (not alarm.repeat) or (current_day in alarm.repeat)

        if match_time and match_day:
            st.session_state.triggered = {
                "label": alarm.label,
                "start": time.time()
            }

# ======================================
# Alarm Ringing UI
# ======================================
if st.session_state.triggered:
    st.error("⏰ Alarm is ringing!")
    st.write(f"Alarm: **{st.session_state.triggered['label']}**")

    if st.button("Stop Alarm"):
        duration = int(time.time() - st.session_state.triggered["start"])
        st.session_state.logs.append(AlarmLog(st.session_state.triggered["label"], duration))
        st.session_state.triggered = None
        st.success("Alarm stopped")

# ======================================
# Logs Section
# ======================================
st.subheader("Alarm Logs")

if not st.session_state.logs:
    st.info("No logs yet.")
else:
    for log in st.session_state.logs:
        st.markdown(
            """
            <div style="
                padding:15px;
                border-radius:14px;
                background:#fafafa;
                border:1px solid #eee;
                margin-bottom:12px;
                box-shadow:0 4px 10px rgba(0,0,0,0.03);
            ">
            """, 
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 6])

        with col1:
            st.image(ICON_LOG, width=38)

        with col2:
            st.write(f"**{log.label}**")
            st.write(f"🗓 {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"⏱ Duration: {format_duration(log.duration)}")

        st.markdown("</div>", unsafe_allow_html=True)
