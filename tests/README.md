# 🧪 Nexus AI — Automated Testing Suite

This directory contains the comprehensive automated testing suite for **Nexus AI**, covering unit, integration, end-to-end (E2E), and load testing.

---

## 📁 Test Architecture & Directory Structure

```
tests/
├── unit/                                 # Unit Tests (Fast & Isolated)
│   ├── test_query_analyzer.py            # Node 1: Intent & HyDE query expansion test
│   ├── test_context_retriever.py         # Node 2: Memory deduplication & threshold filter test
│   ├── test_prompt_builder.py            # Node 3: System prompt dynamic compilation test
│   ├── test_crypto.py                    # Utility: Fernet API key encryption/decryption test
│   └── test_rate_limiter.py              # Middleware: Token Bucket rate limiting test
│
├── integration/                          # Integration Tests (Components & State Machine)
│   ├── test_langgraph_workflow.py        # LangGraph orchestrator state graph execution
│   ├── test_supabase_pgvector.py         # Supabase pgvector RPC payload format validation
│   └── test_memory_service.py            # MemoryNode database CRUD model test
│
├── e2e/                                  # End-to-End Protocol & Auth Tests
│   ├── test_sse_streaming.py             # Server-Sent Events (SSE) streaming token protocol
│   └── test_auth_flow.py                 # Supabase JWT Bearer token authentication flow
│
└── load/                                 # Concurrency & Stress Testing
    ├── locustfile.py                     # Locust stress load-testing script (300+ users)
    └── k6_chat_stress.js                 # k6 TTFT stress testing script (Target < 1s p95)
```

---

## 🚀 Running the Tests

### 1. Run Unit & Integration Tests (pytest)
```bash
# Run all unit tests
pytest tests/unit

# Run all integration tests
pytest tests/integration

# Run full test suite with coverage
pytest tests/
```

### 2. Run Load & Stress Tests

#### Using Locust (Interactive Dashboard):
```bash
pip install locust
locust -f tests/load/locustfile.py --host http://localhost:8000
```
Open `http://localhost:8089` to trigger concurrent user simulation.

#### Using k6 (Headless Performance Gate):
```bash
k6 run tests/load/k6_chat_stress.js
```
