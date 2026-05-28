# n8n Complete Beginner's Guide
### macOS + Node.js (npm) | From Zero to Running Workflows

---

## 📖 What is n8n? (Plain English)

Think of n8n as a **visual plumber for your apps and data**.

- You have App A (say, Gmail) and App B (say, Slack)
- n8n connects them with a **flow**: "When I get an email → send a Slack message"
- No deep coding needed — you drag, drop, and fill in fields
- It's like building with LEGO blocks, where each block does one job

It runs **locally on your computer**, meaning your data never leaves your machine.

---

## 🛠️ Part 1: Installation (macOS + Node.js)

### Step 1 — Install Node.js via nvm (recommended way)

n8n requires **Node.js version 18 or 20** (LTS). The best way to manage Node versions on a Mac is with **nvm** (Node Version Manager) — it lets you switch versions easily without breaking anything.

Open Terminal (Cmd+Space → type "Terminal") and run:

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

After it finishes, **close Terminal and open it again** (this loads nvm into your shell), then run:

```bash
# Install Node.js 20 LTS (Long Term Support — stable version)
nvm install 20

# Set it as your default
nvm use 20
nvm alias default 20
```

**Verify Node is installed:**
```bash
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

> **Why nvm instead of downloading from nodejs.org?**
> Direct installs often cause permission issues with global npm packages. nvm avoids this completely — n8n installs cleanly without needing `sudo`.

---

### Step 2 — Install n8n Globally

Now install n8n as a global npm package — this makes the `n8n` command available anywhere in your Terminal:

```bash
npm install -g n8n
```

This downloads n8n and all its dependencies (~300MB). It takes 2–5 minutes. You'll see lots of output scrolling — that's normal.

**Verify n8n installed:**
```bash
n8n --version
```
You should see a version number like `1.x.x`.

---

### Step 3 — Run n8n

Start n8n with one command:

```bash
n8n start
```

You'll see logs scroll by. When you see:
```
Editor is now accessible via:
http://localhost:5678
```
→ n8n is running! 🎉

n8n automatically creates a `~/.n8n` folder in your home directory to store all your workflows, credentials, and execution history.

---

### Step 4 — Open n8n in Your Browser

Open any browser and go to:
```
http://localhost:5678
```

You'll see the n8n setup screen. Create an owner account (just for local use — pick any email/password you like).

---

### Step 5 — Stop and Restart n8n

**To stop:** Press `Ctrl + C` in Terminal

**To start again next time:**
```bash
n8n start
```

That's it — one command, every time.

**Tip — Run n8n in the background** (so you can use the same Terminal window for other things):
```bash
n8n start &
```
The `&` sends it to the background. To stop it later: `pkill -f n8n`

**Tip — Auto-start on login** (optional, for power users):
```bash
# Create a simple launchd service so n8n starts when you log in
# Run n8n as a background service via npm
n8n start --tunnel
```
Or just keep it simple and run `n8n start` when you need it.

---

### Troubleshooting Common Issues

**"command not found: n8n"** → nvm wasn't loaded. Run `nvm use 20` first, then retry.

**Port 5678 already in use** → Something else is on that port. Run:
```bash
n8n start --port 5679
```
Then open `http://localhost:5679` instead.

**Permission errors during install** → Make sure you're using nvm and NOT the system Node. Run `which node` — it should show a path containing `.nvm`, not `/usr/local/bin`.

**n8n is slow to start first time** → Normal. It's initializing the SQLite database. Subsequent starts are much faster.

---

## 🧠 Part 2: Core Concepts in Plain English

### The n8n Canvas (The main screen)

When you click **"New Workflow"**, you see a big empty canvas. This is your **workspace** — like a whiteboard where you draw your automation.

### Nodes — The Building Blocks

Every step in your workflow is called a **Node**. Each node does exactly ONE thing:
- Fetch data from an API
- Send an email
- Wait for a webhook
- Transform/filter data
- Call an AI model

**Types of nodes:**
| Type | What it does | Example |
|------|-------------|---------|
| **Trigger** | Starts the workflow | "When I receive a webhook", "Every day at 9am" |
| **Action** | Does something | "Send email", "Post to Slack" |
| **Transform** | Changes data | "Set a value", "Filter rows", "Merge data" |
| **Logic** | Makes decisions | "If X then Y", "Loop over items" |
| **AI** | Calls LLMs | "Ask ChatGPT", "Classify text" |

### Connections — The Arrows

Nodes are connected by arrows. Data flows **left → right** through the arrows. The output of one node becomes the input of the next.

### Executions — Running Your Flow

When a workflow runs (either triggered or manually), it's called an **Execution**. You can see all past executions with their status (success ✅ / failed ❌) and inspect exactly what data flowed through each node.

### Credentials — Your Passwords (Stored Safely)

When connecting to Gmail, OpenAI, Slack etc., you store your API keys in **Credentials**. n8n encrypts them and reuses them across workflows — you don't paste API keys into every node.

### Expressions — Dynamic Values

Inside any node field, you can use `{{ }}` to reference data from previous nodes:
```
{{ $json.email }}           ← email field from the previous node's output
{{ $json.name.toUpperCase() }}  ← transform it inline
{{ $now.toISO() }}          ← current timestamp
```

---

## 🚀 Part 3: Your First Workflow (Hello World)

### Goal: Receive a web request → Reply with a message

**Step-by-step:**

1. Click **"New Workflow"** → give it a name: "Hello World"
2. Click the **+ button** in the center OR click **"Add first step"**
3. Search for **"Webhook"** → select it → it becomes your trigger node
4. In the Webhook node:
   - HTTP Method: `GET`
   - Path: `hello`
   - Response Mode: `Respond to Webhook`
5. Click **"Add node"** (the + on the right side of Webhook)
6. Search for **"Respond to Webhook"** → add it
7. In Respond to Webhook:
   - Response Body: `Hello from n8n! You called me at {{ $now.toISO() }}`
8. Connect the two nodes (they may auto-connect)
9. Click **"Listen for test event"** in the Webhook node
10. Open a new browser tab and visit: `http://localhost:5678/webhook-test/hello`
11. You'll see your "Hello from n8n!" response!

**What just happened:** Your browser sent a GET request → Webhook node caught it → Respond node sent back a message. That's a complete workflow!

---

## 🔧 How to Import the Sample Workflows

The sample workflow JSON files in this folder can be imported directly:

1. In n8n, go to **Workflows** → click **"..."** menu → **"Import from file"**
2. Select the `.json` file
3. The workflow opens on your canvas, ready to use
4. Add your API credentials where needed (marked with ⚠️)

---

## 📋 Part 4: Sample Use Cases Overview

| # | File | What it does | Difficulty |
|---|------|-------------|-----------|
| 1 | `workflow-01-hello-world.json` | Webhook → respond with data | ⭐ Beginner |
| 2 | `workflow-02-ai-question-answer.json` | POST a question → OpenAI answers → return response | ⭐⭐ Easy |
| 3 | `workflow-03-scheduled-data-pipeline.json` | Every hour → fetch weather API → save to file | ⭐⭐ Easy |
| 4 | `workflow-04-email-alert.json` | Webhook → send Gmail alert → log it | ⭐⭐⭐ Medium |
| 5 | `workflow-05-slack-notification.json` | HTTP trigger → process data → post to Slack | ⭐⭐⭐ Medium |

---

## 🔍 Part 5: Understanding the UI (Tour)

```
┌─────────────────────────────────────────────────────────────┐
│  [n8n logo]  Workflows  Credentials  Executions  Settings   │  ← Top nav
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [Webhook] ──► [Set data] ──► [OpenAI] ──► [Slack]       │  ← Canvas
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [▶ Execute]  [Save]  [Active toggle]                       │  ← Bottom bar
└─────────────────────────────────────────────────────────────┘
```

**Top Nav:**
- **Workflows** → list of all your flows
- **Credentials** → stored API keys
- **Executions** → history of all runs

**Canvas Controls:**
- Scroll wheel → zoom in/out
- Click + drag on empty space → pan around
- Click a node → open its settings panel on the right
- Drag from a node's right edge → create a connection

**Bottom Bar:**
- **Execute Workflow** → run it manually right now
- **Save** → don't forget to save!
- **Active toggle** → turn the workflow ON so it runs automatically on triggers

---

## 💡 Part 6: Key Tips for Beginners

### Always test before activating
Click **"Execute Workflow"** to test manually. Check each node's output by clicking on it after a test run — you'll see exactly what data it received and produced.

### Use the "Set" node to shape your data
Before sending data anywhere, use a **"Set"** node to pick exactly which fields you want. This keeps your payloads clean.

### Pin data for easier testing
When testing, right-click a node → "Pin data" → paste sample JSON. This lets you test downstream nodes without re-triggering the whole flow.

### The Expression Editor is your friend
Anywhere you see `{{ }}`, you can click the gear icon to open the Expression Editor. It shows you ALL available data from previous nodes in a tree view — just click to insert.

### Check Executions when something breaks
Go to **Executions** tab → click a failed run → see exactly which node failed and what error it threw. n8n gives you the full input/output at every step.

---

## 🔐 Part 7: Setting Up Common Credentials

### OpenAI (for AI workflows)
1. Go to: https://platform.openai.com/api-keys → create a key
2. In n8n: **Credentials** → New → search "OpenAI" → paste your key

### Gmail (for email workflows)
1. In n8n: **Credentials** → New → search "Gmail"
2. n8n uses OAuth2 — click "Sign in with Google" → authorize
3. ⚠️ You need to set up a Google Cloud OAuth app for this (guide: https://docs.n8n.io/integrations/builtin/credentials/google/)

### Slack
1. Go to: https://api.slack.com/apps → create an app → get Bot Token
2. In n8n: **Credentials** → New → "Slack" → paste your Bot Token
3. Add OAuth scopes: `chat:write`, `channels:read`

### Generic HTTP APIs (no special integration needed)
Use the **HTTP Request** node — just paste any REST API URL, pick GET/POST, add headers. Works with any API.

---

## 🏗️ Part 8: n8n Architecture (Quick Mental Model)

```
Your Browser
    │
    ▼
n8n Editor (http://localhost:5678)
    │   (you build workflows visually here)
    ▼
n8n Engine (running in Docker)
    │   (executes workflows, stores data)
    ▼
~/.n8n folder on your Mac
    │   (workflows, credentials, execution logs)
    ▼
External Services (OpenAI, Gmail, Slack, any API...)
```

When a workflow is **Active**, n8n's engine watches for triggers 24/7 (as long as Docker is running). When triggered, it runs the flow automatically in the background.

---

## 📚 Official Resources

- **n8n Docs:** https://docs.n8n.io
- **Node library (400+ integrations):** https://n8n.io/integrations
- **Community forum:** https://community.n8n.io
- **Workflow templates:** https://n8n.io/workflows

---

*Guide created for: Sambasiva Rao | macOS + Node.js (npm) setup | May 2026*
