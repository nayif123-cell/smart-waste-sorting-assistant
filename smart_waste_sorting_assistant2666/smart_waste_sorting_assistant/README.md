# Smart Waste Sorting Assistant

A mobile-friendly, Python + Flask web app for a college Tech Fest. Visitors can enter an item, view its likely category and recommended disposal route, and open a **Why?** explanation.

## Features
- Flask backend written in Python
- Responsive website for phones and computers
- Expanded catalogue with 50 examples each for six categories (300 category examples), plus the original common items
- Database of recyclable, organic, residual, hazardous/special, e-waste, textile and bulky items
- Search aliases such as `bottle`, `phone`, `charger`, `tin can`, and `banana`
- “Why?” explanation and disposal instructions
- Unknown-item fallback instead of guessing
- Simple health endpoint at `/health`

## Run on your computer
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the website:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

To test from a phone on the same Wi-Fi, run Flask with `app.run(host="0.0.0.0", port=5000)` and open `http://YOUR-COMPUTER-LAN-IP:5000` on the phone. Your firewall may ask for permission.

## Deploy it online
This is a **Python Flask** app, so GitHub Pages alone cannot run it (GitHub Pages serves static files, not a live Python server). Deploy it to a Python-compatible host such as Render, Railway, or PythonAnywhere.

For a typical Render deployment:
1. Push this folder to a GitHub repository.
2. Create a new **Web Service** from that repository in Render.
3. Choose Python as the runtime.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy. If the host requires a `Procfile`, add one containing `web: gunicorn app:app`.

For production, add `gunicorn` to `requirements.txt` or use the included optional file `requirements-production.txt` and install that instead.

## Important
Waste rules and bin colours vary by city and service provider. This app is an educational guide; check local municipality instructions. Batteries, medicines, lamps and electronic devices should be taken to appropriate authorised collection points, not put in ordinary household bins.
