# PC680 on its side in the OEM S2000 tray: clamp plate with EPS mount

![preview](preview.png)

The Odyssey battery (measured **130 mm** across as it sits; length 184.5 and thickness 79 are PC680 catalogue values, so confirm them) lies **on its side, directly in the OEM S2000 battery tray** in the engine bay. Odyssey rates it for any mounting orientation. No cradle is used: the OEM tray locates the battery.

There's one printed part, the **clamp plate**. It sits on the battery's upturned face, the OEM J-hooks pull it down, and the **EPS module (Showa 39980-S2A-A01)** bolts on top of it.

The geometry is parametric and lives in [`battery_tray.py`](battery_tray.py). Run `pip install cadquery`, then `python3 battery_tray.py`, to regenerate `out/clamp_plate.stl` and `out/assembly.step`.

## Status
- **EPS mount: done.**
  - Hole pattern measured at **115 × 30 mm**.
  - The module is rotated 90° with its connectors along the battery length, and shifted 15 mm toward the fender end.
  - Bolt heads are recessed on the underside, so they never touch the battery.
  - Settings: `EPS_ROTATE`, `EPS_CONNECTORS`, `EPS_SHIFT`.
- **J-hooks: done.**
  - The OEM hooks run straight up past the battery's front and back faces. The slots are 132 mm apart and the battery is 130 mm across.
  - The plate's hook holes are 8 mm slots across the width, centred on the battery's length (`JHOOK_SPACING`, `JHOOK_X`).
- **Plate:** 188.5 × 164 × 16 mm. It overhangs the battery front and back so it can reach the hooks.

## Hardware
- **Hold-down:** OEM J-hooks with nyloc nuts and large washers on top of the plate
- **EPS module:** 4 × M6 bolts (M5 also fits) from under the plate, with nyloc nuts and washers. Use spacers of 6–10 mm if the module's fin side faces the plate, so air can flow under it.
- **Pad:** 1–2 mm rubber or neoprene between the plate and the battery

## Printing
- **Material:** PA6-CF or PA12-CF, dried properly. Avoid PLA and PETG.
- **Settings:** 5–6 walls, 40%+ gyroid infill, 6 top/bottom layers
- **Orientation:** print battery side down.

## Heat
The tray sits directly above the headers. Fit an aluminium heat shield between the headers and the battery and EPS. PA6-CF holds up far better than PLA or PETG, but sustained radiant header heat will still soften it over time, and heat shortens battery life too.

## Install notes
- **Terminals:** they face the engine side. Make sure the positive terminal can't touch body metal, cover both terminals, and fuse the main positive cable close to the battery.
- **Hook tension:** tighten the J-hooks until the battery can't move, then stop. Over-tightening bows the plate.
