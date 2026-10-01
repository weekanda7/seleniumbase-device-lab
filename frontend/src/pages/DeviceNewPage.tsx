import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, ApiError, DEVICE_TYPES } from "../api";

export default function DeviceNewPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [type, setType] = useState(DEVICE_TYPES[0]);
  const [location, setLocation] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await api.createDevice({ name, type, location });
      navigate("/devices");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Cannot save device");
      setSaving(false);
    }
  }

  return (
    <section>
      <h1>Add device</h1>
      <form className="card" onSubmit={onSubmit} data-testid="device-form">
        <label htmlFor="name">Name</label>
        <input id="name" value={name} onChange={(e) => setName(e.target.value)} />
        <label htmlFor="type">Type</label>
        <select id="type" value={type} onChange={(e) => setType(e.target.value)}>
          {DEVICE_TYPES.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <label htmlFor="location">Location (optional)</label>
        <input id="location" value={location} onChange={(e) => setLocation(e.target.value)} />
        {error && (
          <p className="error" role="alert" data-testid="form-error">
            {error}
          </p>
        )}
        <div className="actions">
          <button type="submit" data-testid="save-device-button" disabled={saving}>
            {saving ? "Saving…" : "Save"}
          </button>
          <Link to="/devices" className="button secondary">
            Cancel
          </Link>
        </div>
      </form>
    </section>
  );
}
