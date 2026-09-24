"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, getToken } from "../../../lib/api";

function renderContent(text) {
  // Very lightweight markdown-ish rendering: code blocks, bold, paragraphs, lists
  const blocks = [];
  const parts = text.split(/```/);
  parts.forEach((part, i) => {
    if (i % 2 === 1) {
      blocks.push(<pre key={i}>{part.replace(/^python\n/, "")}</pre>);
      return;
    }
    const lines = part.split("\n");
    let list = [];
    const flush = (key) => {
      if (list.length) {
        blocks.push(<ul key={`ul${key}`}>{list.map((li, j) => <li key={j}>{inline(li)}</li>)}</ul>);
        list = [];
      }
    };
    lines.forEach((line, j) => {
      const trimmed = line.trim();
      if (trimmed.startsWith("- ")) {
        list.push(trimmed.slice(2));
        return;
      }
      flush(`${i}-${j}`);
      if (!trimmed) return;
      if (/^\d+\.\s/.test(trimmed)) {
        blocks.push(<p key={`${i}-${j}`}><strong>{trimmed}</strong></p>);
      } else {
        blocks.push(<p key={`${i}-${j}`}>{inline(trimmed)}</p>);
      }
    });
    flush(`end-${i}`);
  });
  return blocks;
}

function inline(text) {
  const nodes = [];
  let rest = text;
  let k = 0;
  const re = /\*\*(.+?)\*\*/;
  while (true) {
    const m = rest.match(re);
    if (!m) {
      if (rest) nodes.push(rest);
      break;
    }
    const idx = rest.indexOf(m[0]);
    if (idx > 0) nodes.push(rest.slice(0, idx));
    nodes.push(<strong key={k++}>{m[1]}</strong>);
    rest = rest.slice(idx + m[0].length);
  }
  return nodes;
}

export default function LessonPage({ params }) {
  const id = params.id;
  const [lesson, setLesson] = useState(null);
  const [error, setError] = useState("");
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [done, setDone] = useState(false);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    api(`/me/lessons/${id}/content`)
      .then(setLesson)
      .catch((e) => setError(e.message));
  }, [id]);

  async function complete() {
    try {
      await api("/me/lessons/complete", { method: "POST", body: { lesson_id: Number(id) } });
      setDone(true);
      setMsg("Lesson marked complete ✓");
    } catch (e) {
      setError(e.message);
    }
  }

  async function submitQuiz(e) {
    e.preventDefault();
    try {
      const res = await api("/me/quizzes/submit", {
        method: "POST",
        body: { lesson_id: Number(id), answers },
      });
      setResult(res);
      if (res.passed && !done) await complete();
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) return <div className="error" style={{ marginTop: 24 }}>{error}</div>;
  if (!lesson) return <p className="muted" style={{ marginTop: 24 }}>Loading lesson…</p>;

  const hasQuiz = lesson.quiz_questions.length > 0;

  return (
    <>
      <p className="muted">
        <Link href="/courses">Courses</Link> / Lesson
      </p>
      <h1 style={{ marginTop: 6 }}>{lesson.title}</h1>

      <div className="lesson-content">{renderContent(lesson.content)}</div>

      {lesson.video_url && (
        <p className="muted" style={{ marginTop: 10 }}>
          Optional video (not auto-loaded to save data):{" "}
          <a href={lesson.video_url} target="_blank" rel="noreferrer">
            watch
          </a>
        </p>
      )}

      <p style={{ marginTop: 20 }}>
        <button className="btn" onClick={complete} disabled={done}>
          {done ? "Completed ✓" : "Mark lesson complete"}
        </button>
        {msg && <span className="success" style={{ marginLeft: 12 }}>{msg}</span>}
      </p>

      {hasQuiz && (
        <>
          <h2 className="section-title">Quiz</h2>
          <p className="section-sub">Score 70% or higher to pass. You can retry.</p>
          <form onSubmit={submitQuiz}>
            {lesson.quiz_questions.map((q, qi) => (
              <div className="quiz-q" key={q.id}>
                <div className="question">
                  {qi + 1}. {q.question}
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
            <button className="btn" style={{ marginTop: 18 }}>
              Submit quiz
            </button>
          </form>

          {result && (
            <div className="lesson-content" style={{ borderColor: result.passed ? "var(--green)" : "#ff7b72" }}>
              <h3 className={result.passed ? "success" : ""}>
                {result.passed ? "Passed 🎉" : "Not passed yet"}
              </h3>
              <p>
                Score: {result.score}/{result.total} ({result.percent}%)
              </p>
              {result.incorrect.length > 0 && (
                <>
                  <p className="muted" style={{ marginTop: 8 }}>Review these:</p>
                  <ul>
                    {result.incorrect.map((inc) => (
                      <li key={inc.question_id}>{inc.question}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}
        </>
      )}
    </>
  );
}
