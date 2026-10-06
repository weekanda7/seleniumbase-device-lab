// Thin wrapper around fetch: adds the Bearer token, turns error responses into ApiError.

const TOKEN_KEY = "device-lab-token";

export const auth = {
  get: () => sessionStorage.getItem(TOKEN_KEY),
  set: (token: string) => sessionStorage.setItem(TOKEN_KEY, token),
  clear: () => sessionStorage.removeItem(TOKEN_KEY),
};

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

export type DeviceStatus = "online" | "offline";

export type Device = {
  id: number;
  name: string;
  type: string;
  status: DeviceStatus;
  location: string;
  created_at: string;
};

export type DeviceInput = {
  name: string;
  type: string;
  status: DeviceStatus;
  location: string;
};

export type VersionInfo = { version: string; commit: string };

export type DeviceQuery = { q?: string; status?: DeviceStatus };

export const DEVICE_TYPES = ["Router", "Switch", "AP", "Sensor"];
export const DEVICE_STATUSES: DeviceStatus[] = ["online", "offline"];

// FastAPI returns `detail` as a string (our errors) or a list (422 validation errors).
function toMessage(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map(
        (d: { loc?: unknown[]; msg?: string }) => `${String(d.loc?.at(-1) ?? "field")}: ${d.msg}`,
      )
      .join("; ");
  }
  return "Request failed";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const token = auth.get();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`/api${path}`, { ...options, headers });
  if (res.status === 204) return undefined as T;

  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    // Expired / unknown token (e.g. backend restarted): back to the login page.
    if (res.status === 401 && path !== "/auth/login") {
      auth.clear();
      window.location.assign("/login");
    }
    throw new ApiError(res.status, toMessage(body.detail));
  }
  return body as T;
}

function toQueryString(query: DeviceQuery): string {
  const params = new URLSearchParams();
  if (query.q) params.set("q", query.q);
  if (query.status) params.set("status", query.status);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export const api = {
  login: (username: string, password: string) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  logout: () => request<void>("/auth/logout", { method: "POST" }),
  getVersion: () => request<VersionInfo>("/version"),
  listDevices: (query: DeviceQuery = {}) => request<Device[]>(`/devices${toQueryString(query)}`),
  getDevice: (id: string) => request<Device>(`/devices/${id}`),
  createDevice: (input: DeviceInput) =>
    request<Device>("/devices", { method: "POST", body: JSON.stringify(input) }),
  updateDevice: (id: number, changes: Partial<DeviceInput>) =>
    request<Device>(`/devices/${id}`, { method: "PATCH", body: JSON.stringify(changes) }),
  deleteDevice: (id: number) => request<void>(`/devices/${id}`, { method: "DELETE" }),
};

// antd's *ButtonProps don't declare data-* attributes; spread this in to add a test id.
export const testId = (id: string) => ({ "data-testid": id }) as Record<string, string>;
