"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [filter, setFilter] = useState("All");
  const [error, setError] = useState("");

  useEffect(() => {
    api("/courses", { auth: false })
      .then(setCourses)
      .catch((e) => setError(e.message));
  }, []);

  const categories = ["All", ...Array.from(new Set(courses.map((c) => c.category)))];
  const visible = filter === "All" ? courses : courses.filter((c) => c.category === filter);

  return (
    <>
      <h1>Courses</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        Short, text-first lessons designed to use as little data as possible.
      </p>
      {error && <div className="error" style={{ marginTop: 16 }}>{error}</div>}
      <div className="tabs">
        {categories.map((c) => (
          <span
            key={c}
            className={`chip ${filter === c ? "active" : ""}`}
            onClick={() => setFilter(c)}
          >
            {c}
          </span>
        ))}
      </div>
      <div className="grid">
        {visible.map((c) => (
          <div className="card" key={c.id}>
            <h3>
              <Link className="title-link" href={`/courses/${c.id}`}>
                {c.title}
              </Link>
            </h3>
            <p>{c.description}</p>
            <div className="meta">
              {c.category} · {c.difficulty}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
