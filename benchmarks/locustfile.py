"""
Nexus AI — Locust Load & Stress Testing Tool
Simulates multi-user concurrent SSE chat traffic and measures RPS and response times.
"""

from locust import HttpUser, task, between
import uuid

class NexusUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Simulate user login session initialization."""
        self.conversation_id = str(uuid.uuid4())

    @task(3)
    def send_chat_message(self):
        """Simulates chat streaming request."""
        payload = {
            "message": "What is the core philosophy of Nexus AI?",
            "conversation_id": self.conversation_id
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        with self.client.post("/api/v1/chat/stream", json=payload, headers=headers, catch_response=True, stream=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}: Failed to initialize stream")

    @task(1)
    def check_evolution_stats(self):
        """Simulates public evolution stats request."""
        self.client.get("/api/v1/evolution")
