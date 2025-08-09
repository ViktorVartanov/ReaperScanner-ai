from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class HttpExchange(BaseModel):
    method: str
    url: str
    request_headers: Dict[str, str] = Field(default_factory=dict)
    request_body: Optional[str] = None
    status: Optional[int] = None
    response_headers: Dict[str, str] = Field(default_factory=dict)
    response_body: Optional[str] = None

class Education(BaseModel):
    summary: str
    steps: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class Finding(BaseModel):
    id: str
    type: str
    severity: str
    confidence: float = 0.5
    target: str
    evidence: Dict[str, str] = Field(default_factory=dict)
    education: Optional[Education] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ScanResult(BaseModel):
    target: str
    findings: List[Finding] = Field(default_factory=list)
    stats: Dict[str, int] = Field(default_factory=dict)
