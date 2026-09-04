"use client";
import { useState } from "react";
import { startSession, sendMessage } from "../../../../lib/api";

export default function Chat({ params }) {
  const { vertical, characterId } = params;
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function ensureSession() {
    if (sessionId) return sessionId;
    const { session_id } = await startSession(vertical, characterId);
    setSessionId(session_id);
    return session_id;
  }

  async function handleSend() {
    if (!input.trim()) return;
    const sid = await ensureSession();
    const userMsg = { role: "user", content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    const { reply } = await sendMessage(vertical, sid, userMsg.content);
    setMessages((m) => [...m, { role: "assistant", content: reply }]);
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
      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type a message..."
          style={{ flex: 1, padding: 10 }}
        />
        <button onClick={handleSend}>Send</button>
        {/* Mic button wires to /api/voice/transcribe + /synthesize once mobile-style hold-to-talk is ported here */}
        <button title="Voice input (wire to /api/voice/transcribe)">🎤</button>
      </div>
    </main>
  );
}
