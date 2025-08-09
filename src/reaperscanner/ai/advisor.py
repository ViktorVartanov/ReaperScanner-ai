from __future__ import annotations
import os
from pydantic import BaseModel
from ..models import HttpExchange, Education

class AIResponse(BaseModel):
    vulnerability: str
    confidence: float
    tutorial: Education

class ChatAdvisor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-thinking")

    async def analyze(self, exchange: HttpExchange) -> AIResponse:
        if not self.api_key:
            # Heuristic fallback if no API key
            vul = "Potential File Upload or XSS"
            conf = 0.4
            steps = [
                "Inspect parameters and reflected content for XSS indicators.",
                "If multipart upload is present, try safe extension/MIME tests.",
                "Validate server-side filtering and storage location."
            ]
            return AIResponse(
                vulnerability=vul,
                confidence=conf,
                tutorial=Education(
                    summary=f"Heuristic analysis of {exchange.url}",
                    steps=steps,
                    references=["https://owasp.org/Top10/"]
                )
            )
        # Placeholder for actual SDK call to your chat model provider.
        return AIResponse(
            vulnerability="AI-Assessed: LFI",
            confidence=0.72,
            tutorial=Education(
                summary="Likely path traversal based on response patterns.",
                steps=[
                    "Probe file parameters with ../../ traversal.",
                    "Base64-encoded filter wrapper to avoid filters.",
                    "Confirm via benign file reads and logging evidence."
                ],
                references=["https://owasp.org/Top10/"]
            )
        )
