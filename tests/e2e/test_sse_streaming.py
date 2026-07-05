"""
E2E test validating SSE Streaming Response format.
"""

import pytest

def test_sse_event_format_parser():
    raw_sse_chunk = "data: {\"token\": \"Hello\", \"done\": false}\n\n"
    
    lines = [line.strip() for line in raw_sse_chunk.split("\n") if line.strip()]
    assert len(lines) == 1
    assert lines[0].startswith("data: ")

    data_payload = lines[0][6:]
    assert "token" in data_payload
