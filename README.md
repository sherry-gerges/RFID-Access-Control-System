# 🔐 RFID Access Control System

A smart **RFID-based access control system** built using a **Raspberry Pi Pico**. The system identifies users through RFID cards, displays their information on an I2C LCD, controls access using a servo motor, and provides visual and audio alerts for unauthorized access attempts.

## 📌 Project Overview

This project is designed as a simple smart access-control system for environments such as offices, labs, classrooms, or restricted areas.

When an RFID card is scanned:

* ✅ If the card is registered, the user's **name and role** are displayed.
* 🟢 The green LED turns ON.
* 🚪 The servo motor rotates to simulate **unlocking the door**.
* After a few seconds, the system returns to the locked state.
* ❌ If the card is not registered, access is rejected.
* 🔴 The red LED turns ON.
* After **3 consecutive failed attempts**, the system activates a buzzer and displays **"Access Denied!"**.

---

## ✨ Features

* RFID card identification
* User authentication using stored RFID IDs
* User name and role display
* Servo-controlled door simulation
* Green LED for authorized access
* Red LED for unauthorized access
* Failed-attempt counter
* Buzzer alarm after 3 failed attempts
* 16×2 I2C LCD interface
* SPI communication with the RFID reader
* Implemented using MicroPython

---

## 🧰 Components

| Component           | Purpose                                     |
| ------------------- | ------------------------------------------- |
| Raspberry Pi Pico   | Main microcontroller                        |
| MFRC522 RFID Reader | Reads RFID cards                            |
| RFID Cards/Tags     | User identification                         |
| 16×2 I2C LCD        | Displays system status and user information |
| Servo Motor         | Simulates door locking/unlocking            |
| Green LED           | Indicates authorized access                 |
| Red LED             | Indicates unauthorized access               |
| Buzzer              | Security alarm                              |
| Resistors           | LED current limiting                        |
| Breadboard          | Circuit assembly                            |
| Jumper Wires        | Connections                                 |

---

## 🔌 Pin Connections

### LCD – I2C

| LCD | Raspberry Pi Pico |
| --- | ----------------- |
| SDA | GPIO 20           |
| SCL | GPIO 21           |

I2C Address:

```text
0x27
```

### MFRC522 – SPI

| MFRC522     | Raspberry Pi Pico |
| ----------- | ----------------- |
| SCK         | GPIO 2            |
| MOSI        | GPIO 3            |
| MISO        | GPIO 4            |
| SDA/SS (CS) | GPIO 1            |
| RST         | GPIO 0            |

### Other Components

| Component   |    GPIO |
| ----------- | ------: |
| Servo Motor | GPIO 16 |
| Buzzer      | GPIO 19 |
| Red LED     | GPIO 10 |
| Green LED   | GPIO 11 |

---

## 🧠 System Logic

The system starts by displaying:

```text
System Ready!
```

Then it asks the user to scan an RFID card:

```text
Bring a card ...
```

### 1. RFID Detection

The MFRC522 continuously checks for an RFID card.

When a card is detected, its UID is read and converted into a string.

### 2. User Authentication

The UID is compared with the registered users stored in the `USERS` dictionary.

Example:

```python
USERS = {
    "85102119136": {"name": "Ahmed", "role": "Employee"},
    "1234": {"name": "Sara", "role": "Manager"},
    "17345168": {"name": "Omar", "role": "Employee"},
    "170187204221": {"name": "Menna", "role": "Admin"},
}
```

### 3. Authorized Card

If the UID exists in the database:

```text
Name:Ahmed
Role:Employee
```

The system then:

1. Turns ON the green LED.
2. Displays the user's information.
3. Rotates the servo to simulate unlocking.
4. Keeps the door unlocked for 3 seconds.
5. Turns OFF the green LED.
6. Returns the servo to the locked position.

### 4. Unauthorized Card

If the UID is not registered:

```text
Not Registed
```

The system:

1. Increments the failed-attempt counter.
2. Turns ON the red LED.
3. Rejects access.

### 5. Three Failed Attempts

After three unauthorized attempts:

```text
Not Registed
Access Denied!
```

The buzzer is activated for 3 seconds.

After the alarm, the failed-attempt counter is reset:

```python
failed_attempts = 0
```

---

## 🔄 System Flow

```text
              ┌─────────────────┐
              │  System Starts  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Scan RFID Card │
              └────────┬────────┘
                       │
                       ▼
                ┌─────────────┐
                │ Read RFID UID│
                └──────┬──────┘
                       │
                 ┌─────▼─────┐
                 │ Registered?│
                 └──┬─────┬──┘
                  YES│     │NO
                     │     │
          ┌──────────▼─┐  ┌▼──────────────┐
          │ Green LED  │  │   Red LED     │
          │    ON      │  │      ON       │
          └──────┬─────┘  └──────┬────────┘
                 │               │
                 ▼               ▼
          ┌─────────────┐  ┌──────────────┐
          │Display Name │  │ Failed +1    │
          │ and Role    │  └──────┬───────┘
          └──────┬──────┘         │
                 │          ┌──────▼──────┐
                 │          │ Attempts=3? │
                 │          └───┬────┬────┘
                 │            NO│    │YES
                 │               │    │
                 │               │    ▼
                 │               │  ┌────────┐
                 │               │  │ Buzzer │
                 │               │  │  ON    │
                 │               │  └───┬────┘
                 │               │      │
                 ▼               ▼      ▼
          ┌────────────────────────────────┐
          │       Return to Monitoring     │
          └────────────────────────────────┘
```

---

## 📚 Libraries Used

### `machine`

Used to interface with Raspberry Pi Pico hardware.

```python
from machine import I2C, Pin
from machine import SPI
from machine import PWM
```

* `I2C` → LCD communication
* `SPI` → MFRC522 communication
* `Pin` → LEDs and GPIO control
* `PWM` → Buzzer control

### `DIYables_MicroPython_LCD_I2C`

Used to control the 16×2 I2C LCD.

```python
from DIYables_MicroPython_LCD_I2C import LCD_I2C
```

### `mfrc522`

Used to communicate with the MFRC522 RFID reader and read RFID card UIDs.

```python
from mfrc522 import MFRC522
```

### `servo`

Used to control the servo motor.

```python
from servo import Servo
```

### `time`

Used to create delays between system operations.

```python
from time import sleep
```

---

## 🛠️ How to Run

1. Connect the components according to the pin configuration.
2. Install MicroPython on the Raspberry Pi Pico.
3. Add the required libraries to the Pico:

   * `mfrc522.py`
   * `servo.py`
   * `DIYables_MicroPython_LCD_I2C.py`
4. Upload the main Python program.
5. Power the Raspberry Pi Pico.
6. Scan an RFID card.
7. The system will authenticate the card and control access accordingly.

---

## 🔒 Security Logic

The system uses a simple authentication mechanism based on the RFID card UID.

Registered cards are stored in a dictionary:

```python
USERS = {
    "RFID_UID": {
        "name": "User Name",
        "role": "User Role"
    }
}
```

The failed-attempt mechanism adds an additional security layer by triggering an alarm after three unauthorized scans.

> **Note:** This is an educational prototype. In a real access-control system, RFID UIDs alone should not be considered sufficient for high-security authentication.

---

## 🚀 Possible Future Improvements

* Add a real electronic door lock or solenoid
* Store users in external EEPROM, SD card, or database
* Add an administrator mode for registering new cards
* Add a keypad for PIN authentication
* Add an RTC module to record access time
* Store access logs
* Add Wi-Fi connectivity using ESP32 or another network-enabled board
* Send notifications when multiple failed attempts occur
* Add OLED or larger display
* Implement multiple levels of access based on user roles

---

## 🎯 Applications

This project can be adapted for:

* 🏢 Office access control
* 🧪 Laboratory security
* 🏫 School or university rooms
* 🏠 Smart home entrances
* 🗄️ Restricted storage areas
* 🔐 Educational IoT and embedded-systems projects

---

## 👩‍💻 Technologies

* **Microcontroller:** Raspberry Pi Pico
* **Programming Language:** MicroPython
* **Communication:** I2C & SPI
* **RFID:** MFRC522
* **Display:** 16×2 I2C LCD
* **Actuator:** Servo Motor
* **Alert System:** Buzzer + LEDs

---

## 📄 License

This project is intended for educational and learning purposes.
