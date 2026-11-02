"""
Odyssey PC680 laid on its side on the OEM Honda S2000 battery tray.
Two printed parts:
  cradle.stl       locates the battery on the OEM tray (plug drops into the tray pocket)
  clamp_plate.stl  hold-down plate on the battery's upturned side face; the EPS module bolts on top

Parametric CadQuery model. Run:  python3 battery_tray.py   ->  ./out/

Coordinates: X = battery length, Y = across the tray, Z = up.
Origin = centre of the cradle floor's top surface.

Load path: the OEM J-bolts (or M6 rods) run from the OEM tray's hooks up through
slots in the clamp plate. Steel carries the hold-down load; the plate only spreads it.
"""
import os
import cadquery as cq

# ---------------- Battery: Odyssey PC680, lying on a long side ----------------
# Spec 184.5 L x 79 W x 169.5 H. On its side: footprint L x H, height W.
BAT_X, BAT_Y, BAT_Z = 184.5, 169.5, 79.0
TERMINAL_SIDE = +1     # terminals face +Y (the cradle wall on that side gets a cut-out)
CLEAR = 1.0

# ---------------- OEM S2000 tray — MEASURE AND SET ----------------
OEM_IN_X, OEM_IN_Y = 230.0, 125.0   # inside of the OEM tray pocket (placeholder)
PLUG_H = 8.0                         # how far the cradle's plug drops into the OEM pocket
# J-bolt / rod positions (x, y) where the OEM hooks are (placeholder: both short ends, centred)
ROD_POS = [(-104.0, 0.0), (104.0, 0.0)]
ROD_D = 6.6            # M6 clearance
ROD_SLOT = 12.0        # slots along X absorb measurement error

# ---------------- EPS module — MEASURE AND SET ----------------
EPS_HOLES = [(-60.0, -40.0), (60.0, -40.0), (-60.0, 40.0), (60.0, 40.0)]  # (x, y) from plate centre; placeholder
EPS_SLOT = 10.0
EPS_BOLT_D = 5.5       # M5 clearance
EPS_HEAD_D = 10.0      # counterbore for M5 heads on the underside (heads must not touch the battery)
EPS_HEAD_H = 4.0

# ---------------- Cradle ----------------
FLOOR = 4.0
WALL = 4.0
WALL_H = 20.0          # below the terminals (~40 mm up when the battery is on its side)
TERM_CUT_X = 150.0     # width of the cut-out in the terminal-side wall

# ---------------- Clamp plate ----------------
PLATE_T = 8.0
PLATE_Y = 130.0
RIB_H = 8.0            # stiffening ribs along X on the top edges

PX, PY = BAT_X + 2 * CLEAR, BAT_Y + 2 * CLEAR
OX, OY = PX + 2 * WALL, PY + 2 * WALL


def _slot_x(x, y, length, d, z0, h):
    return (cq.Workplane("XY").slot2D(length + d, d).extrude(h).translate((x, y, z0)))


def cradle():
    base = (cq.Workplane("XY").box(OX, OY, FLOOR + WALL_H, centered=(True, True, False))
            .translate((0, 0, -FLOOR)))
    base = base.cut(cq.Workplane("XY").box(PX, PY, WALL_H + 1, centered=(True, True, False)))
    base = base.edges("|Z").fillet(3)
    # plug that drops into the OEM tray pocket so the cradle can't slide
    plug = (cq.Workplane("XY").box(min(OEM_IN_X - 2, OX), min(OEM_IN_Y - 2, OY), PLUG_H, centered=(True, True, False))
            .translate((0, 0, -FLOOR - PLUG_H)))
    plug = plug.cut(cq.Workplane("XY").box(min(OEM_IN_X - 2, OX) - 12, min(OEM_IN_Y - 2, OY) - 12, PLUG_H, centered=(True, True, False))
                    .translate((0, 0, -FLOOR - PLUG_H)))   # hollow ring: lighter, still locates
    c = base.union(plug)
    # terminal-side wall cut-out
    c = c.cut(cq.Workplane("XY").box(TERM_CUT_X, WALL + 2, WALL_H, centered=(True, True, False))
              .translate((0, TERMINAL_SIDE * (PY / 2 + WALL / 2), 6)))
    # J-bolt passages (slots through floor/plug where the hooks are)
    for (x, y) in ROD_POS:
        c = c.cut(_slot_x(x, y, ROD_SLOT, ROD_D + 2, -FLOOR - PLUG_H - 1, FLOOR + PLUG_H + WALL_H + 2))
    # drain / lightening holes
    for x in (-55, 0, 55):
        for y in (-45, 45):
            c = c.cut(cq.Workplane("XY").circle(6).extrude(FLOOR + 2).translate((x, y, -FLOOR - 1)))
    return c


def clamp_plate():
    xs = [abs(x) for x, _ in ROD_POS]
    half_x = max(max(xs) + ROD_SLOT / 2 + 12, OX / 2)
    z0 = BAT_Z
    p = (cq.Workplane("XY").box(2 * half_x, PLATE_Y, PLATE_T, centered=(True, True, False))
         .translate((0, 0, z0)))
    p = p.edges("|Z").fillet(10)
    for sy in (-1, 1):
        rib = (cq.Workplane("XY").box(2 * half_x - 20, 6, RIB_H, centered=(True, True, False))
               .translate((0, sy * (PLATE_Y / 2 - 3), z0 + PLATE_T)))
        p = p.union(rib)
    for (x, y) in ROD_POS:
        p = p.cut(_slot_x(x, y, ROD_SLOT, ROD_D, z0 - 1, PLATE_T + RIB_H + 2))
    for (x, y) in EPS_HOLES:
        p = p.cut(_slot_x(x, y, EPS_SLOT, EPS_BOLT_D, z0 - 1, PLATE_T + 2))
        p = p.cut(_slot_x(x, y, EPS_SLOT, EPS_HEAD_D, z0 - 0.01, EPS_HEAD_H))
    # lightening windows clear of the EPS pattern
    for x in (-25, 25):
        p = p.cut(cq.Workplane("XY").rect(30, 40).extrude(PLATE_T + 2).edges("|Z").fillet(6)
                  .translate((x, 0, z0 - 1)))
    return p


def battery():
    return cq.Workplane("XY").box(BAT_X, BAT_Y, BAT_Z, centered=(True, True, False))


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    c, p = cradle(), clamp_plate()
    cq.exporters.export(c, os.path.join(out, "cradle.stl"), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(p, os.path.join(out, "clamp_plate.stl"), tolerance=0.05, angularTolerance=0.1)
    asm = (cq.Assembly()
           .add(c, name="cradle", color=cq.Color(0.2, 0.2, 0.2))
           .add(p, name="clamp_plate", color=cq.Color(0.8, 0.1, 0.15))
           .add(battery(), name="PC680 (reference)", color=cq.Color(0.9, 0.9, 0.9, 0.4)))
    asm.export(os.path.join(out, "assembly.step"))
    for name, s in (("cradle", c), ("clamp_plate", p)):
        bb = s.val().BoundingBox()
        print(f"{name}: valid={s.val().isValid()} vol={s.val().Volume()/1000:.0f} cm3 "
              f"size={bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    if OY > OEM_IN_Y:
        print(f"NOTE: cradle is {OY:.0f} mm across vs OEM pocket {OEM_IN_Y:.0f} mm -> overhangs {(OY-OEM_IN_Y)/2:.0f} mm per side")
