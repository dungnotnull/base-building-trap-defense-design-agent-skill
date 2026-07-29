# CLAUDE.md — Skill 250: base-building-trap-defense-design

## Skill Identity
- **Skill Name:** `base-building-trap-defense-design`
- **Tagline:** Trap & Defense System Design for Base-Building Games — Base-Building Game Defense & Trap System Design analysis & decision-support harness.
- **Current Phase:** Production Ready Enhanced (Phase 0–5 complete + Enhancement Phase complete)
- **Version:** 2.1.0
- **Folder:** `D:\972026\250-base-building-trap-defense-design\`

---

## Problem This Skill Solves

This skill provides a structured, evidence-backed analytical workflow for
**Base-Building Game Defense & Trap System Design**. It gathers authoritative
real-time and reference data, applies recognized domain methods (defense-in-
depth layering, chokepoint funneling, trap-synergy chains, cost-vs-coverage
efficiency frontier, PvP counter-play balance), cross-references academic
research, and delivers actionable outputs that are fully evidenced,
risk/limitation-disclosed, and traceable to authoritative sources —
continuously self-improving through an automated knowledge crawl pipeline.

---

## Harness Flow Summary

```
/base-building-trap-defense-design invoked
|
+-- Pre-Flight: language detection (vi/en)
+-- Step 1: sub-gather-requirements   -> normalize object/game/mode/threats/resources
+-- Step 2: sub-evidence-collector    -> fetch live trap/structure stats + patch notes
+-- Step 3: sub-core-analysis         -> L0-L5 layers, chokepoints, trap logic, cost/coverage, counter-play, metrics
+-- Step 4: sub-knowledge-updater     -> Tier-labeled citations + crawl-gap flags
+-- Step 5: sub-advisor               -> risk-disclosed verdict + evidence chain + remediation
\-- Step 6: main (quality gate)       -> verify U1-U6 + G1-G4, auto-fix, deliver
```

Context is passed between steps via a typed **Context Envelope** (see
`skills/main.md` → Context Management) so no evidence, metric, or constraint
is lost across the pipeline.

---

## Sub-Skills

| `skills/sub-gather-requirements.md` | Clarify/normalize object, game, game-mode, threats, resources, timeframe, audience, language before any data fetching. |
| `skills/sub-evidence-collector.md` | Fetch authoritative real-time and reference data: trap/structure stats, wikis, patch notes, recent meta; sets degradation level. |
| `skills/sub-core-analysis.md` | Design layered defense (L0-L5), chokepoints, trap synergy/trigger logic, cost-vs-coverage frontier, PvP counter-play, metrics. |
| `skills/sub-knowledge-updater.md` | Query SECOND-KNOWLEDGE-BRAIN.md; surface Tier-labeled citations; flag crawl gaps. |
| `skills/sub-advisor.md` | Synthesize a risk-disclosed verdict (Strong Defense / Conditional / Easily Raidable / Inconclusive) with evidence chain and remediation. |

---

## Tools Required

- **WebSearch** — live domain news, reports, patch notes
- **WebFetch** — scrape Base-Building Game Defense & Trap System Design authoritative sources
- **Read / Write** — read SECOND-KNOWLEDGE-BRAIN.md; append knowledge entries
- **Bash** — run `tools/knowledge_updater.py` for periodic crawl
- **Skill** — invoke sub-skills sequentially through the harness

---

## Knowledge Sources

### Domain Authoritative Sources
- Official patch notes per game (Rust, 7DTD, Fortnite STW, ARK, Valheim, Conan, Palworld)
- Official game wikis (e.g., Facepunch wiki)
- Community stat wikis (e.g., Rust Labs, 7DTD wiki)
- Datamined stat sheets

### Academic & Research Sources
- Proceedings of CHI PLAY (ACM)
- IEEE Transactions on Games
- Entertainment Computing (Elsevier)
- Computers in Human Behavior (Elsevier)
- Simulation & Gaming (SAGE)
- Journal of Game Design & Development Education

### Academic Crawl Targets
- ArXiv categories `cs.AI`, `cs.HC`
- Semantic Scholar keyword clusters (see `KNOWLEDGE_CONFIG` in `tools/knowledge_updater.py`)
- ArXiv RSS feeds: `http://export.arxiv.org/rss/cs.AI`, `http://export.arxiv.org/rss/cs.HC`

---

## Supporting Python Tools

| File | Purpose |
|------|---------|
| `tools/knowledge_updater.py` | Crawl pipeline: ArXiv + Semantic Scholar + RSS -> SHA256 dedup -> composite score -> append to SECOND-KNOWLEDGE-BRAIN.md Section 7 |
| `tools/test_knowledge_updater.py` | Unit tests: hash, identifier extraction, scoring, format, append idempotency, config |
| `tools/run_test_scenarios.py` | Structural & content validator for the skill bundle |
| `tools/validate_project.py` | 8-File Contract validator + metadata consistency |
| `scripts/setup/initialize.sh` | Environment initialization and directory setup |
| `scripts/setup/validate_environment.py` | Runtime environment validation |
| `scripts/maintenance/cleanup.sh` | Log rotation, temp cleanup, backup management |

---

## Modular Directory Structure (v2.1.0)

```
250-base-building-trap-defense-design/
├── assets/                    # Static resources and schemas
│   ├── diagrams/             # System architecture diagrams
│   ├── schemas/              # JSON schemas for validation
│   └── templates/            # Output format templates
├── config/                   # Type-safe configuration management
│   ├── default.json         # Default configuration
│   ├── production.json      # Production overrides
│   └── schema.json          # Configuration schema
├── hooks/                    # Lifecycle and state management hooks
│   ├── lifecycle/           # Pre-exec and post-exec hooks
│   ├── state/               # Context envelope synchronization
│   ├── event/               # Event emission and subscription
│   ├── token/               # Token tracking and optimization
│   └── error/               # Error classification and recovery
├── references/               # Domain knowledge and prompt templates
│   ├── domain/              # Base-building game defense concepts
│   ├── frameworks/          # Analytical frameworks (L0-L5, metrics)
│   └── prompts/             # Base prompt templates for sub-skills
└── scripts/                  # Automation and setup routines
    ├── setup/               # Installation and initialization
    ├── database/            # Data seeding and migration (future)
    ├── ingestion/           # Data ingestion from external sources (future)
    └── maintenance/         # Cleanup and optimization
```

---

## Automated Knowledge Update Schedule

```cron
# Weekly academic update (Mondays 8:00 AM)
0 8 * * 1 python D:/972026/250-base-building-trap-defense-design/tools/knowledge_updater.py >> logs/knowledge_update.log 2>&1

# Daily news update (Daily 7:00 AM)
0 7 * * * python D:/972026/250-base-building-trap-defense-design/tools/knowledge_updater.py --news-only >> logs/knowledge_news.log 2>&1
```

Manual:
```bash
python tools/knowledge_updater.py --dry-run          # preview, no write
python tools/knowledge_updater.py --news-only          # RSS only
python tools/knowledge_updater.py --keywords "a" "b"   # override cluster
python tools/knowledge_updater.py --json-logs          # structured logs
python tools/knowledge_updater.py --config config.json # external config
```

---

## Active Development Tasks

- [x] Phase 0: Architecture & source map (CLAUDE.md, PROJECT-detail.md, PDPT)
- [x] Phase 1: Core sub-skills (production-grade, real domain methodology)
- [x] Phase 2: Main harness + Context Envelope + quality gates + degradation
- [x] Phase 3: Knowledge pipeline (ArXiv + Semantic Scholar + RSS) + tests + cron
- [x] Phase 4: Testing & validation (all validators pass)
- [x] Phase 5: Integration & polish (PRODUCTION READY v2.0.0)
- [x] Enhancement Phase: Flexible architecture & production standards (v2.1.0)

---

## References

- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — build roadmap (all phases 100%)
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
- `D:\972026\SKILL-STANDARD.md` — library-wide standard