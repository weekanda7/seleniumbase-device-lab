import { Link, Navigate, Outlet, Route, Routes, useNavigate } from "react-router-dom";
import { api, auth } from "./api";
import LoginPage from "./pages/LoginPage";
import DeviceListPage from "./pages/DeviceListPage";
import DeviceNewPage from "./pages/DeviceNewPage";
import DeviceDetailPage from "./pages/DeviceDetailPage";

// Pages behind login. No token -> redirect to /login.
function ProtectedLayout() {
  const navigate = useNavigate();
  if (!auth.get()) return <Navigate to="/login" replace />;

  async function logout() {
    await api.logout().catch(() => undefined);
    auth.clear();
    navigate("/login");
  }

  return (
    <>
      <header className="topbar">
        <Link to="/devices" className="brand">
          Device Lab
        </Link>
        <button className="secondary" data-testid="logout-button" onClick={logout}>
          Log out
        </button>
      </header>
      <main className="container">
        <Outlet />
      </main>
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedLayout />}>
        <Route path="/devices" element={<DeviceListPage />} />
        <Route path="/devices/new" element={<DeviceNewPage />} />
        <Route path="/devices/:id" element={<DeviceDetailPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/devices" replace />} />
    </Routes>
  );
}
