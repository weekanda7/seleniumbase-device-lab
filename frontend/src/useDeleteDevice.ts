import { useCallback } from "react";
import { App } from "antd";
import { useTranslation } from "react-i18next";
import { api, ApiError, Device, testId } from "./api";

/** Shared "delete with confirm dialog + toast" used by the list and detail pages.
 * testid spec: antd Modal container can't take a testid -> locate it by class
 * `dl-warning-modal`, then ant-modal-confirm-title / ant-modal-confirm-content inside.
 * Buttons inside are scoped by that container: delete-button / cancel-button. */
export function useDeleteDevice(onDeleted: (device: Device) => void) {
  const { modal, message } = App.useApp();
  const { t } = useTranslation();

  return useCallback(
    (device: Device) => {
      modal.confirm({
        className: "dl-warning-modal",
        title: t("device.deleteConfirmTitle", { name: device.name }),
        content: t("device.deleteConfirmContent"),
        okText: t("device.delete"),
        okButtonProps: { danger: true, ...testId("delete-button") },
        cancelButtonProps: testId("cancel-button"),
        // Returning a promise keeps the OK button in a loading state until it settles.
        onOk: async () => {
          try {
            await api.deleteDevice(device.id);
            message.success({
              content: t("device.deletedToast", { name: device.name }),
              className: "toast-success",
            });
            onDeleted(device);
          } catch (err) {
            message.error({
              content: err instanceof ApiError ? err.message : t("common.cannotReach"),
              className: "toast-error",
            });
          }
        },
      });
    },
    [modal, message, t, onDeleted],
  );
}
