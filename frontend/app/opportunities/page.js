"use client";

import { useEffect, useState } from "react";
import { api } from "../../lib/api";

const TYPE_COLORS = {
  Learnership: "badge",
  YES: "badge",
  Internship: "badge",
  Job: "badge",
  Certification: "badge",
};

export default function Opportunities() {
  const [opps, setOpps] = useState([]);
  const [filter, setFilter] = useState("All");
  const [error, setError] = useState("");

  useEffect(() => {
    api("/opportunities", { auth: false })
      .then(setOpps)
      .catch((e) => setError(e.message));
  }, []);

  const types = ["All", ...Array.from(new Set(opps.map((o) => o.opportunity_type)))];
  const visible = filter === "All" ? opps : opps.filter((o) => o.opportunity_type === filter);

  return (
    <>
      <h1>Opportunities</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        Learnerships, YES programmes, internships, entry-level jobs and free
        certifications that value digital skills. Listings are informational —
        always verify details with the organisation.
      </p>
      {error && <div className="error" style={{ marginTop: 16 }}>{error}</div>}
      <div className="tabs">
        {types.map((t) => (
          <span
            key={t}
            className={`chip ${filter === t ? "active" : ""}`}
            onClick={() => setFilter(t)}
          >
            {t}
          </span>
        ))}
      </div>
      <div className="grid">
        {visible.map((o) => (
          <div className="card" key={o.id}>
            <span className={TYPE_COLORS[o.opportunity_type] || "badge"}>
              {o.opportunity_type}
            </span>
            <h3 style={{ marginTop: 8 }}>{o.title}</h3>
            <p className="muted" style={{ fontSize: "0.88rem" }}>
              {o.organisation} · {o.location}
            </p>
            <p style={{ marginTop: 8 }}>{o.description}</p>
            <p className="muted" style={{ fontSize: "0.85rem", marginTop: 8 }}>
              <strong>Requirements:</strong> {o.requirements}
            </p>
            <div className="meta">
              {o.closing_date && <>Closes: {o.closing_date}</>}
              {o.url && (
                <>
                  {" · "}
                  <a href={o.url} target="_blank" rel="noreferrer">
                    Official page →
                  </a>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
      <p className="muted" style={{ marginTop: 24, fontSize: "0.88rem" }}>
        EduBridge provides skills guidance only — listing an opportunity is not
        an endorsement or a guarantee of placement.
      </p>
    </>
  );
}
