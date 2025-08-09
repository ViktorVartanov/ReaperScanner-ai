from __future__ import annotations
import uuid
from typing import List
from .base import BaseDetector
from ..models import HttpExchange, Finding

class FileUploadDetector(BaseDetector):
    key = "file_upload"
    severity = "high"

    async def analyze(self, exchange: HttpExchange) -> List[Finding]:
        findings: List[Finding] = []
        if not exchange.request_headers:
            return findings
        ctype = exchange.request_headers.get("content-type","").lower()
        if exchange.method.upper() == "POST" and "multipart/form-data" in ctype:
            body = (exchange.response_body or "")[:200000]
            if "upload" in exchange.url.lower() or "file" in exchange.url.lower():
                findings.append(Finding(
                    id=str(uuid.uuid4()),
                    type="File Upload (potentially unsafe endpoint)",
                    severity=self.severity,
                    confidence=0.5,
                    target=exchange.url,
                    evidence={"content-type": ctype},
                    education=self.edu(
                        "Endpoint processes multipart uploads; validate extension/MIME handling.",
                        [
                            "Attempt to upload a benign .txt, then a .php/.jsp/.aspx renamed to .jpg.",
                            "Try double extensions (shell.php.jpg) and polyglots.",
                            "Confirm storage path; verify execution vs. download-only behavior."
                        ]
                    )
                ))
        return findings
