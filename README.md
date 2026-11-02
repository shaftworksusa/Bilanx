# Honda S2000 Build Tracker

A small web app for tracking an S2000 build. It's plain HTML, CSS and JS, with no build step and no dependencies.

Open `index.html` in a browser, or serve the folder (`python3 -m http.server`) or host it on GitHub Pages.

## Features
- **Dashboard**: total spent against your budget, planned spend, installed part count, wrench hours, overdue service, spend by category
- **Parts**: name, category, brand, vendor, part #, cost, link and notes. Status goes planned → ordered → received → installed. Search, filter and a running total.
- **Maintenance**: a starter S2000 schedule (oil, MTF, diff, brake and clutch fluid, valves, plugs, coolant, soft top). Each item can be due by mileage, by months, or both. "Done" stamps today's date and mileage and writes a log entry.
- **Mod log**: dated entries with odometer, cost, hours and notes
- **To-do**: task list with priorities
- **Settings**: car details (AP1/AP2, VIN, budget, goal), JSON export/import, parts CSV export

Design notes for the custom intake are in [`docs/intake-pipe.md`](docs/intake-pipe.md). Project data from earlier chats is in `seed.js`. It loads on first open, or use **Settings → Merge project data**.

Data is saved in your browser's localStorage. Use **Export JSON** for backups or to move data to another device.

The maintenance intervals are common enthusiast intervals. Check them against your owner's or service manual.

## Keypad decal planner
[`tools/keypad-planner.html`](tools/keypad-planner.html) is an interactive previewer for the Haltech 3×5 (15-button) CAN keypad. You can:
- give each button a label, icon, function and on/off LED colour;
- light the buttons up in test mode;
- drag buttons to swap them;
- copy a real-size decal sheet as SVG.

Online version: https://claude.ai/artifact/AeJw85NEyf6m21DWZ6K1zA
