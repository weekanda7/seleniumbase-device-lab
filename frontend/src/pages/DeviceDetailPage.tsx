import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, ApiError, Device } from "../api";

export default function DeviceDetailPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState<Device | null>(null);
  const [error, setError] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    api
      .getDevice(id)
      .then(setDevice)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Cannot load device"));
  }, [id]);

  async function onDelete() {
    if (!device) return;
    setDeleting(true);
    try {
      await api.deleteDevice(device.id);
      navigate("/devices");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Cannot delete device");
      setDeleting(false);
    }
  }

  return (
    <section>
      <Link to="/devices" data-testid="back-link">
        ← Back to devices
      </Link>
      {error && (
        <p className="error" role="alert" data-testid="detail-error">
          {error}
        </p>
      )}
      {!device && !error && <p data-testid="loading">Loading…</p>}
      {device && (
        <div className="card">
          <h1 data-testid="device-name">{device.name}</h1>
          <dl>
            <dt>Type</dt>
            <dd data-testid="device-type">{device.type}</dd>
            <dt>Location</dt>
            <dd data-testid="device-location">{device.location || "—"}</dd>
            <dt>Created</dt>
            <dd>{new Date(device.created_at).toLocaleString()}</dd>
          </dl>
          <button
            className="danger"
            data-testid="delete-device-button"
            onClick={onDelete}
            disabled={deleting}
          >
            {deleting ? "Deleting…" : "Delete device"}
          </button>
        </div>
      )}
    </section>
  );
}
