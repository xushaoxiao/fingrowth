export const THEMES = [
  { id: "default", label: "Default", accent: "#1b725a" },
  { id: "tesla", label: "Tesla", accent: "#e82127" },
  { id: "nvidia", label: "NVIDIA", accent: "#76b900" },
  { id: "amd", label: "AMD", accent: "#ed1c24" },
  { id: "meta", label: "Meta", accent: "#0866ff" },
  { id: "google", label: "Google", accent: "#4285f4" },
  { id: "amazon", label: "Amazon", accent: "#ff9900" },
  { id: "uber", label: "Uber", accent: "#111111" },
] as const;
export type ThemeId = (typeof THEMES)[number]["id"];
export function resolveTheme(value: unknown): ThemeId {
  return THEMES.some((theme) => theme.id === value)
    ? (value as ThemeId)
    : "default";
}
