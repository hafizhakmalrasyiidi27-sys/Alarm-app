import streamlit as st
import datetime
import time

# ====== CONFIG ======
st.set_page_config(
    page_title="Modern Alarm App",
    page_icon="⏰",
    layout="centered"
)

# ====== SIMPLE IMAGE (Dijamin Tidak Diblokir) ======
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://openmoji.org/data/color/svg/23F0.svg" width="90">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style="text-align:center; font-weight:600; margin-top: -10px;">
        Modern Alarm App
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("")


# ====== SESSION STATE ======
if "alarm_time" not in st.session_state:
    st.session_state.alarm_time = None

if "logs" not in st.session_state:
    st.session_state.logs = []


# ====== SET ALARM ======
st.subheader("⏰ Set Alarm")

alarm_input = st.time_input("Pilih Jam Alarm", value=None)

if st.button("Set Alarm"):
    st.session_state.alarm_time = alarm_input
    st.success(f"Alarm berhasil disetel untuk pukul **{alarm_input}**")


# ====== CEK ALARM ======
st.subheader("🔄 Alarm Status")

current_time = datetime.datetime.now().strftime("%H:%M:%S")
st.write(f"**Waktu Sekarang:** {current_time}")

if st.session_state.alarm_time:
    alarm_str = st.session_state.alarm_time.strftime("%H:%M:00")

    if current_time == alarm_str:
        st.warning("⏰ **Alarm Berbunyi!**")
        st.balloons()

        # Simpan log
        st.session_state.logs.append(
            {"time": current_time, "status": "Alarm triggered"}
        )
    else:
        st.info("Alarm belum berbunyi.")


# ====== LOG ======
st.subheader("📜 Alarm Log")

if len(st.session_state.logs) == 0:
    st.write("Belum ada log alarm.")
else:
    for log in st.session_state.logs:
        st.write(f"- {log['time']} — {log['status']}")
