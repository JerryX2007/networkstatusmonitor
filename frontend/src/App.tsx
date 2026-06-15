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
      const response = await fetch("${API_BASE}/monitors");
      const data = await response.json();
      setMonitors(data);
    }
    fetchMonitors();
  }, []);

  return (
    <div>
      <h1>Network Status monitor</h1>

      {monitors.length === 0 && <p>No monitors added yet.</p>}
      {monitors.map((monitor) => (
        <div key={monitor.id}>
          <h2>{monitor.name}</h2>
          <p>Target: {monitor.target}</p>
          <p>Port: {monitor.port}</p>
          <p>Status: {monitor.status ?? "Not checked yet"}</p>
          <p>Latency: {monitor.latency ?? "Not checked yet"}</p>

        </div>
      ))}
    </div>
  )
}

export default App
