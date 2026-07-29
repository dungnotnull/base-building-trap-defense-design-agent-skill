"""
test_knowledge_updater.py — Skill 250: base-building-trap-defense-design
========================================================================
Unit tests for the knowledge crawl pipeline: identifier extraction, SHA256
dedup, composite scoring, entry formatting, brain append idempotency, and
config integrity. Runs without network access (no live fetch).

Run: python tools/test_knowledge_updater.py
Exit code 0 = all tests pass.
"""
import datetime
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge_updater as ku


_failures = []


def check(name, cond, detail=""):
    if cond:
        print("[OK] " + name)
    else:
        print("[FAIL] " + name + (" — " + detail if detail else ""))
        _failures.append(name)


def test_hash_deterministic():
    a = ku.compute_hash("https://x.com/1")
    b = ku.compute_hash("https://x.com/1")
    c = ku.compute_hash(" https://x.com/1 ")  # whitespace + case insensitive
    d = ku.compute_hash("HTTPS://X.COM/1")
    check("dedup hash deterministic", a == b)
    check("dedup hash whitespace-insensitive", a == c)
    check("dedup hash case-insensitive", a == d)
    check("dedup hash distinct", a != ku.compute_hash("https://x.com/2"))


def test_extract_identifier():
    check("extract DOI", ku.extract_identifier("DOI 10.1109/HICSS.2014.377").endswith("377"))
    check("extract ISBN", ku.extract_identifier("ISBN 978-0123694966").startswith("ISBN:"))
    check("extract URL", ku.extract_identifier("https://example.org/p").startswith("https://"))
    check("extract empty", ku.extract_identifier("") == "")


def test_score_bounds():
    e = {
        "title": ku.KNOWLEDGE_CONFIG["domain"],
        "abstract": ku.KNOWLEDGE_CONFIG["domain"],
        "published_date": datetime.datetime.now(),
        "citation_count": 10,
    }
    s = ku.score_entry(e, ku.KNOWLEDGE_CONFIG["keywords"], datetime.datetime.now())
    check("score in [0,10]", 0 <= s <= 10, "score=" + str(s))
    e_old = {
        "title": "unrelated topic",
        "abstract": "unrelated topic",
        "published_date": datetime.datetime(2000, 1, 1),
        "citation_count": 0,
    }
    s_old = ku.score_entry(e_old, ku.KNOWLEDGE_CONFIG["keywords"], datetime.datetime.now())
    check("recent+relevant scores higher than old+unrelated", s > s_old, "s=" + str(s) + " s_old=" + str(s_old))


def test_format_entry():
    txt = ku.format_entry(
        {
            "title": "Tower Defense Balance",
            "authors": ["A. Author"],
            "year": 2026,
            "venue": "IEEE Trans. Games",
            "doi_or_url": "10.0000/test",
            "abstract": "abstract text",
        },
        7.5,
    )
    check("format has DOI/URL", "DOI/URL:" in txt)
    check("format has score", "Relevance Score:" in txt and "7.5" in txt)
    check("format has title", "Tower Defense Balance" in txt)


def test_append_dry_run_idempotent():
    # Create a temp brain file to avoid mutating the real one.
    with tempfile.TemporaryDirectory() as tmp:
        brain = Path(tmp) / "BRAIN.md"
        brain.write_text(
            "# Brain\n\n## 7. Knowledge Update Log\n\n### 2026-01-01 — Existing\n- **DOI/URL:** 10.1109/HICSS.2014.377\n",
            encoding="utf-8",
        )
        entries = [
            {
                "title": "New Paper A",
                "authors": ["X"],
                "year": 2026,
                "venue": "ArXiv",
                "doi_or_url": "10.1109/HICSS.2014.377",  # duplicate -> skipped
                "abstract": "base building defense design trap synergy",
                "published_date": datetime.datetime.now(),
                "citation_count": 5,
                "source": "arxiv",
            },
            {
                "title": "New Paper B",
                "authors": ["Y"],
                "year": 2026,
                "venue": "ArXiv",
                "doi_or_url": "https://arxiv.org/abs/9999.99999",
                "abstract": "chokepoint funneling pathing",
                "published_date": datetime.datetime.now(),
                "citation_count": 1,
                "source": "arxiv",
            },
            {
                "title": "No Identifier",
                "authors": ["Z"],
                "year": 2026,
                "venue": "Unknown",
                "doi_or_url": "",
                "abstract": "x",
                "published_date": datetime.datetime.now(),
                "citation_count": 0,
                "source": "arxiv",
            },
        ]
        n1 = ku.append_to_brain(entries, dry_run=True, path=brain)
        check("dry-run returns new count (dedup skips dup, rejects no-id)", n1 == 1, "n1=" + str(n1))
        # Re-run dry-run must be idempotent (nothing written between runs).
        n2 = ku.append_to_brain(entries, dry_run=True, path=brain)
        check("dry-run idempotent", n2 == 1, "n2=" + str(n2))
        # Real append.
        n3 = ku.append_to_brain(entries, dry_run=False, path=brain)
        check("append writes exactly one new entry", n3 == 1, "n3=" + str(n3))
        content = brain.read_text(encoding="utf-8")
        check("appended entry present in file", "New Paper B" in content)
        # Append again: now Paper B is deduped.
        n4 = ku.append_to_brain(entries, dry_run=False, path=brain)
        check("second append dedups already-written", n4 == 0, "n4=" + str(n4))


def test_config_integrity():
    cfg = ku.KNOWLEDGE_CONFIG
    check("config has domain", bool(cfg.get("domain")))
    check("config has arxiv categories", bool(cfg.get("arxiv_categories")))
    check("config has RSS feeds", bool(cfg.get("rss_feeds")))
    check("config scoring weights sum ~1.0", abs(sum(cfg["scoring_weights"].values()) - 1.0) < 1e-6)
    check("config keywords non-empty", len(cfg.get("keywords", [])) >= 3)


def main():
    test_hash_deterministic()
    test_extract_identifier()
    test_score_bounds()
    test_format_entry()
    test_append_dry_run_idempotent()
    test_config_integrity()
    if _failures:
        print("\n" + str(len(_failures)) + " test(s) FAILED: " + ", ".join(_failures))
        sys.exit(1)
    print("\nall knowledge_updater tests passed")


if __name__ == "__main__":
    main()