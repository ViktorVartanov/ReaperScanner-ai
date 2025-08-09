from __future__ import annotations
import re, uuid
from typing import List
from .base import BaseDetector
from ..models import HttpExchange, Finding

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "pg_query()",
    "ORA-00933",
]

class SQLiDetector(BaseDetector):
    key = "sqli"
    severity = "high"

    async def analyze(self, exchange: HttpExchange) -> List[Finding]:
        findings: List[Finding] = []
        body = (exchange.response_body or "")[:200000]
        low = body.lower()
        match = next((e for e in SQL_ERRORS if e in low), None)
        if match:
            findings.append(Finding(
                id=str(uuid.uuid4()),
                type="SQL Injection (error-based indicator)",
                severity=self.severity,
                confidence=0.65,
                target=exchange.url,
                evidence={ "error": match },
                education=self.edu(
                    "Response includes database error strings indicating unsanitized input.",
                    [
                        "Toggle between ' and \" in parameters to provoke error-based leakage.",
                        "Try UNION-based checks: ' UNION SELECT 1,2,3 -- -",
                        "Use time-based payloads if no errors are shown: '||pg_sleep(5)--"
                    ]
                )
            ))
        return findings
