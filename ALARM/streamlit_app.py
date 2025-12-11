import streamlit as st
import datetime
import time

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Modern Alarm App",
    page_icon="⏰",
    layout="centered"
)

# =====================================
# HEADER MODERN
# =====================================
st.markdown("""
    <div style="text-align:center; padding: 10px;">
        <img src="https://openmoji.org/data/color/svg/23F0.svg" width="90">
        <h1 style="
            font-weight:700;
            margin-top: 5px;
            color: #333;
        ">Modern Alarm App</h1>
        <p style="margin-top: -10px; color: #777; font-size: 15px;">
            Simple • Clean • Modern Interface
        </p>
    </div>
""", unsafe_allow_html=True)


# =====================================
# SESSION STATE
# =====================================
if "alarm_time" not in st.session_state:
    st.session_state.alarm_time = None

if "logs" not in st.session_state:
    st.session_state.logs = []


# =====================================
# SECTION: SET ALARM (CARD)
# =====================================
st.markdown("""
    <div style="
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #eee;
        margin-bottom: 18px;
    ">
        <h3 style="margin-bottom:5px;">⏰ Set Alarm</h3>
    </div>
""", unsafe_allow_html=True)

alarm_input = st.time_input("Pilih Jam Alarm", value=None)

if st.button("Set Alarm"):
    st.session_state.alarm_time = alarm_input
    st.success(f"Alarm berhasil disetel untuk pukul **{alarm_input}**")


# =====================================
# SECTION: STATUS (CARD)
# =====================================
st.markdown("""
    <div style="
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #eee;
        margin-top: 15px;
        margin-bottom: 18px;
    ">
        <h3 style="margin-bottom:5px;">🔄 Alarm Status</h3>
    </div>
""", unsafe_allow_html=True)

current_time = datetime.datetime.now().strftime("%H:%M:%S")
st.write(f"**Waktu Sekarang:** {current_time}")

if st.session_state.alarm_time:
    alarm_str = st.session_state.alarm_time.strftime("%H:%M:00")

    if current_time == alarm_str:
        st.warning("⏰ Alarm Berbunyi!")
        st.balloons()

        # Simpan log
        st.session_state.logs.append({
            "time": current_time,
            "status": "Alarm triggered"
        })
    else:
        st.info("Alarm belum berbunyi.")


# =====================================
# SECTION: LOGS (CARD)
# =====================================
st.markdown("""
    <div style="
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #eee;
        margin-top: 15px;
    ">
        <h3 style="margin-bottom:5px;">📜 Alarm Log</h3>
    </div>
""", unsafe_allow_html=True)

if len(st.session_state.logs) == 0:
    st.write("Belum ada log alarm.")
else:
    for log in st.session_state.logs:
        st.markdown(
            f"""
            <div style="
                background: #fafafa;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid #e6e6e6;
                margin-bottom: 10px;
            ">
                <b>{log['time']}</b> — {log['status']}
            </div>
            """,
            unsafe_allow_html=True
        )
