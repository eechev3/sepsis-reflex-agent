import pandas as pd
import numpy as np

def create_sepsis_scenario():
    # 1. Create a timeline of 60 seconds
    time = np.arange(0, 60)
    
    # 2. The "Liar" Metric: Blood Pressure stays normal (120)
    bp = [120] * 60 
    
    # 3. The "Truth" Metric: HRV Entropy
    # Healthy (0.9) for first 30s, then "Stiffens" (0.3) at second 30
    hrv = [0.9 if t < 30 else 0.3 for t in time]
    
    # 4. Save to CSV
    df = pd.DataFrame({
        'second': time, 
        'blood_pressure': bp, 
        'hrv_entropy': hrv
    })
    
    df.to_csv("patient_data.csv", index=False)
    print("SUCCESS: 'patient_data.csv' has been created.")

if __name__ == "__main__":
    create_sepsis_scenario()