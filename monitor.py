import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Automatically create required folders if they don't exist
os.makedirs("sessions", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ────────────────────────────────────────────────────────────────
# Page configuration – better mobile & desktop experience
st.set_page_config(
    page_title="Drowsiness Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"   # collapsed on mobile by default
)

# Hide Streamlit default menu/footer/header for cleaner look
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
st.title("🛡️ Drowsiness Monitoring Dashboard")

tab1, tab2 = st.tabs(["📊 Logs", "🎥 Videos"])

# ────────────────────────────────────────────────────────────────
with tab1:
    st.header("Drowsiness Events")

    log_path = "drowsiness_logs.csv"

    if os.path.exists(log_path):
        df = pd.read_csv(log_path)

        if not df.empty:
            # Sort newest first & make table mobile-friendly
            st.dataframe(
                df.sort_values(by="Full Timestamp", ascending=False)
                  .style.set_properties(**{'text-align': 'left'}),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                label="⬇️ Download Full Log as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"drowsiness_log_{datetime.now().strftime('%Y-%m-%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Log file exists but contains no records yet.")
    else:
        st.info("No drowsiness logged yet.\nStart monitoring by running monitor.py")

# ────────────────────────────────────────────────────────────────
with tab2:
    st.header("Session Recordings")

    video_files = [f for f in os.listdir("sessions") 
                   if f.lower().endswith((".mp4", ".avi", ".mov"))]

    if video_files:
        # Newest first
        video_files.sort(reverse=True)

        selected = st.selectbox("Choose session to watch", video_files)

        # Show video player
        st.video(os.path.join("sessions", selected))

        # Try to show nice date/time
        try:
            # Expected format: session_YYYY-MM-DD_HH-MM-SS.mp4
            parts = selected.replace("session_", "").split(".")[0].split("_")
            if len(parts) >= 2:
                date_str = parts[0]
                time_str = parts[1].replace("-", ":")
                readable = f"{date_str} {time_str}"
                st.caption(f"Recorded: {readable}")
            else:
                st.caption(f"Recorded: {selected}")
        except:
            st.caption(f"Recorded: {selected}")
    else:
        st.info("No videos recorded yet.\nRun monitor.py to start a monitoring session.")

# ────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    "**How to use**\n\n"
    "1. Run `monitor.py` on your computer to start watching & recording\n"
    "2. Close eyes for >1–2 seconds to test detection\n"
    "3. Press **Q** to stop monitoring\n"
    "4. Come back here to view logs & videos\n\n"
    "Tip: Use your phone to check this page while monitoring runs on PC."
)