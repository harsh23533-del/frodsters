"use client";
import { useEffect, useState } from "react";
import { getProgress } from "../../../lib/api";

export default function Progress({ params }) {
  const { vertical } = params;
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    getProgress(vertical).then(setMetrics).catch(() => setMetrics({}));
  }, [vertical]);

  return (
    <main style={{ padding: 40, maxWidth: 640, margin: "0 auto" }}>
      <h1>{vertical} progress</h1>
      <pre style={{ background: "#f7f7f7", padding: 16, borderRadius: 10 }}>
        {metrics ? JSON.stringify(metrics, null, 2) : "Loading..."}
      </pre>
    </main>
  );
}
