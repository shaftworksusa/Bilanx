"""
Odyssey PC545 laid on its side directly in the OEM Honda S2000 battery tray (no cradle: the
OEM tray locates the battery). One printed part:
  clamp_plate.stl  battery-shaped cap over the upturned side face, pulled down by the
                   OEM J-hooks; the EPS module bolts on top

Parametric CadQuery model. Run:  python3 battery_tray.py   ->  ./out/

Coordinates: X = battery length, Y = across the tray, Z = up.
Origin = centre of the battery's bottom face (sitting in the OEM tray).

Load path: the OEM J-hooks run from the tray's slots up through holes in the clamp plate.
Steel carries the hold-down load; the plate only spreads it.
"""
import os
import cadquery as cq

# ---------------- Battery: Odyssey PC545, lying on its side in the OEM tray ----------------
# Odyssey spec 7.00 x 3.38 x 5.17 in = 177.8 L x 85.9 W x 131.3 H mm (measured 130 mm across on the car).
# On its side: X = length, Y = across (J-hook direction, = spec height), Z = up (= spec width).
BAT_X, BAT_Y, BAT_Z = 177.8, 131.3, 85.9
TERMINAL_SIDE = +1     # terminals face +Y (the cradle wall on that side gets a cut-out)

# ---------------- OEM S2000 tray J-hooks ----------------
# The J-hooks sit across the battery's WIDTH (Y), centred on its length.
JHOOK_SPACING = 132.0   # measured: OEM J-hook slot centres
JHOOK_X = 0.0           # position along the battery length (assumed centred)
ROD_POS = [(JHOOK_X, -JHOOK_SPACING / 2), (JHOOK_X, JHOOK_SPACING / 2)]
ROD_D = 6.6            # M6 clearance
ROD_SLOT = 8.0         # slot length (along Y): hooks run ~1 mm outside the battery faces

# ---------------- EPS module: Showa 39980-S2A-A01 (S2000) ----------------
# Measured hole pattern: 115 mm across x 30 mm between the upper and lower hole on each flange.
# Outline estimated from a photo scaled off the 115 mm: flanges ~133 mm wide; ~135 mm from the
# flange top edge to the connector ends; the top holes sit ~10 mm below the flange top edge.
EPS_HOLE_X, EPS_HOLE_Y = 115.0, 30.0
EPS_LEN = 135.0             # flange top edge -> connector ends
EPS_TOP_TO_HOLE = 10.0
EPS_CONNECTORS = -1         # connectors point -Y (away from the battery terminals at +Y)
EPS_SHIFT = -15.0           # shift along the connector direction (mm); -15 gives the harness plugs room before the J-bolt
EPS_ROTATE = 90             # module rotation on the plate, degrees (0 = connectors along Y; 90 = connectors along X)
# Module-local coords (u across the 115 mm, v along the connector direction), outline centred on the plate:
_v_top = EPS_CONNECTORS * -(EPS_LEN / 2 - EPS_TOP_TO_HOLE) + EPS_SHIFT * EPS_CONNECTORS
_v_low = _v_top + EPS_CONNECTORS * EPS_HOLE_Y
EPS_HOLES_LOCAL = [(su * EPS_HOLE_X / 2, v) for su in (-1, 1) for v in (_v_top, _v_low)]


def _rot(u, v, deg=EPS_ROTATE):
    import math
    a = math.radians(deg)
    return (u * math.cos(a) - v * math.sin(a), u * math.sin(a) + v * math.cos(a))


EPS_HOLES = [_rot(u, v) for u, v in EPS_HOLES_LOCAL]
EPS_SLOT = 4.0         # small slots: pattern is measured, this is just tolerance
EPS_BOLT_D = 6.4       # M6 clearance (the OEM EPS bolts are likely 6 mm; M5 also works)
EPS_HEAD_D = 12.0      # counterbore for bolt heads on the underside (heads must not touch the battery)
EPS_HEAD_H = 4.5

# ---------------- Clamp plate / battery cap ----------------
PLATE_T = 8.0          # top deck thickness
PLATE_Y = 150.0        # minimum deck width (Y); grows to reach the J-hooks
CAP_CLEAR = 0.75       # clearance per side between the cap pocket and the battery case
CAP_WALL = 4.0         # skirt wall thickness
SKIRT_D = 15.0         # how far the skirt wraps down the battery's sides
CORNER_R = 5.0         # battery case corner radius (est.)
HOOK_NOTCH = 24.0      # gap in the skirt where each J-hook runs down the battery face



def _slot(x, y, length, d, z0, h, angle=0):
    return cq.Workplane("XY").slot2D(length + d, d, angle=angle).extrude(h).translate((x, y, z0))


def _rrect(x, y, r, z0, h):
    return (cq.Workplane("XY").rect(x, y).extrude(h).edges("|Z").fillet(r).translate((0, 0, z0)))


def clamp_plate():
    """Top deck (EPS mount, J-hook slots) + a skirt whose inside is the battery's shape."""
    z0 = BAT_Z
    in_x, in_y = BAT_X + 2 * CAP_CLEAR, BAT_Y + 2 * CAP_CLEAR
    out_x, out_y = in_x + 2 * CAP_WALL, in_y + 2 * CAP_WALL
    r_in, r_out = CORNER_R + CAP_CLEAR, CORNER_R + CAP_CLEAR + CAP_WALL
    half_y = max(PLATE_Y / 2, out_y / 2, max(abs(y) for _, y in ROD_POS) + ROD_SLOT / 2 + 12)
    deck = _rrect(out_x, 2 * half_y, max(r_out, 10), z0, PLATE_T)
    skirt = _rrect(out_x, out_y, r_out, z0 - SKIRT_D, SKIRT_D + 0.01).cut(
        _rrect(in_x, in_y, r_in, z0 - SKIRT_D - 1, SKIRT_D + 1))
    # notches so the J-hooks can run straight down the battery faces
    for (x, y) in ROD_POS:
        skirt = skirt.cut(cq.Workplane("XY").box(HOOK_NOTCH, 2 * CAP_WALL + 20, SKIRT_D + 2, centered=(True, True, False))
                          .translate((x, y, z0 - SKIRT_D - 1)))
    p = deck.union(skirt)
    for (x, y) in ROD_POS:
        p = p.cut(_slot(x, y, ROD_SLOT, ROD_D, z0 - 1, PLATE_T + 2, angle=90))
    for (x, y) in EPS_HOLES:
        for d, zz, hh in ((EPS_BOLT_D, z0 - 1, PLATE_T + 2), (EPS_HEAD_D, z0 - 0.01, EPS_HEAD_H)):
            p = p.cut(cq.Workplane("XY").slot2D(EPS_SLOT + d, d, angle=EPS_ROTATE).extrude(hh).translate((x, y, zz)))
    # vent / lightening windows clear of the EPS pattern
    for x in (-22, 22):
        p = p.cut(cq.Workplane("XY").rect(28, 60).extrude(PLATE_T + 2).edges("|Z").fillet(6)
                  .translate((x, 0, z0 - 1)))
    return p


def eps_reference():
    """Rough EPS outline for fit checks only (photo-estimated)."""
    zc = BAT_Z + PLATE_T
    v_top = EPS_HOLES_LOCAL[0][1]
    yc = v_top + EPS_CONNECTORS * (EPS_LEN / 2 - EPS_TOP_TO_HOLE)
    flange = (cq.Workplane("XY").box(133, 45, 6, centered=(True, True, False))
              .translate((0, v_top + EPS_CONNECTORS * 12, zc)))
    body = (cq.Workplane("XY").box(94, EPS_LEN - 25, 30, centered=(True, True, False))
            .translate((0, yc - EPS_CONNECTORS * 2, zc)))
    plugs = (cq.Workplane("XY").box(90, 22, 20, centered=(True, True, False))
             .translate((0, yc + EPS_CONNECTORS * (EPS_LEN / 2 - 11), zc)))
    return flange.union(body).union(plugs).rotate((0, 0, 0), (0, 0, 1), EPS_ROTATE)


def battery():
    return _rrect(BAT_X, BAT_Y, CORNER_R, 0, BAT_Z)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    p = clamp_plate()
    cq.exporters.export(p, os.path.join(out, "clamp_plate.stl"), tolerance=0.05, angularTolerance=0.1)
    asm = (cq.Assembly()
           .add(p, name="clamp_plate", color=cq.Color(0.8, 0.1, 0.15))
           .add(eps_reference(), name="EPS (reference)", color=cq.Color(0.6, 0.6, 0.62))
           .add(battery(), name="PC545 (reference)", color=cq.Color(0.9, 0.9, 0.9, 0.4)))
    asm.export(os.path.join(out, "assembly.step"))
    for name, s in (("clamp_plate", p),):
        bb = s.val().BoundingBox()
        print(f"{name}: valid={s.val().isValid()} vol={s.val().Volume()/1000:.0f} cm3 "
              f"size={bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    cq.exporters.export(eps_reference(), os.path.join(out, "eps_reference.stl"))
    print("EPS holes (x, y):", [(round(x, 1), round(y, 1)) for x, y in EPS_HOLES])
    inside = [abs(y) < BAT_Y / 2 for _, y in ROD_POS]
    if any(inside):
        print(f"WARNING: J-hook positions (y=±{JHOOK_SPACING/2:.0f}) are inside the battery footprint "
              f"(±{BAT_Y/2:.1f}) — the hooks would have to pass through the battery.")
