"""
Locust load-testing script for simulating 500+ concurrent SSE users.
"""

from locust import HttpUser, task, between
import uuid

class NexusLoadUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.conversation_id = str(uuid.uuid4())

    @task(3)
    def sse_chat_stream(self):
        payload = {
            "message": "Explain the Nexus AI Collective Knowledge Architecture",
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
                response.failure(f"Failed with status: {response.status_code}")
