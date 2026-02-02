import streamlit as st
import pandas as pd
import time
from cerebras.cloud.sdk import Cerebras

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Sepsis Reflex Agent", layout="wide")

# --- 2. THE AI BRAIN (The Logic) ---
def trigger_ai_reflex(client, bp, hrv):
    """Calculates the medical reasoning and measures the Cerebras speed."""
    start_time = time.time()
    
    prompt = (
        f"CRITICAL: Patient BP is {bp} (stable) but HRV is {hrv} (low). "
        "This is Hemodynamic Incoherence. Provide a 1-sentence emergency "
        "clinical instruction for the ICU team."
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a Sepsis Reflex Agent specializing in micro-circulatory failure."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b",
    )
    
    latency = (time.time() - start_time) * 1000 # Speed Test in Milliseconds
    return response.choices[0].message.content, latency

# --- 3. UI LAYOUT ---
st.title("🩺 Sepsis Reflex Agent | Powered by Cerebras")
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Cerebras API Key", type="password")

# Layout Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Hemodynamic Stream")
    chart_placeholder = st.empty()
    metric_col1, metric_col2 = st.columns(2)
    bp_metric = metric_col1.empty()
    hrv_metric = metric_col2.empty()

with col2:
    st.subheader("AI Clinical Reflex")
    alert_placeholder = st.empty()
    speed_placeholder = st.empty()

# --- 4. THE EXECUTION LOOP ---
if st.sidebar.button("Start Live Monitor"):
    if not api_key:
        st.error("Please enter your API Key!")
    else:
        client = Cerebras(api_key=api_key)
        df = pd.read_csv("patient_data.csv")
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Update Graphs and Metrics
            chart_placeholder.line_chart(df.iloc[:i+1].set_index('second')[['blood_pressure', 'hrv_entropy']])
            bp_metric.metric("Blood Pressure", f"{row['blood_pressure']} mmHg")
            hrv_metric.metric("HRV Entropy", f"{row['hrv_entropy']:.2f}")

            # THE DETECTION LOGIC
            if row['hrv_entropy'] < 0.5:
                alert_placeholder.warning("⚠️ CRITICAL SHIFT DETECTED. ANALYZING...")
                
                # CALL THE AI REFLEX
                reasoning, speed = trigger_ai_reflex(client, row['blood_pressure'], row['hrv_entropy'])
                
                # SHOW RESULTS
                alert_placeholder.error(f"**Sepsis Alert:** {reasoning}")
                speed_placeholder.info(f"⚡ Reflex Latency: {speed:.2f}ms")
                break # Stop the demo at the moment of detection
            
            time.sleep(0.2) # Speeds up the demo