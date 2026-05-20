import "./ReviewPanel.css";

function MetricCard({ label, value, color }) {
  return (
    <div className="metric-card">
      <div className="metric-value" style={{ color }}>{value}</div>
      <div className="metric-label">{label}</div>
    </div>
  );
}

function SecurityIssue({ issue }) {
  const sev = issue.severity?.toUpperCase();
  return (
    <div className={`sec-issue sec-${sev?.toLowerCase()}`}>
      <span className={`badge badge-${sev?.toLowerCase()}`}>{sev}</span>
      <span className="sec-label">{issue.issue}</span>
    </div>
  );
}

function MarkdownView({ text }) {
  const lines = text.split("\n");
  return (
    <div className="markdown">
      {lines.map((line, i) => {
        if (line.startsWith("## "))
          return <h2 key={i} className="md-h2">{line.slice(3)}</h2>;
        if (line.startsWith("### "))
          return <h3 key={i} className="md-h3">{line.slice(4)}</h3>;
        if (line.startsWith("| ")) {
          const cells = line.split("|").filter(Boolean).map((c) => c.trim());
          return (
            <div key={i} className="md-table-row">
              {cells.map((c, j) => (
                <span key={j} className="md-cell">{c.replace(/\*\*/g, "")}</span>
              ))}
            </div>
          );
        }
        if (line.startsWith("- ") || line.startsWith("* "))
          return <li key={i} className="md-li">{renderInline(line.slice(2))}</li>;
        if (/^\d+\. /.test(line))
          return <li key={i} className="md-li md-oli">{renderInline(line.replace(/^\d+\. /, ""))}</li>;
        if (line.trim() === "" || line.startsWith("|---"))
          return <div key={i} className="md-gap" />;
        return <p key={i} className="md-p">{renderInline(line)}</p>;
      })}
    </div>
  );
}

function renderInline(text) {
  const parts = text.split(/(\*\*.*?\*\*|`.*?`)/g);
  return parts.map((p, i) => {
    if (p.startsWith("**") && p.endsWith("**"))
      return <strong key={i}>{p.slice(2, -2)}</strong>;
    if (p.startsWith("`") && p.endsWith("`"))
      return <code key={i} className="md-code">{p.slice(1, -1)}</code>;
    return p;
  });
}

export default function ReviewPanel({ review, metrics, security, loading, error }) {
  if (loading) {
    return (
      <div className="panel-empty">
        <div className="spinner" />
        <div className="empty-title">Agent is reviewing your code...</div>
        <div className="empty-sub">This takes 15–30 seconds</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel-empty">
        <div className="error-icon">⚠</div>
        <div className="empty-title">Something went wrong</div>
        <div className="error-msg">{error}</div>
        <div className="empty-sub">Make sure the backend is running: <code>uvicorn server:app --reload</code></div>
      </div>
    );
  }

  if (!review && !metrics) {
    return (
      <div className="panel-empty">
        <div className="empty-icon">◈</div>
        <div className="empty-title">Paste code and click review</div>
        <div className="empty-sub">The agent will analyze bugs, security, performance, and code quality</div>
        <div className="how-it-works">
          <div className="how-title">How the agent works</div>
          {[
            "You submit code to the React UI",
            "React POSTs to FastAPI backend",
            "Agent loop: LLM thinks → calls tools",
            "Tools scan security & complexity",
            "Final structured review returned",
          ].map((s, i) => (
            <div key={i} className="how-step">
              <span className="how-num">{i + 1}</span>
              <span>{s}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="review-panel">
      {/* Metrics */}
      {metrics && (
        <section className="review-section">
          <div className="section-title">⚡ Code Metrics</div>
          <div className="metrics-grid">
            <MetricCard label="Lines" value={metrics.total_lines} color="#00d4ff" />
            <MetricCard label="Functions" value={metrics.function_count} color="#22c55e" />
            <MetricCard label="Complexity" value={metrics.cyclomatic_complexity} color={metrics.cyclomatic_complexity > 20 ? "#ef4444" : metrics.cyclomatic_complexity > 10 ? "#f59e0b" : "#22c55e"} />
            <MetricCard label="Max Depth" value={metrics.max_nesting_depth} color={metrics.max_nesting_depth > 4 ? "#ef4444" : "#7c3aed"} />
          </div>
          <div className="complexity-bar-wrap">
            <span className="complexity-label">Complexity: {metrics.rating}</span>
            <div className="complexity-bar">
              <div
                className="complexity-fill"
                style={{
                  width: `${Math.min((metrics.cyclomatic_complexity / 30) * 100, 100)}%`,
                  background: metrics.rating === "Low" ? "#22c55e" : metrics.rating === "Medium" ? "#f59e0b" : "#ef4444"
                }}
              />
            </div>
          </div>
        </section>
      )}

      {/* Security */}
      {security && (
        <section className="review-section">
          <div className="section-header">
            <div className="section-title">🔒 Security Scan</div>
            <span className={`badge badge-${security.score?.toLowerCase()}`}>
              {security.score} — {security.issues_found} issue{security.issues_found !== 1 ? "s" : ""}
            </span>
          </div>
          {security.issues?.length > 0 ? (
            <div className="sec-list">
              {security.issues.map((issue, i) => (
                <SecurityIssue key={i} issue={issue} />
              ))}
            </div>
          ) : (
            <div className="no-issues">✓ No security patterns detected</div>
          )}
        </section>
      )}

      {/* AI Review */}
      {review && (
        <section className="review-section">
          <div className="section-title">🤖 AI Deep Review</div>
          <div className="review-card">
            <MarkdownView text={review} />
          </div>
        </section>
      )}
    </div>
  );
}
