# Prototype bring-up and verification plan

**Execution status: not performed.** This is the procedure for a future assembled prototype. The published ERC/DRC reports cover CAD checks only.

Use the [pinout](interfaces.md) throughout. Record board revision, fitted part numbers, supply settings, debugger version and firmware commit with the results. Use current-limited 5 V power through a USB breakout for initial bring-up, before connecting a computer USB port.

| Step | Procedure | Acceptance / evidence to record |
|---|---|---|
| 1. Inspection | Check MCU pin 1, regulator orientation, USB solder joints, crystal and passives against the assembly map. | No bridges, reversed components or missing parts; top/bottom photographs. |
| 2. Unpowered checks | Measure VBUS–GND and 3.3 V–GND resistance; check common ground, header mapping and SW1 continuity. | No persistent low-resistance short after capacitors settle; readings recorded. BOOT0 low for flash boot. |
| 3. Controlled power | Apply nominal 5 V with a conservative current limit; observe current and component temperature. Stop on an unexpected current-limit condition. | Stable VBUS, +3.3 V and +3.3VA; first target 3.3 V ±5%, then compare to selected part specifications. |
| 4. Debug access | Connect 3.3 V reference, GND, SWDIO and SWCLK using J2. Read the MCU device ID through SWD. | Stable target detection; tool log and connection details. No external drive onto the regulator output. |
| 5. Clock | Run a minimal program from the internal clock first, then enable the 16 MHz crystal. | Reliable HSE startup and documented clock configuration. Avoid loading crystal pins with unsuitable probes. |
| 6. UART | Configure USART1 remap to PB6/PB7 and transmit a repeating message through J3. | Correct baud rate, clean text and captured serial log. |
| 7. I²C idle | Leave the sensor disconnected; measure SDA and SCL at J4. | Both idle near 3.3 V. Inspect rise time with a scope when available. |
| 8. I²C transaction | Attach a known 3.3 V sensor; start at 100 kHz, read its expected identity register and repeat reads. | Expected address/identity, ACKs and error counts in a saved log. Record pull-ups and cable length. |
| 9. USB | Build firmware with a valid 48 MHz USB clock and a USB device implementation. | Enumeration and repeat reconnect/reset tests on a host; captured descriptors/log. |
| 10. Load/thermal | Test the intended total rail load and ambient conditions. | Rail regulation, ripple, current and regulator temperature documented; define a supported load only after this test. |

Use an oscilloscope for regulator stability, transient response and bus timing. A multimeter alone cannot establish those results. USB signal integrity, ESD and compliance are outside this initial functional plan.

For each executed test, save: test ID, expected result, measured result, instrument/settings, firmware version, pass/fail and the raw evidence file. Leave a test unexecuted when the evidence is unavailable; do not infer a pass from schematic correctness.
