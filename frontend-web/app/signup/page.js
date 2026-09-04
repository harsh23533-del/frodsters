"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signup } from "../../lib/api";

const VERTICALS = [
  { slug: "kids", label: "Kids Learning Companion" },
  { slug: "english", label: "Spoken English Partner" },
  { slug: "interview", label: "Interview Simulator" },
];

export default function Signup() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [vertical, setVertical] = useState("kids");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { token } = await signup(email, password, name, vertical);
      localStorage.setItem("token", token);
      router.push(`/${vertical}`);
    } catch (err) {
      setError(err.message || "Signup failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 40, maxWidth: 420, margin: "0 auto" }}>
      <h1>Create your account</h1>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12, marginTop: 20 }}>
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required style={{ padding: 10 }} />
        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ padding: 10 }}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ padding: 10 }}
        />
        <select value={vertical} onChange={(e) => setVertical(e.target.value)} style={{ padding: 10 }}>
          {VERTICALS.map((v) => (
            <option key={v.slug} value={v.slug}>
              {v.label}
            </option>
          ))}
        </select>
        {error && <p style={{ color: "red", margin: 0 }}>{error}</p>}
        <button type="submit" disabled={loading} style={{ padding: 12 }}>
          {loading ? "Creating account..." : "Sign up"}
        </button>
      </form>
    </main>
  );
}
