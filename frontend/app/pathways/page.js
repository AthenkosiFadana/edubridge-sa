"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";

export default function Pathways() {
  const [pathways, setPathways] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/pathways", { auth: false })
      .then(setPathways)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <>
      <h1>What do you want to become?</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        Choose a goal. EduBridge generates a structured, level-by-level pathway —
        not a pile of random videos.
      </p>
      {error && <div className="error" style={{ marginTop: 16 }}>{error}</div>}
      <div className="grid">
        {pathways.map((p) => (
          <div className="card" key={p.id}>
            <h3>{p.title}</h3>
            <p>{p.description}</p>
            <div className="meta">{p.levels.length} levels</div>
            <div className="meta">
              <Link href={`/pathways/${p.id}`}>View pathway →</Link>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
