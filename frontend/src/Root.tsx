import { BrowserRouter } from "react-router-dom";
import { App as AntApp, ConfigProvider } from "antd";
import enUS from "antd/locale/en_US";
import zhTW from "antd/locale/zh_TW";
import { useTranslation } from "react-i18next";
import App from "./App";

// antd's own texts (pagination, modal buttons, empty table) follow the app language.
export default function Root() {
  const { i18n } = useTranslation();
  return (
    <ConfigProvider
      locale={i18n.language === "zh-TW" ? zhTW : enUS}
      theme={{ token: { colorPrimary: "#2459d6", borderRadius: 6 } }}
    >
      {/* AntApp provides message / modal via App.useApp() */}
      <AntApp>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </AntApp>
    </ConfigProvider>
  );
}
