# Validation notes

Checked on 11 October 2026.

| Item | Result |
|---|---|
| Arduino source | Removed the accidental duplicate opening `setup()` declaration |
| Arduino Uno build | Arduino CLI 1.2.0, Arduino AVR Boards 1.8.6, target `arduino:avr:uno`: pass |
| Flash usage | 1,890 / 32,256 bytes |
| Static SRAM usage | 188 / 2,048 bytes |
| Processing file layout | Main `.pde` name matches its sketch folder; logo is in its local `data/` directory |
| Processing compilation | Processing 4.4.10 Java mode: pass (`Finished.`) |
| Example CSV | Existing recording retained; semicolon-delimited format documented |
| Live hardware / serial session | Not repeated in this update |

The Processing application uses a configured serial port and opens a new `Recording.csv` on startup. The source and README document that behavior; actual serial operation requires an attached board.

To repeat the Arduino compile, use Arduino CLI with the Arduino AVR core installed:

```sh
arduino-cli compile --fqbn arduino:avr:uno Arduino_Code
```
