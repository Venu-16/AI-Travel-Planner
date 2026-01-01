# AI Travel Planner

A simple full-stack sample app that suggests travel itineraries using AI. The project includes a Flask backend and a React frontend to collect user preferences and display results.

## Features ✅

- Enter travel preferences and receive itinerary suggestions
- Simple REST API backend (Flask)
- React frontend with components for auth, form, and results

## Tech stack ��

- Backend: Python, Flask
- Frontend: React, Vite/Create React App (check `frontend/package.json`)
- API: REST

## Repo structure

- `Backend/` – Flask app and Python dependencies
  - `app.py` – main Flask server
  - `requirements.txt`
- `frontend/` – React app
  - `src/` – components and pages
  - `public/` – static files

## Local setup (development) ⚙️

Prerequisites:
- Node.js (v16+ recommended)
- npm or yarn
- Python 3.10+

1. Backend

```bash
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# run server
export FLASK_APP=app.py
flask run
```

2. Frontend

```bash
cd frontend
npm install
npm start
```

Open your browser at http://localhost:3000 (or the port shown by the dev server).

## API / Usage

- Update frontend to point at the backend server (see `frontend/src/services/api.js`).
- The app sends user travel preferences to the backend which returns an itinerary.

## Testing

- Add unit/integration tests for backend and frontend as needed.

## Contributing

Contributions are welcome — open a PR or an issue describing your changes.

## License

MIT

