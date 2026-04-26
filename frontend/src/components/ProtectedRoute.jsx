import { useAuth } from "../auth/AuthContext";

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();

  if (!token) {
    return <h2>Acesso negado. Faça login.</h2>;
  }

  return children;
}