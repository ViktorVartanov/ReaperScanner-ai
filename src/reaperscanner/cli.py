from __future__ import annotations
import asyncio, typer
from .crawler import Crawler
from .pipeline import Pipeline
from .reporting import write_reports

app = typer.Typer(add_completion=False)

@app.command()
def scan(target: str, max_pages: int = typer.Option(100, help="Max pages to crawl"),
         report: str = typer.Option(None, help="Path to HTML report"),
         json_out: str = typer.Option(None, help="Path to JSON report")):
    """Crawl and scan a target URL."""
    async def _run():
        crawler = Crawler(max_pages=max_pages)
        exchanges = await crawler.crawl(target)
        pipe = Pipeline()
        res = await pipe.scan_exchanges(target, exchanges)
        write_reports(res, report, json_out)
        typer.echo(f"Done. Exchanges: {res.stats['exchanges']} Findings: {res.stats['findings']}")
    asyncio.run(_run())

if __name__ == "__main__":
    app()
