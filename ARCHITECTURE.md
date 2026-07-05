# Nexus AI Architecture

## System Overview

Nexus AI implements the **Collective Knowledge Protocol** — a seven-agent architecture using **LangGraph** for orchestration, **Supabase PostgreSQL + pgvector** for persistent memory and vector search, and **LiteLLM** for provider-agnostic LLM access (Gemini, OpenAI, Claude).

The system is designed as an evolving AI companion that remembers users personally, distills collective wisdom from all conversations (the Collective Knowledge), and measurably grows its personality over time.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface                              │
│            Next.js 16 (App Router) → Vercel                         │
│   Landing Page | Auth | Chat (SSE) | Evolution Dashboard | Settings │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS / SSE
                               ▼
┌───────────────────────────────────────────────────────────────────-──┐
│                     FastAPI Backend → Render                         │
│                                                                      │
│  ┌──────────────────── LangGraph Workflow ──────────────────────┐    │
│  │                                                              │    │
│  │  ⚡ QueryAnalyzer → ⚡ ContextRetriever → ⚡ PromptBuilder      │    │
│  │                                        ↓                     │    │
│  │                           ⚡ ResponseGenerator → Response     |    │
│  │                                        ↓                     |    │
│  │                                   ⚡ Chronicler (async)       |    │
│  │                                                              │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─── Background Agents (Periodic) ──------------------─┐            │
│  │  ⚡ Identity Builder → User identity                  │            │
│  │  ⚡ Curator          → Collective Knowledge distill   │            │
│  │  ⚡ EvolutionEngine          → Personality growth.    │            │
│  └───────────────────────────────────----------------─-─┘            │
│                                                                      │
│  ┌─── Services ───────────────────────┐                              │
│  │  LLMService    (LiteLLM)           │                              │
│  │  EmbeddingService (Gemini 768d)    │                              │
│  │  MemoryService (pgvector CRUD)     │                              │
│  │  SupabaseClient                    │                              │
│  └────────────────────────────────────┘                              │
└──────────────────────────────┬───────────────────────────────────-───┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────=──┐
│                   Supabase (Free Tier)                               │
│                                                                      │
│  ┌────────────────────-──┐    ┌──────────────────────┐               │
│  │  PostgreSQL + pgvector│    │  Supabase Auth       │               │
│  │                       │    │  - Email / Password  │               │
│  │  • profiles           │    │  - Google OAuth      │               │
│  │  • user_identities    │    │  - JWT tokens        │               │
│  │  • memory_nodes (vec) │    └──────────────────────┘               │
│  │  • collective_knowledge (vec)│                                    │
│  │  • conversations      │    ┌──────────────────────┐               │
│  │  • messages           │    │  Row Level Security  │               │
│  │  • nexus_evolution    │    │  (data isolation)    │               │
│  └─────────────────────-─┘    └──────────────────────┘               │
└────────────────────────────────────────────────────────────────────-─┘
```

## The Seven Nodes — Agent Architecture

Designed as a unified intelligence powered by a network of specialized agentic nodes.

| Node | Agent | Role | Execution |
|-------|-------|------|-----------|
| ⚡ 1 | **QueryAnalyzer** | Intent detection, Emotional signals, & HyDE query expansion | Sync, per-request |
| ⚡ 2 | **ContextRetriever** | Memory retrieval (personal + hive) via pgvector | Sync, per-request |
| ⚡ 3 | **PromptBuilder** | Dynamic system prompt construction | Sync, per-request |
| ⚡ 4 | **ResponseGenerator** | LLM response generation (provider-agnostic) | Sync, per-request |
| ⚡ 5 | **MemoryExtractor** | Memory extracted & stored (Traits, Preferences, Emotions) | Async, post-response |
| ⚡ 6(A) | **UserProfiler** | Forges and evolves the UserIdentity profile | Async, periodic/cron |
| ⚡ 6(B) | **InsightDistiller** | Collective Knowledge distillation + quality control | Async, periodic/cron |
| ⚡ 7 | **EvolutionEngine** | Personality trait evolution + growth tracking | Async, periodic/cron |

> Nodes 1–4 are in the **critical path** (target TTFT < 600ms).
> Nodes 5–7 run **asynchronously after** the response is sent (zero user-facing latency).

### Latency Budget & Time To First Token (TTFT) Breakdown

```
User Message Sent ──► [Node 1: QueryAnalyzer] ──► [Node 2: ContextRetriever] ──► [Node 3: PromptBuilder] ──► [Node 4: ResponseGenerator] ──► First Token Rendered
                            (~120ms)                    (~180ms)                     (~20ms)                     (~150ms TTFT)             Total TTFT: ~470ms
```

| Pipeline Node | Target Latency | Tech & Optimization Strategy |
| :--- | :--- | :--- |
| **Node 1: QueryAnalyzer** | **100 – 150 ms** | Fast speculative LLM (`gemini-2.0-flash` / `gpt-4o-mini`) for intent & HyDE query |
| **Node 2: ContextRetriever** | **150 – 220 ms** | Parallel execution of pgvector cosine similarity search + identity lookup |
| **Node 3: PromptBuilder** | **15 – 30 ms** | In-memory dynamic system prompt assembly & template compilation |
| **Node 4: ResponseGenerator** | **150 – 300 ms** | Streamed SSE tokens (`http.streamingResponse`) via LiteLLM |
| **Total Pipeline TTFT** | **< 600 ms** | **End-to-End target response stream initialization benchmark** |

### User Concurrency & Throughput Capacity

| Metric | Single Instance Baseline | Auto-Scaled AWS App Runner (5 Nodes) | Bottleneck / Constraint |
| :--- | :--- | :--- | :--- |
| **Concurrent Active Chatters** | ~300 active SSE streams | ~3,000 active SSE streams | Supabase Postgres Pool (`pgBouncer`) |
| **Throughput (RPS)** | ~35 req/sec | ~350 req/sec | Async LLM Gateway Rate Limits (LiteLLM) |
| **Vector DB Search Throughput** | ~500 searches/sec | ~2,500 searches/sec | HNSW Index in `pgvector` (`m=16, ef=64`) |
| **Memory Extraction Throughput**| ~50 extractions/sec (Async) | ~350 extractions/sec (Async) | Non-blocking post-response background worker |

## Data Flow

### 1. User Message → QueryAnalyzer (Node 1)

**Input:**
- `user_id`: UUID from Supabase Auth JWT
- `user_message`: Raw user text

**Processing:**
- Uses a fast/reliable LLM model (e.g., Gemini 2.0 Flash / 2.5 Flash)
- Extracts: `intent` (greeting, question, venting, etc.) and `emotion_signal` (happy, anxious, curious, etc.)
- Generates: `expanded_query` (HyDE - Hypothetical Document Embedding) to improve vector search accuracy.
- Graceful fallback to "other" / "neutral" if extraction fails

**Output:**
- `intent`: string
- `emotion_signal`: string
- `expanded_query`: string

### 2. QueryAnalyzer → ContextRetriever (Node 2)

**Input:**
- `user_id`, `user_message`, `intent`, `emotion_signal`, `expanded_query`

**Processing:**
1. **User Identity Retrieval** — Fetches `user_identities` record from Supabase
2. **Personal Memory Search** — pgvector cosine similarity search on `memory_nodes` filtered by `user_id`
3. **Recency Fallback** — If vector search returns < 2 results, supplements with recent memories sorted by timestamp
4. **Collective Knowledge Search** — pgvector cosine similarity search on `collective_knowledge` table (quality_score >= 0.5)

**RPC Functions Used:**
```sql
search_personal_memories(query_embedding, target_user_id, match_count)
search_collective_knowledge(query_embedding, match_count)
```

**Output:**
- `user_identity`: UserIdentity object (or None for new users)
- `personal_memories`: list of MemorySearchResult (max 5)
- `collective_knowledge_memories`: list of HiveMindInsight (max 3)

### 3. ContextRetriever → PromptBuilder (Node 3)

**Input:**
- All state from QueryAnalyzer + ContextRetriever

**Processing:**
Constructs a dynamic system prompt by assembling:

1. **Core Personality** — From `config/nexus_personality.yaml`
2. **Evolution Modifier** — Based on `nexus_evolution.total_interactions`:
   - Nascent (0-100): Curious, eager
   - Growing (100-1000): Forming insights
   - Mature (1000-10000): Deeply understanding
   - Transcendent (10000+): Profound wisdom
3. **User Identity Section** — Summary, communication style, traits, emotional baseline
4. **Personal Memories** — Top 5 relevant memories, labeled by type
5. **Collective Knowledge Insights** — Top 3 collective wisdom entries
6. **Emotional Context** — If emotion signal is non-neutral, adds empathy guidance

**Output:**
- `system_prompt`: Complete dynamic prompt string

### 4. PromptBuilder → ResponseGenerator (Node 4)

**Input:**
- `system_prompt`, `user_message`, `conversation_history` (last 10 messages)

**Processing:**
- Calls LLM via **LiteLLM** (provider-agnostic)
- Provider is determined by user's profile:
  - If user has their own API key → uses their key + provider
  - If user has free chats remaining → uses developer's default key
  - If neither → returns 402 error ("add your API key")
- Temperature: 0.7, Max tokens: 4096

**Provider Model Mapping:**

| Provider | Main Model | Fast Model |
|----------|-----------|------------|
| Gemini | gemini/gemini-2.5-flash | gemini/gemini-2.0-flash |
| OpenAI | openai/gpt-4o | openai/gpt-4o-mini |
| Anthropic | anthropic/claude-sonnet-4 | anthropic/claude-3.5-haiku |

**Output:**
- `response`: Generated text

### 5. ResponseGenerator → Chronicler (Node 5) — Async

**Input:**
- `user_id`, `user_message`, `response`

**Processing:**
1. Uses fast LLM to extract 0-3 memories from the conversation turn
2. Each memory is classified: `personal_identity`, `preference`, `factual`, `emotional_state`
3. Each memory gets a 768-dim Gemini embedding
4. Stored in `memory_nodes` table with embedding

**Output:**
- `new_memory_ids`: list of stored memory UUIDs

### 6(A). Identity Builder (Node 6A) — Periodic

**Trigger:** Called periodically every t = 30 minutes (cron / manual endpoint)

**Processing:**
1. Fetches recent `memory_nodes` from last userIdentity update and `current_identity` for (n = 50) users.
2. For every user, if at least (k = 5) new memories are found, uses LLM to forge or incrementally update the `UserIdentity` profile (traits, style, baseline).
3. Ensures personality depth grows as the user interacts more.

### 6(B). Curator (Node 6B) — Periodic

**Trigger:** Called periodically every t = 10 minutes (cron / manual endpoint)

**Processing:**
1. Fetches last (m = 100) new recent anonymized memories across all users which have not been used in previous collective knowledge memory generations (content + type only, no user_id)
2. If at least (k = 15) new memories are found, uses LLM to identify universal patterns/wisdom 
3. Validates against minimum contributor threshold
4. Generates embeddings for each insight
5. Stores in `collective_knowledge` table

### 7. EvolutionEngine (Node 7) — Periodic

**Trigger:** Called periodically every t = 25 minutes (cron / manual endpoint)

**Processing:**
1. Counts total interactions (`messages` where role='user')
2. Counts total users (`profiles`)
3. Counts memory types for trait calculation
4. Calculates evolution traits using **logarithmic growth**:
   - `empathy_depth` ← based on emotional_state memory count
   - `knowledge_breadth` ← based on factual memory count
   - `wisdom_score` ← based on collective_knowledge insight count
   - `curiosity_level` ← decreases as interactions grow
5. Bumps `personality_version` (major bump on stage transition)
6. Updates `nexus_evolution` singleton

## Deployment Architecture & CI/CD Pipeline

```
                               ┌──────────────────────────────────────────────┐
                               │               GitHub Repository              │
                               │              (imtej/Nexus-AI)                │
                               └──────┬───────────────────────────────┬───────┘
                                      │ Push to main                  │ Push to main
                                      ▼                               ▼
                      ┌───────────────────────────────┐   ┌───────────────────────────────┐
                      │   Frontend (Next.js 16)       │   │     Backend (FastAPI Engine)  │
                      │   Hosted on Vercel / Amplify  │   │     Render / AWS App Runner   │
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

### 1. Active Auto-Deployment Topology
- **Backend**: Hosted on Render web service (`deployment/render/render.yaml`).
- **Frontend**: Hosted on Vercel (`deployment/vercel/vercel.json`).
- **Database**: Managed Supabase PostgreSQL with `pgvector` (`supabase/migrations/001_initial_schema.sql`).

### 2. AWS Production Blueprint (Strategy B)
- **Backend**: AWS App Runner serverless container deployment using multi-stage Dockerfile (`deployment/aws/backend/Dockerfile` & `deployment/aws/backend/apprunner.yaml`).
- **Frontend**: AWS Amplify hosting (`deployment/aws/frontend/amplify.yml`) or containerized standalone SSR.

### 3. Continuous Integration Automation
- Automated CI pipeline configured in `.github/workflows/ci.yml`.
- Validates backend Python dependencies via `uv`, executes `ruff` linting and `mypy` type checking.
- Validates frontend Next.js compilation (`tsc --noEmit`) and SSR build (`next build`).

## Memory System

### Memory Types

| Type | Description | Example |
|------|-------------|---------|
| `personal_identity` | Core traits and self-concept | "User identifies as a data scientist" |
| `preference` | Likes, dislikes, tastes | "User prefers dark mode and minimalist design" |
| `factual` | Objective facts and events | "User is CEO of Nexus AI, founded in 2026" |
| `emotional_state` | Feelings, moods, patterns | "User experiences morning anxiety" |
| `collective_knowledge` | Shared insights from the collective consciousness | "User is part of a community of learners" |

### Storage Architecture

**Single database (Supabase PostgreSQL + pgvector):**
- `memory_nodes` — Personal memories with `VECTOR(768)` column + HNSW index
- `collective_knowledge` — Shared insights with `VECTOR(768)` column + HNSW index
- `user_identities` — Nexus AI's evolving understanding of each user

### Retrieval Strategy

1. **Vector Similarity Search** — Query embedding vs stored embeddings via pgvector cosine distance
2. **Recency Fallback** — If vector search returns < 2 results, fetch latest by timestamp
3. **Hybrid Merge** — Combine and deduplicate results
4. **Embedding Model** — Gemini `text-embedding-004` (768 dimensions), standardized for all users regardless of chat LLM provider

## API Key Model

### Hybrid Approach

```
New User Signs Up
    ↓
  Gets (n=4) free trial chats (using developer's Gemini key)
    ↓
  free_chats_remaining decremented with each chat
    ↓
  When 0 → HTTP 402 "Add your API key in Settings"
    ↓
  User adds their own key (Gemini / OpenAI / Claude)
    ↓
  Key encrypted with Fernet → stored in profiles.encrypted_api_key
    ↓
  Unlimited chats using their own key
```

## Deployment Architecture

```
┌────────────-───┐      ┌─────────────-─────┐      ┌───────────────┐
│   Vercel       │      │   Render          │      │  Supabase     │
│   (Free Tier)  │ ──── │   (Free 750hr)    │ ──── │  (Free Tier)  │
│                │      │                   │      │               │
│  Next.js 16    │      │  FastAPI          │      │  PostgreSQL   │
│  Frontend      │      │  + LangGraph      │      │  + pgvector   │
│  + SSR         │      │  + LiteLLM        │      │  + Auth       │
│  + SSE client  │      │  + 7 Agents       │      │  + RLS        │
└─────────────-──┘      └───────────────-───┘      └───────────────┘
                              ↑
                        UptimeRobot
                        (5-min pings)
```

### Cold Start Mitigation
- **UptimeRobot** pings `/health` every 5 minutes (keeps Render warm)
- **Frontend** shows "Nexus AI is waking up..." animation during cold start
- **`/warmup` endpoint** pre-loads LangGraph graph on first hit

## Configuration System

### Environment Variables (Backend `.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | ✅ | Supabase project URL |
| `SUPABASE_ANON_KEY` | ✅ | Supabase anon/public key |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ | Service role key (bypasses RLS) |
| `SUPABASE_JWT_SECRET` | ✅ | JWT secret for token verification |
| `DEFAULT_LLM_PROVIDER` | ✅ | Default provider for trial chats (e.g., "gemini") |
| `DEFAULT_LLM_API_KEY` | ✅ | Developer's API key for trial chats |
| `CUSTOM_API_BASE` | ✅ | Base URL if using other OpenAI-compatible endpoints |
| `CUSTOM_MODEL_NAME` | ✅ | Model name if using other OpenAI-compatible endpoints |
| `GEMINI_EMBEDDING_API_KEY` | ✅ | Gemini key for server-side embeddings |
| `ENCRYPTION_KEY` | ✅ | Fernet key for encrypting user API keys |
| `CORS_ORIGINS` | ❌ | Allowed origins (default: localhost + vercel) |
| `DEBUG` | ❌ | Debug mode (default: false) |
| `LOG_LEVEL` | ❌ | Logging level (default: INFO) |

### Environment Variables (Frontend `.env.local`)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | ✅ | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ | Supabase anon key |
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL |

### YAML Configuration (`config/nexus_personality.yaml`)

Contains:
- **Nexus AI personality** — Core traits, communication style, humor, warmth
- **Evolution stages** — Nascent, Growing, Mature, Transcendent (with personality modifiers)
- **Memory settings** — Retrieval limits, classification types, extraction prompts
- **Collective Knowledge settings** — Minimum contributors, quality threshold, distillation prompts

## Error Handling

### Graceful Degradation

| Failure | Behavior |
|---------|----------|
| Memory retrieval fails | Falls back to recent memories, continues with empty if needed |
| Intent detection fails | Defaults to `intent: "other"`, `emotion: "neutral"` |
| Memory storage fails (Chronicler) | Returns empty memory IDs, workflow continues |
| LLM call fails | Returns friendly error message to user |
| Supabase connection fails | Frontend shows "Nexus AI is waking up..." retry |
| Trial expired + no API key | Returns HTTP 402 with friendly message |

## Security Considerations

1. **API Keys** — Encrypted with Fernet before storage; never logged or exposed
7. **Collective Knowledge Privacy** — Only anonymized, distilled insights; raw messages never shared

## Scalability Considerations

### Current Design (Free Tier Optimized)
- Sequential agent execution in LangGraph
- Single Render instance
- pgvector HNSW indexes for sub-ms vector search
- Connection reuse via global Supabase client

### Future Enhancements
- **Async agents** — Run QueryAnalyzer + ContextRetriever in parallel
- **Redis caching** — Cache frequently accessed memories and user identities
- **Streaming from LangGraph** — Stream tokens as they're generated instead of buffering
- **WebSocket** — Replace SSE with WebSocket for bidirectional communication
- **Rate limiting** — Upgrade from in-memory to Redis-backed token bucket per user
- **Monitoring** — Structured logs → Datadog/Grafana

## Testing Strategy & AI Evaluation Framework (Evals)

```
                               ┌─────────────────────────────────────────┐
                               │       Nexus AI Evals Framework          │
                               └────────────────────┬────────────────────┘
                                                    │
         ┌───────────────────┬──────────────────────┼────────────────────┬───────────────────┐
         ▼                   ▼                      ▼                    ▼                   ▼
┌──────────────────┐ ┌───────────────┐   ┌────────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  Retrieval Evals │ │ Memory Evals  │   │ Personality Evals  │ │  Safety Evals   │ │ Latency Benchmark│
│ (RAG Precision)  │ │(Extraction)   │   │(Alignment Score)   │ │(Guardrail Check)│ │   (TTFT Tracking)│
└──────────────────┘ └───────────────┘   └────────────────────┘ └─────────────────┘ └──────────────────┘
```

### 1. Automated Test Suites (`tests/`)
- **Unit Tests (`tests/unit/`)**: Verify Fernet encryption for API keys, Token-bucket rate limiting middleware, and `PromptBuilder` state compilation.
- **Integration Tests (`tests/integration/`)**: Execute LangGraph workflow state machine transitions and Supabase pgvector RPC calls.
- **End-to-End Tests (`tests/e2e/`)**: Validate real-time Server-Sent Events (SSE) token streaming protocols.

### 2. Benchmarking & Stress Testing (`benchmarks/`)
- **Latency Measurement (`benchmarks/latency_benchmark.py`)**: CLI runner tracking TTFT and per-agent execution duration.
- **Concurrency Load Testing (`benchmarks/locustfile.py`)**: Locust load testing script evaluating RPS degradation under 300+ concurrent active chatters.

### 3. AI Evaluation Suite (`evals/`)
- **RAG & Retrieval Precision (`evals/metrics/rag_precision.py`)**: Measures memory node precision and recall across benchmark datasets (`evals/datasets/golden_conversations.json`).
- **Persona Alignment (`evals/metrics/persona_eval.py`)**: LLM-as-a-Judge evaluator scoring response empathy, warmth, and curiosity against core guidelines in `nexus_personality.yaml`.
- **Privacy Sanitization**: Verifies zero PII enters the shared `collective_knowledge` table during `InsightDistiller` runs.
- **Runner (`evals/run_evals.py`)**: Automated execution framework for continuous eval benchmarks.

## Project Structure

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
│   │   │   ├── StreamingText.tsx     # Typewriter token animation
│   │   │   ├── TypingIndicator.tsx   # Thinking dots & brain-orb
│   │   │   └── ConversationList.tsx  # Sidebar history management
│   │   ├── evolution/                # Nexus AI's Growth Visuals
│   │   │   ├── EvolutionOrb.tsx      # Multi-stage stage-colored orb
│   │   │   └── GrowthChart.tsx       # Trait progression grid
│   │   └── layout/                   # Layout Foundations
│   │       ├── Sidebar.tsx           # Collapsible primary navigation
│   │       ├── Header.tsx            # Mobile-optimized top bar
│   │       └── MobileNav.tsx         # Hand-friendly bottom tab bar
│   └── lib/                          # Core Utilities & SDKs
│       ├── api.ts                    # Centralized axios-like fetch wrapper
│       ├── utils.ts                  # Layout & animation helper functions
│       └── supabase/                 # Client/Server-side Auth SDKs
├── .env.example                      # Template for environment variables
├── next.config.ts                    # Next.js configuration settings
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
├── README.md
├── ARCHITECTURE.md
└── .gitignore
```
