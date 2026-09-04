"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { listCharacters } from "../../lib/api";

export default function CharacterList({ params }) {
  const { vertical } = params;
  const [characters, setCharacters] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    listCharacters(vertical).then(setCharacters).catch((e) => setError(e.message));
  }, [vertical]);

  return (
    <main style={{ padding: 40, maxWidth: 720, margin: "0 auto" }}>
      <h1>{vertical} characters</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div style={{ display: "grid", gap: 12, marginTop: 20 }}>
        {characters.map((c) => (
          <Link
            key={c.id}
            href={`/${vertical}/chat/${c.id}`}
            style={{ border: "1px solid #ddd", borderRadius: 10, padding: 16, textDecoration: "none", color: "inherit" }}
          >
            {c.name}
          </Link>
        ))}
      </div>
      <p style={{ marginTop: 24 }}>
        <Link href={`/${vertical}/progress`}>View progress →</Link>
      </p>
    </main>
  );
}
