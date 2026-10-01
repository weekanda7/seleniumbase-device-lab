import i18n from "i18next";
import { initReactI18next } from "react-i18next";

export const LANG_KEY = "device-lab-lang";
export const LANGUAGES = [
  { value: "en", label: "EN" },
  { value: "zh-TW", label: "中文" },
];

const en = {
  app: { title: "Device Lab" },
  nav: { logout: "Log out" },
  common: {
    save: "Save",
    saving: "Saving…",
    cancel: "Cancel",
    back: "Back to devices",
    cannotReach: "Cannot reach the server",
  },
  login: {
    title: "Sign in",
    username: "Username",
    password: "Password",
    submit: "Log in",
    usernameRequired: "Please enter your username",
    passwordRequired: "Please enter your password",
    invalid: "Invalid username or password",
  },
  status: { online: "Online", offline: "Offline", all: "All statuses" },
  device: {
    listTitle: "Devices",
    add: "Add device",
    searchPlaceholder: "Search name or location",
    count_one: "{{count}} device",
    count_other: "{{count}} devices",
    name: "Name",
    type: "Type",
    status: "Status",
    location: "Location",
    actions: "Actions",
    created: "Created",
    edit: "Edit",
    delete: "Delete",
    more: "More actions",
    basicInfo: "Basic info",
    newTitle: "Add device",
    editTitle: "Edit device",
    nameRequired: "Please enter a device name",
    nameTooLong: "Name must be 50 characters or fewer",
    duplicate: "Device name '{{name}}' already exists",
    deleteConfirmTitle: "Delete {{name}}?",
    deleteConfirmContent: "This cannot be undone.",
    createdToast: "Device {{name}} created",
    updatedToast: "Device {{name}} updated",
    deletedToast: "Device {{name}} deleted",
    notFound: "Device not found",
    loadFailed: "Cannot load devices",
  },
};

const zhTW: typeof en = {
  app: { title: "Device Lab" },
  nav: { logout: "登出" },
  common: {
    save: "儲存",
    saving: "儲存中…",
    cancel: "取消",
    back: "回到裝置列表",
    cannotReach: "無法連線到伺服器",
  },
  login: {
    title: "登入",
    username: "帳號",
    password: "密碼",
    submit: "登入",
    usernameRequired: "請輸入帳號",
    passwordRequired: "請輸入密碼",
    invalid: "帳號或密碼錯誤",
  },
  status: { online: "上線", offline: "離線", all: "全部狀態" },
  device: {
    listTitle: "裝置",
    add: "新增裝置",
    searchPlaceholder: "搜尋名稱或位置",
    count_one: "共 {{count}} 台裝置",
    count_other: "共 {{count}} 台裝置",
    name: "名稱",
    type: "類型",
    status: "狀態",
    location: "位置",
    actions: "操作",
    created: "建立時間",
    edit: "編輯",
    delete: "刪除",
    more: "更多操作",
    basicInfo: "基本資訊",
    newTitle: "新增裝置",
    editTitle: "編輯裝置",
    nameRequired: "請輸入裝置名稱",
    nameTooLong: "名稱最多 50 個字",
    duplicate: "裝置名稱「{{name}}」已存在",
    deleteConfirmTitle: "確定刪除 {{name}}？",
    deleteConfirmContent: "刪除後無法復原。",
    createdToast: "已新增裝置 {{name}}",
    updatedToast: "已更新裝置 {{name}}",
    deletedToast: "已刪除裝置 {{name}}",
    notFound: "找不到這台裝置",
    loadFailed: "無法載入裝置",
  },
};

function initialLanguage(): string {
  try {
    const saved = localStorage.getItem(LANG_KEY);
    if (saved && LANGUAGES.some((l) => l.value === saved)) return saved;
  } catch {
    // storage blocked: fall back to English
  }
  return "en";
}

i18n.use(initReactI18next).init({
  resources: { en: { translation: en }, "zh-TW": { translation: zhTW } },
  lng: initialLanguage(),
  fallbackLng: "en",
  interpolation: { escapeValue: false }, // React already escapes
});

i18n.on("languageChanged", (lng) => {
  document.documentElement.lang = lng;
  try {
    localStorage.setItem(LANG_KEY, lng);
  } catch {
    // ignore
  }
});
document.documentElement.lang = i18n.language;

export default i18n;
