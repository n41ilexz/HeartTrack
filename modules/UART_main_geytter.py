import serial

port='/dev/ttyS0'
baudrate=115200
timeout=0.1

ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

def get_ekg():
    try:
        print(ser.readline().decode('utf-8', errors='ignore').strip())
        return ser.readline().decode('utf-8', errors='ignore').strip()
    except Exception as e:
        print("Eroare citire serial:", e)
        return None
    
if __name__ == "__main__":
    while True:
        get_ekg()