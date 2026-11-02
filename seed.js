/* Project data brought in from earlier S2000 chats.
   It loads automatically on first open. If you already have data, use Settings → "Merge project data". */
window.S2000_SEED = {
  car: {
    goal: 'Street build: custom 3D-printed 3.5" intake with a 74 mm Bosch throttle body',
  },
  parts: [
    { name: 'Bosch 74 mm throttle body', category: 'Intake', brand: 'Bosch', status: 'received', cost: '',
      notes: 'Inlet lip: 80 mm OD, 15 mm long, 74 mm bore. No adapter; coupler goes directly on the lip.' },
    { name: '3.5" intake pipe, 3D-printed (3 sections)', category: 'Intake', brand: 'Custom', status: 'planned', cost: '',
      notes: '6" bellmouth at the filter end. Throttle end (section 3): 80 mm OD × 74 mm bore spigot, 50 mm long, 1.5 mm bead 12 mm from the end, 45° coupler stop. STLs come smooth and dimpled.' },
    { name: 'PA6-CF filament', category: 'Intake', status: 'planned', cost: '',
      notes: 'Material for the intake pipe sections' },
    { name: 'Silicone coupler, straight 80 mm ID', category: 'Intake', status: 'planned', cost: '',
      notes: '4-ply, 50–65 mm (2–2.5") long. Joins the pipe spigot to the throttle body lip with no step.' },
    { name: 'T-bolt clamps (×2), 80 mm coupler', category: 'Intake', status: 'planned', cost: '',
      notes: 'Throttle side centred on the 15 mm lip; pipe side between the bead and the shoulder' },
    { name: 'Intake pipe support bracket + rubber isolators', category: 'Intake', status: 'planned', cost: '',
      notes: 'Mount near the bend so the short coupler joint doesn’t carry the pipe’s weight or engine rock' },
  ],
  log: [
    { date: '2026-10-26', title: 'Intake pipe: section 3 rebuilt for the Bosch 74 mm throttle body', cost: '', hours: '',
      notes: 'Throttle-end spigot changed to 80 mm OD / 74 mm bore to match the throttle body lip, so one straight 80 mm coupler fits with no internal step. Bore tapers 85.6 → 74 mm over the last 80 mm. Sections 1–2 and the bellmouth unchanged. All parts checked watertight.' },
  ],
  todos: [
    { text: 'Dry PA6-CF at 80 °C for 8–12 h (70 °C: 12–24 h); print from a dry box at 45–55 °C, <15–20% RH', priority: 1, done: false },
    { text: 'Print intake sections 1–3 from the latest STLs (intake_pipe_3.5in.zip)', priority: 1, done: false },
    { text: 'Buy a straight 80 mm ID 4-ply silicone coupler (50–65 mm long) and 2 T-bolt clamps', priority: 2, done: false },
    { text: 'Make the intake pipe bracket with rubber isolators near the bend', priority: 2, done: false },
    { text: 'Test fit: pipe end within 2–3 mm of the throttle body face inside the coupler', priority: 2, done: false },
  ],
};
