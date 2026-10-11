# Manufacturing outputs — revision 0.1

These files are exported from the committed PCB for design review and prototype preparation. They are **not an approved production order**: component sourcing and fabricator-specific DFM review remain open.

| Output | Location |
|---|---|
| Copper, mask, silk, paste and outline | [`gerbers/`](gerbers/) |
| Plated / unplated Excellon drills and maps | [`drill/`](drill/) |
| Grouped component values and footprints | [`bom.csv`](bom.csv) |
| Top-side SMD placement | [`assembly/placement.csv`](assembly/placement.csv) |
| Assembly layers | [`assembly/assembly-top.svg`](assembly/assembly-top.svg) |
| Readable reference map | [`../docs/images/component-map.svg`](../docs/images/component-map.svg) |

## Saved board parameters

- Nominal outline: **40 × 28.75 mm**; 1.6 mm thickness.
- Two copper layers; nominal 35 µm copper on each side in the saved stackup.
- Four 2.2 mm NPTH mounting holes.
- Silkscreen is clipped against solder mask during export.
- Drill coordinates use the absolute board origin; placement coordinates use KiCad's exported convention. Placement is top-side SMD only and omits through-hole headers and mechanical holes.
- Paste layers are supplied for stencil review. Surface finish, mask color, tolerances and any controlled-impedance requirements are not specified by this package.

## Assembly release checks

The BOM is a design BOM, not a purchase list. Exact manufacturer part numbers, tolerances, voltage ratings and approved alternates are not populated for all parts. Confirm in particular:

1. U2 manufacturer/variant and C13 effective capacitance/ESR compatibility.
2. Y1 load capacitance, ESR and package pinout against the 10 pF load capacitors.
3. FB1 impedance at its specified frequency, DCR and current capability.
4. USB connector, slide-switch and MCU pin-1 orientation against the selected manufacturer drawings.
5. Placement rotation conventions with the assembly provider; machine exports are not universal feeder instructions.
6. Copper-to-edge, mask slivers, annular rings, drill sizes and board outline in the fabricator's CAM review.

The USB model is a mechanical reference. A 3D fit and a clean DRC do not verify the purchased part or assembled hardware.
