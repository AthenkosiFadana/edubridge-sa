"use client";

import Link from "next/link";
import { useState } from "react";
import { api, setToken } from "../../lib/api";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const data = await api("/auth/login", { method: "POST", auth: false, body: form });
      setToken(data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="auth" onSubmit={submit}>
      <h1>Welcome back</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        Login to continue your pathway.
      </p>
      <label>Email</label>
      <input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <label>Password</label>
      <input required type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button className="btn" disabled={busy}>
        {busy ? "Logging in…" : "Login"}
      </button>
      {error && <div className="error">{error}</div>}
      <p className="muted" style={{ marginTop: 16, textAlign: "center" }}>
        New here? <Link href="/register">Create an account</Link>
      </p>
    </form>
  );
}
