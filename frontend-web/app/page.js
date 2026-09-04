import Link from "next/link";

const VERTICALS = [
  { slug: "kids", label: "Kids Learning Companion", blurb: "Adaptive learning for ages 5-11." },
  { slug: "english", label: "Spoken English Partner", blurb: "Voice-first fluency practice." },
  { slug: "interview", label: "Interview Simulator", blurb: "Interview & confidence coaching." },
];

export default function Home() {
  return (
    <main style={{ padding: 40, maxWidth: 720, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ margin: 0 }}>Choose a vertical</h1>
        <Link href="/signup" style={{ padding: "8px 16px", border: "1px solid #333", borderRadius: 8 }}>
          Sign up
        </Link>
      </div>
      <p style={{ color: "#666" }}>You need an account before chatting — sign up first if you haven't.</p>
      <div style={{ display: "grid", gap: 16, marginTop: 24 }}>
        {VERTICALS.map((v) => (
          <Link
            key={v.slug}
            href={`/${v.slug}`}
            style={{
              border: "1px solid #ddd",
              borderRadius: 12,
              padding: 20,
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <h2 style={{ margin: 0 }}>{v.label}</h2>
            <p style={{ margin: "8px 0 0", color: "#666" }}>{v.blurb}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
