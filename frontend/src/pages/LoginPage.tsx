import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Alert, Button, Card, Form, Input, Typography } from "antd";
import { useTranslation } from "react-i18next";
import { api, ApiError, auth } from "../api";
import LanguageSwitch from "../components/LanguageSwitch";
import FieldLabel from "../components/FieldLabel";
import VersionInfo from "../components/VersionInfo";

type LoginValues = { username: string; password: string };

export default function LoginPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (auth.get()) return <Navigate to="/devices" replace />;

  async function onFinish(values: LoginValues) {
    setError("");
    setSubmitting(true);
    try {
      const { access_token } = await api.login(values.username, values.password);
      auth.set(access_token);
      navigate("/devices");
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 401
          ? t("login.invalid")
          : t("common.cannotReach"),
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <Card className="login-card" extra={<LanguageSwitch />} title={t("app.title")}>
        <Typography.Title level={4} data-testid="page-title">
          {t("login.title")}
        </Typography.Title>
        <Form name="login" layout="vertical" onFinish={onFinish} requiredMark={false}>
          <Form.Item
            label={<FieldLabel name="username">{t("login.username")}</FieldLabel>}
            name="username"
            rules={[{ required: true, message: t("login.usernameRequired") }]}
          >
            <Input autoComplete="username" data-testid="username-input" />
          </Form.Item>
          <Form.Item
            label={<FieldLabel name="password">{t("login.password")}</FieldLabel>}
            name="password"
            rules={[{ required: true, message: t("login.passwordRequired") }]}
          >
            <Input.Password autoComplete="current-password" data-testid="password-input" />
          </Form.Item>
          {/* testid spec: red error Alert gets no testid; tests assert on its text. */}
          {error && <Alert type="error" showIcon message={error} className="form-alert" />}
          {/* Button text changes with the language, so it gets a testid (spec: unstable text). */}
          <Button
            type="primary"
            htmlType="submit"
            block
            loading={submitting}
            data-testid="login-button"
          >
            {t("login.submit")}
          </Button>
        </Form>
      </Card>
      <VersionInfo />
    </main>
  );
}
