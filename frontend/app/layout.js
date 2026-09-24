import "./globals.css";
import Nav from "../components/Nav";

export const metadata = {
  title: "EduBridge SA — Free digital skills for everyone",
  description:
    "Bridging the digital skills gap in South Africa. Structured learning pathways in computer literacy, Python, Linux, networking, cybersecurity and AWS Cloud.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main>
          <div className="container">{children}</div>
        </main>
        <footer className="site">
          <div className="container">
            EduBridge SA v1.0 — Bridging the digital skills gap, one learner at a time.
            <br />
            Skills guidance only; employment is never guaranteed.
          </div>
        </footer>
      </body>
    </html>
  );
}
