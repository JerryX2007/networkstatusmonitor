import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = "http://127.0.0.1:8000";
 
 type Monitor = {
 id: number;
 name: string;
 target: string;
 port: number;
 timeout: number;
 status: string | null;
 latency: number | null;
 last_checked: string | null;
 last_error: string | null;
 };


function App() {
  const [monitors, setMonitors] = useState<Monitor[]>([]);

  useEffect(() => {
    async function fetchMonitors() {
      const response = await fetch(`${API_BASE}/monitors`);
      const data = await response.json();
      setMonitors(data);
    }
    fetchMonitors();
  }, []);

  async function checkMonitor(id: number) {
    const response = await fetch(`${API_BASE}/monitors/${id}/check`, { method: "POST", });
    const result = await response.json();

    setMonitors((prevMonitors) => prevMonitors.map((monitor) => monitor.id === id ? {
      ...monitor,
      status: result.status,
      latency: result.latency,
      last_checked: result.checked_at,
      last_error: result.last_error,
    } : monitor));
  };

  return (
    <div>
      <h1>Network Status Monitor</h1>

      {monitors.length === 0 && <p>No monitors added yet.</p>}
      {monitors.map((monitor) => (
        <div key={monitor.id}>
          <h2>{monitor.name}</h2>
          <p>Target: {monitor.target}</p>
          <p>Port: {monitor.port}</p>
          <p>Status: {monitor.status ?? "Not checked yet"}</p>
          <p>
            Latency: {" "}
            {monitor.latency !== null ? `${monitor.latency} ms` : "Not checked yet"}
          </p>
          <p>Last checked: {monitor.last_checked ?? "Never"}</p>
          <p>Error: {monitor.last_error ?? "None"}</p>
          <button onClick={() => checkMonitor(monitor.id)}>
            Check now
          </button>
        </div>
      ))}
    </div>
  );
}

export default App
