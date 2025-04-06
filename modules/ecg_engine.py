import neurokit2 as nk
import numpy as np
import time
from datetime import datetime
import json
import modules.global_variables as gv
import modules.email_sending as email
import modules.vibratteur as vibratteur
import threading

calibrate_signal = nk.ecg_simulate(duration=50, sampling_rate=1000, heart_rate=75)
calibrate_signals, calibrate_info = nk.ecg_process(calibrate_signal)

test_signal = nk.ecg_simulate(duration=50, sampling_rate=1000, heart_rate=75)
test_signals, test_info = nk.ecg_process(test_signal)

baseline_st = 0
baseline_hr = 0
baseline_ppr = 0

def save_anomalies_to_json(anomalies, average_heartrate, average_st, log_file="anomalies_log.json"):
    """
    Salvează anomaliile într-un fișier JSON cu data și ora curentă.

    Parametri:
    - anomalies: Lista cu anomalii detectate
    - average_heartrate: Ritmul cardiac mediu
    - average_st: Valoarea medie a segmentului ST
    - log_file: Numele fișierului JSON în care vor fi salvate anomaliile
    """
    
    # Obținem data și ora curentă
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Creăm entry-ul de log
    log_entry = {
        "timestamp": timestamp,
        "anomalies": anomalies,
        "average_heartrate": average_heartrate,
        "average_st": average_st
    }

    # Citim fișierul JSON existent, dacă există, și adăugăm log-ul
    try:
        with open(log_file, "r") as f:
            log_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = []

    # Adăugăm noul entry la log
    log_data.append(log_entry)

    # Salvăm log-ul înapoi în fișier
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    print(f"Anomalies saved with timestamp: {timestamp}")
def calibrate(signals, info, sampling_rate, calibration_cycles=15):
    start_time = time.time()
    print("=========================================================")
    print("||Incepem calibrarea...")
    print(f"||Cicluri de calibrare: {calibration_cycles}")

    #extragere varfuri
    s_peaks = info["ECG_S_Peaks"]
    t_peaks = info["ECG_T_Peaks"]
    r_peaks = info["ECG_R_Peaks"]
    p_peaks = info["ECG_P_Peaks"]
    #procesare heart rate mediu
    hr = nk.ecg_rate(r_peaks, sampling_rate=sampling_rate)
    baseline_hr = np.mean(hr)  

    ppr = nk.ecg_rate(p_peaks, sampling_rate=sampling_rate)
    baseline_ppr = np.mean(ppr)
    #pre-procesare varfuri
    avg_length = min(len(s_peaks), len(t_peaks))
    s_peaks, t_peaks = s_peaks[:avg_length], t_peaks[:avg_length]

    s_peaks = np.array(s_peaks)
    t_peaks = np.array(t_peaks)
    s_peaks = s_peaks[~np.isnan(s_peaks)].astype(int)
    t_peaks = t_peaks[~np.isnan(t_peaks)].astype(int)

    #calcul final de calibrare
    baseline_values = [(signals["ECG_Clean"][s] + signals["ECG_Clean"][t]) / 2 for s, t in zip(s_peaks[:calibration_cycles], t_peaks[:calibration_cycles])]
    baseline_st = np.mean(baseline_values)

    #statistici
    elapsed_time = time.time() - start_time
    print(f"||Calibrare terminata! Durata: {elapsed_time:.4f} secunde")
    print(f"||Segment ST mediu: {baseline_st:.3f}")
    print(f"||Ritmul cardiac mediu: {baseline_hr:.2f} BPM")
    print(f"||Ritm unde P mediu : {baseline_ppr}")
    print("=========================================================")
    return baseline_st, baseline_hr, baseline_ppr
def anomalies_detection(signals, info, sampling_rate, baseline_st, baseline_hr, baseline_ppr):
    start_time = time.time()
    print("=========================================================")
    s_peaks = np.array(info["ECG_S_Peaks"])
    t_peaks = np.array(info["ECG_T_Peaks"])
    r_peaks = np.array(info["ECG_R_Peaks"])
    p_peaks = np.array(info["ECG_P_Peaks"])
    
    # Curățarea și validarea datelor
    r_peaks = r_peaks[~np.isnan(r_peaks)].astype(int)
    p_peaks = p_peaks[~np.isnan(p_peaks)].astype(int)
    
    # Verificăm dacă avem suficiente date pentru analiză
    if len(r_peaks) < 3 or len(p_peaks) < 3:
        print("||Date insuficiente pentru analiză robustă")
        return ["⚠️ DATE INSUFICIENTE PENTRU ANALIZĂ ROBUSTĂ"], None, None
    
    # Calcul ST mai robust
    st_values = []
    s_peaks = s_peaks[~np.isnan(s_peaks)].astype(int)
    t_peaks = t_peaks[~np.isnan(t_peaks)].astype(int)
    
    # Asigurăm că avem perechi valide S-T
    valid_st_pairs = []
    for s in s_peaks:
        # Găsim cel mai apropiat vârf T după vârful S
        valid_t = [t for t in t_peaks if t > s and t - s < sampling_rate * 0.2]  # Max 200ms între S și T
        if valid_t:
            valid_st_pairs.append((s, min(valid_t)))
    
    for s, t in valid_st_pairs:
        st_value = (signals["ECG_Clean"][s] + signals["ECG_Clean"][t]) / 2
        st_values.append(st_value)
    
    st_medium = np.mean(st_values) if st_values else None
    
    # Calculul HR (heart rate) mai robust folosind medie mediană pentru a reduce influența valorilor extreme
    hr = nk.ecg_rate(r_peaks, sampling_rate)
    avg_hr = np.median(hr) if len(hr) > 0 else None
    
    # Calculul PPR mai robust
    ppr = nk.ecg_rate(p_peaks, sampling_rate) if len(p_peaks) > 1 else np.array([])
    
    # Calculul statisticilor pentru PPR pentru a detecta valori aberante
    if len(ppr) > 0:
        ppr_mean = np.mean(ppr)
        ppr_std = np.std(ppr)
    else:
        ppr_mean = None
        ppr_std = None
    
    # Afișarea valorilor calculate
    if st_medium is not None:
        print(f"||ST mediu: {st_medium:.3f}")
    else:
        print("||Nu s-a putut calcula ST mediu.")
    
    print(f"||HR mediu: {avg_hr:.2f} bpm" if avg_hr is not None else "||Nu s-a putut calcula HR")
    
    anomalies = []
    aritmie = False
    
    # Algoritm îmbunătățit pentru detectarea extrasistolelor cu praguri adaptative
    # Utilizăm deviația standard pentru a defini pragurile în loc de valori fixe
    if ppr_mean is not None and ppr_std is not None and len(ppr) >= 3:
        # Definim praguri adaptative bazate pe deviația standard
        lower_threshold = max(baseline_ppr - 3 * ppr_std, baseline_ppr * 0.6)  # Minim 60% din baseline
        upper_threshold = min(baseline_ppr + 3 * ppr_std, baseline_ppr * 1.4)  # Maxim 140% din baseline
        
        # Identificăm secvențe de 3 valori consecutive pentru a confirma anomaliile
        for index in range(1, len(ppr) - 1):
            current_value = ppr[index]
            prev_value = ppr[index - 1]
            next_value = ppr[index + 1]
            
            # Verificăm pattern-ul specific extrasistolei: scădere-vârf-scădere sau vârf-scădere-vârf
            if ((prev_value < lower_threshold and current_value > upper_threshold) or 
                (current_value < lower_threshold and (prev_value > upper_threshold or next_value > upper_threshold))):
                
                # Verificăm și magnitudinea schimbării (>40% diferență între valori consecutive)
                if (abs(current_value - prev_value) / prev_value > 0.4 or 
                    abs(current_value - next_value) / next_value > 0.4):
                    print(f"ARITMIE/EXTRASISTOLA POSIBILA la index {index} (val: {current_value:.1f}, prev: {prev_value:.1f}, next: {next_value:.1f})")
                    aritmie = True
    
    if aritmie:
        anomalies.append("⚠️ EXTRASISTOLĂ/ARITMIE POSIBILĂ!")
    
    # Verificarea valorilor HR și ST pentru alte anomalii
    if avg_hr is not None:
        if avg_hr < baseline_hr - 20 or avg_hr < 60:
            print("||⚠️ PULS SCAZUT SEMNIFICATIV! EVITAȚI ANALIZA ST.")
        
        if st_medium is not None and st_medium > baseline_st + 4 and avg_hr >= 60: 
            print("||‼️ SEGMENT ST ELEVAT! POSIBIL INFARCT!")
            anomalies.append("‼️ SEGMENT ST ELEVAT! POSIBIL INFARCT!")
        
        if avg_hr > baseline_hr + 20 or avg_hr > 100:
            if avg_hr >= 120:
                print("||‼️ PULS FOARTE ELEVAT! POSIBILĂ TAHICARDIE!")
                anomalies.append("‼️ PULS FOARTE ELEVAT! POSIBILĂ TAHICARDIE!")
            elif avg_hr >= 100:
                print("||⚠️ PULS ELEVAT! POSIBILĂ TAHICARDIE!")
                anomalies.append("⚠️ PULS ELEVAT! POSIBILĂ TAHICARDIE!")
        elif avg_hr < baseline_hr - 10 or avg_hr < 60:
            if avg_hr <= 40:
                print(f"||‼️ PULS FOARTE SCAZUT! CONTACTATI UN MEDIC! |{avg_hr:.1f} BPM|")
                anomalies.append("‼️ PULS FOARTE SCAZUT! CONTACTATI UN MEDIC!")
            elif avg_hr <= 60:
                print(f"||⚠️ PULS SCAZUT! POSIBILĂ BRADICARDIE! |{avg_hr:.1f} BPM|")
                anomalies.append("⚠️ PULS SCAZUT! POSIBILĂ BRADICARDIE!")
    
    elapsed_time = time.time() - start_time
    print(f"||Durata analiza : {elapsed_time:.3f}s")
    print("=========================================================")
    return anomalies, avg_hr, st_medium
calibrate(calibrate_signals, calibrate_info, 1000, 500)

def main():
    try:
        global calibrate_signals, calibrate_info, baseline_st, baseline_hr, baseline_ppr, ispressed, iscalibrated
        while True:
            anomalies, average_heartrate, average_st = anomalies_detection(calibrate_signals, calibrate_info, 1000, baseline_st, baseline_hr, baseline_ppr)
            if len(anomalies) > 0:
                print("||ANOMALII DETECTATE:")
                vibratteur.vibratteur_on()
                time.sleep(1)
                vibratteur.vibratteur_off()
                for anomaly in anomalies:
                    print(f"||{anomaly}")
                    email.send_email(anomaly)
                print("=========================================================")
            else:
                print("||Nu sunt anomalii detectate.")
    except KeyboardInterrupt:
        vibratteur.vibratteur_off()

gv.ECG_SIGNAL = test_signal
main_thread = threading.Thread(target=main, daemon=True)
main_thread.start()