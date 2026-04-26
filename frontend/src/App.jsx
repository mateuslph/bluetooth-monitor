import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./auth/AuthContext";

function App() {
  const { token } = useAuth();

  return token ? (
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  ) : (
    <LoginPage />
  );
}

export default App;