"""
Odyssey PC680 battery tray + hold-down holder with Honda S2000 EPS module mount.

Parametric CadQuery model. Run:  python3 battery_tray.py
Writes tray.stl, holder.stl, assembly.step to ./out/

Coordinates: X = battery length, Y = battery width, Z = up.
Origin = centre of the tray floor's top surface (where the battery sits).

Load path: two M6 threaded rods (steel) run from captive nuts in the tray up
through the top clamp bar. The rods carry the hold-down load, so the battery
is never held by printed plastic in tension alone.
"""
import os
import cadquery as cq

# ---------------- Battery: Odyssey PC680 (published spec) ----------------
BAT_L, BAT_W, BAT_H = 184.5, 79.0, 169.5   # mm (7.27 x 3.11 x 6.67 in)
CLEAR = 1.0                                # clearance per side in the pocket

# ---------------- EPS module mount — MEASURE AND SET THESE ----------------
# Centre-to-centre spacing of the EPS module's mounting holes / tabs,
# as (x, z) offsets from the plate centre. Placeholder rectangle until measured.
EPS_HOLES = [(-60.0, -40.0), (60.0, -40.0), (-60.0, 40.0), (60.0, 40.0)]
EPS_SLOT = 10.0       # slot length in X for each hole (tolerance for measurement error)
EPS_BOLT_D = 5.5      # clearance for M5 bolts
EPS_PLATE_X = 175.0   # plate width (X)

# ---------------- Tray ----------------
WALL = 5.0
FLOOR = 5.0
WALL_H = 35.0          # tray wall height above floor top
FLANGE_EXT = 18.0      # mounting flange beyond each short end
FLANGE_T = 6.0
MOUNT_D = 8.5          # M8 clearance
MOUNT_SLOT = 10.0      # slot length (adjust position on the car)
DRAIN_D = 8.0

# ---------------- Rods / holder ----------------
ROD_D = 6.6            # M6 clearance
NUT_AF, NUT_H = 10.2, 5.5   # M6 hex nut pocket (across flats, depth)
BOSS_R = 9.0
BAR_W = 30.0           # top bar width (X); centred between the terminals
BAR_T = 10.0
LEG_GAP = 2.0          # gap between leg bottom and boss top so the bar clamps the battery
PLATE_T = 6.0
LUG_X = 70.0           # tray lugs that the EPS plate bolts to (+/- X)
LUG_W = 20.0
INSERT_D = 6.4         # M5 heat-set insert hole in the tray lugs

PL, PW = BAT_L + 2 * CLEAR, BAT_W + 2 * CLEAR
OL, OW = PL + 2 * WALL, PW + 2 * WALL
Y_ROD = PW / 2 + WALL + 5.0
Y_PLATE = Y_ROD + 10.0        # inner face of the EPS plate (+Y side)
PLATE_Z0 = 10.0
PLATE_Z1 = BAT_H + BAR_T


def tray():
    body = (cq.Workplane("XY").box(OL, OW, FLOOR + WALL_H, centered=(True, True, False))
            .translate((0, 0, -FLOOR)))
    body = body.cut(cq.Workplane("XY").box(PL, PW, WALL_H + 1, centered=(True, True, False)))
    # inside corner fillets help the battery seat and stiffen the walls
    flange = (cq.Workplane("XY").box(OL + 2 * FLANGE_EXT, OW, FLANGE_T, centered=(True, True, False))
              .translate((0, 0, -FLOOR)))
    body = body.union(flange)
    # M8 mounting slots, two per end
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * (OL / 2 + FLANGE_EXT / 2)
            slot = (cq.Workplane("XY").slot2D(MOUNT_SLOT + MOUNT_D, MOUNT_D, angle=90)
                    .extrude(FLANGE_T + 2).translate((x, sy * OW / 4, -FLOOR - 1)))
            body = body.cut(slot)
    # gussets between the flange and the end walls
    for sx in (-1, 1):
        for sy in (-1, 0, 1):
            g = (cq.Workplane("XZ").polyline([(0, 0), (FLANGE_EXT - 2, 0), (0, WALL_H - 5)]).close()
                 .extrude(2.5, both=True)
                 .translate((0, sy * (OW / 2 - 8), -FLOOR + FLANGE_T)))
            if sx < 0:
                g = g.mirror("YZ")
            body = body.union(g.translate((sx * OL / 2, 0, 0)))
    # rod bosses with captive nut pockets, both long sides at mid-length
    for sy in (-1, 1):
        boss = (cq.Workplane("XY").circle(BOSS_R).extrude(FLOOR + WALL_H)
                .translate((0, sy * Y_ROD, -FLOOR)))
        web = (cq.Workplane("XY").box(2 * BOSS_R, Y_ROD - OW / 2 + 1, FLOOR + WALL_H, centered=(True, False, False))
               .translate((0, OW / 2 - 1, -FLOOR)))
        if sy < 0:
            web = web.mirror("XZ")
        body = body.union(boss).union(web)
        body = body.cut(cq.Workplane("XY").circle(ROD_D / 2).extrude(FLOOR + WALL_H + 2)
                        .translate((0, sy * Y_ROD, -FLOOR - 1)))
        body = body.cut(cq.Workplane("XY").polygon(6, NUT_AF / 0.866).extrude(NUT_H)
                        .translate((0, sy * Y_ROD, -FLOOR)))
    # lugs on the +Y side for the EPS plate's lower edge
    for sx in (-1, 1):
        lug = (cq.Workplane("XY").box(LUG_W, Y_PLATE - OW / 2 + 1, WALL_H - PLATE_Z0 + FLOOR, centered=(True, False, False))
               .translate((sx * LUG_X, OW / 2 - 1, PLATE_Z0 - FLOOR)))
        body = body.union(lug)
        body = body.cut(cq.Workplane("XZ").circle(INSERT_D / 2).extrude(-12)
                        .translate((sx * LUG_X, Y_PLATE + 0.01, PLATE_Z0 + 12)))
    # drain / weight-saving holes in the floor
    for x in (-60, -20, 20, 60):
        body = body.cut(cq.Workplane("XY").circle(DRAIN_D / 2).extrude(FLOOR + 2)
                        .translate((x, 0, -FLOOR - 1)))
    return body


def holder():
    # top clamp bar resting on the battery lid, centred lengthwise (clear of the terminals)
    bar = (cq.Workplane("XY").box(BAR_W, Y_PLATE + Y_ROD + 10, BAR_T, centered=(True, False, False))
           .translate((0, -Y_ROD - 10, BAT_H)))
    bar = bar.edges("|Z").fillet(3)
    # +Y leg: joins the bar to the plate, guides the rod
    leg_z0 = WALL_H + LEG_GAP
    leg = (cq.Workplane("XY").box(BAR_W, Y_PLATE - (Y_ROD - 8), BAT_H - leg_z0, centered=(True, False, False))
           .translate((0, Y_ROD - 8, leg_z0)))
    # vertical EPS plate on the +Y side
    plate = (cq.Workplane("XY").box(EPS_PLATE_X, PLATE_T, PLATE_Z1 - PLATE_Z0, centered=(True, False, False))
             .translate((0, Y_PLATE, PLATE_Z0)))
    plate = plate.edges("|Y").fillet(8)
    h = bar.union(leg).union(plate)
    # rod holes through bar and leg
    for sy in (-1, 1):
        h = h.cut(cq.Workplane("XY").circle(ROD_D / 2).extrude(BAT_H + 40).translate((0, sy * Y_ROD, 0)))
    # EPS module slots, relative to the plate centre
    zc = (PLATE_Z0 + PLATE_Z1) / 2
    for (x, z) in EPS_HOLES:
        s = (cq.Workplane("XZ").slot2D(EPS_SLOT + EPS_BOLT_D, EPS_BOLT_D).extrude(-(PLATE_T + 2))
             .translate((x, Y_PLATE - 1, zc + z)))
        h = h.cut(s)
    # bolts to the tray lugs (M5 into heat-set inserts)
    for sx in (-1, 1):
        h = h.cut(cq.Workplane("XZ").circle(EPS_BOLT_D / 2).extrude(-(PLATE_T + 2))
                  .translate((sx * LUG_X, Y_PLATE - 1, PLATE_Z0 + 12)))
    # vent / lightening windows that avoid the EPS hole pattern
    for x in (-35, 35):
        w = (cq.Workplane("XZ").rect(30, 50).extrude(-(PLATE_T + 2))
             .edges("|Y").fillet(6).translate((x, Y_PLATE - 1, zc)))
        h = h.cut(w)
    return h


def battery():
    return cq.Workplane("XY").box(BAT_L, BAT_W, BAT_H, centered=(True, True, False))


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    t, hd = tray(), holder()
    cq.exporters.export(t, os.path.join(out, "tray.stl"), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(hd, os.path.join(out, "holder.stl"), tolerance=0.05, angularTolerance=0.1)
    asm = (cq.Assembly()
           .add(t, name="tray", color=cq.Color(0.2, 0.2, 0.2))
           .add(hd, name="holder", color=cq.Color(0.8, 0.1, 0.15))
           .add(battery(), name="PC680 (reference)", color=cq.Color(0.9, 0.9, 0.9, 0.4)))
    asm.save(os.path.join(out, "assembly.step"))
    for name, s in (("tray", t), ("holder", hd)):
        bb = s.val().BoundingBox()
        print(f"{name}: valid={s.val().isValid()} vol={s.val().Volume()/1000:.0f} cm3 "
              f"size={bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"rod length ~{FLOOR + BAT_H + BAR_T + 15:.0f} mm (M6, incl. nut + washer on top)")
