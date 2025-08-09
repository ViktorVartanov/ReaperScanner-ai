from __future__ import annotations
import re, uuid
from typing import List
from .base import BaseDetector
from ..models import HttpExchange, Finding

REFLECT_PATTERNS = [
    r"<script[^>]*>",
    r"onerror\s*=",
    r"alert\s*\(",
]

class XSSDetector(BaseDetector):
    key = "xss"
    severity = "medium"

    async def analyze(self, exchange: HttpExchange) -> List[Finding]:
        findings: List[Finding] = []
        body = (exchange.response_body or "")[:200000]
        if any(re.search(p, body, flags=re.I) for p in REFLECT_PATTERNS):
            findings.append(Finding(
                id=str(uuid.uuid4()),
                type="Reflected XSS (indicator)",
                severity=self.severity,
                confidence=0.55,
                target=exchange.url,
                evidence={
                    "snippet": body[:400]
                },
                education=self.edu(
                    "Response contains common XSS indicators (script tags, handlers).",
                    [
                        "Try injecting a harmless payload into a reflected parameter, e.g. q='\"><svg onload=alert(1)>",
                        "Confirm if the payload is unencoded and executed in the DOM.",
                        "Check for appropriate output encoding and CSP headers."
                    ]
                )
            ))
        return findings
