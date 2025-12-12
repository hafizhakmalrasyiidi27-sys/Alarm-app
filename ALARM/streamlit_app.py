import streamlit as st
import datetime
import time

# -----------------------------------------------------------
# Auto Refresh (agar alarm bisa trigger)
# -----------------------------------------------------------
# Note: ini mengubah query param setiap run agar Streamlit melakukan refresh.
# Jika ingin hentikan auto-refresh, hapus atau komentari baris ini.
st.experimental_set_query_params(refresh=str(int(time.time())))

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
# Background (TAMBAHAN)
# -----------------------------------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%);
    background-size: cover;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


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

# Gambar jam modern
st.image(
    "https://cdn-icons-png.flaticon.com/512/992/992700.png",
    width=150
)


# -----------------------------------------------------------
# Display Active Alarms
# -----------------------------------------------------------
st.subheader("Active Alarms")

if len(st.session_state.alarms) == 0:
    st.info("No alarms available.")
else:
    # Iterate by index to keep references stable for buttons
    for idx in range(len(st.session_state.alarms)):
        # Guard: in some rare cases list could have changed; re-check length
        if idx >= len(st.session_state.alarms):
            break

        alarm = st.session_state.alarms[idx]

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.write(f"{alarm.label} — {alarm.time_str}")

        with col2:
            st.write(", ".join(alarm.repeat) if alarm.repeat else "No Repeat")

        # Buttons use unique keys based on idx + stable prefix
        toggle_key = f"toggle_{idx}"
        delete_key = f"delete_{idx}"

        with col3:
            if st.button("Toggle", key=toggle_key):
                # verify idx still valid
                if 0 <= idx < len(st.session_state.alarms):
                    st.session_state.alarms[idx].enabled = not st.session_state.alarms[idx].enabled

        with col4:
            if st.button("Delete", key=delete_key):
                # Safe removal: build new list without the selected index
                if 0 <= idx < len(st.session_state.alarms):
                    st.session_state.alarms = [a for i, a in enumerate(st.session_state.alarms) if i != idx]
                # Do NOT call st.experimental_rerun(); Streamlit will re-run after button click automatically.


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
            # Only set triggered if none currently triggered (prevents overwriting start_time)
            if not st.session_state.triggered:
                st.session_state.triggered = {
                    "label": alarm.label,
                    "start_time": time.time()
                }


# -----------------------------------------------------------
# Triggered Alarm Interface
# -----------------------------------------------------------
if st.session_state.triggered:
    st.warning(f"⏰ Alarm: {st.session_state.triggered['label']} is ringing!")

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
