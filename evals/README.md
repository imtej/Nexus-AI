# 🧠 Nexus AI — Evaluation (Evals) Framework

This directory contains the AI evaluation framework for assessing response quality, persona alignment, RAG retrieval precision, and PII privacy sanitization in **Nexus AI**.

---

## 📐 Evaluation Dimensions

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

---

## 📁 Directory Structure & File Index

```
evals/
├── README.md                         # Framework architecture & usage guide
│
├── datasets/                         # Benchmark Datasets
│   ├── golden_conversations.json     # Multi-turn benchmark dialogue test cases
│   └── memory_test_cases.json        # Test cases for memory extraction & PII detection
│
├── metrics/                          # Evaluation Evaluators
│   ├── persona_eval.py               # Persona & Empathy alignment score (0.0 to 1.0)
│   ├── rag_precision.py              # Memory retrieval precision & recall evaluator
│   └── pii_sanitization_eval.py       # Regex evaluator verifying zero PII in Collective Knowledge
│
└── run_evals.py                      # CLI runner executing the full evaluation suite
```

---

## 🛠 Included Evaluation Metrics

1. **RAG & Retrieval Precision (`evals/metrics/rag_precision.py`)**:
   - Tests whether `ContextRetriever` and HyDE expansion retrieve relevant memory nodes without noise.
   - Calculates Precision Score = `(Matching Memory Types / Total Retrieved Memories)`.

2. **Persona & Empathy Alignment (`evals/metrics/persona_eval.py`)**:
   - Scores responses against `nexus_personality.yaml` guidelines (0.0 to 1.0 scale).
   - Flags robotic corporate phrases (e.g., *"As an AI..."*, *"I am an assistant..."*).

3. **PII & Privacy Protection (`evals/metrics/pii_sanitization_eval.py`)**:
   - Validates zero PII (Emails, Phone numbers, SSNs) enters the shared `collective_knowledge` table during `InsightDistiller` runs.

---

## 🚀 Running the Evaluation Suite

Execute the CLI evaluation runner across all benchmark datasets:

```bash
python evals/run_evals.py
```
