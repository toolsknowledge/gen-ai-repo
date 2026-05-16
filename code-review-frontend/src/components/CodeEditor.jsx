import { useRef } from "react";
import "./CodeEditor.css";

const LANGUAGES = ["python", "javascript", "java", "go", "typescript"];

const EXT_MAP = {
  ".py": "python", ".js": "javascript", ".jsx": "javascript",
  ".ts": "typescript", ".tsx": "typescript", ".java": "java",
  ".go": "go", ".rb": "ruby", ".cpp": "cpp", ".c": "c",
};

const LOG_COLORS = {
  info: "#6060a0", tool: "#00d4ff", done: "#22c55e", error: "#ef4444",
};

export default function CodeEditor({
  code, language, onChange, onLanguageChange,
  onQuickScan, onFullReview, loading, scanning,
  agentLog, sampleCodes,
}) {
  const fileInputRef = useRef(null);

  const readFile = (file) => {
    if (!file) return;
    const ext = "." + file.name.split(".").pop().toLowerCase();
    const detectedLang = EXT_MAP[ext] || "python";
    onLanguageChange(detectedLang);
    const reader = new FileReader();
    reader.onload = (e) => onChange(e.target.result);
    reader.readAsText(file);
  };

  const handleFileUpload = (e) => {
    readFile(e.target.files[0]);
    e.target.value = "";
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove("drag-over");
    readFile(e.dataTransfer.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add("drag-over");
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove("drag-over");
  };

  return (
    <div className="editor-wrap">

      {/* Toolbar */}
      <div className="editor-toolbar">
        <div className="lang-tabs">
          {LANGUAGES.map((l) => (
            <button
              key={l}
              className={`lang-tab ${language === l ? "active" : ""}`}
              onClick={() => onLanguageChange(l)}
            >
              {l}
            </button>
          ))}
        </div>
        <div className="toolbar-right">
          <button
            className="btn btn-upload btn-sm"
            onClick={() => fileInputRef.current.click()}
          >
            📁 Upload File
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".py,.js,.jsx,.ts,.tsx,.java,.go,.rb,.cpp,.c,.cs,.php,.swift,.kt,.rs"
            style={{ display: "none" }}
            onChange={handleFileUpload}
          />
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => onChange(sampleCodes[language] || "")}
          >
            Sample
          </button>
        </div>
      </div>

      {/* Drop zone banner — shown when no code */}
      {!code.trim() && (
        <div
          className="drop-zone"
          onClick={() => fileInputRef.current.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="drop-icon">📂</div>
          <div className="drop-title">Drop your code file here</div>
          <div className="drop-sub">or click to browse — .py .js .ts .java .go .cpp and more</div>
        </div>
      )}

      {/* Code area */}
      {code.trim() && (
        <div
          className="editor-area"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="line-numbers">
            {code.split("\n").map((_, i) => (
              <span key={i}>{i + 1}</span>
            ))}
          </div>
          <textarea
            className="code-textarea"
            value={code}
            onChange={(e) => onChange(e.target.value)}
            spellCheck={false}
          />
        </div>
      )}

      {/* Action buttons */}
      <div className="editor-actions">
        <button
          className="btn btn-secondary"
          onClick={onQuickScan}
          disabled={loading || scanning || !code.trim()}
        >
          {scanning ? "⏳ Scanning..." : "⚡ Quick Scan"}
        </button>
        <button
          className="btn btn-primary"
          onClick={onFullReview}
          disabled={loading || !code.trim()}
          style={{ flex: 1 }}
        >
          {loading ? "⏳ Agent Working..." : "🚀 Full AI Review"}
        </button>
      </div>

      {/* Agent log */}
      {agentLog.length > 0 && (
        <div className="agent-log">
          <div className="log-title">AGENT LOG</div>
          {agentLog.map((entry, i) => (
            <div key={i} className="log-entry" style={{ color: LOG_COLORS[entry.type] }}>
              <span className="log-num">[{String(i + 1).padStart(2, "0")}]</span>
              {entry.msg}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
