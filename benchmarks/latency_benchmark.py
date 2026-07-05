#!/usr/bin/env python3
"""
Nexus AI — Latency & Time To First Token (TTFT) Benchmark Tool
Measures end-to-end SSE streaming response time and first token latency.
"""

import argparse
import time
import requests
import json
import sys

def benchmark_ttft(base_url: str, auth_token: str = None, prompt: str = "Hello Nexus AI, who are you?"):
    """
    Measures Time To First Token (TTFT) and total stream duration.
    """
    url = f"{base_url.rstrip('/')}/api/v1/chat/stream"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    payload = {
        "message": prompt,
        "conversation_id": None
    }

    print(f"🚀 Benchmarking URL: {url}")
    print(f"💬 Prompt: '{prompt}'")
    print("--------------------------------------------------")

    start_time = time.perf_counter()
    ttft = None
    total_tokens = 0
    full_response = ""

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=15)
        response.raise_for_status()

        for line in response.iter_lines():
            line_str = line.decode('utf-8') if line else ""
            if line_str.startswith("data: "):
                token_data = line_str[6:].strip()
                if token_data and token_data != "[DONE]":
                    if ttft is None:
                        ttft = (time.perf_counter() - start_time) * 1000  # ms
                        print(f"⚡ Time To First Token (TTFT): {ttft:.2f} ms")
                    
                    total_tokens += 1
                    full_response += token_data

        total_time = (time.perf_counter() - start_time) * 1000  # ms
        tokens_per_sec = (total_tokens / (total_time / 1000)) if total_time > 0 else 0

        print("--------------------------------------------------")
        print(f"📊 Results Summary:")
        print(f"   • TTFT:                 {ttft:.2f} ms" if ttft else "   • TTFT: N/A")
        print(f"   • Total Response Time:  {total_time:.2f} ms")
        print(f"   • Total Tokens:         {total_tokens}")
        print(f"   • Token Throughput:     {tokens_per_sec:.2f} tokens/sec")
        print("--------------------------------------------------")
        return {
            "ttft_ms": ttft,
            "total_time_ms": total_time,
            "total_tokens": total_tokens,
            "tokens_per_sec": tokens_per_sec
        }

    except Exception as e:
        print(f"❌ Error during latency benchmark: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus AI Latency & TTFT Benchmark Tool")
    parser.add_argument("--url", default="http://localhost:8000", help="Backend base URL")
    parser.add_argument("--token", default=None, help="Supabase JWT Bearer token")
    parser.add_argument("--prompt", default="Explain quantum computing in two concise sentences.", help="Prompt text")

    args = parser.parse_args()
    benchmark_ttft(args.url, args.token, args.prompt)
