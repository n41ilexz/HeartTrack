import modules.spo2 as sensor
import threading
import modules.LCD_driver.I2C_LCD_driver as lcd
import time
import RPi.GPIO as GPIO
import modules.global_variables as gv

# Configurare GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RB_PIN = 13
LB_PIN = 6

GPIO.setup(RB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Inițializări globale
spo2_value = 0
hr_value = 0
screen_mode = "HR"  # HR sau SPO2

lcd.lcd_init()

pressed_state = gv.DUAL_PRESSED_STATE

def listen_buttons():
    def _listener():
        global screen_mode, pressed_state
        last_rb = GPIO.input(RB_PIN)
        last_lb = GPIO.input(LB_PIN)

        while True:
            current_rb = GPIO.input(RB_PIN)
            current_lb = GPIO.input(LB_PIN)

            # Ambele butoane apăsate
            if current_rb == GPIO.LOW and current_lb == GPIO.LOW:
                pressed_state = True
                print(f"Stare ambele butoane: {pressed_state}")
            else:
                pressed_state = False

            # Comutare între HR și SPO2
            if last_rb == GPIO.HIGH and current_rb == GPIO.LOW:
                screen_mode = "HR"
                print("Comutat la HR")

            elif last_lb == GPIO.HIGH and current_lb == GPIO.LOW:
                screen_mode = "SPO2"
                print("Comutat la SPO2")

            last_rb = current_rb
            last_lb = current_lb
            time.sleep(0.05)

    thread = threading.Thread(target=_listener, daemon=True)
    thread.start()

def get_sensor_data():
    global hr_value, spo2_value
    while True:
        try:
            hr, hr_valid, spo2, spo2_valid = sensor.read_sensor()
            if hr_valid and spo2_valid:
                hr_value = hr
                spo2_value = spo2
                print(f"HR: {hr} BPM, SpO2: {spo2}%")
            time.sleep(1)
        except IOError:
            print("Eroare senzor. Reîncerc...")
            time.sleep(1)

def display_loop():
    while True:
        try:
            lcd.lcd_message("=====HTK-V1======", lcd.LCD_LINE_1)
            if screen_mode == "HR":
                lcd.lcd_message(f"HR: {hr_value:.2f} BPM", lcd.LCD_LINE_2)
            elif screen_mode == "SPO2":
                lcd.lcd_message(f"SPO2: {spo2_value:.2f}%", lcd.LCD_LINE_2)
        except OSError:
            print("Eroare LCD")
        time.sleep(1)

# Pornește thread-urile
listen_buttons()

threading.Thread(target=get_sensor_data, daemon=True).start()
threading.Thread(target=display_loop, daemon=True).start()

# Main loop
