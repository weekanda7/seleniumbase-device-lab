import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Alert, App, Skeleton, Typography } from "antd";
import { useTranslation } from "react-i18next";
import { api, ApiError, Device, DeviceInput } from "../api";
import DeviceForm from "./DeviceForm";

export default function DeviceEditPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { message } = App.useApp();
  const { t } = useTranslation();
  const [device, setDevice] = useState<Device | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getDevice(id)
      .then(setDevice)
      .catch((err) =>
        setError(
          err instanceof ApiError && err.status === 404
            ? t("device.notFound")
            : t("device.loadFailed"),
        ),
      );
  }, [id, t]);

  async function save(values: DeviceInput) {
    if (!device) return;
    const updated = await api.updateDevice(device.id, values);
    message.success({
      content: t("device.updatedToast", { name: updated.name }),
      className: "toast-success",
    });
    navigate(`/devices/${updated.id}`);
  }

  return (
    <section>
      <Typography.Title level={3} data-testid="page-title">
        {t("device.editTitle")}
      </Typography.Title>
      {error && <Alert type="error" showIcon message={error} />}
      {!device && !error && <Skeleton active />}
      {device && (
        <DeviceForm
          initialValues={{
            name: device.name,
            type: device.type,
            status: device.status,
            location: device.location,
          }}
          cancelTo={`/devices/${device.id}`}
          onSubmit={save}
        />
      )}
    </section>
  );
}
