"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, getToken } from "../../lib/api";

export default function Assessment() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    api("/assessment/questions")
      .then(setQuestions)
      .catch((e) => setError(e.message));
  }, []);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const res = await api("/assessment/submit", { method: "POST", body: { answers } });
      setResult(res);
      window.scrollTo(0, 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  if (error && !questions.length)
    return <div className="error" style={{ marginTop: 24 }}>{error}</div>;

  if (result) {
    return (
      <>
        <h1>Your Digital Skills Profile</h1>
        <p className="muted" style={{ marginTop: 6 }}>
          Overall: <strong>{result.overall_percent}%</strong> — assessed across{" "}
          {result.scores.length} skill areas.
        </p>

        <div className="lesson-content" style={{ marginTop: 20 }}>
          {result.scores.map((s) => (
            <div key={s.category} style={{ marginBottom: 14 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{s.category}</strong>
                <span className="muted">
                  {s.score}/{s.total} · {s.percent}%
                </span>
              </div>
              <span className="progress-bar">
                {"█".repeat(Math.round(s.percent / 10))}
                {"░".repeat(10 - Math.round(s.percent / 10))}
              </span>
            </div>
          ))}
        </div>

        <h2 className="section-title">Recommended pathway</h2>
        <div className="card" style={{ marginTop: 12 }}>
          <h3>{result.recommended_pathway?.title || "Digital Foundations"}</h3>
          <p>{result.reason}</p>
          <div className="meta" style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            {result.recommended_pathway && (
              <Link href={`/pathways/${result.recommended_pathway.id}`}>
                View your pathway →
              </Link>
            )}
            <Link href="/dashboard">See skills profile →</Link>
          </div>
        </div>

        <p className="muted" style={{ marginTop: 18 }}>
          Results saved to your profile. Retake anytime to track improvement.
        </p>
        <p style={{ marginTop: 12 }}>
          <button
            className="btn secondary"
            onClick={() => {
              setResult(null);
              setAnswers({});
            }}
          >
            Retake assessment
          </button>
        </p>
      </>
    );
  }

  if (!questions.length) return <p className="muted" style={{ marginTop: 24 }}>Loading assessment…</p>;

  return (
    <>
      <h1>Digital Skills Assessment</h1>
      <p className="muted" style={{ marginTop: 8 }}>
        15 questions · about 3 minutes · answers your skill bars and recommends a
        career pathway. Uses almost no data.
      </p>
      {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}
      <form onSubmit={submit}>
        {questions.map((q, i) => (
          <div className="quiz-q" key={q.id}>
            <div className="question">
              {i + 1}. {q.question}{" "}
              <span className="muted" style={{ fontWeight: 400, fontSize: "0.85rem" }}>
                ({q.category})
              </span>
            </div>
            {["a", "b", "c", "d"].map((opt) => (
              <label key={opt}>
                <input
                  type="radio"
                  name={`q${q.id}`}
                  value={opt}
                  checked={answers[String(q.id)] === opt}
                  onChange={() => setAnswers({ ...answers, [String(q.id)]: opt })}
                  required
                />
                {q[`option_${opt}`]}
              </label>
            ))}
          </div>
        ))}
        <button className="btn" style={{ marginTop: 20 }} disabled={busy}>
          {busy ? "Scoring…" : "See my skills profile"}
        </button>
      </form>
    </>
  );
}
