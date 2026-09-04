const API_BASE = "http://localhost:8000"; // swap for your deployed backend URL per vertical

export async function transcribe(uri, token) {
  const form = new FormData();
  form.append("audio", { uri, name: "clip.m4a", type: "audio/m4a" });
  const res = await fetch(`${API_BASE}/api/voice/transcribe`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) throw new Error("Transcribe failed");
  return (await res.json()).text;
}

export async function sendMessage(vertical, sessionId, content, token) {
  const res = await fetch(
    `${API_BASE}/api/${vertical}/sessions/${sessionId}/messages?content=${encodeURIComponent(content)}`,
    { method: "POST", headers: { Authorization: `Bearer ${token}` } }
  );
  if (!res.ok) throw new Error("Send message failed");
  return (await res.json()).reply;
}

export async function synthesize(text, voiceId, token) {
  const res = await fetch(
    `${API_BASE}/api/voice/synthesize?text=${encodeURIComponent(text)}&voice_id=${voiceId}`,
    { method: "POST", headers: { Authorization: `Bearer ${token}` } }
  );
  if (!res.ok) throw new Error("Synthesize failed");
  return res.blob(); // caller plays this via expo-av
}
