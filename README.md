# 🔍 Code audit ai: AI-Powered Code Quality & Security Audit System

![Code audit ai Banner](https://img.shields.io/badge/Code%20Audit%20AI-v2.0-blue?style=for-the-badge&logo=shield)
![Status](https://img.shields.io/badge/Status-Complete%20Overhaul-success?style=for-the-badge)
[![CI/CD](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/actions)

**Live Demo:** [https://code-audit-ai-frontend.onrender.com/](https://code-audit-ai-frontend.onrender.com/)

Code audit ai is a high-performance, containerized code auditing system that combines pattern-based security scans with AI-powered analysis. Built for speed, privacy, and modern developer workflows.

---

### ✨ Features
- **🚀 High Performance:** Powered by FastAPI with asynchronous background processing.
- **🎨 Premium UI:** Modern dashboard with real-time logs, glassmorphism design, and Light/Dark mode.
- **🤖 Dual AI Engine:** Supports local **Ollama** (DeepSeek/Llama) and cloud-based **Portfolio Mode** for free expert analysis.
- **🛡️ CI/CD Integrated:** Automated testing and build verification via GitHub Actions.
- **📊 Advanced Analytics:** Real-time risk scoring and threat distribution charts.
- **🐳 Cloud Ready:** Fully containerized and deployed on Render.

---

### 🛠️ Tech Stack
- **Frontend:** HTML5/CSS3, Lucide Icons, Chart.js, Nginx (Dockerized).
- **Backend:** FastAPI (Python), PostgreSQL, SQLAlchemy.
- **AI Engine:** Ollama (Local) / Built-in Expert Knowledge Base (Cloud).
- **Infrastructure:** Docker, GitHub Actions, Render Cloud.

---

### 🚀 Getting Started

#### 1. Local Setup
```bash
# Clone the repository
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent.git
cd Code-Quality-Security-Audit-System-AI-Agent

# Setup Backend
cd backend
python -m venv venv
# Windows: .\venv\Scripts\activate | Unix: source venv/bin/activate
pip install -r requirements.txt
python main.py

# Setup Frontend
cd ../frontend
python -m http.server 3000
```

#### 2. Docker Setup
```bash
docker-compose up -d --build
```

#### 3. Access
- **Live Site**: [https://code-audit-ai-frontend.onrender.com/](https://code-audit-ai-frontend.onrender.com/)
- **Local Dashboard**: [http://localhost:3000](http://localhost:3000)

---

### 📁 Project Structure
```text
├── .github/workflows/  # CI/CD Pipeline
├── backend/            # FastAPI Python Backend
│   ├── app/            # Logic, DB, & AI Services
│   ├── tests/          # Pytest Suite
│   └── Dockerfile      # API Container
├── frontend/           # Modern UI
│   ├── index.html      # Main Dashboard
│   └── Dockerfile      # Nginx Container
└── render.yaml         # Cloud Infrastructure (Blueprint)
```

---

### 🧮 Risk Score Interpretation
The system uses a **Density-Based Scoring (0-100)** algorithm checking vulnerabilities per LOC.
- **🔴 80-100: CRITICAL** - Immediate remediation required.
- **🟡 40-79: WARNING** - Significant technical & security debt.
- **🟢 0-39: STABLE** - Clean codebase with manageable risks.

---

### 🧪 Automated Quality Assurance
Every push to `main` triggers our GitHub Actions pipeline:
1. **Linting**: Checks code for PEP8 compliance.
2. **Pytest**: Verifies API endpoints and database integrity.
3. **Docker Build**: Ensures both containers build without errors before deployment.

---

<div align="center">
  <p><strong>Developed by Muhammad Farhan Tanvir ❤️</strong></p>
</div>
