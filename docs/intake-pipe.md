# S2000 custom intake: design notes

Brought in from the "Intake engine bay modifications" chat (Oct 20–26, 2026). The STL and image files were made in that chat's temporary workspace and are **not in this repo**. If you downloaded `intake_pipe_3.5in.zip`, add it under `cad/`.

## Car context
- Honda S2000. Chassis (AP1/AP2) and year weren't stated.
- Engine: "210 hp 2.4L" (owner). It was treated as a K-series swap, but that's unconfirmed.
- Different intake manifold with the throttle body moved forward
- **Bosch 74 mm drive-by-wire throttle body**. Inlet lip: 80 mm OD, 15 mm long, 74 mm bore. No adapter.
- Existing Password:JDM carbon intake with snorkel. Its airbox was scanned for the first designs.
- Fuelling assumed speed-density on a MAP sensor (unconfirmed), so no MAF provision

## How the design evolved
1. **Oct 20–22: cut-down plenum (dropped).** Three versions of the Password airbox cut back to the new throttle body position:
   - v1: 13.1 → 7.5 L
   - v2: about 12.0 L
   - v3: about 11.9 L, with an internal 74 mm pipe and a 4" bellmouth
2. **CFD (OpenFOAM, k-ω SST).** Pressure loss at 0.16 m³/s (about 250 hp):

   | Layout | Loss |
   |---|---|
   | v3 | 294 Pa |
   | Layout A | 298 Pa |
   | Layout B (100 mm bend) | 232 Pa |
   | Plain 3.5" pipe | 63 Pa |

3. **Re-run at 210 hp (0.134 m³/s)**, with each layout in a modelled 150×170 mm cone filter:

   | Layout | Loss | Loss coefficient | Uniformity |
   |---|---|---|---|
   | Layout B | 158 Pa | 0.27 | 0.94 |
   | **3.5" pipe** | **52 Pa** | **0.09** | **0.95** |
   | 3.0" pipe | 99 Pa | 0.17 | 0.89 |

   Going to 4" gains about 0.03 hp at 210 hp, so 3.5" was kept.

## Final design: single 3.5" pipe
- **Routing:** from the throttle body, one 90° bend toward the passenger-front corner. The filter sits there in a sealed heat-shield box fed from the snorkel, with a drain hole.
- **Pipe:** 85.6 mm bore, 3 mm wall (91.6 mm OD), 100 mm bend radius, 570 mm centreline
- **Bellmouth / filter end:**
  - 152.4 mm (6") collar, 45 mm long, with a 1.5 mm bead 6 mm from the edge
  - 146 mm mouth, 30.4 mm lip radius, 45° cone down to the pipe
- **Throttle body end (rebuilt Oct 26):**
  - Spigot: 80.0 mm OD, 74.0 mm bore, 50 mm long, 3 mm wall
  - Bore tapers 85.6 → 74 mm over the last 80 mm
  - 1.5 mm bead 12 mm from the end, a 45° shoulder where the coupler stops, 0.6 mm end chamfer
- **Sections:** three parts joined by 25 mm keyed slip sockets (0.2 mm clearance) and bonded with high-temp epoxy. Each fits a 256 mm printer bed. A one-piece version also exists.

  | Part | Size |
  |---|---|
  | 1, filter end | 200 × 155 × 155 mm |
  | 2, middle | 206 × 100 × 142 mm |
  | 3, throttle body end | 173 × 203 × 100 mm |

- **Surface:** smooth (recommended) or dimpled (433 dimples, 5 mm Ø, 0.6 mm deep). Dimples don't help airflow.

## Hardware
- **Throttle side:** straight **80 mm ID** silicone coupler, 4-ply, 50–65 mm long, with **T-bolt clamps**.
  - Put the throttle-side clamp centred on the 15 mm lip.
  - Put the pipe-side clamp between the bead and the shoulder.
  - Leave no more than a 2–3 mm gap between the pipe end and the throttle body face.
- **Filter:** cone filter with a 6" flange, at least 150 mm base, about 150–180 mm long
- **Bracket:** on rubber isolators near the bend. The 15 mm lip is a short joint, and couplers are known to pop off Bosch inlets.

## Printing
- **Material:** PA6-CF (or PA12-CF). PETG/PETG-CF soften at about 70 °C, ASA is marginal and PC warps.
- **Drying:**
  - 80 °C for 8–12 h, or 70 °C for 12–24 h
  - Print from a dry box at 45–55 °C, below 15–20% RH
  - Dry means another 2 h changes the spool weight by less than 1 g.
- **Printer and slicing:**
  - Hardened 0.4–0.6 mm nozzle, enclosed printer, 4–5 walls
  - Stand each section on its joint end, so no internal supports are needed.
  - Section 1 needs about 25% gyroid infill (the flare-to-collar region is solid).
- **After printing:** anneal per the filament maker, then bond the sections with high-temp epoxy (e.g. JB Weld).

## Open items
- Test-fit the route and measure clearance to the hood, radiator and filler neck. Check the 6" collar in the passenger corner near the frame rail and headlight.
- Decide on an IAT bung (straight section, at least 150 mm from the bend) and a 3/4" breather fitting near the filter end. Neither is in the current model.
- Design the sealed heat-shield filter box (offered but not started)
- Optional: CFD confirmation run at 4"
