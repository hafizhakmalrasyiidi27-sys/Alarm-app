import streamlit as st
import datetime
import base64

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="ALARM MODERN",
    page_icon="⏰",
    layout="centered"
)

# ======================================================
# STYLE
# ======================================================
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
}
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("<h1 class='title'>⏰ ALARM MODERN</h1>", unsafe_allow_html=True)

# ======================================================
# SESSION STATE SETUP
# ======================================================
if "alarm_time" not in st.session_state:
    st.session_state.alarm_time = None

if "alarm_active" not in st.session_state:
    st.session_state.alarm_active = False

if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = False  # Browser butuh interaksi manual

# ======================================================
# LOAD SOUND (BASE64 SHORT BEEP)
# ======================================================
alarm_sound = """
<script>
function playAlarm(){
  var audio = new Audio("data:audio/mp3;base64,{}");
  audio.play();
}
</script>
""".format(base64.b64encode(open("beep.mp3", "rb").read()).decode())
st.markdown(alarm_sound, unsafe_allow_html=True)

# ======================================================
# INPUT WAKTU ALARM
# ======================================================
st.subheader("Atur Waktu Alarm")
alarm_input = st.time_input("Pilih waktu", value=datetime.datetime.now().time())

# ======================================================
# TOMBOL SET ALARM
# ======================================================
if st.button("Set Alarm ⏰"):
    st.session_state.alarm_time = alarm_input
    st.session_state.alarm_active = True
    st.success(f"Alarm disetel pada {alarm_input}")

# ======================================================
# TOMBOL STOP ALARM
# ======================================================
if st.button("Stop Alarm 🛑"):
    st.session_state.alarm_active = False
    st.session_state.sound_enabled = False
    st.warning("Alarm dimatikan.")

# ======================================================
# STATUS ALARM (ON / OFF)
# ======================================================
st.markdown("### Status Alarm")
if st.session_state.alarm_active:
    st.markdown("<h3 style='color:green;'>🟢 ON</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3 style='color:red;'>🔴 OFF</h3>", unsafe_allow_html=True)

# ======================================================
# TEST SOUND (HARUS TEKAN SEKALI AGAR BROWSER IZIN)
# ======================================================
if st.button("Test Sound 🔊"):
    st.session_state.sound_enabled = True
    st.markdown("<script>playAlarm()</script>", unsafe_allow_html=True)
    st.info("Jika suara terdengar, alarm siap berfungsi.")

# ======================================================
# CEK WAKTU ALARM
# ======================================================
current_time = datetime.datetime.now().strftime("%H:%M")
alarm_time_str = str(st.session_state.alarm_time)[:5] if st.session_state.alarm_time else None

if st.session_state.alarm_active and alarm_time_str == current_time:
    if st.session_state.sound_enabled:
        st.markdown("<script>playAlarm()</script>", unsafe_allow_html=True)
    st.error("⏰ Alarm Berbunyi!")

# ======================================================
# REFRESH OTOMATIS
# ======================================================
st.experimental_rerun()
