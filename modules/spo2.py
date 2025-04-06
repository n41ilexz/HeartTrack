import modules.max30102.max30102 as max30102
import modules.max30102.hrcalc as hrcalc
import threading
import time

m = None

sensor_found = False
cnt = 0
while sensor_found == False:
    try:
        m = max30102.MAX30102()
        sensor_found = True
    except IOError as e:
        cnt+=1
        print(f"Senzor nedetectat. Reincercare! | {cnt}")
        time.sleep(1)
        pass

def read_sensor():
        while True:
            # Read data from the sensor
            red, ir = m.read_sequential()
            # Calculate heart rate and SpO2
            hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)

            #  Check if valid readings are obtained
            # if hr_valid and spo2_valid:
            #     print("Heart Rate: ", hr, "BPM")
            #     print("SpO2 Level: ", spo2, "%")
            # else:
            #     print("Invalid readings. Please try again.")
            return hr, hr_valid, spo2, spo2_valid


if __name__ == "__main__":
    sensor_thread = threading.Thread(target=read_sensor, daemon=True)
    sensor_thread.start()
    hr, hr_valid, spo2, spo2_valid = read_sensor()
    if hr_valid and spo2_valid:
        print("Heart Rate: ", hr, "BPM")
        print("SpO2 Level: ", spo2, "%")
    else:
        print("Invalid readings. Please try again.")