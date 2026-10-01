import { Segmented } from "antd";
import { useTranslation } from "react-i18next";
import { LANGUAGES } from "../i18n";

// testid spec: two-state toggle -> language-switch; each choice -> {value}-radio
export default function LanguageSwitch() {
  const { i18n } = useTranslation();
  return (
    <Segmented
      data-testid="language-switch"
      size="small"
      options={LANGUAGES.map((l) => ({
        value: l.value,
        label: <span data-testid={`${l.value.toLowerCase()}-radio`}>{l.label}</span>,
      }))}
      value={i18n.language}
      onChange={(lng) => i18n.changeLanguage(String(lng))}
    />
  );
}
