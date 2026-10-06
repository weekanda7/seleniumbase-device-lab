import { useEffect, useState } from "react";
import { Typography } from "antd";
import { useTranslation } from "react-i18next";
import { api, type VersionInfo as Version } from "../api";

// Web version is baked into the bundle at build time; API version comes from GET /api/version.
// Showing both makes a front-end / back-end version mismatch visible at a glance.
const WEB: Version = {
  version: import.meta.env.VITE_APP_VERSION || "dev",
  commit: import.meta.env.VITE_GIT_SHA || "unknown",
};

const format = (v: Version) => `${v.version} (${v.commit})`;

export default function VersionInfo() {
  const { t } = useTranslation();
  const [apiVersion, setApiVersion] = useState("…");

  useEffect(() => {
    api
      .getVersion()
      .then((v) => setApiVersion(format(v)))
      .catch(() => setApiVersion("—"));
  }, []);

  return (
    <Typography.Text type="secondary" className="version-info" data-testid="version-area">
      {t("version.web")} <span data-testid="web-version">{format(WEB)}</span>
      {" · "}
      {t("version.api")} <span data-testid="api-version">{apiVersion}</span>
    </Typography.Text>
  );
}
