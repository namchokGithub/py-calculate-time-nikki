# py-calculate-time-nikki
"A Python utility for calculating and managing time with ease."

py-calculate-time-nikki is a Python-based tool designed to simplify time calculations and management for energy Infinity Nikki.


### Deploy

```bash
pyinstaller --onefile --windowed --add-data "nikki-logo.png;." cal-time-nikki.py
```

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" --icon="assets/nikkicon.ico" cal-time-nikki.py
```

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" --icon="assets/nikkicon.ico" --clean cal-time-nikki.py
```