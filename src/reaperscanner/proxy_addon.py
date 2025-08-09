from __future__ import annotations
from mitmproxy import http
import asyncio
from .models import HttpExchange
from .pipeline import Pipeline

pipeline = Pipeline()

async def process(flow: http.HTTPFlow):
    ex = HttpExchange(
        method=flow.request.method,
        url=flow.request.pretty_url,
        request_headers=dict(flow.request.headers),
        request_body=flow.request.get_text(),
        status=flow.response.status_code if flow.response else None,
        response_headers=dict(flow.response.headers) if flow.response else {},
        response_body=flow.response.get_text() if flow.response else None,
    )
    findings = await pipeline.analyze_exchange(ex)
    if findings and flow.response:
        flow.response.headers["X-Reaper-Findings"] = str(len(findings))

def response(flow: http.HTTPFlow):
    asyncio.get_event_loop().create_task(process(flow))
