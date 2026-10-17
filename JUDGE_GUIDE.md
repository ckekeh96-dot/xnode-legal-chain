# XNode LegalChain AI - Judge Evaluation Guide

## System Overview

XNode LegalChain AI is a comprehensive legal practice management system designed for South African law firms. It combines matter management, client tracking, document handling, HR management, and financial oversight in a single integrated platform.

**Version:** v10.0  
**Technology Stack:** FastAPI (Python), SQLite, Vanilla JavaScript  
**Access:** http://localhost:8787

---

## Demo Login Credentials

The system includes 14 pre-configured demo accounts representing different roles and departments:

### Executive & Management
- **CEO:** `demo14` / `DemoOnly!2026` - Johan Botha (Chief Executive Officer)
  - Full system access including Finance, HR, and Audit modules

### Human Resources
- **HR Manager:** `demo13` / `DemoOnly!2026` - Fatima Patel
  - Access to HR module with employee management, leave tracking, and performance scores

### Finance
- **Trust Accountant:** `demo12` / `DemoOnly!2026` - David van der Merwe
  - Access to Finance module for trust accounting and financial records

### Legal Departments (demo1 - demo11)
All legal staff use password: `DemoOnly!2026`

| Username | Department | Name | Position |
|----------|-----------|------|----------|
| demo1 | Litigation & Dispute Resolution | Thabo Mokoena | Senior Associate |
| demo2 | Commercial & Corporate Law | Naledi Dlamini | Partner |
| demo3 | Conveyancing & Property Law | Sipho Nkosi | Conveyancer |
| demo4 | Family Law & Matrimonial | Zanele Mthembu | Associate |
| demo5 | Criminal Defense | Mandla Zulu | Senior Associate |
| demo6 | Administration of Estates & Trusts | Lerato Khumalo | Trust Administrator |
| demo7 | Labor & Employment Law | Bongani Sithole | Associate |
| demo8 | Personal Injury & MVA | Ayanda Ngcobo | Associate |
| demo9 | Debt Collection & Insolvency | Precious Molefe | Collections Manager |
| demo10 | Candidate Attorneys / Trainees | Kagiso Motaung | Candidate Attorney |
| demo11 | Legal Support & Secretarial | Nomvula Dube | Legal Secretary |

---

## Core Features

### 1. Dashboard
- Overview of matters, tasks, and documents
- Quick access to all accessible matters based on department permissions
- Real-time metrics display

### 2. Matter Management
- Create and track legal matters across 14 departments
- Priority levels: Low, Normal, High, Urgent
- Case types: Civil Litigation, Contract Drafting, Property Transfer, Family Law, Criminal Defense, Estate Administration, Labor Dispute, Personal Injury, Debt Collection
- Status tracking: Open, In Progress, Complete
- Detailed matter views with notes, events, workflows, documents, and agreements

### 3. Client Management
- Register synthetic clients with full contact details
- Client document uploads with SHA-256 hashing
- Related matters view for each client
- Address and ID number tracking

### 4. Calendar & Events
- Schedule court dates, consultations, and deadlines
- Event location tracking (venue or video link)
- Department-scoped event visibility

### 5. Matter Notes
- Private case notes per matter
- Timestamped entries with author tracking
- Chronological note history

### 6. Draft Studio
- Offline drafting templates (not AI-generated)
- Document type selection per matter
- Copy-to-clipboard functionality
- Attorney review required disclaimer

### 7. Smart Contract Builder
- Solidity template generation for demo purposes
- Local compilation support (requires solc)
- Metadata-only agreement titles
- No blockchain deployment or wallet connection
- Download generated .sol files

### 8. Agreement Review
- Version control for agreements
- Internal approval workflow (submit → approve/reject)
- Client review portal with invitation tokens
- SHA-256 content hashing
- PDF export functionality
- Evidence bundle generation
- Base Sepolia testnet anchoring (demo only)

### 9. Client Review Portal
- Token-based client access
- Review/decline decisions
- SHA-256 verification of agreement content
- No legally valid signature (demo only)

### 10. Registry Artifacts (CEO only)
- Base Sepolia registry artifact management
- Runtime bytecode verification
- Deployment tracking
- Transaction intent preparation and approval
- Session management and audit controls
- Audit report export with SHA-256 verification

### 11. Local AI Assistant
- Local AI legal draft assistant
- Provider and model status display
- Matter-specific document generation
- Synthetic text processing only

### 12. Clause Review
- Local keyword-based clause checks
- Not AI or legal advice
- Flag identification for sample contract text

### 13. Account Security
- Password change functionality
- Session management
- 12-character minimum password requirement

### 14. Security Activity
- Recent login history
- Password change tracking
- Audit trail visibility

### 15. Workflows
- Specialized legal workflow checklists
- Stage management (Pending, In Progress, Complete)
- Department-specific workflow templates
- Statutory date verification reminders

### 16. Messages
- Private department message board
- Subject and body messaging
- Department-scoped visibility

### 17. Documents
- File upload (max 5MB)
- SHA-256 hash verification
- Matter-scoped document management
- Download functionality

### 18. Sharing
- Cross-department document sharing requests
- Approval/rejection workflow
- CEO oversight of all sharing activities

### 19. Tasks
- Department-scoped task creation
- Due date tracking
- Status management

### 20. Finance (Finance & CEO only)
- Trust accounting demonstration
- Financial entry tracking
- Amount tracking in cents
- Kind classification (deposit, withdrawal, transfer, fee)
- Description logging

### 21. HR (HR & CEO only)
- **Department Overview:** 14 departments with employee counts
- **Employee List:** Clickable department cards showing all employees
- **Employee Details:**
  - Personal information (ID, department, position, email, phone, start date)
  - Leave balance (total days, taken days, remaining days)
  - Performance score (current year with visual progress bar)
  - **Performance Trend Chart:** Last 4 quarters visualization with line graph
  - Matters created by employee
  - Recent activities from audit log

### 22. Audit (CEO only)
- Complete audit trail
- Actor, action, resource, and timestamp tracking
- Chronological event history

---

## Department Access Control

The system implements strict department-scoped access:

- **Legal Staff (demo1-demo11):** Can only access their department's matters, clients, and documents
- **Finance (demo12):** Access to Finance module + their department
- **HR (demo13):** Access to HR module + their department
- **CEO (demo14):** Full system access including Finance, HR, and Audit

Workspace access is displayed on the Dashboard showing all departments the logged-in user can view.

---

## Security Features

1. **Session Management:** Token-based authentication with expiration
2. **CSRF Protection:** Optional CSRF token enforcement via environment variable
3. **Security Headers:** X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Cache-Control
4. **Cross-Origin Blocking:** Origin validation for state-changing requests
5. **Audit Chain:** Cryptographic hash chaining of audit events
6. **Password Hashing:** SHA-256 with salt
7. **Session Revocation:** Individual or bulk session termination

---

## Data Integrity

- **SHA-256 Hashing:** All documents and agreements are hashed
- **Audit Trail:** Every action is logged with timestamp and actor
- **Blockchain Anchoring:** Demo testnet hash payload preparation (Base Sepolia)
- **Evidence Bundles:** JSON export with bundle SHA-256 verification

---

## Mobile Responsive Design

The system is fully responsive with three breakpoints:
- **Desktop:** Full sidebar navigation (240px)
- **Tablet (≤1024px):** Compressed sidebar (200px)
- **Mobile (≤768px):** Hamburger menu with slide-out sidebar
- **Small Mobile (≤480px):** Single-column layout

---

## Important Disclaimers

️ **LOCAL DEMO — Do not enter real client data, upload confidential files, or record real trust funds.**

- All data is synthetic and for demonstration purposes only
- Smart contracts are demo templates, NOT legal agreements
- No blockchain deployment or wallet connection
- AI assistant is local-only, not connected to external services
- Clause review uses keyword matching, not AI or legal advice
- Client review portal has no identity verification or legally valid signature
- Agreement review is internal approvals only, not electronic signatures

---

## Technical Architecture

### Backend
- **Framework:** FastAPI with Uvicorn
- **Database:** SQLite with foreign key enforcement
- **Authentication:** Session tokens with SHA-256 hashing
- **Middleware:** Security headers, CSRF protection, CORS blocking

### Frontend
- **Technology:** Vanilla JavaScript (no framework)
- **Styling:** CSS Grid, Flexbox, custom properties
- **Responsive:** Mobile-first with media queries
- **Charts:** SVG-based performance trend visualization

### Database Schema
- 25+ tables covering users, matters, clients, documents, agreements, workflows, messages, tasks, finance, HR, audit, blockchain registry, and security events
- Foreign key relationships for data integrity
- Indexes on frequently queried columns

---

## Running the System

```bash
# Install dependencies
pip install fastapi uvicorn python-multipart

# Start server
python -m uvicorn app:app --host 0.0.0.0 --port 8787

# Access application
# Open http://localhost:8787 in browser
```

The database is automatically created on first run with all demo data seeded.

---

## Evaluation Criteria

When evaluating this system, consider:

1. **Functionality:** All 22 modules are operational with proper access control
2. **Security:** Multiple layers of security including session management, CSRF protection, and audit trails
3. **User Experience:** Clean, modern UI with mobile responsiveness
4. **Data Integrity:** SHA-256 hashing, audit chains, and evidence bundles
5. **HR Management:** Comprehensive employee tracking with leave, performance, and activity monitoring
6. **Financial Oversight:** Trust accounting demo with proper access restrictions
7. **Blockchain Integration:** Demo testnet anchoring with proper disclaimers
8. **Code Quality:** Clean separation of concerns, proper error handling, and comprehensive API documentation

---

## Contact & Support

This is a demonstration system for evaluation purposes. All data is synthetic and should not be used for production legal practice management.

**System Status:** Fully operational  
**Last Updated:** October 2026  
**Demo Environment:** Localhost only
