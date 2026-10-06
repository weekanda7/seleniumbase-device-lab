import { Navigate, Outlet, Route, Routes, useNavigate, Link } from "react-router-dom";
import { Button, Layout, Space } from "antd";
import { LogoutOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { api, auth } from "./api";
import LanguageSwitch from "./components/LanguageSwitch";
import VersionInfo from "./components/VersionInfo";
import LoginPage from "./pages/LoginPage";
import DeviceListPage from "./pages/DeviceListPage";
import DeviceNewPage from "./pages/DeviceNewPage";
import DeviceEditPage from "./pages/DeviceEditPage";
import DeviceDetailPage from "./pages/DeviceDetailPage";

// Pages behind login. No token -> redirect to /login.
function ProtectedLayout() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  if (!auth.get()) return <Navigate to="/login" replace />;

  async function logout() {
    await api.logout().catch(() => undefined);
    auth.clear();
    navigate("/login");
  }

  return (
    <Layout className="app-layout">
      <Layout.Header className="topbar">
        <Link to="/devices" className="brand" id="logo">
          {t("app.title")}
        </Link>
        <Space>
          <LanguageSwitch />
          <Button icon={<LogoutOutlined />} data-testid="logout-button" onClick={logout}>
            {t("nav.logout")}
          </Button>
        </Space>
      </Layout.Header>
      <Layout.Content className="container">
        <Outlet />
      </Layout.Content>
      <Layout.Footer className="app-footer">
        <VersionInfo />
      </Layout.Footer>
    </Layout>
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
        <Route path="/devices/:id/edit" element={<DeviceEditPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/devices" replace />} />
    </Routes>
  );
}
