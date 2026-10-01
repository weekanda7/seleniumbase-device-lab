import { useState } from "react";
import { Link } from "react-router-dom";
import { Alert, Button, Card, Form, Input, Radio, Select, Space } from "antd";
import { useTranslation } from "react-i18next";
import { ApiError, DEVICE_STATUSES, DEVICE_TYPES, DeviceInput } from "../api";
import FieldLabel from "../components/FieldLabel";

type Props = {
  initialValues?: Partial<DeviceInput>;
  cancelTo: string;
  onSubmit: (values: DeviceInput) => Promise<void>;
};

/** Shared by "Add device" and "Edit device". testids follow .claude/skills/testid-spec. */
export default function DeviceForm({ initialValues, cancelTo, onSubmit }: Props) {
  const { t } = useTranslation();
  const [form] = Form.useForm<DeviceInput>();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function onFinish(values: DeviceInput) {
    setError("");
    setSaving(true);
    try {
      await onSubmit({ ...values, location: values.location ?? "" });
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        // Duplicate name: show it under the Name field, like client-side validation.
        form.setFields([{ name: "name", errors: [t("device.duplicate", { name: values.name })] }]);
      } else {
        setError(err instanceof ApiError ? err.message : t("common.cannotReach"));
      }
      setSaving(false);
    }
  }

  return (
    <Card>
      <Form
        form={form}
        name="device"
        layout="vertical"
        initialValues={{ type: DEVICE_TYPES[0], status: "online", location: "", ...initialValues }}
        onFinish={onFinish}
      >
        <Form.Item
          label={<FieldLabel name="name">{t("device.name")}</FieldLabel>}
          name="name"
          rules={[
            { required: true, whitespace: true, message: t("device.nameRequired") },
            { max: 50, message: t("device.nameTooLong") },
          ]}
        >
          <Input data-testid="name-input" />
        </Form.Item>
        <Form.Item
          label={<FieldLabel name="type">{t("device.type")}</FieldLabel>}
          name="type"
          rules={[{ required: true }]}
        >
          {/* The dropdown renders in a portal at the end of <body>; each option gets type-option. */}
          <Select
            data-testid="type-select"
            options={DEVICE_TYPES.map((type) => ({ value: type, label: type }))}
            optionRender={(option) => <span data-testid="type-option">{option.label}</span>}
          />
        </Form.Item>
        <Form.Item
          label={<FieldLabel name="status">{t("device.status")}</FieldLabel>}
          name="status"
        >
          <Radio.Group>
            {DEVICE_STATUSES.map((s) => (
              <Radio key={s} value={s} data-testid={`${s}-radio`}>
                {t(`status.${s}`)}
              </Radio>
            ))}
          </Radio.Group>
        </Form.Item>
        <Form.Item
          label={<FieldLabel name="location">{t("device.location")}</FieldLabel>}
          name="location"
        >
          <Input maxLength={100} data-testid="location-input" />
        </Form.Item>
        {error && <Alert type="error" showIcon message={error} className="form-alert" />}
        <Space>
          <Button type="primary" htmlType="submit" loading={saving} data-testid="save-button">
            {t("common.save")}
          </Button>
          <Link to={cancelTo}>
            <Button data-testid="cancel-button">{t("common.cancel")}</Button>
          </Link>
        </Space>
      </Form>
    </Card>
  );
}
