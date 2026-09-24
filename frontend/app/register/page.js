"use client";

import Link from "next/link";
import { useState } from "react";
import { api, setToken } from "../../lib/api";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "", location: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  function set(k) {
    return (e) => setForm({ ...form, [k]: e.target.value });
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const data = await api("/auth/register", {
        method: "POST",
        auth: false,
        body: form,
      });
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
      <h1>Create your free account</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        Start your digital skills journey. No cost, ever.
      </p>
      <label>Full name</label>
      <input required minLength={2} value={form.name} onChange={set("name")} placeholder="Athenkosi Fadana" />
      <label>Email</label>
      <input required type="email" value={form.email} onChange={set("email")} placeholder="you@example.com" />
      <label>Password (min 8 characters)</label>
      <input required minLength={8} type="password" value={form.password} onChange={set("password")} />
      <label>Location (optional)</label>
      <input value={form.location} onChange={set("location")} placeholder="e.g. Whittlesea, Eastern Cape" />
      <button className="btn" disabled={busy}>
        {busy ? "Creating account…" : "Register"}
      </button>
      {error && <div className="error">{error}</div>}
      <p className="muted" style={{ marginTop: 16, textAlign: "center" }}>
        Already registered? <Link href="/login">Login</Link>
      </p>
    </form>
  );
}
