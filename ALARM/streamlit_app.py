import streamlit as st
import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="ALARM MODERN",
    page_icon="⏰",
    layout="centered"
)

# =====================================
# CUSTOM CSS (MODERN LOOK)
# =====================================
st.markdown("""
<style>
.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    border: 1px solid #eee;
    margin-bottom: 20px;
}
.log-box {
    background: #f8f8f8;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #e5e5e5;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER TANPA LOGO + GAMBAR ALARM ESTETIK
# =====================================
st.markdown("""
    <div style="text-align:center; padding: 20px 10px;">
        <img src="https://cdn-icons-png.flaticon.com/512/1048/1048944.png"
             width="120" style="margin-bottom:15px;">
        <h1 style="
            font-weight:800;
            margin-top: 5px;
            color:#222;
        ">ALARM MODERN</h1>
        <p style="margin-top:-8px; color:#666; font-size:15px;">
            Minimal • Clean • Smooth Interface
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
# SECTION: SET ALARM
# =====================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### ⏰ Set Alarm")

alarm_input = st.time_input("Pilih Jam Alarm", value=None)

if st.button("Set Alarm"):
    st.session_state.alarm_time = alarm_input
    st.success(f"Alarm berhasil disetel untuk pukul **{alarm_input}**")
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# SECTION: STATUS
# =====================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔄 Status Alarm")

current_time = datetime.datetime.now().strftime("%H:%M:%S")
st.write(f"**Waktu Sekarang:** {current_time}")

if st.session_state.alarm_time:
    alarm_str = st.session_state.alarm_time.strftime("%H:%M:00")

    if current_time == alarm_str:
        st.warning("⏰ Alarm Berbunyi!")
        st.balloons()

        st.session_state.logs.append({
            "time": current_time,
            "status": "Alarm triggered"
        })
    else:
        st.info("Alarm belum berbunyi.")
else:
    st.write("Belum ada alarm yang disetel.")

st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# SECTION: LOGS
# =====================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📜 Alarm Log")

if len(st.session_state.logs) == 0:
    st.write("Belum ada log alarm.")
else:
    for log in st.session_state.logs:
        st.markdown(
            f"""<div class="log-box">
                <b>{log['time']}</b> — {log['status']}
            </div>""",
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)
