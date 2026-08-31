# 🔐 SMART ACCESS SYSTEM

A smart RFID-based access control system simulated using **Raspberry Pi Pico on Wokwi** and programmed with **MicroPython**.

## 🔗 Project Simulation

**Wokwi Simulation:**
https://wokwi.com/projects/473783904082108417

## 📌 Project Overview

This project simulates a smart access control system using an RFID reader to identify authorized users.

When an RFID card is scanned, the system checks its UID against a predefined list of registered users.

* 🟢 **Authorized Card:** The user's name and role are displayed on the LCD, the green LED turns ON, and the servo motor rotates to simulate unlocking the door.
* 🔴 **Unauthorized Card:** The red LED turns ON and access is rejected.
* 🚨 **Three Failed Attempts:** The system displays "Access Denied!" and activates the buzzer as an alarm.

## 🖥️ Simulation Environment

The complete project was designed and tested using:

* **Wokwi Simulator**
* **Raspberry Pi Pico**
* **MicroPython**

The project is currently implemented as a simulation and was not tested on physical hardware.

## 🧰 Components

* Raspberry Pi Pico
* MFRC522 RFID Reader
* RFID Cards
* 16×2 I2C LCD
* Servo Motor
* Green LED
* Red LED
* Buzzer
* Resistors
* Breadboard

## 📡 Communication Protocols

### I2C

Used to communicate between the Raspberry Pi Pico and the 16×2 LCD.

### SPI

Used to communicate between the Raspberry Pi Pico and the MFRC522 RFID reader.

### PWM

Used to control the buzzer.

## 🔌 Pin Configuration

| Component | Pico GPIO |
| --------- | --------: |
| LCD SDA   |   GPIO 20 |
| LCD SCL   |   GPIO 21 |
| RFID SCK  |    GPIO 2 |
| RFID MOSI |    GPIO 3 |
| RFID MISO |    GPIO 4 |
| RFID CS   |    GPIO 1 |
| RFID RST  |    GPIO 0 |
| Servo     |   GPIO 16 |
| Buzzer    |   GPIO 19 |
| Red LED   |   GPIO 10 |
| Green LED |   GPIO 11 |

## ⚙️ System Workflow

```text
Start
  ↓
System Ready
  ↓
Scan RFID Card
  ↓
Read UID
  ↓
Check Registered Users
  ↓
 ┌───────────────┐
 │               │
YES              NO
 │               │
 ▼               ▼
Green LED       Red LED
ON              ON
 │               │
 ▼               ▼
Display Name    Failed Attempt +1
and Role         │
 │               ▼
 ▼          3 Attempts?
Servo Unlock      │
 │          ┌─────┴─────┐
 ▼         NO          YES
Wait 3 sec              │
 │                      ▼
 ▼                   Buzzer
Servo Lock           Alarm
 │                      │
 └──────────┬───────────┘
            ▼
      Continue Scanning
```

## 👥 Registered Users

The current simulation contains predefined users with different roles:

| Name  | Role     |
| ----- | -------- |
| Ahmed | Employee |
| Sara  | Manager  |
| Omar  | Employee |
| Menna | Admin    |

## 📚 Libraries Used

```python
from machine import I2C, Pin, SPI, PWM
from DIYables_MicroPython_LCD_I2C import LCD_I2C
from time import sleep
from mfrc522 import MFRC522
from servo import Servo
```

* `machine` → GPIO, I2C, SPI, and PWM hardware interfaces
* `DIYables_MicroPython_LCD_I2C` → LCD control
* `mfrc522` → RFID reader communication
* `servo` → Servo motor control
* `time` → Timing and delays

## 🚀 Future Improvements

* Add an administrator mode to register new RFID cards.
* Add a keypad for PIN-based authentication.
* Store user data in external memory.
* Add date and time logging for every access attempt.
* Add Wi-Fi connectivity.
* Send notifications after multiple failed attempts.
* Implement the system on physical Raspberry Pi Pico hardware.

## 🎯 Project Goal

The goal of this project is to practice **MicroPython, Raspberry Pi Pico, RFID communication, I2C, SPI, PWM, GPIO control, and embedded-system design** through a practical access-control application.

## 🛠️ Technologies

**Raspberry Pi Pico | MicroPython | Wokwi | RFID | MFRC522 | I2C | SPI | PWM | Embedded Systems**

---

### 🔗 Wokwi Project

**Run the simulation:**
https://wokwi.com/projects/473783904082108417
