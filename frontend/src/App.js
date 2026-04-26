import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [logs, setLogs] = useState([]);
  const [token, setToken] = useState("");

  useEffect(() => {
    axios.post("http://localhost:5000/login", {
      user: "admin",
      password: "123"
    }).then(res => setToken(res.data.token));
  }, []);

  useEffect(() => {
    if (token) {
      axios.get("http://localhost:5000/logs", {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setLogs(res.data));
    }
  }, [token]);

  return (
    <div style={{ background: "#111", color: "#fff", padding: 20 }}>
      <h1>Bluetooth Dashboard</h1>
      {logs.map((l, i) => (
        <div key={i}>{l[1]} | {l[2]} | {l[3]}</div>
      ))}
    </div>
  );
}

export default App;