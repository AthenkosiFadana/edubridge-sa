"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, getToken, progressBar } from "../../lib/api";

export default function Dashboard() {
  const [me, setMe] = useState(null);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    Promise.all([api("/auth/me"), api("/me/profile")])
      .then(([u, p]) => {
        setMe(u);
        setProfile(p);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="error" style={{ marginTop: 24 }}>{error}</div>;
  if (!profile || !me) return <p className="muted" style={{ marginTop: 24 }}>Loading your skills profile…</p>;

  return (
    <>
      <h1>{me.name.split(" ")[0]}'s Skills Profile</h1>
      <p className="muted">
        {me.location ? `${me.location} · ` : ""}Member since {new Date(me.created_at).toLocaleDateString()}
      </p>

      <div className="stat-row">
        <div className="stat">
          <div className="num">{profile.percent}%</div>
          <div className="lbl">Course progress</div>
        </div>
        <div className="stat">
          <div className="num">
            {profile.lessons_completed}/{profile.lessons_total}
          </div>
          <div className="lbl">Lessons done</div>
        </div>
        <div className="stat">
          <div className="num">{profile.quizzes_passed}</div>
          <div className="lbl">Quizzes passed</div>
        </div>
        <div className="stat">
          <div className="num">{profile.certificates.length}</div>
          <div className="lbl">Certificates</div>
        </div>
      </div>

      {/* Personalised next step */}
      {profile.next_lesson ? (
        <div className="card" style={{ marginTop: 24, borderLeft: "4px solid var(--green)" }}>
          <h3>▶ Continue where you left off</h3>
          <p>
            <strong>{profile.next_lesson.title}</strong>
            <br />
            <span className="muted">
              {profile.next_lesson.level_title
                ? `${profile.next_lesson.level_title} → `
                : ""}
              {profile.next_lesson.course_title} · {profile.next_lesson.module_title}
            </span>
          </p>
          <div className="meta">
            <Link href={`/lessons/${profile.next_lesson.lesson_id}`}>Open next lesson →</Link>
          </div>
        </div>
      ) : (
        <div className="card" style={{ marginTop: 24 }}>
          <h3>🎉 All lessons completed</h3>
          <p>You've finished every lesson on the platform. Amazing work.</p>
        </div>
      )}

      <h2 className="section-title">Overall progress</h2>
      <div className="lesson-content" style={{ marginTop: 12 }}>
        <span className="progress-bar">{progressBar(profile.percent)}</span> {profile.percent}%
        <div className="muted" style={{ marginTop: 6, fontSize: "0.9rem" }}>
          {profile.lessons_completed} of {profile.lessons_total} lessons completed
        </div>
      </div>

      {/* Digital skills assessment */}
      <h2 className="section-title">Digital skills assessment</h2>
      {profile.assessment ? (
        <div className="lesson-content" style={{ marginTop: 12 }}>
          <p className="muted" style={{ fontSize: "0.9rem", marginBottom: 12 }}>
            Taken {new Date(profile.assessment.taken_at).toLocaleDateString()} ·
            Overall {profile.assessment.overall_percent}%
            {" · "}
            <Link href="/assessment">Retake</Link>
          </p>
          {profile.assessment.scores.map((s) => (
            <div key={s.category} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.95rem" }}>
                <span>{s.category}</span>
                <span className="muted">{s.percent}%</span>
              </div>
              <span className="progress-bar" style={{ fontSize: "0.9rem" }}>
                {progressBar(s.percent)}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="card" style={{ marginTop: 12 }}>
          <h3>Find your current skill level</h3>
          <p>15 quick questions → skill bars per area → a recommended pathway.</p>
          <div className="meta">
            <Link href="/assessment">Take the assessment →</Link>
          </div>
        </div>
      )}

      {/* Category skills from learning progress */}
      <h2 className="section-title">Skills earned through learning</h2>
      <div className="lesson-content" style={{ marginTop: 12 }}>
        {profile.category_skills.map((s) => (
          <div key={s.category} style={{ marginBottom: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.95rem" }}>
              <span>{s.category}</span>
              <span className="muted">{s.percent}%</span>
            </div>
            <span className="progress-bar" style={{ fontSize: "0.9rem" }}>
              {progressBar(s.percent)}
            </span>
          </div>
        ))}
      </div>

      <h2 className="section-title">Your pathway</h2>
      {profile.pathway ? (
        <div className="card" style={{ marginTop: 12 }}>
          <h3>{profile.pathway.title}</h3>
          <p>{profile.pathway.description}</p>
          <div className="meta">
            <Link href={`/pathways/${profile.pathway.id}`}>View levels →</Link>
          </div>
        </div>
      ) : (
        <div className="card" style={{ marginTop: 12 }}>
          <h3>No pathway chosen yet</h3>
          <p>Pick a career goal, or let the assessment recommend one for you.</p>
          <div className="meta">
            <Link href="/pathways">Choose your goal →</Link>
            {"  ·  "}
            <Link href="/assessment">Take the assessment →</Link>
          </div>
        </div>
      )}

      <h2 className="section-title">Certificates</h2>
      {profile.certificates.length === 0 ? (
        <p className="muted" style={{ marginTop: 8 }}>
          Complete every lesson in a course <em>and</em> pass its quizzes to earn a
          certificate.
        </p>
      ) : (
        <div className="grid" style={{ marginTop: 12 }}>
          {profile.certificates.map((c) => (
            <div className="card" key={c.id} style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem" }}>🏅</div>
              <h3>{c.course_title}</h3>
              <p className="muted" style={{ fontSize: "0.85rem" }}>
                Issued {new Date(c.issued_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}

      <h2 className="section-title">Badges</h2>
      <div style={{ marginTop: 10 }}>
        {profile.badges.length === 0 ? (
          <p className="muted">Complete every lesson in a course to earn its badge.</p>
        ) : (
          profile.badges.map((b) => (
            <span className="badge" key={b}>
              🏅 {b}
            </span>
          ))
        )}
      </div>

      <h2 className="section-title">Next opportunities</h2>
      <div className="grid" style={{ marginTop: 12 }}>
        <div className="card">
          <h3>Learnerships &amp; YES programmes</h3>
          <p>Curated entry points that value the skills you're building.</p>
          <div className="meta">
            <Link href="/opportunities">Browse opportunities →</Link>
          </div>
        </div>
        <div className="card">
          <h3>Job readiness</h3>
          <p>Build a one-page CV and prepare for interviews.</p>
          <div className="meta">
            <Link href="/courses">Open CV course →</Link>
          </div>
        </div>
      </div>
    </>
  );
}
