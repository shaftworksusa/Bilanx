"""
Crop the official Haltech decal sheets (HT-011500, sheets A–I, 28 decals each) into
individual decals and embed them in keypad-planner.html.

Put sheet images in ./sheets/ as sheetA.png .. sheetI.png (same 7 x 4 layout as the
Haltech sheet images). Then:  python3 build_decals.py
Sheets that are missing still appear in the planner by name; their tiles show the decal
name until the image is added.
"""
import base64, io, json, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "keypad-planner.html")

# Decal names per sheet, in reading order (7 columns x 4 rows), from the HT-011500 sheets.
SHEETS = {
    "A": ["Ignition key", "Start", "Start/Stop", "ACC", "Hazard", "Reset", "Air con",
          "Thermofan 1", "Thermofan 2", "Fan 1", "Fan 2", "Trans fan", "Oil fan", "Helmet fan",
          "Shocks", "Horn", "Diff pump", "P/S pump", "Engine pump", "Trans pump", "I/C pump",
          "AWD", "Torque control", "Traction control", "Fuel pump 1", "Fuel pump 2", "Fuel pump 3", "Fuel pump 4"],
    "B": ["Burnout", "Stage", "Launch", "Bump", "Creep", "Water/meth", "Data log",
          "Wipers high", "Wipers low", "Wash", "Anti-lag", "Boost", "Boost up", "Boost down",
          "Turn left", "Turn right", "Cabin light", "Dim", "Low beam", "High beam", "Fog lights",
          "P", "R", "N", "D", "M", "S", "Overdrive"],
    "C": ["N2O arm 1", "N2O arm 2", "N2O arm 3", "N2O arm 4", "N2O arm 5", "N2O arm 6", "N2O heater 1",
          "N2O heater 2", "N2O purge 1", "N2O purge 2", "Cruise", "Set/Coast", "Resume/ACC", "Cruise reset",
          "Page down", "Page up", "Upshift", "Downshift", "Front demist", "Rear demist", "Exhaust bypass",
          "Aux 1", "Aux 2", "Aux 3", "Aux 4", "Aux 5", "Main fuel", "Reserve fuel"],
    "D": ["1", "2", "3", "4", "5", "6", "7",
          "8", "9", "Pit speed", "Valet mode", "Fast (rabbit)", "Slow (turtle)", "Haltech logo",
          "Arrow right", "Arrow left", "Arrow down", "Arrow up", "Don't panic!", "Warp speed", "After burner",
          "Plus", "Minus", "Cross", "Tick", "Middle finger extender", "Enable invisibility cloak", "Initiate self destruct sequence"],
    "E": ["Radiation", "Smiley", "Angry face", "Mushroom", "Ejector seat", "Skull & crossbones", "Flux capacitor",
          "Just send it!", "Go baby go!", "Unleash the beast", "Page up for power", "It's ass whoopin' time!", "Gimme mo powa!", "Enable swearing module"]
         + [f"Blank {i}" for i in range(1, 15)],
    "F": ["Start (red)", "Start/Stop (red)", "Off (red)", "ACC (red)", "IGN (red)", "AUX (red)", "Hazard (red)",
          "Lock", "Unlock", "Lock/Unlock", "Boot release", "Seat heater", "Seat heater left", "Seat heater right",
          "Reading lights", "Dome light", "Interior light", "Lights left", "Lights right", "Lights front", "Lights rear",
          "Parking lights", "Low/High beam", "Lights off/park/low", "Rain light", "Rain light flash", "Underglow", "Light bar"],
    "G": ["Winch on/off", "Winch in", "Winch out", "Camera", "Rear camera", "Battery", "Heater",
          "ABS on/off", "Park brake", "Line lock", "Cool suit", "Drink", "Radio", "Helmet",
          "Intercooler spray", "Push to pass", "Scramble boost", "Fuel pump override", "VHF", "UHF", "Bilge pump",
          "Sway bar", "Idle up", "Fuel fan", "Sport mode", "Eco mode", "Fan off/1/2/3", "Air compressor"],
    "H": ["Throttle map", "Map 1", "Map 2", "AWD (text)", "Trans brake", "Chute active", "Clutch slipper active",
          "LPG", "2 step", "2 step up", "2 step down", "IGN retard", "IGN retard +", "IGN retard −",
          "Front window up left", "Front window down left", "Front window up right", "Front window down right", "Wiper speed", "Wiper int", "Water pump",
          "Rear window up left", "Rear window down left", "Rear window up right", "Rear window down right", "Rear wiper", "Rear wiper int", "Rear wash"],
    "I": ["12V socket", "USB charger", "Cool down", "Rear diff lock", "Centre diff lock", "Front diff lock", "Diff lock",
          "Speed limiter", "Aux RPM limiter", "Rolling anti-lag", "Rotational idle", "Brap brap", "Ghost", "Pops & crackles",
          "Prev screen", "Next screen", "Fuel transfer switch", "Auto/manual", "N2O open/close", "Torque control up", "Torque control down",
          "Cancel alarm", "Trip 1 reset", "Trip 2 reset", "Check engine reset", "Dash dim", "Trim +", "Trim −"],
}


def find_cells(im):
    """Locate the 7 x 4 grid from the yellow frames (falls back to proportional positions)."""
    w, h = im.size
    px = im.load()
    yel = lambda p: p[0] > 200 and p[1] > 150 and p[2] < 90
    H = int(h * 0.84)
    col = [sum(yel(px[x, y]) for y in range(0, H, 2)) for x in range(w)]
    row = [sum(yel(px[x, y]) for x in range(0, w, 2)) for y in range(H)]

    def runs(a, thr):
        out, s = [], None
        for i, v in enumerate(a):
            if v > thr and s is None:
                s = i
            if v <= thr and s is not None:
                out.append((s, i)); s = None
        return out

    cx = [r for r in runs(col, max(col) * 0.45) if r[0] > 8 and r[1] < w - 8]
    ry = [r for r in runs(row, max(row) * 0.45) if r[0] > 8]
    if len(cx) == 14 and len(ry) >= 8:
        xs = [(cx[2 * i][0], cx[2 * i + 1][1]) for i in range(7)]
        ys = [(ry[2 * i][0], ry[2 * i + 1][1]) for i in range(4)]
        return xs, ys
    # proportional fallback (based on the 774 x 543 reference)
    fx = lambda v: round(v / 774 * w); fy = lambda v: round(v / 543 * h)
    xs = [(fx(20 + i * 105.3), fx(118 + i * 105.3)) for i in range(7)]
    ys = [(fy(21 + j * 105.3), fy(119 + j * 105.3)) for j in range(4)]
    return xs, ys


def crop_sheet(path):
    im = Image.open(path).convert("RGB")
    xs, ys = find_cells(im)
    out = []
    for (y0, y1) in ys:
        for (x0, x1) in xs:
            inset = round((x1 - x0) * 0.085)          # drop the yellow frame
            tile = im.crop((x0 + inset, y0 + inset, x1 - inset, y1 - inset)).resize((128, 128), Image.LANCZOS)
            buf = io.BytesIO(); tile.save(buf, "WEBP", quality=88)
            out.append("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode())
    return out


def main():
    decals = []
    for sheet, names in SHEETS.items():
        path = os.path.join(HERE, "sheets", f"sheet{sheet}.png")
        imgs = crop_sheet(path) if os.path.exists(path) else [None] * 28
        for i, name in enumerate(names):
            decals.append({"id": f"{sheet}{i + 1:02d}", "sheet": sheet, "pos": i + 1, "name": name, "img": imgs[i]})
        print(f"sheet {sheet}: {'cropped' if imgs[0] else 'names only (no image yet)'}")
    html = open(HTML, encoding="utf-8").read()
    data = "const DECALS = " + json.dumps(decals, separators=(",", ":")) + ";"
    html, n = re.subn(r"/\*DECALS:START\*/.*?/\*DECALS:END\*/", lambda m: "/*DECALS:START*/" + data + "/*DECALS:END*/", html, flags=re.S)
    assert n == 1, "decal markers not found in keypad-planner.html"
    open(HTML, "w", encoding="utf-8").write(html)
    print(f"embedded {len(decals)} decals, page is {len(html) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
