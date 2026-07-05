# 🚀 Nexus AI — Deployment & Infrastructure Blueprint

This directory contains the production-ready deployment blueprints, container definitions, and CI/CD configurations for **Nexus AI**.

The project is structured to support both **instant auto-deployments** (Render + Vercel) and **classic Cloud Provider infrastructures** (AWS App Runner / AWS ECS / AWS Amplify).

---

## 🏗 System Architecture Overview

```
                               ┌──────────────────────────────────────────────┐
                               │               GitHub Repository              │
                               │              (imtej/Nexus-AI)                │
                               └──────┬───────────────────────────────┬───────┘
                                      │ Push to main                  │ Push to main
                                      ▼                               ▼
                      ┌───────────────────────────────┐   ┌───────────────────────────────┐
                      │   Frontend (Next.js 16)       │   │     Backend (FastAPI Engine)    │
                      │   Hosted on Vercel / Amplify  │   │     Render / AWS App Runner     │
                      └───────────────┬───────────────┘   └───────────────┬───────────────┘
                                      │                                   │
                                      └─────────────────┬─────────────────┘
                                                        │
                                                        ▼
                                       ┌──────────────────────────────────┐
                                       │  Supabase PostgreSQL + pgvector  │
                                       │   (Collective Knowledge DB)      │
                                       └──────────────────────────────────┘
```

---

## 📁 Deployment Directory Structure

```
deployment/
├── README.md                     # Master Deployment & Architecture Documentation
├── aws/
│   ├── backend/
│   │   ├── Dockerfile            # Multi-stage Python 3.12 Docker container (FastAPI + uv)
│   │   ├── .dockerignore
│   │   └── apprunner.yaml        # AWS App Runner service specification (Strategy B)
│   ├── frontend/
│   │   ├── Dockerfile            # Multi-stage Next.js standalone container
│   │   ├── .dockerignore
│   │   └── amplify.yml           # AWS Amplify hosting build specification
│   └── scripts/
│       ├── health_check.sh       # Automated API endpoint health check
│       └── run_migrations.sh     # Supabase database migration runner
├── render/
│   └── render.yaml               # Render Cloud Blueprint for FastAPI backend
└── vercel/
    └── vercel.json               # Vercel project configuration for Next.js frontend
```

---

## ⚡ 1. Primary Auto-Deployment Setup (Render + Vercel)

### Backend (Render)
* **Configuration File**: `deployment/render/render.yaml` (and `backend/render.yaml`)
* **Environment Variables Required**:
  * `SUPABASE_URL`
  * `SUPABASE_SERVICE_ROLE_KEY`
  * `JWT_SECRET`
  * `OPENAI_API_KEY` or `GEMINI_API_KEY`
* **Trigger**: Automatic deployment on push to `main` branch.

### Frontend (Vercel)
* **Configuration File**: `deployment/vercel/vercel.json`
* **Environment Variables Required**:
  * `NEXT_PUBLIC_API_URL`: Backend URL (e.g., `https://nexus-backend.onrender.com`)
  * `NEXT_PUBLIC_SUPABASE_URL`
  * `NEXT_PUBLIC_SUPABASE_ANON_KEY`
* **Trigger**: Automatic deployment on push to `main` branch.

---

## ☁️ 2. AWS Cloud Blueprint (Strategy B: AWS App Runner + Amplify)

For deploying to AWS with minimal operational overhead and auto-scaling support:

### Backend (AWS App Runner)
AWS App Runner provides fully managed container deployments directly from AWS ECR or GitHub.

1. **Build Container**:
   ```bash
   docker build -t nexus-backend -f deployment/aws/backend/Dockerfile ./backend
   ```
2. **Deploy via App Runner**:
   Use `deployment/aws/backend/apprunner.yaml` to specify service parameters, CPU/RAM scaling rules, and health checks.

### Frontend (AWS Amplify)
AWS Amplify Hosting natively supports Next.js Server-Side Rendering (SSR).

1. Connect repository `imtej/Nexus-AI` in the AWS Amplify Console.
2. Point the build specification to `deployment/aws/frontend/amplify.yml`.

---

## 🛠 3. Local Docker Testing

You can run the entire production-grade stack locally using Docker:

```bash
# Build backend container
docker build -t nexus-backend -f deployment/aws/backend/Dockerfile ./backend

# Run backend container
docker run -d -p 8000:8000 --env-file ./backend/.env nexus-backend
```

Check backend health:
```bash
bash deployment/aws/scripts/health_check.sh http://localhost:8000
```
