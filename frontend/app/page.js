import Link from "next/link";

const CATEGORIES = [
  { emoji: "💻", title: "Computer Skills", desc: "Hardware, OS, files and troubleshooting" },
  { emoji: "🐍", title: "Python", desc: "Programming foundations and automation" },
  { emoji: "🐧", title: "Linux", desc: "The OS behind the cloud" },
  { emoji: "🌐", title: "Networking", desc: "IP, DNS, ports and how data moves" },
  { emoji: "🔐", title: "Cybersecurity", desc: "Passwords, phishing and safe browsing" },
  { emoji: "☁️", title: "AWS Cloud", desc: "Cloud concepts and core AWS services" },
  { emoji: "💼", title: "Job Readiness", desc: "CV writing and interview preparation" },
  { emoji: "✉️", title: "Digital Literacy", desc: "Email, Google Workspace and online safety" },
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <h1>EDUBRIDGE SA</h1>
        <div className="tagline">Learn. Build. Connect. Grow.</div>
        <p className="lead">
          Free, structured digital skills training designed for low-bandwidth
          environments — townships, rural communities, and anyone who has been
          left behind by expensive courses.
        </p>
        <Link href="/register" className="btn">
          Start Learning
        </Link>
        {" "}
        <Link href="/pathways" className="btn secondary">
          Choose a career pathway
        </Link>
      </section>

      <h2 className="section-title">What do you want to learn?</h2>
      <p className="section-sub">Text-first lessons. Small pages. Works on mobile data.</p>
      <div className="grid">
        {CATEGORIES.map((c) => (
          <div className="card" key={c.title}>
            <h3>
              {c.emoji} {c.title}
            </h3>
            <p>{c.desc}</p>
            <div className="meta">
              <Link href="/courses">Browse courses →</Link>
            </div>
          </div>
        ))}
      </div>

      <h2 className="section-title">How it works</h2>
      <div className="grid">
        <div className="card">
          <h3>1. Set your goal</h3>
          <p>Choose a career pathway — IT Support, Cloud, Developer, Security or Entrepreneur.</p>
        </div>
        <div className="card">
          <h3>2. Follow the levels</h3>
          <p>EduBridge gives you an ordered journey instead of 500 random videos.</p>
        </div>
        <div className="card">
          <h3>3. Learn &amp; prove it</h3>
          <p>Complete lessons, pass quizzes, earn badges and build a skills profile.</p>
        </div>
        <div className="card">
          <h3>4. Get job-ready</h3>
          <p>Finish with CV and interview preparation tailored to entry-level tech roles.</p>
        </div>
      </div>
    </>
  );
}
