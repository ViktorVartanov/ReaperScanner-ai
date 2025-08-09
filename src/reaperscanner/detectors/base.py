from __future__ import annotations
from typing import List
from ..models import HttpExchange, Finding, Education

class BaseDetector:
    key: str = "base"
    severity: str = "info"

    async def analyze(self, exchange: HttpExchange) -> List[Finding]:
        raise NotImplementedError

    @staticmethod
    def edu(summary: str, steps: list[str]) -> Education:
        return Education(summary=summary, steps=steps, references=[
            "https://owasp.org/Top10/",
        ])
