# 🔍 Code audit ai: AI-Powered Code Quality & Security Audit System

![Code audit ai Banner](https://img.shields.io/badge/Code%20Audit%20AI-v2.0-blue?style=for-the-badge&logo=shield)
![Status](https://img.shields.io/badge/Status-Complete%20Overhaul-success?style=for-the-badge)
![CI/CD](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)

Code audit ai is a high-performance, containerized code auditing system that combines pattern-based security scans with AI-powered analysis. Built for speed, privacy, and modern developer workflows.

---

### ✨ Features
- **🚀 High Performance:** Powered by FastAPI with asynchronous background processing.
- **🎨 Premium UI:** Modern dashboard with real-time logs, glassmorphism design, and Light/Dark mode.
- **🤖 Dual AI Engine:** Supports local **Ollama** (DeepSeek/Llama) and cloud-based **Groq** for lightning-fast analysis.
- **�️ CI/CD Integrated:** Automated testing and build verification via GitHub Actions.
- **� Advanced Analytics:** Real-time risk scoring and threat distribution charts.
- **🐳 Cloud Ready:** Optimized for 100% free hosting on Render (Backend) and Vercel (Frontend).

---

### 🛠️ Tech Stack
- **Frontend:** HTML5/CSS3 (Modern Design System), Lucide Icons, Chart.js.
- **Backend:** FastAPI (Python), Git (Shallow cloning), PostgreSQL (Cloud) / SQLite (Local).
- **AI Engine:** Ollama (Local) or Groq API (Cloud).
- **Infrastructure:** Docker, GitHub Actions (CI/CD).

---

### 🚀 Getting Started

#### 1. Local Setup (Development)
```bash
# Clone the repository
git clone https://github.com/your-username/Code-Quality-Security-Audit-System-AI-Agent.git
cd Code-Quality-Security-Audit-System-AI-Agent

# Setup Backend
cd backend
python -m venv venv
source venv/bin/scripts/activate  # On Windows: .\venv\Scripts\activate
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

#### 3. Access the Dashboard
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8005/api/v1](http://localhost:8005/api/v1)

---

### 📁 Project Structure
```text
├── .github/workflows/  # CI/CD Pipeline (GitHub Actions)
├── backend/            # FastAPI Python Backend
│   ├── app/
│   │   ├── api/        # REST Endpoints
│   │   ├── core/       # Security Analysis Engine (Regex Patterns)
│   │   ├── db/         # SQLAlchemy Models & Session Management
│   │   └── services/   # AI Integration (Ollama & Groq)
│   ├── tests/          # Automated Test Suite (Pytest)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/           # Modern Dashboard (HTML/CSS/JS)
│   ├── index.html      # Main Application UI
│   └── src/            # Design System & Scripts
└── docker-compose.yml  # Container Orchestration
```

---

### 🧮 Risk Score Interpretation

The system uses a **Density-Based Scoring (0-100)** algorithm that measures the concentration of vulnerabilities per 200 lines of code.

- **🔴 80 - 100: CRITICAL**
  - High density of high-severity vulnerabilities. Dangerous for deployment.
- **🟡 40 - 79: WARNING**
  - Significant security or quality debt. Needs structured review.
- **🟢 0 - 39: STABLE**
  - Clean codebase with manageable risks.

---

### 🧪 CI/CD Verification
This project includes a fully automated CI/CD pipeline. Every push to `main` triggers:
1. **Dependency Validation**: Ensures all packages install correctly.
2. **Automated Testing**: Runs the Pytest suite to verify API integrity.
3. **Docker Build Check**: Verifies that the container image builds without errors.

---

<div align="center">
  <p><strong>Developed for the Modern Security Community ❤️</strong></p>
</div>
