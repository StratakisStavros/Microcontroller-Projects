# CAD verification

Revision 0.1 was checked with **KiCad 9.0.6 on 11 October 2026**.

| Check | Result | Evidence |
|---|---|---|
| Schematic electrical rules | 0 violations | [`erc.json`](erc.json) |
| PCB design rules | 0 violations | [`drc.json`](drc.json) |
| Unconnected PCB items | 0 | [`drc.json`](drc.json) |
| Schematic / PCB parity | 0 issues | [`drc.json`](drc.json) |
| Source identity | SHA-256 manifest | [`source-sha256.txt`](source-sha256.txt) |

The checks use the committed project settings and project-local footprint variants. No ERC or DRC exclusions were added. Rules intentionally disabled in the project are not evaluated; a clean report is not a substitute for a fabrication or electrical design review.

Selected saved constraints: 0.20 mm minimum track width and copper clearance; 0.30 mm minimum through-hole drill; 0.70 mm minimum via diameter; 0.13 mm minimum annular width; 0.80 mm minimum silkscreen text height and 0.08 mm stroke. The saved minimum copper-to-edge and silk clearance values are 0 mm, so fabricator-specific edge/mask constraints still require review.

## Changes made for the documented revision

The incoming PCB had no unconnected items or parity errors, but reported 55 warnings: 50 text-size/stroke warnings, two edge/silkscreen warnings, one silkscreen/mask warning, one duplicate drilled via and one library-footprint mismatch. The documented copy:

- removes the duplicate 3.3 V via;
- moves the undersized references to F.Fab and enlarges them for assembly documentation;
- moves the two USB outline segments that crossed the edge onto F.Fab;
- records the intended USB/switch footprint variants locally;
- gives the project consistent names and portable model paths.

The circuit net connections and component values are unchanged. The original working files are retained outside this published package.

## Reproduce

From the project directory:

```sh
kicad-cli sch erc --format json --exit-code-violations -o validation/erc.json hardware/stm32-i2c-board.kicad_sch
kicad-cli pcb drc --schematic-parity --format json --exit-code-violations -o validation/drc.json hardware/stm32-i2c-board.kicad_pcb
```

Alternatively run [`scripts/export.py`](../scripts/export.py), which performs the checks before regenerating exports and a checksum manifest.

**Physical validation:** assembly, rail measurements, SWD access, UART, I²C and USB operation have not been verified. Their acceptance steps are defined in the [bring-up plan](../docs/bring-up.md).
