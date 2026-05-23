
import { useState, useCallback } from 'react'
import Editor from '@monaco-editor/react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const API = 'http://localhost:8000'

const PRIORITIES = {
  P1: { color: '#ef4444', bg: '#fef2f2', border: '#fecaca', label: 'Critical' },
  P2: { color: '#f97316', bg: '#fff7ed', border: '#fed7aa', label: 'High' },
  P3: { color: '#ca8a04', bg: '#fefce8', border: '#fde68a', label: 'Medium' },
  P4: { color: '#3b82f6', bg: '#eff6ff', border: '#bfdbfe', label: 'Low' },
  P5: { color: '#6b7280', bg: '#f9fafb', border: '#e5e7eb', label: 'Info' },
}

const LANGUAGES = [
  { value: 'python', label: 'Python', ext: '.py' },
  { value: 'java', label: 'Java', ext: '.java' },
  { value: 'javascript', label: 'JavaScript', ext: '.js' },
  { value: 'typescript', label: 'TypeScript', ext: '.ts' },
  { value: 'c', label: 'C', ext: '.c' },
  { value: 'cpp', label: 'C++', ext: '.cpp' },
  { value: 'csharp', label: 'C#', ext: '.cs' },
  { value: 'go', label: 'Go', ext: '.go' },
  { value: 'rust', label: 'Rust', ext: '.rs' },
  { value: 'ruby', label: 'Ruby', ext: '.rb' },
  { value: 'shell', label: 'Shell', ext: '.sh' },
  { value: 'sql', label: 'SQL', ext: '.sql' },
]

const SAMPLE_CODE = `import pickle, subprocess

def login(username, password):
    conn = get_db()
    query = "SELECT * FROM users WHERE name='" + username + "'"
    user = conn.execute(query).fetchone()
    if user and user["password"] == password:
        return True
    return False

def run_command(cmd):
    subprocess.call(cmd, shell=True)

def load_data(data):
    return pickle.loads(data)
`

function ScoreRing({ score }) {
  const color = score < 40 ? '#ef4444' : score < 70 ? '#f97316' : '#22c55e'
  const label = score < 40 ? 'Critical Risk' : score < 70 ? 'Needs Work' : 'Good Quality'
  const r = 52, circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
      <svg width="124" height="124" viewBox="0 0 124 124">
        <circle cx="62" cy="62" r={r} fill="none" stroke="#e2e8f0" strokeWidth="10" />
        <circle cx="62" cy="62" r={r} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          transform="rotate(-90 62 62)" style={{ transition: 'stroke-dashoffset 1.2s ease' }} />
        <text x="62" y="57" textAnchor="middle" fontSize="26" fontWeight="900" fill={color}>{score}</text>
        <text x="62" y="74" textAnchor="middle" fontSize="11" fill="#94a3b8">/100</text>
      </svg>
      <div>
        <div style={{ fontSize: 18, fontWeight: 700, color, marginBottom: 4 }}>{label}</div>
        <div style={{ fontSize: 13, color: '#64748b' }}>Code Quality Score</div>
      </div>
    </div>
  )
}

function IssueCard({ issue, index }) {
  const [open, setOpen] = useState(index < 4)
  const p = PRIORITIES[issue.priority] || PRIORITIES.P5
  return (
    <div style={{
      borderRadius: 10, marginBottom: 10, overflow: 'hidden',
      border: `1px solid ${p.border}`, borderLeft: `5px solid ${p.color}`,
      background: 'white', boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    }}>
      <div onClick={() => setOpen(!open)} style={{
        padding: '13px 18px', cursor: 'pointer', display: 'flex',
        alignItems: 'center', gap: 8, background: open ? p.bg : 'white',
        transition: 'background 0.15s',
      }}>
        <span style={{ background: p.color, color: 'white', padding: '2px 9px', borderRadius: 5, fontSize: 11, fontWeight: 700, flexShrink: 0 }}>
          {issue.priority}
        </span>
        <span style={{ background: '#f1f5f9', color: '#475569', padding: '2px 9px', borderRadius: 5, fontSize: 11, flexShrink: 0 }}>
          {issue.category}
        </span>
        {issue.cwe_reference && (
          <span style={{ background: '#fef3c7', color: '#92400e', padding: '2px 9px', borderRadius: 5, fontSize: 11, fontWeight: 600, flexShrink: 0 }}>
            {issue.cwe_reference}
          </span>
        )}
        {issue.line_number && (
          <span style={{ color: '#94a3b8', fontSize: 11, flexShrink: 0 }}>Line {issue.line_number}</span>
        )}
        <span style={{ fontWeight: 600, fontSize: 14, color: '#1e293b', flex: 1, marginLeft: 2 }}>
          {issue.title}
        </span>
        <span style={{ color: '#cbd5e1', fontSize: 14, flexShrink: 0 }}>{open ? '▲' : '▼'}</span>
      </div>

      {open && (
        <div style={{ padding: '4px 18px 18px', borderTop: `1px solid ${p.border}` }}>
          <p style={{ color: '#475569', fontSize: 14, margin: '12px 0 10px' }}>{issue.description}</p>
          {issue.code_snippet && (
            <pre style={{
              background: '#0f172a', color: '#e2e8f0', padding: '13px 16px',
              borderRadius: 8, fontSize: 13, overflowX: 'auto', margin: '8px 0',
              fontFamily: "'Fira Code','Cascadia Code',monospace",
            }}>{issue.code_snippet}</pre>
          )}
          {issue.suggested_fix && (
            <div style={{ background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 8, padding: '12px 16px', marginTop: 10 }}>
              <div style={{ color: '#15803d', fontWeight: 600, fontSize: 13, marginBottom: 6 }}>✅ Suggested Fix</div>
              <code style={{ color: '#166534', fontSize: 13, whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                {issue.suggested_fix}
              </code>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [tab, setTab] = useState('editor')
  const [code, setCode] = useState(SAMPLE_CODE)
  const [fileName, setFileName] = useState('example.py')
  const [language, setLanguage] = useState('python')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [reportUrl, setReportUrl] = useState(null)
  const [reviewTime, setReviewTime] = useState(null)

  const onDrop = useCallback(async (files) => {
    const file = files[0]
    if (!file) return
    const text = await file.text()
    setCode(text)
    setFileName(file.name)
    const ext = '.' + file.name.split('.').pop().toLowerCase()
    const found = LANGUAGES.find(l => l.ext === ext)
    if (found) setLanguage(found.value)
    setTab('editor')
    setResult(null)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/*': LANGUAGES.map(l => l.ext) },
    maxFiles: 1,
  })

  const reviewCode = async () => {
    if (!code.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    setReportUrl(null)
    const t0 = Date.now()
    try {
      const res = await axios.post(`${API}/review/code`, { code, file_name: fileName, language })
      setResult(res.data.result)
      setReportUrl(`${API}${res.data.report_url}`)
      setReviewTime(((Date.now() - t0) / 1000).toFixed(1))
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Review failed')
    } finally {
      setLoading(false)
    }
  }

  const counts = result
    ? Object.fromEntries(['P1','P2','P3','P4','P5'].map(p => [p, result.issues.filter(i => i.priority === p).length]))
    : {}

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif', overflow: 'hidden' }}>

      {/* ── Header ─────────────────────────────────── */}
      <header style={{
        background: 'linear-gradient(135deg,#0f172a 0%,#1e293b 100%)',
        padding: '0 28px', height: 60, display: 'flex', alignItems: 'center',
        justifyContent: 'space-between', flexShrink: 0,
        boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: 'linear-gradient(135deg,#3b82f6,#8b5cf6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 17,
          }}>🔍</div>
          <div>
            <div style={{ color: 'white', fontWeight: 700, fontSize: 15, lineHeight: 1.2 }}>Code Review Agent</div>
            <div style={{ color: '#64748b', fontSize: 11 }}>RAG · MCP · Claude AI · CWE/OWASP</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {reviewTime && (
            <span style={{ color: '#64748b', fontSize: 12 }}>⏱ {reviewTime}s</span>
          )}
          <span style={{ background: 'rgba(99,102,241,0.2)', color: '#a5b4fc', padding: '4px 12px', borderRadius: 20, fontSize: 11, fontWeight: 500 }}>
            Claude Sonnet 4.6
          </span>
          <button onClick={reviewCode} disabled={loading || !code.trim()} style={{
            background: loading ? '#374151' : 'linear-gradient(135deg,#3b82f6,#6366f1)',
            color: 'white', border: 'none', borderRadius: 8,
            padding: '9px 22px', fontSize: 13, fontWeight: 600,
            cursor: loading ? 'not-allowed' : 'pointer',
            boxShadow: loading ? 'none' : '0 4px 14px rgba(99,102,241,0.45)',
            transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: 7,
          }}>
            <span style={loading ? { display: 'inline-block', animation: 'spin 1s linear infinite' } : {}}>
              {loading ? '⟳' : '🔍'}
            </span>
            {loading ? 'Analyzing...' : 'Review Code'}
          </button>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Left — Code Input */}
        <div style={{ width: '50%', display: 'flex', flexDirection: 'column', borderRight: '1px solid #e2e8f0', background: 'white' }}>

          {/* Toolbar */}
          <div style={{
            padding: '10px 14px', background: '#f8fafc', borderBottom: '1px solid #e2e8f0',
            display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', flexShrink: 0,
          }}>
            {/* Tab toggle */}
            <div style={{ display: 'flex', background: '#e2e8f0', borderRadius: 7, padding: 3 }}>
              {[['editor','✏️ Editor'],['upload','📁 Upload']].map(([id, lbl]) => (
                <button key={id} onClick={() => setTab(id)} style={{
                  padding: '5px 13px', borderRadius: 5, border: 'none',
                  background: tab === id ? 'white' : 'transparent',
                  color: tab === id ? '#1e293b' : '#64748b',
                  fontWeight: tab === id ? 600 : 400,
                  cursor: 'pointer', fontSize: 12,
                  boxShadow: tab === id ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
                  transition: 'all 0.15s',
                }}>{lbl}</button>
              ))}
            </div>

            <input value={fileName} onChange={e => setFileName(e.target.value)}
              placeholder="filename.py"
              style={{ flex: 1, minWidth: 110, padding: '6px 11px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12, outline: 'none', color: '#1e293b' }} />

            <select value={language} onChange={e => setLanguage(e.target.value)}
              style={{ padding: '6px 11px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12, color: '#1e293b', background: 'white', cursor: 'pointer', outline: 'none' }}>
              {LANGUAGES.map(l => <option key={l.value} value={l.value}>{l.label}</option>)}
            </select>
          </div>

          {/* Editor / Drop zone */}
          <div style={{ flex: 1, overflow: 'hidden' }}>
            {tab === 'editor' ? (
              <Editor height="100%" language={language} value={code}
                onChange={v => setCode(v || '')} theme="vs-dark"
                options={{
                  fontSize: 14, minimap: { enabled: false },
                  scrollBeyondLastLine: false, padding: { top: 14 },
                  fontFamily: "'Fira Code','Cascadia Code',monospace",
                  fontLigatures: true, lineNumbers: 'on',
                  renderLineHighlight: 'all', smoothScrolling: true,
                }} />
            ) : (
              <div {...getRootProps()} style={{
                height: '100%', display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center',
                background: isDragActive ? '#eff6ff' : '#f8fafc',
                border: `3px dashed ${isDragActive ? '#3b82f6' : '#e2e8f0'}`,
                cursor: 'pointer', transition: 'all 0.2s', padding: 40, textAlign: 'center',
              }}>
                <input {...getInputProps()} />
                <div style={{ fontSize: 52, marginBottom: 14 }}>{isDragActive ? '📂' : '📁'}</div>
                <div style={{ fontSize: 16, fontWeight: 600, color: '#1e293b', marginBottom: 6 }}>
                  {isDragActive ? 'Drop it here!' : 'Drag & drop a code file'}
                </div>
                <div style={{ color: '#94a3b8', fontSize: 13, marginBottom: 14 }}>or click to browse</div>
                <div style={{ background: '#e2e8f0', color: '#64748b', padding: '5px 16px', borderRadius: 20, fontSize: 11 }}>
                  .py .java .js .ts .c .cpp .cs .go .rs .rb .sh .sql
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right — Results */}
        <div style={{ width: '50%', overflow: 'auto', background: '#f1f5f9' }}>

          {/* Empty state */}
          {!loading && !result && !error && (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 40, textAlign: 'center' }}>
              <div style={{ fontSize: 60, marginBottom: 20 }}>🛡️</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: '#1e293b', marginBottom: 10 }}>Ready to Review</div>
              <div style={{ color: '#64748b', fontSize: 14, maxWidth: 320, lineHeight: 1.7, marginBottom: 28 }}>
                A sample vulnerable Python file is already loaded.<br />
                Click <strong>Review Code</strong> to see it in action.
              </div>
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
                {[['🔍','CWE Detection'],['🛡️','OWASP Rules'],['🔧','Fix Suggestions'],['📊','P1–P5 Scoring'],['📝','HTML Report'],['⚡','RAG Context']].map(([icon,lbl]) => (
                  <div key={lbl} style={{ background: 'white', border: '1px solid #e2e8f0', borderRadius: 8, padding: '10px 16px', fontSize: 13, color: '#475569', display: 'flex', alignItems: 'center', gap: 6 }}>
                    {icon} {lbl}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: 40 }}>
              <div style={{ fontSize: 52, marginBottom: 20, animation: 'spin 2s linear infinite', display: 'inline-block' }}>⚙️</div>
              <div style={{ fontSize: 17, fontWeight: 600, color: '#1e293b', marginBottom: 16 }}>Analyzing your code...</div>
              {['Querying CWE & OWASP knowledge bases via RAG','Embedding code and searching fix examples','Calling Claude AI for deep security analysis','Building structured P1–P5 review report'].map((s, i) => (
                <div key={i} style={{ color: '#64748b', fontSize: 13, margin: '3px 0', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ color: '#3b82f6' }}>▶</span> {s}
                </div>
              ))}
            </div>
          )}

          {/* Error */}
          {error && (
            <div style={{ padding: 24 }}>
              <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 10, padding: 20, color: '#dc2626' }}>
                <div style={{ fontWeight: 700, marginBottom: 8 }}>❌ Review Failed</div>
                <div style={{ fontSize: 14 }}>{error}</div>
              </div>
            </div>
          )}

          {/* Results */}
          {result && (
            <div style={{ padding: 22 }}>

              {/* Score card */}
              <div style={{ background: 'white', borderRadius: 14, padding: '24px 28px', marginBottom: 16, boxShadow: '0 2px 10px rgba(0,0,0,0.08)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
                  <ScoreRing score={result.overall_score} />
                  <div style={{ flex: 1, minWidth: 200 }}>
                    <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 3 }}>{result.file_name}</div>
                    <div style={{ color: '#64748b', fontSize: 13, marginBottom: 10 }}>
                      {result.language} · {result.total_lines} lines · {result.issues.length} issues
                      {reviewTime && <span> · {reviewTime}s</span>}
                    </div>
                    <div style={{ color: '#475569', fontSize: 14, lineHeight: 1.65 }}>{result.review_summary}</div>
                    {reportUrl && (
                      <a href={reportUrl} target="_blank" rel="noreferrer" style={{
                        display: 'inline-flex', alignItems: 'center', gap: 6,
                        marginTop: 14, background: '#eff6ff', color: '#3b82f6',
                        padding: '8px 16px', borderRadius: 8, fontSize: 13, fontWeight: 600,
                        textDecoration: 'none', border: '1px solid #bfdbfe',
                      }}>
                        📥 Download HTML Report
                      </a>
                    )}
                  </div>
                </div>
              </div>

              {/* Priority stats */}
              <div style={{ display: 'flex', gap: 10, marginBottom: 18, flexWrap: 'wrap' }}>
                {Object.entries(PRIORITIES).map(([p, cfg]) => (
                  <div key={p} style={{
                    background: 'white', borderRadius: 10, padding: '14px 16px',
                    flex: 1, minWidth: 80, textAlign: 'center',
                    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
                    borderTop: `3px solid ${cfg.color}`,
                  }}>
                    <div style={{ fontSize: 26, fontWeight: 800, color: cfg.color }}>{counts[p] || 0}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{p}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8' }}>{cfg.label}</div>
                  </div>
                ))}
              </div>

              {/* Issue list */}
              <div style={{ fontWeight: 700, fontSize: 14, color: '#1e293b', marginBottom: 12 }}>
                Issues Found ({result.issues.length})
              </div>
              {result.issues.map((issue, i) => (
                <IssueCard key={i} issue={issue} index={i} />
              ))}
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }
        * { box-sizing: border-box }
        ::-webkit-scrollbar { width: 6px; height: 6px }
        ::-webkit-scrollbar-track { background: #f1f5f9 }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8 }
      `}</style>
    </div>
  )
}