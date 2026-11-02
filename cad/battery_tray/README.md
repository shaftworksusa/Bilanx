# PC545 on its side in the OEM S2000 tray: clamp cap with EPS mount

![preview](preview.png)

The **Odyssey PC545** (spec 7.00 × 3.38 × 5.17 in, which is 177.8 × 85.9 × 131.3 mm; measured 130 mm across on the car) lies **on its side, directly in the OEM S2000 battery tray** in the engine bay. Odyssey rates it for any mounting orientation. No cradle is used: the OEM tray locates the battery.

There's one printed part, the **clamp cap**. Its underside is shaped to the battery: a pocket with 0.75 mm clearance and rounded corners, plus a 15 mm skirt that wraps the battery's top edges so the cap can't slide. The OEM J-hooks pull it down, and the **EPS module (Showa 39980-S2A-A01)** bolts on top of it.

The geometry is parametric and lives in [`battery_tray.py`](battery_tray.py). Run `pip install cadquery`, then `python3 battery_tray.py`, to regenerate `out/clamp_plate.stl` and `out/assembly.step`.

## Status
- **EPS mount: done.**
  - Hole pattern measured at **115 × 30 mm**.
  - The module is rotated 90° with its connectors along the battery length, and shifted 15 mm toward the fender end.
  - **Four M6 heat-set inserts** sit flush in the deck, and the module **sits flat on the plate**. Each hole is 8.0 mm across and 14 mm deep. They're blind, with a 2 mm floor, so a bolt can never reach the battery.
  - The deck is 16 mm thick to hold the full-length inserts. The J-hook slots have 22 mm-wide, 8 mm-deep recesses, so the hook nuts sit at the same height as on a thin plate.
  - Settings: `EPS_ROTATE`, `EPS_CONNECTORS`, `EPS_SHIFT`.
- **J-hooks: done.**
  - The OEM hooks run straight up past the battery's front and back faces. The slots are 132 mm apart and the battery is 130 mm across.
  - The plate's hook holes are 8 mm slots across the width, centred on the battery's length (`JHOOK_SPACING`, `JHOOK_X`).
- **Cap:** 187.3 × 164 × 31 mm (16 mm deck plus 15 mm skirt).
  - The skirt has 24 mm notches where the J-hooks run down the battery faces.
  - The top deck overhangs front and back so it can reach the hooks.
  - The top is flat, with no ribs, because the skirt stiffens the cap.

## Hardware
- **Hold-down:** OEM J-hooks with nyloc nuts and large washers on top of the plate
- **EPS module:**
  - 4 × M6 heat-set inserts, M6 × 12.7 mm (hole sized at 8.0 mm; check your insert's datasheet and adjust `INSERT_D` if needed).
  - 4 × M6 bolts with washers. Choose a length equal to the EPS flange thickness plus washer plus 10–12 mm of thread. Don't go longer, because the blind hole is 14 mm deep.
  - A drop of medium threadlocker, or a spring washer, since the bolts see engine vibration.
- **Pad (optional):** a 1 mm rubber or neoprene pad inside the cap. The pocket has 0.75 mm clearance per side, so add a pad only to the top face, not the walls.

## Printing (PA6-CF, 0.6 mm hardened nozzle)
**File:** [`out/clamp_plate_PRINT.step`](out/clamp_plate_PRINT.step), already oriented top-face-down and centred on Z = 0. Import it as-is and don't rotate it. `out/clamp_plate_PRINT.stl` is the same part, and `out/clamp_plate.step` is the as-installed orientation for CAD.

| Setting | Value |
|---|---|
| Nozzle | 0.6 mm **hardened** steel / ruby (CF wears brass quickly) |
| Line width | 0.65 mm (outer 0.62) |
| Layer height | 0.25–0.30 mm (first layer 0.30) |
| Walls | 4 (~2.6 mm) |
| Top / bottom | 5 / 4 layers |
| Infill | 40% gyroid. Add a **100% modifier** (16 mm cylinder) around each of the 4 insert holes and the 2 J-hook slots. |
| Nozzle temp | 270–290 °C (check your filament's datasheet) |
| Bed | 90–110 °C, on PEI with glue stick, or the plate the filament maker recommends |
| Chamber | Enclosed and warm (about 40–50 °C if you can). No drafts. |
| Part cooling | 0–20%; up to 40% for bridges only |
| Speed | 60–100 mm/s infill, 30–40 mm/s outer wall |
| Brim | 5–8 mm. The part is 187 mm long and flat, so nylon will want to lift at the corners. |
| Supports | None needed. The pocket roof and the slots bridge, or open upward. |
| Filament | Dry at 80 °C for 8–12 h and print from a dry box (below 20% RH) |

Estimated material: about 300–350 g at 40% infill. Check in your slicer.

**After printing:**
1. **Cool down:** let the part cool on the bed before removing it, to limit warping.
2. **Anneal:** anneal if your filament's datasheet recommends it. This improves heat resistance, which helps above the headers.
3. **Inserts:** press in the 4 × M6 heat-set inserts from the flat top at about 250–270 °C. Keep them square and flush.
4. **Fit test:** test-fit the cap on the PC545. If it's tight, sand the skirt's inner walls lightly, or reprint with `CAP_CLEAR = 1.0`.

## Heat
The tray sits directly above the headers. Fit an aluminium heat shield between the headers and the battery and EPS. PA6-CF holds up far better than PLA or PETG, but sustained radiant header heat will still soften it over time, and heat shortens battery life too.

## Install notes
- **Terminals:** they face the engine side. Make sure the positive terminal can't touch body metal, cover both terminals, and fuse the main positive cable close to the battery.
- **Hook tension:** tighten the J-hooks until the battery can't move, then stop. Over-tightening bows the plate.
