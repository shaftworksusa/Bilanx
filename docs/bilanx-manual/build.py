import base64, pathlib, sys

here = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
tpl = (here / "template.html").read_text()
logo = base64.b64encode((here / "logo.jpg").read_bytes()).decode()

INFO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" '
        'stroke="var(--teal-ink)" stroke-width="2"/><rect x="11" y="10" width="2" height="7" fill="var(--teal-ink)"/>'
        '<rect x="11" y="6.5" width="2" height="2" fill="var(--teal-ink)"/></svg>')
WARN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8 22.5 21H1.5Z" fill="none" '
        'stroke="var(--warn)" stroke-width="2" stroke-linejoin="round"/><rect x="11" y="9" width="2" height="6.5" '
        'fill="var(--warn)"/><rect x="11" y="17" width="2" height="2" fill="var(--warn)"/></svg>')


def scale():
    x0, x1 = 24, 696
    X = lambda c: x0 + (x1 - x0) * c / 32
    s = ['<svg viewBox="0 0 720 112" xmlns="http://www.w3.org/2000/svg">']
    segs = [(4, 12, "var(--ink)", 1, "Racing Slicks"),
            (12, 24, "var(--teal-ink)", 1, "Track Day"),
            (24, 32, "var(--teal)", 1, "Driving Home")]
    for a, b, col, op, name in segs:
        s.append(f'<rect x="{X(a)+1:.1f}" y="30" width="{X(b)-X(a)-2:.1f}" height="16" fill="{col}" fill-opacity="{op}"/>')
        s.append(f'<text x="{(X(a)+X(b))/2:.1f}" y="22" text-anchor="middle" font-size="13" font-weight="700" '
                 f'fill="var(--ink)" font-family="Source Sans 3, sans-serif">{name}</text>')
    s.append(f'<line x1="{x0}" x2="{x1}" y1="54" y2="54" stroke="var(--ink)" stroke-width="1.5"/>')
    for c in range(33):
        h = 10 if c % 4 == 0 else 5
        s.append(f'<line x1="{X(c):.1f}" x2="{X(c):.1f}" y1="54" y2="{54+h}" stroke="var(--ink-soft)" stroke-width="1"/>')
    for c in (0, 4, 12, 24, 32):
        s.append(f'<text x="{X(c):.1f}" y="80" text-anchor="middle" font-size="13" font-weight="700" '
                 f'fill="var(--ink)" font-family="JetBrains Mono, monospace">{c}</text>')
    s.append(f'<text x="{x0}" y="100" font-size="12" fill="var(--ink-soft)" font-family="Source Sans 3, sans-serif">Full firm</text>')
    s.append(f'<text x="{x1}" y="100" text-anchor="end" font-size="12" fill="var(--ink-soft)" font-family="Source Sans 3, sans-serif">Full soft</text>')
    s.append('</svg>')
    return "".join(s)


def groove():
    edge = "var(--ink)"
    g = 330

    def damper(c, m, exposed):
        p = [f'<rect x="{c-11}" y="84" width="22" height="60" fill="none" stroke="{edge}" stroke-width="1.25"/>',
             f'<rect x="{c-23}" y="144" width="46" height="{m-144}" rx="3" fill="none" stroke="{edge}" stroke-width="1.25"/>']
        for i in range((m - 204) // 4):
            p.append(f'<line x1="{c-23}" x2="{c+23}" y1="{204+i*4}" y2="{206+i*4}" stroke="{edge}" stroke-width="0.5"/>')
        p += [f'<rect x="{c-31}" y="{m}" width="62" height="8" rx="1.5" fill="none" stroke="{edge}" stroke-width="1.25"/>',
              f'<rect x="{c-28}" y="{m+8}" width="56" height="70" rx="4" fill="none" stroke="{edge}" stroke-width="1.25"/>',
              f'<circle cx="{c}" cy="{m+56}" r="10" fill="none" stroke="{edge}" stroke-width="1.25"/>',
              f'<circle cx="{c}" cy="{m+56}" r="4.5" fill="none" stroke="{edge}" stroke-width="1.25"/>']
        if exposed:
            p.append(f'<line x1="{c-23}" x2="{c+23}" y1="{g}" y2="{g}" stroke="var(--warn)" stroke-width="2.5"/>')
        else:
            p.append(f'<line x1="{c-23}" x2="{c+23}" y1="{g}" y2="{g}" stroke="var(--teal-ink)" stroke-width="2" stroke-dasharray="4 3"/>')
        return "".join(p)

    t = lambda x, y, s, anchor="start", fill="var(--ink-soft)", w=400, size=12: (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{fill}" '
        f'font-family="Source Sans 3, sans-serif">{s}</text>')
    cl, cr = 200, 520
    s = ['<svg viewBox="0 0 760 440" xmlns="http://www.w3.org/2000/svg">',
         t(cl, 62, "OK: groove covered", "middle", "var(--teal-ink)", 700, 15),
         t(cr, 62, "Too far: groove exposed", "middle", "var(--warn)", 700, 15),
         damper(cl, 316, False), damper(cr, 340, True),
         t(cl - 34, 184, "Damper body", "end"), t(cl - 40, 324, "Lock ring", "end"),
         t(cl - 40, 366, "Lower mount", "end"), t(cl + 40, 334, "Groove inside mount", fill="var(--ink)"),
         t(cr + 40, 326, "Machined groove visible", fill="var(--warn)", w=700),
         t(cr + 40, 342, "Wind the mount back up", fill="var(--ink)"),
         '</svg>']
    return "".join(s)


html = (tpl.replace("{{LOGO}}", logo).replace("{{INFO}}", INFO).replace("{{WARN}}", WARN)
        .replace("{{SCALE}}", scale()).replace("{{GROOVE}}", groove()))
out.write_text(html)
print(len(html))
