"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { startSession, sendMessage } from "../../../../lib/api";

export default function Chat({ params }) {
  const { vertical, characterId } = params;
  const router = useRouter();
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [error, setError] = useState(null);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined" && !localStorage.getItem("token")) {
      router.push("/signup");
    }
  }, [router]);

  async function ensureSession() {
    if (sessionId) return sessionId;
    const { session_id } = await startSession(vertical, characterId);
    setSessionId(session_id);
    return session_id;
  }

  async function handleSend() {
    if (!input.trim() || sending) return;
    setError(null);
    setSending(true);
    const content = input;
    try {
      const sid = await ensureSession();
      setMessages((m) => [...m, { role: "user", content }]);
      setInput("");
      const { reply } = await sendMessage(vertical, sid, content);
      setMessages((m) => [...m, { role: "assistant", content: reply }]);
    } catch (err) {
      setError(err.message || "Something went wrong sending that message.");
    } finally {
      setSending(false);
    }
  }

  return (
    <main style={{ padding: 40, maxWidth: 640, margin: "0 auto" }}>
      <h1>Chat</h1>
      <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 16, minHeight: 300 }}>
        {messages.map((m, i) => (
          <p key={i}>
            <strong>{m.role === "user" ? "You" : "AI"}:</strong> {m.content}
          </p>
        ))}
      </div>
      {error && (
        <p style={{ color: "red", marginTop: 8 }}>
          Error: {error} — <a href="/signup">sign up again</a> if your session expired.
        </p>
      )}
      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type a message..."
          style={{ flex: 1, padding: 10 }}
        />
        <button onClick={handleSend} disabled={sending}>
          {sending ? "Sending..." : "Send"}
        </button>
        <button title="Voice input (wire to /api/voice/transcribe)">🎤</button>
      </div>
    </main>
  );
}
