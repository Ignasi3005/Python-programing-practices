# 991Ex — Scientific & Symbolic Calculator (PySide6)

Minimal scaffold for an fx-991EX–style desktop calculator with symbolic algebra via SymPy.

Requirements
- Python 3.11+
- See `requirements.txt` (PySide6, SymPy)

Quick start
1. Create & activate a venv:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
2. Install dependencies: `pip install -r requirements.txt`
3. Run app: `python src/991ex/main.py`

Features (scaffold)
- Expression bar, history pane, numeric & symbolic evaluation (simplify, diff, integrate, solve)
- Dark theme (default) with switchable option planned

Next steps
- Implement full fx-991EX parity (modes, matrices, statistics), more symbolic commands, and packaging with PyInstaller.

Contributing
- Open issues for features/bugs and contributions are welcome.