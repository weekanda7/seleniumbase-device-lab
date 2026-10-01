import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, ApiError, Device } from "../api";

export default function DeviceListPage() {
  const [devices, setDevices] = useState<Device[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .listDevices()
      .then(setDevices)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Cannot load devices"));
  }, []);

  return (
    <section>
      <div className="page-header">
        <h1>Devices</h1>
        <Link to="/devices/new" className="button" data-testid="add-device-button">
          Add device
        </Link>
      </div>

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      {!devices && !error && <p data-testid="loading">Loading…</p>}

      {devices && (
        <>
          <p className="muted" data-testid="device-count">
            {devices.length} devices
          </p>
          <table data-testid="device-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((d) => (
                <tr key={d.id} data-testid="device-row">
                  <td>
                    <Link to={`/devices/${d.id}`} data-testid="device-link">
                      {d.name}
                    </Link>
                  </td>
                  <td>{d.type}</td>
                  <td>{d.location || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </section>
  );
}
