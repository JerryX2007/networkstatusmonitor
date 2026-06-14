Network Status Monitor

A full-stack network monitoring application that allows users to track the availability, latency, uptime, check history, and outage incidents of websites, IP addresses, and services.

The project uses a FastAPI backend, SQLite database, and React + TypeScript frontend.

Features
- Create, read, update, and delete network monitors
- Check whether a target and port are online or offline
- Measure latency in milliseconds
- Store check history in SQLite
- Calculate uptime statistics
- Track outage incidents automatically
- View ongoing and resolved incidents
- Validate monitor input fields
- Explore API routes through FastAPI documentation
Tech Stack:
Backend
Python
FastAPI
SQLite
Pydantic
Uvicorn
Frontend
React
TypeScript
Vite
Project Structure
networkstatusmonitor/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   └── monitors.py
│   └── monitor.db
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
Backend API Routes
General
Method	Endpoint	Description
GET	/	Confirms the API is running
Monitors
Method	Endpoint	Description
POST	/monitors	Create a new monitor
GET	/monitors	Get all monitors
GET	/monitors/{monitor_id}	Get one monitor
PUT	/monitors/{monitor_id}	Update a monitor
DELETE	/monitors/{monitor_id}	Delete a monitor
POST	/monitors/{monitor_id}/check	Run a manual status check
GET	/monitors/{monitor_id}/history	Get check history for a monitor
GET	/monitors/{monitor_id}/stats	Get uptime and latency statistics
GET	/monitors/{monitor_id}/incidents	Get outage incidents for a monitor
Example Monitor Request
{
  "name": "Google",
  "target": "google.com",
  "port": 80,
  "timeout": 3.0
}
Example Check Response
{
  "id": 1,
  "monitor_id": 1,
  "status": "online",
  "latency": 24.52,
  "checked_at": "2026-06-14 10:30:00",
  "last_error": null
}
Example Stats Response
{
  "total_checks": 10,
  "online_checks": 8,
  "offline_checks": 2,
  "avg_latency": 25.13,
  "uptime_percentage": 80.0
}
How to Run Locally
1. Clone the repository
git clone <your-repository-url>
cd networkstatusmonitor
2. Run the backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn pydantic
python -m uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000

FastAPI documentation is available at:

http://127.0.0.1:8000/docs
3. Run the frontend

Open a new terminal:

cd frontend
npm install
npm run dev

The frontend will usually run at:

http://localhost:5173
Database

The backend uses SQLite for local persistence.

The database includes three main tables:

monitors

Stores monitor configuration and the latest status.

check_history

Stores every status check result.

incidents

Stores outage incidents, including ongoing and resolved outages.

Current Status

The backend API is functional and includes monitor management, manual checks, history tracking, statistics, and incident tracking.

The frontend is currently being developed with React and TypeScript.

Future Improvements
Add automatic background checks
Add a React dashboard for monitor cards and status display
Add charts for latency and uptime history
Add user authentication
Add Docker support
Add automated tests with pytest
Deploy the backend and frontend
Improve UI styling and responsiveness
Purpose

This project was built to practice full-stack software engineering concepts, including REST API design, database persistence, backend validation, frontend development, and system monitoring logic.