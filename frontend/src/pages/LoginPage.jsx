import { useState } from "react";
import { useAuth } from "../auth/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();

      if (res.ok) {
        login(data.token);
        setMsg("Login OK");
      } else {
        setMsg(data.msg);
      }

    } catch {
      setMsg("Erro ao conectar backend");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Login</h1>

      <input placeholder="Usuário" onChange={e => setUsername(e.target.value)} />
      <br /><br />
      <input type="password" placeholder="Senha" onChange={e => setPassword(e.target.value)} />
      <br /><br />

      <button onClick={handleLogin}>Entrar</button>

      <p>{msg}</p>
    </div>
  );
}