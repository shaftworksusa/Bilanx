# PC680 battery tray + holder with S2000 EPS module mount

![preview](preview.png)

There are two printed parts. The geometry is parametric and lives in [`battery_tray.py`](battery_tray.py). Run `pip install cadquery`, then `python3 battery_tray.py`, to regenerate `out/tray.stl`, `out/holder.stl` and `out/assembly.step`.

| Part | Size (mm) | What it does |
|---|---|---|
| **Tray** | 232.5 × 120 × 40 | Pocket for the PC680 (184.5 × 79 × 169.5 spec, 1 mm clearance per side). It has four M8 slots on end flanges for mounting to the car, two rod bosses with captive M6 nut pockets, two lugs for the EPS plate, and drain holes. |
| **Holder** | 175 × 127 × 170 | Top clamp bar across the battery lid, centred lengthwise so it clears the terminals. It joins a vertical plate on the +Y long side, and the **EPS module** bolts to that plate. |

## ⚠️ Set the EPS hole pattern before printing
`EPS_HOLES` in `battery_tray.py` is a **placeholder** (a 120 × 80 mm rectangle). To set it:
1. Measure the centre-to-centre spacing of the EPS module's mounting tabs or holes.
2. Enter them as (x, z) offsets from the plate centre.
3. Re-run the script.

Each hole is a 10 mm horizontal slot, so small measurement errors are tolerated. If the module is bigger than about 175 × 160 mm, also raise `EPS_PLATE_X`.

## Hardware
- **Hold-down:**
  - 2 × M6 threaded rods, about 200 mm long. Steel carries the hold-down load, not printed plastic.
  - 2 × M6 nuts in the tray's nut pockets, plus 2 × M6 nyloc nuts and large washers on top of the bar
- **Tray to car:** 4 × M8 bolts with large washers
- **EPS plate to tray:**
  - 2 × M5 bolts
  - 2 × M5 heat-set inserts (6.4 mm hole) in the tray lugs
- **EPS module to plate:** 4 × M5 bolts with nyloc nuts and washers
- **Optional:** 1–2 mm rubber or neoprene pad under the battery and under the clamp bar

## Printing
- **Material:** PA6-CF or PA12-CF (same filament as the intake), dried properly. Avoid PETG and PLA: a trunk or engine bay gets too hot, and a 7 kg battery creeps them.
- **Strength settings:** 5–6 walls, 40%+ gyroid infill, 6 top/bottom layers
- **Tray:** print floor-down.
- **Holder:** print with the EPS plate's outer face on the bed. The top bar then stands up as a vertical fin.

## Before final install
- **Bar height:** confirm the clamp bar sits flat on your battery's lid between the terminals. The bar's underside is at the spec height of 169.5 mm, so add a pad if your battery measures shorter.
- **Rod tension:** tighten the rods until the battery can't move, then stop. The leg has a 2 mm gap above the boss on purpose, so the bar clamps the battery and not the frame.
- **Heat:** keep the EPS module away from exhaust heat.
- **Terminals:** cover both battery terminals and fuse the main positive cable close to the battery.
- **Strength:** a printed tray is not crash-certified. Inspect it periodically for cracks or creep. For track use, consider making the tray in aluminium from the same dimensions.
