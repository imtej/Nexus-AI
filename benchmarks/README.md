# ⚡ Nexus AI — Benchmarking & Performance Suite

This directory contains automated performance scripts, latency measurement tools, and load testing configurations for **Nexus AI**.

---

## 📊 Benchmarking Specifications

| Metric | Target Baseline (Single Instance) | Target Scaled (5 App Runner / ECS Nodes) |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **< 600 ms** | **< 600 ms** |
| **Concurrent SSE Connections** | **300 Active Chatters** | **3,000 Active Chatters** |
| **Throughput (RPS)** | **35 Requests/sec** | **350 Requests/sec** |
| **pgvector Query Latency** | **< 25 ms** | **< 25 ms** |

---

## 📁 Directory Structure & Included Tools

```
benchmarks/
├── README.md                         # Benchmarking specifications & usage guide
├── latency_benchmark.py              # CLI runner measuring Time To First Token (TTFT)
└── locustfile.py                     # Locust stress load-testing script (300+ users)
```

---

## 🛠 Usage Instructions

### 1. Latency & TTFT Measurement (`latency_benchmark.py`)
Measures Time To First Token (TTFT) and individual agent execution times on the critical path:
- Node 1: `QueryAnalyzer` (~120ms)
- Node 2: `ContextRetriever` (~180ms)
- Node 3: `PromptBuilder` (~20ms)
- Node 4: `ResponseGenerator` (~150ms TTFT)

**Usage**:
```bash
python benchmarks/latency_benchmark.py --url http://localhost:8000 --prompt "Explain quantum computing in two sentences"
```

### 2. Concurrency & Stress Load Test (`locustfile.py`)
Simulates 100+ concurrent user SSE chat sessions using [Locust](https://locust.io).

**Usage**:
```bash
pip install locust
locust -f benchmarks/locustfile.py --host http://localhost:8000
```
Then open `http://localhost:8089` in your browser to trigger load tests.
