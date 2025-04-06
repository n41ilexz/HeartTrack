import modules.vibratteur as vibratteur
import modules.LCD_driver.I2C_LCD_driver as lcd

vibratteur.vibratteur_on()
lcd.lcd_init()
lcd.lcd_message("=====HTK-V1=====", lcd.LCD_LINE_1)
lcd.lcd_message("==INITIALIZARE==", lcd.LCD_LINE_2)

import time
import sys
import modules.ecg_engine
import modules.lcdder
import modules.oledder_graph

vibratteur.vibratteur_off()
try:
    while True:
        pass
except KeyboardInterrupt:
    vibratteur.vibratteur_off()
    sys.exit()
    print("===APARAT OPRIIT===")