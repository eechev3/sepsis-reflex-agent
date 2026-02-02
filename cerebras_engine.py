import pandas as pd
import time
from cerebras.cloud.sdk import Cerebras


client = Cerebras(api_key="csk-2833m28v8htvmmeyckkdw3fen4w2y6kn395dcrh9y5nkd44h")
df = pd.read_csv("patient_data.csv")

print("--- STARTING LIVE PATIENT MONITOR ---")
print("Monitoring vitals at 1Hz (1 reading per second)...")
print("-" * 50)

for index, row in df.iterrows():
    
    status = f"SEC: {int(row['second'])} | BP: {row['blood_pressure']} | HRV: {row['hrv_entropy']}"
    
    # If HRV is high, everything is green
    if row['hrv_entropy'] > 0.5:
        print(f"{status} | STATUS: [ NORMAL ]")
    else:
        # THE REFLEX MOMENT
        print(f"{status} | STATUS: [ !!! WARNING !!! ]")
        print("\n>>> CRITICAL SHIFT DETECTED. CALLING CEREBRAS FOR REFLEX ANALYSIS...")
        
        prompt = f"ACT AS A SEPSIS AGENT: BP is {row['blood_pressure']} but HRV has dropped to {row['hrv_entropy']}. Analyze the danger."
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b",
        )
        
        print(f"\nAI REFLEX ALERT: {response.choices[0].message.content}")
        print("\n--- MONITORING STOPPED: MEDICAL INTERVENTION REQUIRED ---")
        break # Stops the demo once the sepsis is found
        
    time.sleep(0.5) # Speed it up slightly (0.5s instead of 1s) for the demo