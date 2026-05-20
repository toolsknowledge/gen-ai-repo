import { useState, useCallback } from "react";
import CodeEditor from "./components/CodeEditor";
import ReviewPanel from "./components/ReviewPanel";
import Header from "./components/Header";
import "./App.css";

const SAMPLE_CODES = {
  python: `def get_user(user_id):
    password = "admin123"
    conn = db.connect("postgresql://root:pass@prod/db")
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    result = conn.execute(query)
    data = pickle.loads(result[0])
    return data

def calculate_total(items):
    total = 0
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] == items[j] and i != j:
                total += items[i].price * 2
    return total`,

  javascript: `const API_KEY = "sk-prod-abc123xyz";
const db_password = "supersecret123";

app.get('/user', (req, res) => {
    const userId = req.query.id;
    const query = "SELECT * FROM users WHERE id = " + userId;
    db.query(query, (err, result) => {
        eval("console.log('fetching: " + userId + "')");
        res.send(result);
    });
});

function processUsers(users) {
    let result = [];
    for (let i = 0; i < users.length; i++) {
        for (let j = 0; j < users.length; j++) {
            for (let k = 0; k < users.length; k++) {
                result.push(users[i].name + users[j].age);
            }
        }
    }
    return result;
}`,

  java: `public class UserService {
    private String DB_PASSWORD = "admin123";
    private String SECRET_KEY = "jwt-secret-key-2024";

    public User getUser(String userId) {
        String query = "SELECT * FROM users WHERE id = '" + userId + "'";
        ResultSet rs = db.execute(query);
        return parseUser(rs);
    }

    public String hashPassword(String password) {
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] hash = md.digest(password.getBytes());
        return Arrays.toString(hash);
    }

    public void processAll(List<User> users) {
        for (int i = 0; i < users.size(); i++) {
            for (int j = 0; j < users.size(); j++) {
                if (users.get(i).equals(users.get(j))) {
                    process(users.get(i));
                }
            }
        }
    }
}`
};

export default function App() {
  const [code, setCode] = useState(SAMPLE_CODES.python);
  const [language, setLanguage] = useState("python");
  const [review, setReview] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [security, setSecurity] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);
  const [agentLog, setAgentLog] = useState([]);

  const addLog = (msg, type = "info") =>
    setAgentLog((prev) => [...prev, { msg, type, ts: Date.now() }]);

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    setCode(SAMPLE_CODES[lang] || "");
    setReview(null);
    setMetrics(null);
    setSecurity(null);
    setAgentLog([]);
  };

  const quickScan = useCallback(async () => {
    if (!code.trim()) return;
    setScanning(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
      });
      const data = await res.json();
      setMetrics(data.metrics);
      setSecurity(data.security);
    } catch {
      setError("Cannot connect to backend. Is the server running on port 8000?");
    }
    setScanning(false);
  }, [code, language]);

  const runFullReview = useCallback(async () => {
    if (!code.trim()) return;
    setLoading(true);
    setReview(null);
    setError(null);
    setAgentLog([]);

    addLog("Starting agent...", "info");
    addLog("Running security scanner...", "tool");
    addLog("Analyzing complexity metrics...", "tool");
    addLog("Sending to Claude AI for deep review...", "info");

    try {
      const res = await fetch("http://localhost:8000/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error");
      }

      const data = await res.json();
      addLog("Review complete!", "done");
      setReview(data.review);
      setMetrics(data.metrics);
      setSecurity(data.security);
    } catch (err) {
      addLog(`Error: ${err.message}`, "error");
      setError(err.message);
    }

    setLoading(false);
  }, [code, language]);

  return (
    <div className="app">
      <Header />
      <div className="main-layout">
        <div className="left-panel">
          <CodeEditor
            code={code}
            language={language}
            onChange={setCode}
            onLanguageChange={handleLanguageChange}
            onQuickScan={quickScan}
            onFullReview={runFullReview}
            loading={loading}
            scanning={scanning}
            agentLog={agentLog}
            sampleCodes={SAMPLE_CODES}
          />
        </div>
        <div className="right-panel">
          <ReviewPanel
            review={review}
            metrics={metrics}
            security={security}
            loading={loading}
            error={error}
          />
        </div>
      </div>
    </div>
  );
}
