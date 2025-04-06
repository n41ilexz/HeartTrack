import RPi.GPIO as GPIO

MOTOR_PIN = 17  # GPIO-ul conectat la baza tranzistorului
BUZZER_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def vibratteur_on():
    print("Vibrație ON")
    GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Pornire motor
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def vibratteur_off():
    print("Vibrație OFF")
    GPIO.output(MOTOR_PIN, GPIO.LOW)  # Oprire motor
    GPIO.output(BUZZER_PIN, GPIO.LOW)
