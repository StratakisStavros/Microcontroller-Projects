# Interfaces and connection guide

All header pin numbers below come from the schematic netlist. Pin 1 is the square PCB pad; use the [component map](images/component-map.svg) and [top copper drawing](images/layout-top.svg) to establish orientation. Header labels identify interfaces, but individual signal names are not printed on the board.

## J4 — I²C sensor interface

| Pin | Net | MCU pin | Role |
|---|---|---|---|
| 1 | +3.3V | — | Sensor supply from the board |
| 2 | I2C2_SCL | PB10, package pin 21 | I²C2 clock |
| 3 | I2C2_SDA | PB11, package pin 22 | I²C2 data |
| 4 | GND | — | Common reference |

R4 and R5 each provide a 1.5 kΩ pull-up to 3.3 V. Use a 3.3 V peripheral and account for any additional pull-ups on its breakout board. There is no 5 V↔3.3 V level translator. Do not connect a 5 V-pulled-up bus as though this were an Arduino UNO level-shifter board.

## J2 — SWD programming and debug

| Pin | Signal | MCU pin |
|---|---|---|
| 1 | +3.3V / target voltage reference | — |
| 2 | SWDIO | PA13, package pin 34 |
| 3 | SWCLK | PA14, package pin 37 |
| 4 | GND | — |

Power the board from USB VBUS and use pin 1 as the debugger's target-voltage reference. It is directly connected to the 3.3 V rail: verify the probe pinout and avoid connecting an enabled probe power output to it. NRST is not on J2, so connect-under-reset is not available through this four-pin header.

## J3 — UART

| Pin | Signal | MCU pin | Connect to adapter |
|---|---|---|---|
| 1 | +3.3V | — | Usually leave adapter VCC disconnected |
| 2 | USART1_TX | PB6, package pin 42 | RX |
| 3 | USART1_RX | PB7, package pin 43 | TX |
| 4 | GND | — | GND |

Use a USB-UART adapter with 3.3 V logic. Firmware must enable **USART1 remapping to PB6/PB7**; the default PA9/PA10 signals are not connected to J3. This connector is an application UART, not a verified ROM-bootloader programming interface.

## J1 — USB Micro-B

| Pin | Connection |
|---|---|
| 1 | VBUS → regulator input and C12 |
| 2 | USB D− → PA11 |
| 3 | USB D+ → PA12; R2 = 1.5 kΩ to 3.3 V |
| 4 | ID, intentionally unconnected |
| 5 | GND |
| Shield | Electrically unconnected in this revision |

USB data operation needs firmware and a valid 48 MHz USB clock. A lit power LED alone does not demonstrate USB enumeration. No external USB ESD protection or input fuse is fitted.

## SW1 — BOOT0 selection

SW1 connects BOOT0 through R1 (10 kΩ) to GND or +3.3 V. Set BOOT0 low for normal user-flash boot. Confirm switch continuity before first power-up; the board does not label the two switch positions. PB2/BOOT1 is not externally strapped, and the UART header uses remapped pins, so BOOT0 high is not a documented programming workflow for this revision. Use SWD.

Peripheral mapping and boot behavior should be read alongside ST's [STM32F103x8/xB datasheet](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf) and [RM0008 reference manual](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf).
