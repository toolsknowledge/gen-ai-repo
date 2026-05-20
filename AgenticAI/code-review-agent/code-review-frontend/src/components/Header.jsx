import { useState, useEffect } from "react";
import "./Header.css";

export default function Header() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((r) => r.json())
      .then((d) => setStatus(d.api_key_set ? "ready" : "no-key"))
      .catch(() => setStatus("offline"));
  }, []);

  const statusConfig = {
    checking: { dot: "#f59e0b", label: "Connecting..." },
    ready:    { dot: "#22c55e", label: "Agent Ready" },
    "no-key": { dot: "#f59e0b", label: "API Key Missing" },
    offline:  { dot: "#ef4444", label: "Backend Offline" },
  };
  const s = statusConfig[status];

  return (
    <header className="header">
      <div className="header-brand">
        <div className="header-logo">⬡</div>
        <div>
          <div className="header-title">Code Review Agent</div>
          <div className="header-sub">ReAct · Tool Calling · Claude AI</div>
        </div>
      </div>
      <div className="header-status">
        <span className="status-dot" style={{ background: s.dot }} />
        <span className="status-label">{s.label}</span>
      </div>
    </header>
  );
}
