import { useNavigate } from "react-router-dom";
import { App, Typography } from "antd";
import { useTranslation } from "react-i18next";
import { api, DeviceInput } from "../api";
import DeviceForm from "./DeviceForm";

export default function DeviceNewPage() {
  const navigate = useNavigate();
  const { message } = App.useApp();
  const { t } = useTranslation();

  async function create(values: DeviceInput) {
    const device = await api.createDevice(values);
    message.success({
      content: t("device.createdToast", { name: device.name }),
      className: "toast-success",
    });
    navigate("/devices");
  }

  return (
    <section>
      <Typography.Title level={3} data-testid="page-title">
        {t("device.newTitle")}
      </Typography.Title>
      <DeviceForm cancelTo="/devices" onSubmit={create} />
    </section>
  );
}
