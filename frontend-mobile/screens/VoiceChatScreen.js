import { useRef, useState } from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import { transcribe, sendMessage, synthesize } from "../lib/api";

/**
 * Core flow (Step 13): record on press-hold -> /api/voice/transcribe
 * -> /api/{vertical}/sessions/{id}/messages -> /api/voice/synthesize -> play audio reply.
 */
export default function VoiceChatScreen({ route }) {
  const { vertical, sessionId, voiceId, token } = route.params;
  const recordingRef = useRef(null);
  const [status, setStatus] = useState("idle");

  async function startRecording() {
    setStatus("recording");
    const { granted } = await Audio.requestPermissionsAsync();
    if (!granted) return setStatus("idle");
    await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
    const recording = new Audio.Recording();
    await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
    await recording.startAsync();
    recordingRef.current = recording;
  }

  async function stopRecordingAndSend() {
    setStatus("processing");
    const recording = recordingRef.current;
    if (!recording) return setStatus("idle");
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();

    const text = await transcribe(uri, token);
    const reply = await sendMessage(vertical, sessionId, text, token);
    const audioBlob = await synthesize(reply, voiceId, token);

    const sound = new Audio.Sound();
    await sound.loadAsync({ uri: URL.createObjectURL(audioBlob) });
    await sound.playAsync();

    setStatus("idle");
  }

  return (
    <View style={styles.container}>
      <Text style={styles.status}>{status}</Text>
      <Pressable
        onPressIn={startRecording}
        onPressOut={stopRecordingAndSend}
        style={[styles.mic, status === "recording" && styles.micActive]}
      >
        <Text style={styles.micLabel}>Hold to talk</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", gap: 24 },
  status: { fontSize: 16, color: "#666" },
  mic: { width: 140, height: 140, borderRadius: 70, backgroundColor: "#4f46e5", alignItems: "center", justifyContent: "center" },
  micActive: { backgroundColor: "#dc2626" },
  micLabel: { color: "white", fontWeight: "600" },
});
