from __future__ import annotations
import asyncio
from typing import List, Type
from .models import HttpExchange, ScanResult, Finding
from .detectors.base import BaseDetector
from .detectors.xss import XSSDetector
from .detectors.lfi import LFIDetector
from .detectors.sqli import SQLiDetector
from .detectors.file_upload import FileUploadDetector

DEFAULT_DETECTORS: List[Type[BaseDetector]] = [
    XSSDetector, LFIDetector, SQLiDetector, FileUploadDetector
]

class Pipeline:
    def __init__(self, detectors: List[Type[BaseDetector]] | None = None):
        self.detectors = [d() for d in (detectors or DEFAULT_DETECTORS)]

    async def analyze_exchange(self, exchange: HttpExchange) -> List[Finding]:
        tasks = [d.analyze(exchange) for d in self.detectors]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        findings: List[Finding] = [f for sub in results for f in sub]
        return findings

    async def scan_exchanges(self, target: str, exchanges: List[HttpExchange]) -> ScanResult:
        result = ScanResult(target=target)
        for ex in exchanges:
            fs = await self.analyze_exchange(ex)
            result.findings.extend(fs)
        result.stats = {"exchanges": len(exchanges), "findings": len(result.findings)}
        return result
