from machine import I2C, Pin
from machine import SPI
from machine import PWM
from DIYables_MicroPython_LCD_I2C import LCD_I2C
from time import sleep
from mfrc522 import MFRC522
from servo import Servo 


I2C_ADDR = 0x27  
LCD_ROWS = 2
LCD_COLS = 16


i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
lcd = LCD_I2C(i2c, I2C_ADDR, LCD_ROWS, LCD_COLS)
buzzer = PWM(Pin(19))
red_led = Pin(10, Pin.OUT)
green_led = Pin(11, Pin.OUT)
servo=Servo(pin=16)


spi = SPI(
    0,
    baudrate=100000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(4),
)

RST_PIN = 0
CS_PIN = 1

rfid = MFRC522(spi, RST_PIN, CS_PIN, 2)

USERS = {
    "85102119136": {"name": "Ahmed", "role": "Employee"},
    "1234": {"name": "Sara", "role": "Manager"},
    "17345168": {"name": "Omar", "role": "Employee"},
    "170187204221": {"name": "Menna", "role": "Admin"},
}

failed_attempts = 0

lcd.move_to(0, 0)
lcd.putstr("System Ready!")
sleep(2)
lcd.clear()
lcd.putstr("Bring a card ...")

while True:
   
    (stat, tag_type) = rfid.request(rfid.PICC_REQIDL)
    if stat == rfid.OK:
        (stat, uid) = rfid.anticoll()
        if stat == rfid.OK:
            card_id = "".join([str(x) for x in uid])

            if card_id in USERS:
                user = USERS[card_id]
                lcd.clear()
                green_led.on()
                lcd.move_to(0, 0)
                lcd.putstr("Name:" + user["name"][:11])

                lcd.move_to(0, 1)
                lcd.putstr("Role:" + user["role"][:11])
                servo.move(180)
                sleep(3)
    
                lcd.clear()
                green_led.off()
                servo.move(0)
        
            else:
                failed_attempts += 1

                red_led.on()
                lcd.clear()
                lcd.putstr("Not Registed")

                if failed_attempts >= 3:
                   lcd.move_to(0, 1)
                   lcd.putstr("Access Denied!")
                   buzzer.freq(440)
                   buzzer.duty_u16(32768)
                   sleep(3)
                   buzzer.duty_u16(0)
        
                   failed_attempts = 0  
                else:
                   sleep(3)
        
                   lcd.clear()
                   red_led.off()
            

            sleep(0.5)

    sleep(0.5)






