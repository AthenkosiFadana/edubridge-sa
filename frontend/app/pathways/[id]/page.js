"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, getToken } from "../../../lib/api";

export default function PathwayDetail({ params }) {
  const id = params.id;
  const [pathway, setPathway] = useState(null);
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    api(`/pathways/${id}`, { auth: false })
      .then(setPathway)
      .catch((e) => setError(e.message));
  }, [id]);

  async function choose() {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    try {
      await api("/me/pathway", { method: "POST", body: { pathway_id: Number(id) } });
      setMsg("Pathway saved to your profile!");
    } catch (e) {
      setError(e.message);
    }
  }

  if (error) return <div className="error" style={{ marginTop: 24 }}>{error}</div>;
  if (!pathway) return <p className="muted" style={{ marginTop: 24 }}>Loading pathway…</p>;

  return (
    <>
      <h1>{pathway.title}</h1>
      <p className="muted" style={{ marginTop: 6 }}>
        Target role: {pathway.role_title}
      </p>
      <p style={{ marginTop: 10 }}>{pathway.description}</p>
      <p style={{ marginTop: 16 }}>
        <button className="btn" onClick={choose}>
          Add this pathway to my profile
        </button>
      </p>
      {msg && <p className="success" style={{ marginTop: 10 }}>{msg}</p>}

      <ol className="levels">
        {pathway.levels.map((lvl) => (
          <li key={lvl.id}>
            <span className="level-title">{lvl.title}</span>
            {lvl.course_id ? (
              <Link className="btn small secondary" href={`/courses/${lvl.course_id}`}>
                Start level →
              </Link>
            ) : (
              <span className="muted">Hands-on project — coming soon</span>
            )}
          </li>
        ))}
      </ol>
      <p className="muted" style={{ marginTop: 18 }}>
        Complete each level in order for the best result.
      </p>
    </>
  );
}
