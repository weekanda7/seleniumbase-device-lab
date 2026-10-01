import { Tag } from "antd";
import { useTranslation } from "react-i18next";
import { DeviceStatus } from "../api";

// testid spec: status lamp -> status-{state}, e.g. status-online / status-offline
export default function StatusTag({ status }: { status: DeviceStatus }) {
  const { t } = useTranslation();
  return (
    <Tag color={status === "online" ? "green" : "default"} data-testid={`status-${status}`}>
      {t(`status.${status}`)}
    </Tag>
  );
}
