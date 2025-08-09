from __future__ import annotations
import asyncio, urllib.parse
from typing import Set, List
import aiohttp
from bs4 import BeautifulSoup
from .models import HttpExchange

class Crawler:
    def __init__(self, max_pages: int = 200, timeout: int = 20, respect_robots: bool = True):
        self.max_pages = max_pages
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.respect_robots = respect_robots

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> HttpExchange | None:
        try:
            async with session.get(url, timeout=self.timeout) as resp:
                text = await resp.text(errors="ignore")
                return HttpExchange(
                    method="GET", url=str(resp.url),
                    request_headers={}, request_body=None,
                    status=resp.status,
                    response_headers=dict(resp.headers),
                    response_body=text
                )
        except Exception:
            return None

    async def crawl(self, start_url: str) -> List[HttpExchange]:
        seen: Set[str] = set()
        to_visit: asyncio.Queue[str] = asyncio.Queue()
        await to_visit.put(start_url)
        base = "{uri.scheme}://{uri.netloc}".format(uri=urllib.parse.urlparse(start_url))
        results: List[HttpExchange] = []

        async with aiohttp.ClientSession() as session:
            while not to_visit.empty() and len(seen) < self.max_pages:
                url = await to_visit.get()
                if url in seen:
                    continue
                seen.add(url)
                ex = await self.fetch(session, url)
                if not ex:
                    continue
                results.append(ex)
                soup = BeautifulSoup(ex.response_body or "", "lxml")
                for a in soup.find_all("a", href=True):
                    href = urllib.parse.urljoin(url, a["href"])
                    if href.startswith(base) and href not in seen:
                        await to_visit.put(href)
        return results
