# I2C_LCD_driver.py
import smbus2
import time

LCD_ADDR = 0x27  # modifică dacă ai altă adresă (ex: 0x3f)
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

bus = smbus2.SMBus(1)

def lcd_strobe(data):
    bus.write_byte(LCD_ADDR, data | ENABLE | LCD_BACKLIGHT)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, (data & ~ENABLE) | LCD_BACKLIGHT)
    time.sleep(0.0001)

def lcd_write(bits, mode):
    high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
    bus.write_byte(LCD_ADDR, high)
    lcd_strobe(high)
    bus.write_byte(LCD_ADDR, low)
    lcd_strobe(low)

def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    time.sleep(0.005)

def lcd_message(message, line):
    lcd_write(line, LCD_CMD)
    for char in message.ljust(LCD_WIDTH, " "):
        lcd_write(ord(char), LCD_CHR)
