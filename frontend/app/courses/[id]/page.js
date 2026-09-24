"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "../../../lib/api";

export default function CourseDetail({ params }) {
  const id = params.id;
  const [course, setCourse] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api(`/courses/${id}`, { auth: false })
      .then(setCourse)
      .catch((e) => setError(e.message));
  }, [id]);

  if (error) return <div className="error" style={{ marginTop: 24 }}>{error}</div>;
  if (!course) return <p className="muted" style={{ marginTop: 24 }}>Loading course…</p>;

  return (
    <>
      <p className="muted">
        <Link href="/courses">Courses</Link> / {course.category}
      </p>
      <h1 style={{ marginTop: 6 }}>{course.title}</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        {course.difficulty} · {course.category}
      </p>
      <p style={{ marginTop: 10 }}>{course.description}</p>

      {course.modules.map((m) => (
        <div key={m.id}>
          <h2 className="section-title">
            Module {m.order_number}: {m.title}
          </h2>
          <p className="section-sub">{m.description}</p>
          <ol className="levels">
            {m.lessons.map((l) => (
              <li key={l.id}>
                <span className="level-title">
                  Lesson {l.order_number}: {l.title}
                </span>
                <Link className="btn small" href={`/lessons/${l.id}`}>
                  Open lesson →
                </Link>
              </li>
            ))}
          </ol>
        </div>
      ))}
    </>
  );
}
