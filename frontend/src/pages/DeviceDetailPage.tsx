import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Alert, Breadcrumb, Button, Card, Descriptions, Skeleton, Space, Typography } from "antd";
import { ArrowLeftOutlined, DeleteOutlined, EditOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { api, ApiError, Device } from "../api";
import { useDeleteDevice } from "../useDeleteDevice";
import StatusTag from "../components/StatusTag";
import FieldLabel from "../components/FieldLabel";

export default function DeviceDetailPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
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

  const goToList = useCallback(() => navigate("/devices"), [navigate]);
  const confirmDelete = useDeleteDevice(goToList);

  return (
    <section>
      {/* testid spec (Detail Page): breadcrumb-link / breadcrumb-name, back-icon-button */}
      <Space className="detail-nav">
        <Button
          type="text"
          icon={<ArrowLeftOutlined />}
          aria-label={t("common.back")}
          data-testid="back-icon-button"
          onClick={goToList}
        />
        <Breadcrumb
          items={[
            {
              title: (
                <Link to="/devices" data-testid="breadcrumb-link">
                  {t("device.listTitle")}
                </Link>
              ),
            },
            ...(device
              ? [{ title: <span data-testid="breadcrumb-name">{device.name}</span> }]
              : []),
          ]}
        />
      </Space>
      {error && <Alert type="error" showIcon message={error} className="form-alert" />}
      {!device && !error && <Skeleton active />}
      {device && (
        <>
          <div className="page-header">
            <Typography.Title level={3} data-testid="page-title">
              {device.name}
            </Typography.Title>
            <Button
              danger
              icon={<DeleteOutlined />}
              data-testid="delete-button"
              onClick={() => confirmDelete(device)}
            >
              {t("device.delete")}
            </Button>
          </div>
          <Card
            className="detail-card"
            title={<span data-testid="basic-info-title">{t("device.basicInfo")}</span>}
            extra={
              <Button
                type="text"
                icon={<EditOutlined />}
                aria-label={t("device.edit")}
                data-testid="basic-info-edit-button"
                onClick={() => navigate(`/devices/${device.id}/edit`)}
              />
            }
          >
            {/* Read-only field trio: {name}-field (title) + {name} (value) */}
            <Descriptions column={1} size="small">
              <Descriptions.Item label={<FieldLabel name="type">{t("device.type")}</FieldLabel>}>
                <span data-testid="type">{device.type}</span>
              </Descriptions.Item>
              <Descriptions.Item
                label={<FieldLabel name="status">{t("device.status")}</FieldLabel>}
              >
                <StatusTag status={device.status} />
              </Descriptions.Item>
              <Descriptions.Item
                label={<FieldLabel name="location">{t("device.location")}</FieldLabel>}
              >
                <span data-testid="location">{device.location || "—"}</span>
              </Descriptions.Item>
              <Descriptions.Item
                label={<FieldLabel name="created">{t("device.created")}</FieldLabel>}
              >
                <span data-testid="created">
                  {new Date(device.created_at).toLocaleString(i18n.language)}
                </span>
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </>
      )}
    </section>
  );
}
