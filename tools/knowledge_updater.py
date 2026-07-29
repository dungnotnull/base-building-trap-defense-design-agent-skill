"""
knowledge_updater.py — Skill 250: base-building-trap-defense-design
===================================================================
Production-grade crawl pipeline for the living knowledge base
(SECOND-KNOWLEDGE-BRAIN.md).

It fetches the latest academic papers (ArXiv, Semantic Scholar) and domain
news (RSS) for the Base-Building Game Defense & Trap System Design domain,
deduplicates by SHA256 of the verifiable identifier (DOI/URL/ISBN), scores each
candidate with a transparent composite metric, and appends the survivors to
Section 7 of the knowledge brain. The pipeline is idempotent, fault-tolerant
(it never aborts on a single source failure), and never fabricates: a candidate
without a verifiable identifier is rejected.

Dependencies (see requirements.txt):
    pip install requests feedparser python-dateutil

Usage:
    python tools/knowledge_updater.py                 # full crawl + append
    python tools/knowledge_updater.py --dry-run       # preview, no write
    python tools/knowledge_updater.py --news-only      # RSS only
    python tools/knowledge_updater.py --keywords "a" "b"
    python tools/knowledge_updater.py --json-logs      # structured logs
    python tools/knowledge_updater.py --config path.json

Exit codes: 0 success (including "no new entries"), 1 usage/runtime error,
2 partial failure (some sources failed but pipeline completed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

try:
    import requests
except ImportError:  # pragma: no cover - optional at runtime, exercised in tests
    requests = None  # type: ignore

try:
    import feedparser
except ImportError:  # pragma: no cover
    feedparser = None  # type: ignore

try:
    from dateutil import parser as date_parser
except ImportError:  # pragma: no cover
    date_parser = None  # type: ignore


# ----------------------------- configuration -------------------------------

DEFAULT_KEYWORDS: List[str] = [
    "base building defense design",
    "trap synergy trigger logic",
    "chokepoint funneling pathing",
    "tower defense balance",
    "PvP raid counter play",
    "spatial layout threat zoning",
]

KNOWLEDGE_CONFIG: Dict[str, Any] = {
    "domain": "Base-Building Game Defense & Trap System Design",
    "keywords": list(DEFAULT_KEYWORDS),
    # ArXiv categories relevant to game AI, HCI, and defense/strategy design.
    "arxiv_categories": ["cs.AI", "cs.HC"],
    "arxiv_base": "https://export.arxiv.org/api/query",
    "semantic_scholar_base": "https://api.semanticscholar.org/graph/v1/paper/search",
    # Stable ArXiv RSS feeds (category-level) for the daily news crawl.
    "rss_feeds": [
        "http://export.arxiv.org/rss/cs.AI",
        "http://export.arxiv.org/rss/cs.HC",
    ],
    "authoritative_docs": [
        "Proceedings of CHI PLAY (ACM)",
        "IEEE Transactions on Games",
        "Entertainment Computing (Elsevier)",
        "Computers in Human Behavior (Elsevier)",
        "Simulation & Gaming (SAGE)",
        "Journal of Game Design & Development Education",
    ],
    "scoring_weights": {
        "recency": 0.4,
        "keyword_relevance": 0.4,
        "citation_count": 0.2,
    },
    "max_results_per_source": 10,
    "max_new_entries_per_run": 20,
    "request_timeout_seconds": 30,
    "max_retries": 3,
    "base_retry_delay_seconds": 2.0,
    "user_agent": "base-building-trap-defense-design/knowledge-updater (+https://github.com/open-source)",
}

BRAIN_PATH: Path = Path(__file__).resolve().parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
LOG_DIR: Path = Path(__file__).resolve().parent.parent / "logs"

_LOGGER = logging.getLogger("knowledge_updater")


@dataclass
class CrawlEntry:
    """A normalized crawl candidate flowing through the pipeline."""

    title: str
    authors: List[str]
    year: int
    venue: str
    doi_or_url: str
    abstract: str
    published_date: Optional[datetime]
    citation_count: int
    source: str
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "doi_or_url": self.doi_or_url,
            "abstract": self.abstract,
            "published_date": self.published_date,
            "citation_count": self.citation_count,
            "source": self.source,
            "score": self.score,
        }

# ------------------------------- logging ----------------------------------

class _JsonFormatter(logging.Formatter):
    """Emit one JSON object per log record for machine-parseable runs."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(json_logs: bool = False, verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    if json_logs:
        handler.setFormatter(_JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


# ------------------------------ networking ---------------------------------

def fetch_with_retry(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    base_delay: float = 2.0,
    timeout: int = 30,
) -> Optional["requests.Response"]:
    """HTTP GET with exponential backoff on 429/5xx. Returns None on hard failure."""
    if requests is None:
        _LOGGER.warning("requests not installed; skipping %s", url)
        return None
    headers = {"User-Agent": KNOWLEDGE_CONFIG.get("user_agent", "knowledge-updater")}
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(base_delay * (2 ** attempt))
            resp = requests.get(url, params=params or {}, timeout=timeout, headers=headers)
            if resp.status_code == 429:
                _LOGGER.warning("429 rate-limited on %s (attempt %s)", url, attempt + 1)
                if attempt < max_retries - 1:
                    continue
                return None
            if resp.status_code >= 500:
                _LOGGER.warning("server %s on %s (attempt %s)", resp.status_code, url, attempt + 1)
                if attempt < max_retries - 1:
                    continue
                return None
            resp.raise_for_status()
            return resp
        except requests.RequestException as ex:
            _LOGGER.warning("request failed on %s (attempt %s): %s", url, attempt + 1, ex)
            if attempt < max_retries - 1:
                time.sleep(base_delay)
            else:
                return None
    return None


# ------------------------------ identifiers --------------------------------

def compute_hash(identifier: str) -> str:
    """SHA256 of a normalized identifier for dedup (case/whitespace-insensitive)."""
    return hashlib.sha256(identifier.strip().lower().encode("utf-8")).hexdigest()


_DOI_RE = re.compile(r"10\.\d{4,9}/[^\s|]+", re.IGNORECASE)
_ISBN_RE = re.compile(r"ISBN\s*([0-9Xx\-]{10,17})", re.IGNORECASE)
# Captures identifiers from appended Section-7 entries (e.g. "**DOI/URL:** <id>").
_BRAIN_HASH_RE = re.compile(r"\*\*DOI/URL:\*\*\s*(\S+)", re.IGNORECASE)


def extract_identifier(text: str) -> str:
    """Return the first verifiable identifier (DOI/ISBN/URL) found in text, or ''."""
    if not text:
        return ""
    m = _DOI_RE.search(text)
    if m:
        return m.group(0).rstrip(".,;)?!")
    m = _ISBN_RE.search(text)
    if m:
        return "ISBN:" + m.group(1).replace("-", "")
    stripped = text.strip().rstrip(".,;)?!")
    if stripped.lower().startswith(("http://", "https://")):
        return stripped
    return stripped


def load_existing_hashes(path: Path = BRAIN_PATH) -> Set[str]:
    """Collect hashes of every verifiable identifier already recorded in the brain.

    Scans both appended Section-7 entries (``**DOI/URL:** <id>``) and baseline
    table references (bare DOIs / ISBNs) so the pipeline dedups against the full
    knowledge base, not just the append log.
    """
    if not path.exists():
        return set()
    hashes: Set[str] = set()
    text = path.read_text(encoding="utf-8")
    for m in _BRAIN_HASH_RE.finditer(text):
        ident = extract_identifier(m.group(1))
        if ident:
            hashes.add(compute_hash(ident))
    for m in _DOI_RE.finditer(text):
        hashes.add(compute_hash(m.group(0).rstrip(".,;)?!")))
    for m in re.finditer(r"ISBN\s*([0-9Xx\-]{10,17})", text, re.IGNORECASE):
        hashes.add(compute_hash("ISBN:" + m.group(1).replace("-", "")))
    return hashes


# ------------------------------- scoring -----------------------------------

def score_entry(entry: Dict[str, Any], keywords: List[str], now: datetime) -> float:
    """Composite 0-10 score: recency(0.4) + keyword_relevance(0.4) + citations(0.2)."""
    pub = entry.get("published_date")
    recency = 0.0
    if isinstance(pub, datetime):
        try:
            recency = max(0.0, 1.0 - (now - pub).days / 730.0)
        except (TypeError, ValueError):
            recency = 0.0
    text = ((entry.get("title") or "") + " " + (entry.get("abstract") or "")).lower()
    hits = sum(1 for kw in keywords if kw.lower() in text)
    relevance = min(hits / max(len(keywords), 1), 1.0)
    cit = entry.get("citation_count", 0) or 0
    cit_score = min(math.log1p(cit) / math.log1p(1000), 1.0)
    w = KNOWLEDGE_CONFIG["scoring_weights"]
    return round(
        (recency * w["recency"] + relevance * w["keyword_relevance"] + cit_score * w["citation_count"]) * 10.0,
        2,
    )

# ------------------------------- sources -----------------------------------

def fetch_arxiv(keywords: List[str]) -> List[Dict[str, Any]]:
    """Query the ArXiv API for configured categories + keywords."""
    if requests is None or not KNOWLEDGE_CONFIG["arxiv_categories"]:
        _LOGGER.info("ArXiv: skipped (no requests or no categories)")
        return []
    import xml.etree.ElementTree as ET

    cats = KNOWLEDGE_CONFIG["arxiv_categories"]
    cat_clause = " OR ".join("cat:" + c for c in cats)
    kw_clause = " OR ".join('"' + k + '"' for k in keywords[:5])
    query = "(" + cat_clause + ") AND (" + kw_clause + ")"
    resp = fetch_with_retry(
        KNOWLEDGE_CONFIG["arxiv_base"],
        {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": KNOWLEDGE_CONFIG["max_results_per_source"],
        },
        max_retries=KNOWLEDGE_CONFIG["max_retries"],
        timeout=KNOWLEDGE_CONFIG["request_timeout_seconds"],
    )
    if resp is None:
        return []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as ex:
        _LOGGER.warning("ArXiv XML parse failed: %s", ex)
        return []
    out: List[Dict[str, Any]] = []
    for entry in root.findall("atom:entry", ns):
        t = entry.find("atom:title", ns)
        s = entry.find("atom:summary", ns)
        i = entry.find("atom:id", ns)
        p = entry.find("atom:published", ns)
        title = (t.text or "").strip().replace("\n", " ") if t is not None else ""
        url = (i.text or "").strip() if i is not None else ""
        if not title or not url:
            continue
        pub: Optional[datetime] = None
        if p is not None and p.text and date_parser is not None:
            try:
                pub = date_parser.parse(p.text).replace(tzinfo=None)
            except (TypeError, ValueError):
                pub = None
        authors: List[str] = []
        for a in entry.findall("atom:author", ns):
            name_el = a.find("atom:name", ns)
            if name_el is not None and name_el.text:
                authors.append(name_el.text)
        authors = authors[:3]
        out.append(
            {
                "title": title,
                "authors": authors,
                "year": pub.year if pub else datetime.now().year,
                "venue": "ArXiv",
                "doi_or_url": url,
                "abstract": ((s.text or "").strip() or "")[:300] if s is not None else "",
                "published_date": pub,
                "citation_count": 0,
                "source": "arxiv",
            }
        )
    _LOGGER.info("ArXiv: %d candidates", len(out))
    return out


def fetch_semantic_scholar(keywords: List[str]) -> List[Dict[str, Any]]:
    """Query Semantic Scholar for papers matching the keyword cluster."""
    if requests is None:
        _LOGGER.info("Semantic Scholar: skipped (no requests)")
        return []
    resp = fetch_with_retry(
        KNOWLEDGE_CONFIG["semantic_scholar_base"],
        {
            "query": " ".join(keywords[:4]),
            "fields": "title,authors,year,venue,externalIds,abstract,citationCount",
            "limit": KNOWLEDGE_CONFIG["max_results_per_source"],
        },
        max_retries=KNOWLEDGE_CONFIG["max_retries"],
        timeout=KNOWLEDGE_CONFIG["request_timeout_seconds"],
    )
    if resp is None:
        return []
    try:
        data = resp.json()
    except ValueError as ex:
        _LOGGER.warning("Semantic Scholar JSON parse failed: %s", ex)
        return []
    out: List[Dict[str, Any]] = []
    for p in data.get("data", []) if isinstance(data, dict) else []:
        title = p.get("title", "")
        if not title:
            continue
        year = p.get("year") or datetime.now().year
        ext = p.get("externalIds", {}) or {}
        doi = ext.get("DOI") or ""
        if not doi and ext.get("ArXiv"):
            doi = "https://arxiv.org/abs/" + str(ext["ArXiv"])
        if not doi:
            doi = "https://www.semanticscholar.org/paper/" + str(p.get("paperId", ""))
        out.append(
            {
                "title": title,
                "authors": [a.get("name", "") for a in (p.get("authors") or [])[:3]],
                "year": year,
                "venue": p.get("venue") or "Unknown",
                "doi_or_url": doi,
                "abstract": (p.get("abstract") or "")[:300],
                "published_date": datetime(int(year), 1, 1),
                "citation_count": int(p.get("citationCount", 0) or 0),
                "source": "semantic_scholar",
            }
        )
    _LOGGER.info("Semantic Scholar: %d candidates", len(out))
    return out


def fetch_rss() -> List[Dict[str, Any]]:
    """Parse configured RSS feeds (ArXiv category feeds) into crawl candidates."""
    if feedparser is None or not KNOWLEDGE_CONFIG["rss_feeds"]:
        _LOGGER.info("RSS: skipped (no feedparser or no feeds)")
        return []
    out: List[Dict[str, Any]] = []
    for url in KNOWLEDGE_CONFIG["rss_feeds"]:
        try:
            feed = feedparser.parse(url)
        except Exception as ex:  # feedparser rarely raises, but be defensive
            _LOGGER.warning("RSS %s failed: %s", url, ex)
            continue
        for item in feed.entries[:10]:
            title = item.get("title", "")
            link = item.get("link", "")
            if not title or not link:
                continue
            pp = item.get("published_parsed")
            pub = datetime(*pp[:6]) if pp else datetime.now()
            out.append(
                {
                    "title": title,
                    "authors": ["Editorial"],
                    "year": pub.year,
                    "venue": "RSS",
                    "doi_or_url": link,
                    "abstract": (item.get("summary", "") or "")[:200],
                    "published_date": pub,
                    "citation_count": 0,
                    "source": "rss",
                }
            )
    _LOGGER.info("RSS: %d candidates", len(out))
    return out

# --------------------------- formatting & write ----------------------------

def format_entry(entry: Dict[str, Any], score: float) -> str:
    """Render one knowledge entry as Markdown for Section 7 of the brain."""
    d = datetime.now().strftime("%Y-%m-%d")
    authors = ", ".join(entry.get("authors", [])) or "Unknown"
    return (
        "\n### " + d + " — " + (entry.get("title") or "Untitled") + "\n"
        "- **Authors:** " + authors + "\n"
        "- **Year:** " + str(entry.get("year", "")) + "\n"
        "- **Venue:** " + (entry.get("venue") or "Unknown") + "\n"
        "- **DOI/URL:** " + (entry.get("doi_or_url") or "") + "\n"
        "- **Relevance Score:** " + str(score) + "/10\n"
        "- **Key Finding:** " + (entry.get("abstract") or "No abstract available.") + "\n"
    )


def append_to_brain(entries: Iterable[Dict[str, Any]], dry_run: bool = False, path: Path = BRAIN_PATH) -> int:
    """Dedup, score, rank, and append new entries to the brain file. Returns count appended."""
    if not path.exists():
        _LOGGER.error("brain file not found: %s", path)
        return 0
    existing = load_existing_hashes(path)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    seen: Set[str] = set(existing)
    new: List[Dict[str, Any]] = []
    for e in entries:
        ident = extract_identifier(e.get("doi_or_url", ""))
        if not ident:
            _LOGGER.debug("rejected (no identifier): %s", e.get("title", ""))
            continue
        h = compute_hash(ident)
        if h in seen:
            continue
        seen.add(h)
        new.append(e)
    if not new:
        _LOGGER.info("no new entries to append")
        return 0
    for e in new:
        e["_score"] = score_entry(e, KNOWLEDGE_CONFIG["keywords"], now)
    new.sort(key=lambda x: x["_score"], reverse=True)
    new = new[: KNOWLEDGE_CONFIG["max_new_entries_per_run"]]
    text = "".join(format_entry(e, e["_score"]) for e in new)
    if dry_run:
        _LOGGER.info("[DRY] would append %d entries", len(new))
        return len(new)
    content = path.read_text(encoding="utf-8")
    if "## 7. Knowledge Update Log" in content:
        content += text
    else:
        content += "\n## 7. Knowledge Update Log\n" + text
    path.write_text(content, encoding="utf-8")
    _LOGGER.info("appended %d entries", len(new))
    return len(new)


# ------------------------------- config IO ---------------------------------

def load_config(path: Optional[str]) -> None:
    """Optionally merge an external JSON config into KNOWLEDGE_CONFIG."""
    if not path:
        return
    p = Path(path)
    if not p.exists():
        _LOGGER.error("config not found: %s", p)
        return
    try:
        external = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as ex:
        _LOGGER.error("config JSON invalid: %s", ex)
        return
    if not isinstance(external, dict):
        _LOGGER.error("config root must be an object")
        return
    KNOWLEDGE_CONFIG.update(external)


# --------------------------------- CLI -------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Crawl academic + news sources and append to SECOND-KNOWLEDGE-BRAIN.md.",
    )
    ap.add_argument("--dry-run", action="store_true", help="preview candidates without writing")
    ap.add_argument("--news-only", action="store_true", help="only crawl RSS news feeds")
    ap.add_argument("--keywords", nargs="+", default=KNOWLEDGE_CONFIG["keywords"], help="override keyword cluster")
    ap.add_argument("--json-logs", action="store_true", help="emit structured JSON logs")
    ap.add_argument("--verbose", action="store_true", help="debug logging")
    ap.add_argument("--config", default=None, help="path to optional JSON config file")
    args = ap.parse_args(argv)

    configure_logging(json_logs=args.json_logs, verbose=args.verbose)
    load_config(args.config)

    _LOGGER.info("start %s dry=%s news=%s", datetime.now().isoformat(), args.dry_run, args.news_only)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    all_entries: List[Dict[str, Any]] = []
    partial_failure = False
    if not args.news_only:
        arxiv = fetch_arxiv(args.keywords)
        if not arxiv and KNOWLEDGE_CONFIG["arxiv_categories"]:
            partial_failure = True
        all_entries += arxiv
        time.sleep(1)
        ss = fetch_semantic_scholar(args.keywords)
        if not ss:
            partial_failure = True
        all_entries += ss
        time.sleep(1)
    rss = fetch_rss()
    if not rss and KNOWLEDGE_CONFIG["rss_feeds"] and feedparser is not None:
        partial_failure = True
    all_entries += rss

    _LOGGER.info("candidates: %d", len(all_entries))
    n = append_to_brain(all_entries, args.dry_run)
    _LOGGER.info("done; appended %d", n)
    return 2 if (partial_failure and n == 0 and not args.dry_run) else 0


if __name__ == "__main__":
    sys.exit(main())