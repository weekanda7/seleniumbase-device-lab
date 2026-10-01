import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Alert, Button, Dropdown, Input, Select, Space, Table, Typography } from "antd";
import type { TableColumnsType } from "antd";
import { MoreOutlined, PlusOutlined } from "@ant-design/icons";
import { useDebounce } from "use-debounce";
import { useTranslation } from "react-i18next";
import { api, ApiError, Device, DEVICE_STATUSES, DEVICE_TYPES, DeviceStatus, testId } from "../api";
import { useDeleteDevice } from "../useDeleteDevice";
import StatusTag from "../components/StatusTag";

// testid spec (List Page): column title tc-title-{col}, cell tc-{col} (repeats on every row).
// Rows have no testid: scope by row index or by text inside the row (antd also sets data-row-key=id).
function tc(column: string) {
  return {
    onHeaderCell: () => testId(`tc-title-${column}`),
    onCell: () => testId(`tc-${column}`),
  };
}

export default function DeviceListPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<DeviceStatus | undefined>();
  // Wait until the user stops typing for 400 ms before calling the API.
  const [debouncedSearch] = useDebounce(search.trim(), 400);

  const load = useCallback(() => {
    setLoading(true);
    setError("");
    api
      .listDevices({ q: debouncedSearch || undefined, status })
      .then(setDevices)
      .catch((err) => setError(err instanceof ApiError ? err.message : t("device.loadFailed")))
      .finally(() => setLoading(false));
  }, [debouncedSearch, status, t]);

  useEffect(load, [load]);

  const confirmDelete = useDeleteDevice(load);

  const columns: TableColumnsType<Device> = [
    {
      title: t("device.name"),
      dataIndex: "name",
      sorter: (a, b) => a.name.localeCompare(b.name),
      render: (name: string, d) => <Link to={`/devices/${d.id}`}>{name}</Link>,
      ...tc("name"),
    },
    {
      title: t("device.type"),
      dataIndex: "type",
      // Client-side column filter (header funnel icon); search + status go to the API.
      filters: DEVICE_TYPES.map((type) => ({ text: type, value: type })),
      onFilter: (value, d) => d.type === value,
      ...tc("type"),
    },
    {
      title: t("device.status"),
      dataIndex: "status",
      render: (s: DeviceStatus) => <StatusTag status={s} />,
      ...tc("status"),
    },
    {
      title: t("device.location"),
      dataIndex: "location",
      render: (loc: string) => loc || "—",
      ...tc("location"),
    },
    {
      // testid spec: row-end More icon -> more-button; its Dropdown options -> option-{action}
      key: "more",
      width: 64,
      render: (_, d) => (
        <Dropdown
          trigger={["click"]}
          menu={{
            items: [
              { key: "edit", label: <span data-testid="option-edit">{t("device.edit")}</span> },
              {
                key: "remove",
                danger: true,
                label: <span data-testid="option-remove">{t("device.delete")}</span>,
              },
            ],
            onClick: ({ key }) =>
              key === "edit" ? navigate(`/devices/${d.id}/edit`) : confirmDelete(d),
          }}
        >
          <Button
            type="text"
            icon={<MoreOutlined />}
            aria-label={t("device.more")}
            data-testid="more-button"
          />
        </Dropdown>
      ),
    },
  ];

  return (
    <section>
      <div className="page-header">
        <Typography.Title level={3} data-testid="page-title">
          {t("device.listTitle")}
        </Typography.Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          data-testid="add-device-button"
          onClick={() => navigate("/devices/new")}
        >
          {t("device.add")}
        </Button>
      </div>

      <Space className="toolbar" wrap>
        <Input.Search
          allowClear
          placeholder={t("device.searchPlaceholder")}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          data-testid="search-input"
          style={{ width: 260 }}
        />
        {/* The dropdown renders in a portal at the end of <body>; each option gets status-option. */}
        <Select
          data-testid="status-select"
          allowClear
          placeholder={t("status.all")}
          value={status}
          onChange={setStatus}
          options={DEVICE_STATUSES.map((s) => ({ value: s, label: t(`status.${s}`) }))}
          optionRender={(option) => <span data-testid="status-option">{option.label}</span>}
          style={{ width: 160 }}
        />
        <Typography.Text type="secondary" data-testid="total-num">
          {t("device.count", { count: devices.length })}
        </Typography.Text>
      </Space>

      {error && <Alert type="error" showIcon message={error} className="form-alert" />}

      <Table
        rowKey="id"
        columns={columns}
        dataSource={devices}
        loading={loading}
        pagination={{ pageSize: 5, showSizeChanger: false }}
      />
    </section>
  );
}
