from __future__ import annotations
import re, uuid
from typing import List
from .base import BaseDetector
from ..models import HttpExchange, Finding

LFI_MARKERS = [
    r"root:x:0:0:",  # /etc/passwd
    r"\[boot loader\]|partition\=",  # boot.ini
    r"<\?php",  # raw PHP
]

class LFIDetector(BaseDetector):
    key = "lfi"
    severity = "high"

    async def analyze(self, exchange: HttpExchange) -> List[Finding]:
        findings: List[Finding] = []
        body = (exchange.response_body or "")[:200000]
        if any(re.search(p, body, flags=re.I) for p in LFI_MARKERS):
            findings.append(Finding(
                id=str(uuid.uuid4()),
                type="Local File Inclusion (indicator)",
                severity=self.severity,
                confidence=0.7,
                target=exchange.url,
                evidence={ "snippet": body[:400] },
                education=self.edu(
                    "Response contains file content patterns suggesting LFI.",
                    [
                        "Try path traversal payloads in file parameters: ../../../../etc/passwd",
                        "URL-encode traversal: ..%2f..%2f..%2fetc%2fpasswd",
                        "Test wrappers: php://filter/convert.base64-encode/resource=index.php",
                        "Validate with out-of-band confirmation if possible."
                    ]
                )
            ))
        return findings
