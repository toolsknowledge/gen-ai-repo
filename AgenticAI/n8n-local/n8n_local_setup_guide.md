# n8n Customer Support Bot — Local Setup Guide
**Stack:** Docker · n8n (self-hosted) · ngrok · OpenAI GPT-4o · Gmail OAuth · Google Sheets · Jira

---

## Overview

This guide sets up the full Customer Support Bot on your local machine — no cloud n8n account needed. The architecture is identical to the cloud version; only the install and credential setup differ.

```
Your Machine
├── Docker Container: n8n (port 5678)
├── Docker Volume:    n8n_data (workflows + credentials persisted)
└── ngrok tunnel:     https://xxxx.ngrok-free.app → localhost:5678
         │
         └── Used ONLY for Google OAuth callback (Gmail auth)
             After auth is done, ngrok can stay running or be stopped
```

---

## Part 1 — Install & Run n8n with Docker

### 1a. Prerequisites

```bash
# Verify Docker is installed
docker --version        # Need 20.x or higher
docker compose version  # Need v2.x

# If not installed:
# Mac:     brew install --cask docker  (then open Docker.app)
# Ubuntu:  sudo apt install docker.io docker-compose-plugin
# Windows: install Docker Desktop from docker.com
```

### 1b. Create a project folder

```bash
mkdir ~/n8n-local && cd ~/n8n-local
```

### 1c. Create docker-compose.yml

Create the file `~/n8n-local/docker-compose.yml` with this content:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      # Core config
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production

      # IMPORTANT: This tells n8n what URL to use for OAuth callbacks
      # We'll update this with the ngrok URL in Part 2
      - WEBHOOK_URL=http://localhost:5678/

      # Security — change this to a strong random string
      - N8N_ENCRYPTION_KEY=your-super-secret-key-change-this-32chars

      # Optional: disable telemetry
      - N8N_DIAGNOSTICS_ENABLED=false
      - N8N_VERSION_NOTIFICATIONS_ENABLED=false

      # Timezone
      - GENERIC_TIMEZONE=Asia/Kolkata

    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
    driver: local
```

> **N8N_ENCRYPTION_KEY** is critical — it encrypts all saved credentials. Generate a random 32-char string:
> ```bash
> openssl rand -hex 16
> ```
> Save this key somewhere safe. If lost, all saved credentials become unreadable.

### 1d. Start n8n

```bash
cd ~/n8n-local
docker compose up -d

# Verify it's running
docker compose logs -f n8n
# Look for: "n8n ready on 0.0.0.0, port 5678"
```

### 1e. Open n8n UI

Open your browser: **http://localhost:5678**

On first run, n8n will ask you to create an owner account (name + email + password). This is local-only — not connected to any cloud service.

---

## Part 2 — Set Up ngrok (for Gmail OAuth Callback)

Gmail OAuth requires a publicly accessible HTTPS callback URL. ngrok creates a temporary tunnel from the internet to your localhost.

### 2a. Install ngrok

```bash
# Mac
brew install ngrok

# Ubuntu / Debian
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Or download directly from: https://ngrok.com/download
```

### 2b. Create a free ngrok account

Go to **https://ngrok.com** → Sign up (free) → Copy your authtoken from the dashboard.

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### 2c. Start the tunnel

```bash
ngrok http 5678
```

You'll see output like:
```
Forwarding   https://a1b2-103-21-45-67.ngrok-free.app -> http://localhost:5678
```

**Copy that HTTPS URL** — you need it in the next two steps.

> **Important:** Free ngrok URLs change every time you restart ngrok. For a permanent URL, upgrade to ngrok paid tier ($8/mo) or use a self-signed cert setup. For initial setup and testing, the free URL is fine.

### 2d. Update n8n's WEBHOOK_URL

Edit `docker-compose.yml` and replace the WEBHOOK_URL line:

```yaml
- WEBHOOK_URL=https://a1b2-103-21-45-67.ngrok-free.app/
```

Restart n8n to pick up the change:

```bash
docker compose down && docker compose up -d
```

Now n8n will tell Google to redirect OAuth callbacks to your ngrok URL → which tunnels back to your local n8n.

---

## Part 3 — Create Google OAuth App (for Gmail)

This is a one-time setup. You need a Google Cloud project with Gmail API enabled.

### 3a. Create a Google Cloud Project

1. Go to **https://console.cloud.google.com**
2. Top left → click project dropdown → **New Project**
3. Name: `n8n-local` → **Create**
4. Make sure the new project is selected in the top bar

### 3b. Enable Gmail API

1. Go to **APIs & Services → Library**
2. Search: `Gmail API` → Click it → **Enable**
3. Also enable: `Google Sheets API` (needed for the KB tool later)

### 3c. Configure OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**
2. User Type: **External** → **Create**
3. Fill in:
   - App name: `n8n Local`
   - User support email: your Gmail
   - Developer contact: your Gmail
4. Click **Save and Continue** through the Scopes page (skip adding scopes here)
5. On **Test users** page → **Add Users** → add your Gmail address
6. Click **Save and Continue** → **Back to Dashboard**

> **Why "External" + Test users?** For personal use you don't need Google to verify your app. Adding yourself as a test user lets you authenticate without verification.

### 3d. Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. **+ Create Credentials** → **OAuth client ID**
3. Application type: **Web application**
4. Name: `n8n Gmail`
5. Under **Authorized redirect URIs** → **+ Add URI**:
   ```
   https://a1b2-103-21-45-67.ngrok-free.app/rest/oauth2-credential/callback
   ```
   *(Use your actual ngrok URL)*
6. **Create** → Copy the **Client ID** and **Client Secret**

---

## Part 4 — Add Credentials in n8n

### 4a. Add Gmail (OAuth2) Credential

1. In n8n: **Settings → Credentials → + Add Credential**
2. Search: **Gmail OAuth2**
3. Fill in:
   - **Client ID**: from Google Cloud Console
   - **Client Secret**: from Google Cloud Console
4. Click **Sign in with Google** → Complete the OAuth flow in the popup
5. You'll see `"Account connected"` — Save

### 4b. Add OpenAI Credential

1. **+ Add Credential** → **OpenAI**
2. Paste your **API Key** from platform.openai.com
3. Save

### 4c. Add Google Sheets Credential

1. **+ Add Credential** → **Google Sheets OAuth2**
2. Use the same Client ID + Client Secret (Google project has both APIs enabled)
3. Click **Sign in with Google** → Authorize
4. Save

---

## Part 5 — Create the Knowledge Base (Google Sheet)

Create a new Google Sheet and populate it:

| category | keywords | answer |
|---|---|---|
| password_reset | password, reset, forgot, login, cant login | To reset your password, visit Settings → Security → Reset Password. You'll receive an email within 2 minutes. |
| billing | invoice, charge, refund, payment, receipt | Log in and go to Account → Billing for invoices. Refunds take 3–5 business days. |
| account_locked | locked, suspended, access denied, banned | Accounts lock after 5 failed logins. Wait 15 minutes or email us with your account address. |
| slow_performance | slow, lag, loading, timeout, performance | Try clearing cache (Ctrl+Shift+R). If persists, check our status page at status.yourapp.com |
| feature_request | feature, suggestion, idea, improvement | We love feedback! Post suggestions at feedback.yourapp.com — upvoted items go to the roadmap. |

Note the **Sheet ID** from the URL:
`https://docs.google.com/spreadsheets/d/`**`[SHEET_ID_HERE]`**`/edit`

---

## Part 6 — Build the Workflow

Open **http://localhost:5678** → **+ New Workflow** → Name it `Customer Support Bot`

### Node 1: Gmail Trigger

1. **+ Add node** → search `Gmail Trigger`
2. **Credential**: select your Gmail OAuth2 credential
3. Settings:
   - **Trigger On**: `New Email`
   - **Filters → Label Names**: `INBOX`
   - **Poll Times**: `Every Minute` (for testing)
4. Under **Options**:
   - **Download Attachments**: OFF
   - **Include Spam/Trash**: OFF

Add an **IF node** after Gmail Trigger to filter noise:
- **Condition**: `{{ $json.from }}` **does not contain** `noreply`
- Connect `true` branch to the AI Agent

### Node 2: AI Agent

1. **+ Add node** → search `AI Agent`
2. **Agent**: `Tools Agent`
3. **Prompt → User Message**:
```
New support email received.

From: {{ $json.from }}
Subject: {{ $json.subject }}
Body:
{{ $json.text }}

Message ID: {{ $json.id }}

Analyze this email and handle it using your available tools.
```
4. **Options**:
   - **Max Iterations**: `5` (prevents infinite loops)
   - **Return Intermediate Steps**: ON (for debugging)

### Node 3: OpenAI Chat Model (connect to Agent's "Chat Model" input)

1. **+ Add node** → `OpenAI Chat Model`
2. **Credential**: your OpenAI credential
3. Settings:
   - **Model**: `gpt-4o`
   - **Temperature**: `0.2`
   - **Max Tokens**: `1000`

### Node 4: Tool — Search Knowledge Base (connect to Agent's "Tools" input)

1. **+ Add node** → `Google Sheets`
2. **Credential**: your Google Sheets credential
3. Settings:
   - **Operation**: `Read Rows`
   - **Document ID**: paste your Sheet ID
   - **Sheet Name**: `Sheet1`
4. Rename node: `Search Knowledge Base`
5. **Settings tab → Tool Description**:
```
Search the FAQ knowledge base for answers to common support questions.
Call this FIRST before any other tool.
Returns rows with: category, keywords, and answer columns.
Match the customer's issue against keywords to find the right answer.
```

### Node 5: Tool — Send Email Reply (connect to Agent's "Tools" input)

1. **+ Add node** → `Gmail`
2. **Credential**: same Gmail credential
3. **Operation**: `Send`
4. Rename node: `Send Email Reply`
5. Set these fields as **Expressions** (click the `=` toggle on each field):
   - **To**: `{{ $fromAI('to', 'Recipient email address') }}`
   - **Subject**: `{{ $fromAI('subject', 'Email subject line starting with Re:') }}`
   - **Message**: `{{ $fromAI('body', 'The reply message body in plain text') }}`
6. **Settings tab → Tool Description**:
```
Send an email reply to the customer.
Use when you have a clear answer from the knowledge base.
Be professional, warm, and concise. Sign off as "Support Team".
Inputs required: to (customer email), subject (prefix with "Re: "), body (plain text answer under 150 words).
```

### Node 6: Tool — Create Support Ticket (connect to Agent's "Tools" input)

1. **+ Add node** → `HTTP Request`
2. Rename node: `Create Support Ticket`
3. Settings:
   - **Method**: `POST`
   - **URL**: `https://YOUR-DOMAIN.atlassian.net/rest/api/3/issue`
   - **Authentication**: `Header Auth`
   - **Name**: `Authorization`
   - **Value**: `Basic ` + base64 of `your@email.com:your_jira_api_token`

   Generate the base64 value:
   ```bash
   echo -n "your@email.com:your_jira_api_token" | base64
   ```

4. **Body → JSON**:
```json
{
  "fields": {
    "project": { "key": "SUPPORT" },
    "summary": "={{ $fromAI('summary', 'One line ticket title') }}",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [{
        "type": "paragraph",
        "content": [{
          "type": "text",
          "text": "={{ $fromAI('description', 'Full issue description with customer email and details') }}"
        }]
      }]
    },
    "issuetype": { "name": "Support Request" }
  }
}
```

5. **Settings tab → Tool Description**:
```
Create a Jira support ticket for issues that cannot be resolved from the knowledge base.
Use for: billing disputes, account investigations, bugs, or anything needing human review.
Inputs: summary (short title), description (include sender email + full issue context).
IMPORTANT: After creating the ticket, always follow up with Send Email Reply to acknowledge the customer.
```

### Node 7: Window Buffer Memory (connect to Agent's "Memory" input)

1. **+ Add node** → `Window Buffer Memory`
2. Settings:
   - **Session ID**: `{{ $('Gmail Trigger').item.json.from }}`
   - **Context Window Length**: `5`

### System Prompt (in AI Agent node)

In the AI Agent node → **System Message** field:

```
You are a helpful customer support agent for [Your Company Name].

Your workflow for every email:
1. ALWAYS call "Search Knowledge Base" first — no exceptions
2. Review the returned KB rows and check if any keywords match the customer's issue
3. Decision:
   - MATCH FOUND → Call "Send Email Reply" with the KB answer, adapted naturally for the customer
   - NO MATCH or COMPLEX ISSUE (billing disputes, account bans, data issues, bugs) → Call "Create Support Ticket" then "Send Email Reply" with an acknowledgment

TONE & RULES:
- Professional, warm, and concise — under 150 words per reply
- Use the customer's name if visible in their email signature
- Never invent information not in the KB
- Never promise timelines unless the KB specifies them
- Sign every reply: "Best regards, Support Team"
- Do not call the same tool more than once per email
```

---

## Part 7 — Test Locally

### Test 1: Auto-reply path

Send an email to your Gmail (the one n8n is connected to):
```
Subject: I forgot my password and can't get into my account
Body:   Hi, I forgot my password and the reset email isn't coming. Can you help?
```

**Watch the execution:**
1. Go to **Executions** tab in n8n
2. Click the latest run → expand AI Agent node
3. You should see the ReAct trace:
   - Thought: "I should search the knowledge base first"
   - Action: `Search Knowledge Base`
   - Observation: [KB rows returned]
   - Thought: "password_reset row matches — I'll send a reply"
   - Action: `Send Email Reply`
   - Final answer: done

### Test 2: Ticket creation path

```
Subject: I was charged twice this month
Body:   Hello, I see two charges of $29.99 on my credit card for this month. 
        I need one of them refunded. My account email is test@example.com
```

**Expected:** Agent creates Jira ticket + sends acknowledgment email.

### Debug tips

```bash
# View n8n logs in real time
docker compose logs -f n8n

# If a node errors, click it in the execution view
# The "Input" and "Output" panels show exact data flowing through

# Common error: "OAuth token expired"
# Fix: Go to Credentials → Gmail → Reconnect
```

---

## Part 8 — Keeping It Running

### Make n8n start on system boot

The `restart: unless-stopped` in docker-compose.yml handles this automatically once Docker starts. To ensure Docker starts on boot:

```bash
# Mac: Docker Desktop → Settings → General → "Start Docker Desktop when you log in"

# Ubuntu/Linux:
sudo systemctl enable docker
```

### Backup your workflows and credentials

```bash
# Export all workflows to JSON
docker exec n8n n8n export:workflow --all --output=/home/node/.n8n/workflows-backup.json

# Copy the backup out of the container
docker cp n8n:/home/node/.n8n/workflows-backup.json ~/n8n-backup-$(date +%Y%m%d).json

# To restore later:
docker cp ~/n8n-backup.json n8n:/home/node/.n8n/
docker exec n8n n8n import:workflow --input=/home/node/.n8n/n8n-backup.json
```

### Upgrade n8n

```bash
cd ~/n8n-local
docker compose pull          # pull latest image
docker compose down
docker compose up -d         # restart with new image
```

### ngrok persistence issue

Free ngrok URLs change on restart. Two options:

**Option A — Keep ngrok running in a tmux session:**
```bash
tmux new-session -d -s ngrok 'ngrok http 5678'
tmux attach -t ngrok        # to check the URL
```

**Option B — Use a static domain (ngrok free tier gives 1 free static domain):**
```bash
# In ngrok dashboard → Domains → Claim a free domain
ngrok http --domain=your-name.ngrok-free.app 5678
```
Then set this permanently in docker-compose.yml and you never need to update it again.

---

## Troubleshooting Quick Reference

| Problem | Fix |
|---|---|
| n8n UI not loading on :5678 | `docker compose ps` — check container is Up. `docker compose logs n8n` for errors |
| Gmail OAuth fails / redirect_uri_mismatch | Google Cloud Console → Credentials → make sure ngrok URL exactly matches (include trailing slash) |
| `$fromAI()` returns null | Field not switched to Expression mode. Click `=` toggle next to the field |
| Agent makes wrong decision | Improve Tool Description text — be more explicit about when to use/not use each tool |
| Agent runs forever (loops) | Set **Max Iterations** to 5 in Agent node Options |
| Credentials lost after restart | You didn't set `N8N_ENCRYPTION_KEY` consistently. Never change this key once set |
| Google Sheet returns empty | Check Sheet ID is correct and Sheet name matches exactly (case-sensitive) |

---

## Local vs Cloud — Key Differences Summary

| Aspect | n8n Cloud | Local (this guide) |
|---|---|---|
| Setup time | 2 min | ~45 min first time |
| Cost | $20/mo+ | Free (only pay OpenAI) |
| Gmail OAuth | Works out of box | Needs ngrok + Google Cloud app |
| Data privacy | Data on n8n servers | All on your machine |
| Uptime | 99.9% SLA | Depends on your machine |
| Upgrades | Automatic | Manual `docker compose pull` |
| Team sharing | Multi-user built in | Need reverse proxy + auth |

---

*Guide version: May 2026 | n8n self-hosted via Docker + ngrok*
