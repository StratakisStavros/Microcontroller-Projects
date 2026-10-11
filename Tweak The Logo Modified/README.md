# Arduino Sensor Visualization and Logging

An Arduino Uno reads a potentiometer and streams its full 10-bit ADC value to a Processing application. The desktop view maps the reading to a background hue and a percentage gauge; optional CSV logging captures the values for later inspection.

This project extends **Tweak the Logo**, Project 14 in the *Arduino Projects Book*, with full-resolution readings, a gauge, image scaling and switchable data logging.

## Hardware and wiring

| Part / connection | Configuration |
|---|---|
| Board | Arduino Uno or compatible |
| Input | 10 kΩ potentiometer |
| Potentiometer outer terminals | 5 V and GND |
| Potentiometer wiper | A0 |
| Computer connection | USB; serial at 9600 baud |

The Arduino sends one integer (`0`–`1023`) per line, with a 10 ms delay between samples. Processing updates the display when complete lines arrive.

## Run

1. Open [`Arduino_Code/Arduino_Code.ino`](Arduino_Code/Arduino_Code.ino) in the Arduino IDE, select **Arduino Uno** and the board's port, then upload.
2. Open [`Processing/Tweak_The_Logo/Tweak_The_Logo.pde`](Processing/Tweak_The_Logo/Tweak_The_Logo.pde) in Processing's Java mode. The bundled `data/arduino_logo.png` must remain inside that sketch folder.
3. Change the serial-port string `COM3` to the Arduino's actual port. `Serial.list()` can list available ports. Close the Arduino Serial Monitor before starting Processing.
4. Run the sketch and rotate the potentiometer. Press **L** to toggle logging.

`Recording.csv` is created in the Processing sketch directory when the application starts. Starting the application again overwrites that file; save or rename recordings you want to retain. Logging begins disabled.

## Example recording

[`Recording Example.csv`](Recording%20Example.csv) contains a recorded sensor session. Columns are separated by semicolons:

```text
Time(ms);SensorValue;Percentage
9935;215;21
```

`Time(ms)` is elapsed Processing time, `SensorValue` is the ADC reading and `Percentage` is the integer-mapped value from 0 to 100. The data demonstrates the logging format; it is not a calibrated voltage measurement.

## Verification

The corrected Arduino sketch was compiled for `arduino:avr:uno` with Arduino CLI 1.2.0 on 11 October 2026: **1,890 bytes flash and 188 bytes SRAM**. The desktop sketch also compiled successfully in **Processing 4.4.10 Java mode**. Build and file-layout notes are recorded in [`VALIDATION.md`](VALIDATION.md). A fresh live hardware session has not been performed as part of this repository update.

## Software licence

The Arduino and Processing source code was published under the MIT licence in the original repository. That software licensing statement is retained. The Arduino name and logo remain the property of their respective owners.
