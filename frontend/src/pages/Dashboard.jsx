import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";

export default function Dashboard() {
  const { token, logout } = useAuth();

  const [logs, setLogs] = useState([]);
  const [chartData, setChartData] = useState([]);

  const fetchLogs = async () => {
    try {
      const res = await fetch("/api/logs", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();
      setLogs(data);

      // transforma logs em dados de gráfico
      const grouped = {};

      data.forEach(log => {
        const time = new Date(log.datetime).toLocaleTimeString();

        if (!grouped[time]) {
          grouped[time] = 0;
        }
        grouped[time]++;
      });

      const chart = Object.keys(grouped).map(key => ({
        time: key,
        value: grouped[key]
      }));

      setChartData(chart);

    } catch (err) {
      console.error(err);
    }
  };

  // Atualização automática
  useEffect(() => {
    fetchLogs();

    const interval = setInterval(fetchLogs, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard em Tempo Real</h1>

      <button onClick={logout}>Sair</button>

      <h2>Eventos por Tempo</h2>

      <LineChart width={600} height={300} data={chartData}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" />
      </LineChart>

      <h2>Logs</h2>

      <ul>
        {logs.map(log => (
          <li key={log.id}>
            [{log.level}] {log.message}
          </li>
        ))}
      </ul>
    </div>
  );
}