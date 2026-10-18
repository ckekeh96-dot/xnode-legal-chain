# XNode LegalChain AI

**AI-powered legal practice management platform** — a comprehensive demo integrating case management, document automation, smart contracts, blockchain agreement verification, client management, court scheduling, and legal workflows.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Windows 11 / macOS / Linux

### Installation & Run

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Start the server
python -m uvicorn app:app --host 0.0.0.0 --port 8787
```

Open **http://localhost:8787** in your browser.

### Demo Credentials

| User | Department | Password |
|------|-----------|----------|
| demo1–demo11 | Legal departments | DemoOnly!2026 |
| demo12 | Finance & Trust Accounting | DemoOnly!2026 |
| demo13 | Human Resources | DemoOnly!2026 |
| demo14 | CEO & Management (full access) | DemoOnly!2026 |

### Run Tests

```bash
python -m pip install pytest httpx
python -m pytest tests/ -q
```

**43 tests passing** — covers all API endpoints, authentication, authorization, and dashboard functionality.

##  Features

### Core Legal Practice Management
- **Matter Management** — Case tracking across 11 legal departments
- **Client Management** — Client records with document associations
- **Task Management** — Department-scoped tasks with due dates and status tracking
- **Calendar** — Court dates, consultations, and deadlines
- **Matter Notes** — Private case notes with audit logging

### Document & Workflow Automation
- **Document Management** — Upload, hash, and share documents across departments
- **Document Sharing** — Cross-department sharing with approval workflows
- **Draft Studio** — Deterministic offline templates for legal documents
- **Smart Contract Builder** — Solidity template generation (demo only, no deployment)
- **Workflows** — Multi-stage approval workflows per department

### Security & Compliance
- **Agreement Review** — Version control, approvals, and audit chain
- **Client Review Portal** — Token-based client review invitations
- **Clause Review** — Keyword-based contract clause checking
- **Account Security** — Session management, password changes, security events
- **Audit Chain** — Hash-linked audit log with CEO verification
- **CSRF Protection** — Optional enforcement via `XNODE_ENFORCE_CSRF=1`

### Advanced Features
- **Local AI Assistant** — Optional offline AI drafting (requires Ollama)
- **Registry Artifacts** — Base Sepolia smart contract registry (demo)
- **Finance & Trust Accounting** — Transaction tracking and reporting
- **HR Module** — Leave tracking and performance reviews
- **Messages** — Internal messaging system

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python 3.12 + FastAPI
- **Database**: SQLite (single-file, zero-config)
- **Frontend**: Vanilla JavaScript SPA (no build step)
- **Testing**: pytest + httpx (43 tests)

### Project Structure

```
XNode_LegalChai Demo/
├── app.py                 # FastAPI backend (all endpoints)
├── static/
│   └── index.html         # Single-page application
├── tests/
│   ├── test_v3.py         # Core auth & matters
│   ├── test_v7.py         # Documents & sharing
│   ├── test_v10.py        # Workflows
│   ├── test_v11.py        # Messages
│   ├── test_v12.py        # Finance
│   ├── test_v13.py        # HR
│   ├── test_v14.py        # Audit chain
│   ├── test_v15.py        # Security events
│   ├── test_v16.py        # Account security
│   ├── test_v17.py        # Client portal
│   ├── test_v18.py        # Registry artifacts
│   ├── test_v19.py        # Blockchain intents
│   ├── test_v20.py        # Deployment tracking
│   ├── test_v21.py        # Reconciliation
│   ├── test_v22.py        # AI + v25 dashboards
│   ├── test_v23.py        # Clause review
│   ├── test_v24.py        # Security hardening
│   └── test_access.py     # Access control
├── contracts/
│   ├── AgreementRegistry.sol
│   ── MilestoneEscrow.sol
├── requirements.txt
├── README.md
└── JUDGE_GUIDE.md         # Detailed feature walkthrough
```

### Security Model

- **Authentication**: Session-based with hashed tokens
- **Authorization**: Department-scoped access (CEO sees all)
- **CSRF**: Optional enforcement via environment variable
- **Audit**: Hash-linked chain for new events (CEO verification endpoint)
- **Data**: All synthetic — no real client data, no live blockchain

## 🔒 Security Notes

This is a **demonstration project** with synthetic data only:

- ✅ Session-based authentication with password hashing
- ✅ Department-scoped authorization
- ✅ CSRF protection (optional)
- ✅ Audit chain with hash linking
- ✅ Input validation on all endpoints

- ❌ No encryption-at-rest
- ❌ No MFA
- ❌ No rate limiting
- ❌ Audit chain can be rewritten by DB admin
- ❌ Not suitable for production or confidential data

**Production deployment would require**: comprehensive authentication, browser-origin review, MFA, encrypted data, independent security assessment, and immutable audit storage.

## 📝 License

MIT License — see LICENSE file for details.

## 🤝 Contributing

This is a hackathon demonstration project. For production use cases, contact XNode.

---

**Built for hackathon submission** — demonstrates full-stack legal tech platform with modern security practices.
