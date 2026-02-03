# 🔍 Code audit ai: Code Quality & Security Audit System

![Code audit ai Banner](https://img.shields.io/badge/Code%20Audit%20AI-v2.0-blue?style=for-the-badge&logo=shield)
![Status](https://img.shields.io/badge/Status-Complete%20Overhaul-success?style=for-the-badge)

Code audit ai is a high-performance, containerized code auditing system that combines pattern-based security scans with local AI-powered analysis (via Ollama). Built for speed, privacy, and modern developer workflows.

---

### ✨ Features
- **🚀 High Performance:** Powered by FastAPI with asynchronous background processing.
- **🎨 Premium UI:** Modern dashboard with real-time logs and glassmorphism design.
- **🤖 AI-Driven:** Integrated with local Ollama models (`deepseek-coder`, `deepseek-r1`) for deep security insights.
- **🐳 Dockerified:** Simple one-command deployment for both frontend and backend.
- **🔒 Privacy First:** Scans and AI analysis run entirely on your local infrastructure.

---

### 🛠️ Tech Stack
- **Frontend:** HTML5/CSS3 (Modern Design System), Lucide Icons, Chart.js.
- **Backend:** FastAPI (Python), Git (Shallow cloning).
- **AI Engine:** Ollama (Local LLM API).
- **Infrastructure:** Docker, Nginx (Reverse Proxy).

---

### 🚀 Getting Started

#### 1. Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.ai/) (Running locally)

#### 2. Run the System
```bash
docker-compose up -d --build
```

#### 3. Access the Dashboard
Open your browser and navigate to:
**[http://localhost](http://localhost)**

---

### 📁 Structure
```
├── backend/            # FastAPI Python Backend
│   ├── app/
│   │   ├── api/        # REST Endpoints
│   │   ├── core/       # Security Analysis Engine
│   │   └── services/   # AI Integration
│   └── Dockerfile
├── frontend/           # Modern Dashboard Frontend
│   ├── src/            # Styles and Design System
│   └── index.html
└── docker-compose.yml  # Orchestration
```

---


---

### 🧮 Risk Score Interpretation

Code audit ai uses a density-based scoring system (0-100) to measure project health:

- **🔴 80 - 100: CRITICAL**
  - High density of high-severity vulnerabilities.
  - Dangerous for deployment. Immediate remediation required.
- **🟡 40 - 79: WARNING**
  - Significant security or quality debt.
  - Code needs cleanup and structured review.
- **🟢 0 - 39: STABLE**
  - Traceable issues but generally safe codebase concentration.
  - Follow recommendations for long-term health.

<div align="center">
  <p><strong>Made with ❤️ for the security community</strong></p>
</div>
