const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

function authHeaders() {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function listCharacters(vertical) {
  const res = await fetch(`${API_BASE}/api/${vertical}/characters`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to load characters");
  return res.json();
}

export async function startSession(vertical, characterId) {
  const res = await fetch(`${API_BASE}/api/${vertical}/sessions?character_id=${characterId}`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to start session");
  return res.json();
}

export async function sendMessage(vertical, sessionId, content) {
  const res = await fetch(
    `${API_BASE}/api/${vertical}/sessions/${sessionId}/messages?content=${encodeURIComponent(content)}`,
    { method: "POST", headers: authHeaders() }
  );
  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
}

export async function getProgress(vertical) {
  const res = await fetch(`${API_BASE}/api/${vertical}/progress`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to load progress");
  return res.json();
}

export async function signup(email, password, name, vertical) {
  const res = await fetch(
    `${API_BASE}/api/auth/signup?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&name=${encodeURIComponent(name)}&vertical=${vertical}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Signup failed");
  return res.json();
}
