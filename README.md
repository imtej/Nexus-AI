# Nexus AI: The Collective Knowledge Protocol ⚡ 

> **Nexus AI**: A cohesive network of specialized agentic nodes driving a singular evolving intelligence. 

> {Nexus refers to a connection or series of connections linking two or more things — a metaphor for multiple specialized nodes driving one unified system.} 

A production-grade evolving AI system (AI companion), designed as a dynamic and empathetic companion. Nexus AI learns, remembers, and grows wiser with every conversation (with personal memory and *Collective Knowledge* evolution).

---

## 1. The Core Idea: How an Evolving AI Actually Works

Before any code, here's the **big idea** — how does Nexus AI actually *evolve* when more users chat with it?

### The Collective Knowledge Evolution Model

```
┌────────────────────────────────────────────────────────-──────────┐
│                     NEXUS AI'S CONSCIOUSNESS                      │
│                                                                   │
│  ┌─────────-────┐  ┌─────────-────┐  ┌─────────-────┐             │
│  │  User A's    │  │  User B's    │  │  User C's    │             │
│  │  Personal    │  │  Personal    │  │  Personal    │  ...        │
│  │  Memory      │  │  Memory      │  │  Memory      │             │
│  │  (Private)   │  │  (Private)   │  │  (Private)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                 │                     │
│         ▼                 ▼                 ▼                     │
│  ┌─────────────────────────────────────────────────-─────┐        │
│  │           COLLECTIVE KNOWLEDGE LAYER (Shared)         │        │
│  │                                                       │        │
│  │  • Distilled Insights (anonymized wisdom)             │        │
│  │  • Pattern Recognition (what many users discuss)      │        │
│  │  • Emotional Intelligence (learned empathy patterns)  │        │
│  │  • World Knowledge (curated facts from all users)     │        │
│  │  • Behavioral Patterns (what approaches work)         │        │
│  └───────────────────────────────────────────────────────┘        │
│                          │                                        │
│                          ▼                                        │
│  ┌─────────────────────────────────────────────────────-──┐       │
│  │           NEXUS AI'S EVOLVING PERSONALITY              │       │
│  │                                                        │       │
│  │  personality_version: 1.0 → 1.1 → 1.2 → ...            │       │
│  │  wisdom_score: grows with more interactions            │       │
│  │  empathy_depth: deepens with emotional conversations   │       │
│  │  knowledge_breadth: expands with diverse topics        │       │
│  └────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────-─────────┘
```

### How Evolution Happens — The 3 Loops

**Loop 1: Personal Memory Loop (Per-User)**
- Every conversation extracts `MemoryNodes` (facts, preferences, emotions, identity)
- Stored privately per user in Supabase + pgvector
- Nexus AI remembers *you* specifically — adapting to your unique conversational style and history.

**Loop 2: Collective Knowledge Distillation Loop (Cross-User)**
- When a pattern or insight appears across multiple users, it gets **promoted** to the Collective Knowledge
- Example: If 50 users discuss anxiety management, Nexus AI distills the best patterns into a shared insight
- This is NOT copying private data — it's *distilling wisdom* (e.g., "Many people find morning journaling helpful for anxiety")
- A **curation pipeline** scores, deduplicates, and validates before promotion

**Loop 3: Personality Evolution Loop (Nexus AI's Growth)**
- Periodically (or at threshold moments), Nexus AI's core personality traits get updated
- Tracked numerically: `empathy_depth`, `knowledge_breadth`, `wisdom_score`, `interaction_count`
- The system prompt evolves: early Nexus AI is curious and learning → mature Nexus AI is wise and insightful
- Users can see "Nexus AI has evolved" moments in the UI — creating a living, growing companion

Evolution stages: `🌱 Nascent → 🌿 Growing → 🌳 Mature → ✨ Transcendent`

### Privacy-First Collective Knowledge Rules
1. **Never share raw user messages** — only distilled, anonymized insights
2. **Opt-in only** — users must consent to contribute to the Collective Knowledge
3. **One-way promotion** — insights go UP to Collective Knowledge, never DOWN to identify users
4. **Minimum threshold** — an insight needs N+ user occurrences before promotion
5. **Moderation layer** — LLM-based review before any Collective Knowledge promotion

---

## ✨ What Makes Nexus AI Special

- **Personal Memory** — Nexus AI remembers *you*: your preferences, stories, emotions, and personality
- **Collective Knowledge Evolution** — Nexus AI distills anonymized wisdom from all conversations, growing collectively wiser
- **Provider Agnostic** — Works with Gemini, OpenAI, or Anthropic (bring your own key)
- **7 AI Agents** — Structured as a network of specialized agentic nodes, each handling a dedicated task
- **Privacy First** — Personal data is never shared; only anonymized insights enter the Collective Knowledge

---

## 🏗️ Architecture — The Seven Nodes

| Node | Agent | Role | Runs |
|-------|-------|------|------|
| ⚡ 1 | **QueryAnalyzer** | Intent detection, Emotions, & HyDE query expansion | Sync, critical path |
| ⚡ 2 | **ContextRetriever** | Vector retrieval (Personal + Collective Knowledge) via pgvector | Sync, critical path |
| ⚡ 3 | **PromptBuilder** | Constructs the dynamic system prompt | Sync, critical path |
| ⚡ 4 | **ResponseGenerator** | Streams LLM responses to the user | Sync, critical path |
| ⚡ 5 | **MemoryExtractor** | Memory extracted & stored (Traits, Preferences, Emotions) | Async, post-response |
| ⚡ 6(A) | **UserProfiler** | Forges and evolves the UserIdentity profile | Periodic/cron background |
| ⚡ 6(B) | **InsightDistiller** | Distills shared wisdom into Collective Knowledge insights | Periodic/cron background |
| ⚡ 7 | **EvolutionEngine** | Calculates & updates Nexus AI's psychological growth | Periodic/cron background |

### System Flow

```
User Message → QueryAnalyzer → ContextRetriever → PromptBuilder → ResponseGenerator → Response
                                                            ↓
                                                        Chronicler (async)
                                                            ↓
                                                        Identity Builder & Curator
                                                         + 
                                                        EvolutionEngine (periodic/cron)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.12) + UV |
| AI Orchestration | LangGraph |
| LLM Gateway | LiteLLM (Gemini/OpenAI/Claude) |
| Database | Supabase PostgreSQL + pgvector |
| Auth | Supabase Auth (Email + Google OAuth) |
| Frontend | Next.js 16 (App Router) |
| Primary Hosting | Render (backend) + Vercel (frontend) |
| Cloud Blueprint | AWS App Runner (backend) + AWS Amplify (frontend) |
| Containerization | Multi-stage Docker (Python 3.12 + Node 20) |
| CI/CD Pipeline | GitHub Actions (Linting, Type-Check, Build validation) |
| Package Manager | UV (backend) + npm (frontend) |

---

## 🔐 API Key Model

- **n (n=1000) free trial chats** with the developer's default API key
- After trial, users provide their own key (Gemini, OpenAI, or Claude)
- Keys are encrypted at rest using Fernet

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+, UV, Node.js 20+
- [Supabase](https://supabase.com) account (free tier)
- API key for at least one LLM provider

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/nexus-ai.git
cd nexus-ai
```

### 2. Backend

```bash
cd backend
cp .env.example .env  # Fill in your values
uv sync
uv run uvicorn app.main:app --reload
```

### 3. Frontend

```bash
cd frontend
cp .env.example .env.local  # Fill in your values
npm install
npm run dev
```

### 4. Database

Run the SQL migration in your Supabase SQL Editor:
```
supabase/migrations/001_initial_schema.sql
```

### 5. Access
 For local development:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## ☁️ Deployment & Infrastructure

Nexus AI supports both **instant auto-deployments** and **production cloud blueprints**:

- **Auto-Deployment Setup (Active)**:
  - **Backend**: Hosted on [Render](https://render.com) (`backend/render.yaml` & `deployment/render/render.yaml`).
  - **Frontend**: Hosted on [Vercel](https://vercel.com) (`deployment/vercel/vercel.json`).
- **AWS Cloud Blueprint (Strategy B)**:
  - **Backend**: Containerized via multi-stage Dockerfile (`deployment/aws/backend/Dockerfile`) and deployed to **AWS App Runner** (`deployment/aws/backend/apprunner.yaml`).
  - **Frontend**: Deployed to **AWS Amplify Hosting** (`deployment/aws/frontend/amplify.yml`) or containerized standalone SSR.
- **CI/CD Automation**: `.github/workflows/ci.yml` validates backend Python linting/type-checking and Next.js frontend builds on every commit.

For detailed instructions, see [`deployment/README.md`](file:///Users/ravitej/From%20Windows%20D/AI%20ML%20&%20DL%20Projects/Nexus%20AI/deployment/README.md).

---

## 📊 Performance, Latency (TTFT) & Concurrency Benchmarks

### 1. User Concurrency & Throughput Capacity

| Metric | Single Instance Baseline | Auto-Scaled AWS App Runner (5 Nodes) | Bottleneck / Constraint |
| :--- | :--- | :--- | :--- |
| **Concurrent Active Chatters** | ~300 active SSE streams | ~3,000 active SSE streams | Supabase Postgres Pool (`pgBouncer`) |
| **Throughput (RPS)** | ~35 req/sec | ~350 req/sec | Async LLM Gateway Rate Limits (LiteLLM) |
| **Vector DB Search Throughput** | ~500 searches/sec | ~2,500 searches/sec | HNSW Index in `pgvector` (`m=16, ef=64`) |
| **Memory Extraction Throughput**| ~50 extractions/sec (Async) | ~350 extractions/sec (Async) | Non-blocking post-response background task |

### 2. Time To First Token (TTFT) Critical Path Budget

```
User Message Sent ──► [Node 1: QueryAnalyzer] ──► [Node 2: ContextRetriever] ──► [Node 3: PromptBuilder] ──► [Node 4: ResponseGenerator] ──► First Token Rendered
                            (~120ms)                    (~180ms)                     (~20ms)                     (~150ms TTFT)             Total TTFT: ~470ms
```

- **Target TTFT**: **< 600 ms** (End-to-End SSE token stream initialization)
- **Benchmarking Suite**: Run `python benchmarks/latency_benchmark.py` or execute stress load testing via `benchmarks/locustfile.py`.

---

## 🧪 Testing Suites & AI Evals Framework

Nexus AI incorporates automated quality assurance across system logic and non-deterministic LLM behavior:

- **Automated Test Suites (`tests/`)**:
  - **Unit Tests (`tests/unit/`)**: Crypto utilities (Fernet key encryption), Token Bucket rate limiter, system prompt generator, `QueryAnalyzer`, and `ContextRetriever`.
  - **Integration Tests (`tests/integration/`)**: LangGraph state machine execution, Supabase pgvector RPC payload validation, and MemoryService database models.
  - **E2E Tests (`tests/e2e/`)**: SSE streaming token response protocol and Supabase JWT authentication flow.
  - **Load Tests (`tests/load/`)**: Locust user concurrency simulation and k6 TTFT stress performance testing.


- **AI Evaluation Framework (`evals/`)**:
  - **RAG & Retrieval Precision (`evals/metrics/rag_precision.py`)**: Evaluates `ContextRetriever` & HyDE query precision against benchmark test sets (`evals/datasets/golden_conversations.json`).
  - **Persona & Empathy Alignment (`evals/metrics/persona_eval.py`)**: LLM-as-a-Judge script scoring responses against core persona guidelines in `nexus_personality.yaml`.
  - **PII Anonymization (`evals/metrics/pii_sanitization_eval.py`)**: Validates zero PII enters the shared `collective_knowledge` table.
  - **Runner**: Execute full eval matrix via `python evals/run_evals.py`.

---

## 📁 Project Structure

```
nexus-ai/
├── .github/
│   └── workflows/
│       └── ci.yml                        # Automated CI (Python + Next.js checks)
│
├── backend/                              # FastAPI + LangGraph (UV)
│   ├── app/
│   │   ├── main.py                       # FastAPI entry point, lifecycle & CORS
│   │   ├── agents/                       # The 7 Orchestration Agents (8 units)
│   │   │   ├── memory_extractor.py       # ⚡ 5: Post-response memory extraction
│   │   │   ├── insight_distiller.py      # ⚡ 6(B): Collective Knowledge distillation
│   │   │   ├── evolution_engine.py       # ⚡ 7: Personality growth tracking
│   │   │   ├── response_generator.py     # ⚡ 4: LLM response generation
│   │   │   ├── graph.py                  # LangGraph workflow orchestration
│   │   │   ├── user_profiler.py          # ⚡ 6(A): User identity profiling
│   │   │   ├── query_analyzer.py         # ⚡ 1: Intent, emotion & HyDE expansion
│   │   │   ├── context_retriever.py      # ⚡ 2: Vector & relational memory retrieval
│   │   │   ├── state.py                  # TypedDict shared state schema
│   │   │   ├── prompt_builder.py         # ⚡ 3: Dynamic prompt construction
│   │   │   └── __init__.py               # Agent package initialization
│   │   ├── api/
│   │   │   ├── deps.py                   # Dependency injection (Supabase, Auth)
│   │   │   ├── middleware/
│   │   │   │   ├── auth.py               # Supabase JWT token verification
│   │   │   │   ├── rate_limit.py         # In-memory token-bucket rate limiting
│   │   │   │   └── __init__.py           # Middleware package initialization
│   │   │   ├── routes/
│   │   │   │   ├── auth.py               # Auth verification & user info
│   │   │   │   ├── chat.py               # SSE streaming chat endpoint
│   │   │   │   ├── conversations.py      # Conversation CRUD & management
│   │   │   │   ├── evolution.py          # Public evolution statistics
│   │   │   │   ├── profile.py            # Profile & custom API key management
│   │   │   │   └── __init__.py           # Routes package initialization
│   │   │   └── __init__.py               # API package initialization
│   │   ├── config/
│   │   │   ├── settings.py               # Pydantic-based env configuration
│   │   │   ├── nexus_personality.yaml    # Core personality & evolution settings
│   │   │   └── __init__.py               # Config package initialization
│   │   ├── models/
│   │   │   ├── conversation.py           # Schemas for chat messages & sessions
│   │   │   ├── evolution.py              # Nexus AI's trait-based growth models
│   │   │   ├── memory.py                 # MemoryNode & HiveMindInsight schemas
│   │   │   ├── user.py                   # Profile & UserIdentity models
│   │   │   └── __init__.py               # Models package initialization
│   │   ├── services/
│   │   │   ├── embedding_service.py      # Gemini text-embedding generation
│   │   │   ├── llm_service.py            # LiteLLM provider-agnostic gateway
│   │   │   ├── memory_service.py         # pgvector & relational database logic
│   │   │   ├── supabase_client.py        # Supabase client instantiation
│   │   │   └── __init__.py               # Services package initialization
│   │   ├── utils/
│   │   │   ├── crypto.py                 # Fernet encryption for API keys
│   │   │   ├── logging.py                # Structured logging implementation
│   │   │   └── __init__.py               # Utils package initialization
│   │   └── __init__.py                   # App package initialization
│   ├── .env.example                      # Template for environment variables
│   ├── Dockerfile                        # Multi-stage container production config
│   ├── pyproject.toml                    # UV project & dependency specifications
│   ├── render.yaml                       # Render deployment configuration
│   ├── uv.lock                           # Python dependency lock file
│   └── README.md                         # Backend-specific documentation
│
├── benchmarks/                           # Latency & Concurrency Stress Suite
│   ├── README.md                         # Benchmarking specifications & guide
│   ├── latency_benchmark.py              # TTFT & agent latency measurement CLI
│   └── locustfile.py                     # Locust stress load-testing script
│
├── deployment/                           # Multi-cloud deployment blueprints
│   ├── README.md                         # Architecture & deployment master guide
│   ├── aws/                              # AWS App Runner / Amplify blueprint
│   │   ├── backend/                      # Dockerfile & apprunner.yaml
│   │   ├── frontend/                     # Dockerfile & amplify.yml
│   │   └── scripts/                      # Health checks & migration scripts
│   ├── render/                           # Render cloud configuration
│   └── vercel/                           # Vercel deployment configuration
│
├── evals/                                # AI Evaluation Framework
│   ├── README.md                         # Evals architecture documentation
│   ├── datasets/                         # Golden benchmark test datasets
│   │   ├── golden_conversations.json     # Multi-turn dialogue test set
│   │   └── memory_test_cases.json        # Memory extraction & PII test cases
│   ├── metrics/                          # Evaluation evaluators
│   │   ├── persona_eval.py               # Persona & empathy alignment evaluator
│   │   ├── rag_precision.py              # Retrieval precision & recall evaluator
│   │   └── pii_sanitization_eval.py       # PII regex sanitization evaluator
│   └── run_evals.py                      # CLI runner for evaluation suite
│
├── frontend/                             # Next.js 16 (App Router)
│   ├── src/
│   │   ├── app/                          # Next.js App Router (Pages & Layouts)
│   │   │   ├── (auth)/                   # Authentication Group
│   │   │   │   ├── login/page.tsx        # Google OAuth & Email login
│   │   │   │   └── signup/page.tsx       # Registration & Confirmation
│   │   │   ├── (dashboard)/              # Auth-protected Dashboard Group
│   │   │   │   ├── chat/page.tsx         # SSE-based token-streaming interface
│   │   │   │   ├── evolution/page.tsx    # Nexus AI's lifecycle & trait metrics
│   │   │   │   ├── settings/page.tsx     # Profile & BYOK (Bring Your Own Key)
│   │   │   │   └── layout.tsx            # Persistent sidebar & state wrapper
│   │   │   ├── (policies)/               # Static Legal & Info Pages
│   │   │   │   ├── about/page.tsx        # Project philosophy & lore
│   │   │   │   ├── privacy/page.tsx      # Target data usage and Collective Knowledge policy
│   │   │   │   └── terms/page.tsx        # Hobby project AS-IS disclaimers
│   │   │   ├── globals.css               # Design system tokens & CSS variables
│   │   │   ├── layout.tsx                # Root provider & font configuration
│   │   │   └── page.tsx                  # Premium landing page
│   │   ├── components/                   # Modular UI Components
│   │   │   ├── chat/                     # Chat ecosystem (Bubbles, Indicators)
│   │   │   │   ├── ChatWindow.tsx        # Scroll-optimized message container
│   │   │   │   ├── MessageBubble.tsx     # Markdown-aware message bubble
│   │   │   │   ├── StreamingText.tsx     # Typewriter token animation
│   │   │   │   ├── TypingIndicator.tsx   # Thinking dots & brain-orb
│   │   │   │   └── ConversationList.tsx  # Sidebar history management
│   │   │   ├── evolution/                # Nexus AI's Growth Visuals
│   │   │   │   ├── EvolutionOrb.tsx      # Multi-stage stage-colored orb
│   │   │   │   └── GrowthChart.tsx       # Trait progression grid
│   │   │   └── layout/                   # Layout Foundations
│   │   │       ├── Sidebar.tsx           # Collapsible primary navigation
│   │   │       ├── Header.tsx            # Mobile-optimized top bar
│   │   │       └── MobileNav.tsx         # Hand-friendly bottom tab bar
│   │   └── lib/                          # Core Utilities & SDKs
│   │       ├── api.ts                    # Centralized axios-like fetch wrapper
│   │       ├── utils.ts                  # Layout & animation helper functions
│   │       └── supabase/                 # Client/Server-side Auth SDKs
│   ├── .env.example                      # Template for environment variables
│   ├── next.config.ts                    # Next.js configuration settings
│   ├── package.json                      # Dependencies & NPM scripts
│   ├── tsconfig.json                     # TypeScript compiler configuration
│   └── README.md                         # Frontend documentation
│
├── tests/                                # Automated Test Suites
│   ├── README.md                         # Test suite architecture documentation
│   ├── unit/                             # Unit Tests
│   │   ├── test_query_analyzer.py        # Intent & HyDE query expansion test
│   │   ├── test_context_retriever.py     # Memory deduplication & threshold filter test
│   │   ├── test_prompt_builder.py        # System prompt dynamic compilation test
│   │   ├── test_crypto.py                # Fernet API key encryption/decryption test
│   │   └── test_rate_limiter.py          # Token bucket rate limiting test
│   ├── integration/                      # Integration Tests
│   │   ├── test_langgraph_workflow.py    # LangGraph state machine execution
│   │   ├── test_supabase_pgvector.py     # Supabase pgvector RPC payload format test
│   │   └── test_memory_service.py        # MemoryNode database CRUD model test
│   ├── e2e/                              # End-to-End Tests
│   │   ├── test_sse_streaming.py         # SSE streaming token protocol test
│   │   └── test_auth_flow.py             # Supabase JWT authentication flow test
│   └── load/                             # Concurrency Stress Tests
│       ├── locustfile.py                 # Locust load-testing script
│       └── k6_chat_stress.js             # k6 TTFT stress testing script
│
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql       # Full schema + pgvector + RLS
│
├── ARCHITECTURE.md                       # Detailed technical architecture
├── README.md
└── .gitignore
```

---

## 📄 License

This project is for Nexus AI.

## 👤 Contributors

- Ravi Tej (Data Scientist & Applied AI Researcher)

---

**Nexus AI** — Building Evolving Intelligence ⚡
