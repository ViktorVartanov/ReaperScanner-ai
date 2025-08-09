from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src.reaperscanner.models import HttpExchange, ScanResult
from src.reaperscanner.pipeline import Pipeline
from src.reaperscanner.ai.advisor import ChatAdvisor, AIResponse

app = FastAPI(title="ReaperScanner AI API", version="0.1.0")

pipeline = Pipeline()
advisor = ChatAdvisor()

class AnalyzePayload(BaseModel):
    exchange: HttpExchange

@app.post("/analyze", response_model=AIResponse)
async def analyze(payload: AnalyzePayload):
    return await advisor.analyze(payload.exchange)

class BatchPayload(BaseModel):
    exchanges: List[HttpExchange]
    target: str

@app.post("/scan", response_model=ScanResult)
async def scan(payload: BatchPayload):
    result = await pipeline.scan_exchanges(payload.target, payload.exchanges)
    return result
