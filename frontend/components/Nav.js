"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { clearToken, getToken } from "../lib/api";

export default function Nav() {
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    setAuthed(!!getToken());
    const onStorage = () => setAuthed(!!getToken());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  function logout() {
    clearToken();
    setAuthed(false);
    window.location.href = "/";
  }

  return (
    <header className="site">
      <div className="container">
        <Link href="/" className="logo">
          EDU<span>BRIDGE</span> SA
        </Link>
        <nav>
          <Link href="/courses">Courses</Link>
          <Link href="/pathways">Pathways</Link>
          <Link href="/assessment">Assessment</Link>
          <Link href="/opportunities">Opportunities</Link>
          {authed ? (
            <>
              <Link href="/dashboard">Dashboard</Link>
              <a href="#" onClick={(e) => { e.preventDefault(); logout(); }}>Logout</a>
            </>
          ) : (
            <>
              <Link href="/login">Login</Link>
              <Link href="/register">Register</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
