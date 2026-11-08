# Bilanx Owners Manual

Owner's manual for Shaftworks USA Bilanx coilovers (ONE, P2 and P3): kit contents, mounting, ride height and travel, damper adjustment, remote reservoir quick disconnect, setup data, service schedule and tuning guide.

- **PDF:** [`Bilanx-Owners-Manual.pdf`](Bilanx-Owners-Manual.pdf), US Letter, 8 pages. Each section stays whole on its page.
- **Web version:** [`bilanx-manual.html`](bilanx-manual.html), also published at https://claude.ai/artifact/FpdBWzjj3kVxyFdxT3CUUo
- **On the store:** linked from every Bilanx coilover product page. The link is https://cdn.shopify.com/s/files/1/0497/4919/6967/files/Bilanx_Suspension_Manual.pdf. The file keeps its old name so existing links keep working.

## Editing

Edit `template.html`, then rebuild:

```bash
python3 build.py . bilanx-manual.html
```

`build.py` inlines the logo and draws the info/warning icons, the click ruler and the lower-mount groove illustration.

To make the PDF, use Node with Playwright and Chromium installed:

```bash
node pdf.js bilanx-manual.html Bilanx-Owners-Manual.pdf
```

Page breaks for print are set in `template.html` (`.pb` marks a new page; see the `@media print` block). After a content change, check that no section splits across pages.

## Key values

| Setting | Value |
| --- | --- |
| Adjuster counting | From full firm (0), counterclockwise |
| Bilanx ONE | 1 adjuster, 32 clicks |
| Bilanx P2 | Rebound 32, compression 22 |
| Bilanx P3 | Rebound 32, low-speed compression 25, high-speed compression 17 |
| Reservoir nitrogen charge | 180 psi, damper at full droop |
| Minimum bump travel / droop | 35 mm / 50 mm |
| Rebound starting points | Racing slicks 4–12, track day 12–24, driving home 24–32 |
| Service | Competition every 2 years; racing 2–5 years; street every 18,000 miles or 5 years |
