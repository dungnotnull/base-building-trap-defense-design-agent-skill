# base-building-trap-defense-design

**Trap & Defense System Design for Base-Building Games**

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production--ready-success)](PROJECT-DEVELOPMENT-PHASE-TRACKING.md)

A professional-grade Claude Code harness for **Base-Building Game Defense & Trap System Design** — gathers real-time
authoritative data, applies recognized domain methods (defense-in-depth layering, chokepoint funneling,
trap-synergy chains, cost-vs-coverage efficiency frontier, PvP counter-play balance), integrates academic
research, and delivers evidence-backed, risk-disclosed outputs.

## Features
- **Defense-in-depth layering** — L0–L5 model (outer detection → perimeter → funneling chokepoints → kill-zones → inner keep → TC core).
- **Trap synergy & trigger logic** — CC → damage → finish chains, AoE stacking, trigger-to-exit timing.
- **Cost-vs-coverage efficiency frontier** — coverage %, efficiency ranking, redundancy rule.
- **PvP counter-play balance** — sulfur ratio, net balance, single-point-failure analysis, online vs offline.
- **Robust context management** — typed Context Envelope flows step-to-step so no evidence/metric is lost.
- **Production-grade error handling** — graceful degradation Levels 0–4, bounded retries, fail-loud flags, no fabrication.
- **Self-improving knowledge pipeline** — weekly academic + daily news crawl (ArXiv, Semantic Scholar, RSS) with SHA256 dedup.
- **Bilingual** — Vietnamese / English output with pre-flight language detection.

## Installation
```bash
pip install -r requirements.txt
```
Install the skill files to `~/.claude/skills/` or use them via the project `CLAUDE.md`.

## Usage
```bash
/base-building-trap-defense-design [your query]
```

## Architecture
Harness flow: requirements → evidence → core analysis → knowledge → synthesis → quality gate.
Context is passed via a typed **Context Envelope** (JSON) between steps. See `PROJECT-detail.md` for the full
architecture and `skills/main.md` for the execution protocol.

## Quality Gates
Universal gates U1–U6 plus domain gates G1–G4, all defined in `skills/main.md` with auto-fix logic.

## Data Sources
- Official patch notes per game (Rust, 7DTD, Fortnite STW, ARK, Valheim, Conan, Palworld)
- Official & community stat wikis (e.g., Rust Labs, 7DTD wiki)
- Academic: CHI PLAY, IEEE Trans. Games, Entertainment Computing, Computers in Human Behavior, Simulation & Gaming

## Testing
```bash
python tools/test_knowledge_updater.py   # unit tests (no network)
python tools/run_test_scenarios.py       # structural & content validator
python tools/validate_project.py         # 8-File Contract validator
python tools/knowledge_updater.py --dry-run   # crawl preview (network-optional)
```

## Knowledge Base
`SECOND-KNOWLEDGE-BRAIN.md` is auto-updated weekly via `tools/knowledge_updater.py`.

## Roadmap
- [x] Phase 0: Architecture & source map
- [x] Phase 1: Core sub-skills (5) with real domain methodology
- [x] Phase 2: Main harness + Context Envelope + quality gates + degradation
- [x] Phase 3: Knowledge pipeline (ArXiv + Semantic Scholar + RSS) + tests + cron
- [x] Phase 4: Testing & validation
- [x] Phase 5: Integration & polish — PRODUCTION READY v2.0.0

## License
MIT — see [LICENSE](LICENSE).

## Citation
```bibtex
@software{base-building-trap-defense-design,
  title  = {base-building-trap-defense-design: Trap & Defense System Design for Base-Building Games},
  year   = {2026},
  version= {2.0.0}
}
```

## Why This Skill

Base-Building Game Defense & Trap System Design practitioners face fragmented data, inconsistent methodology, and tools
that do not self-improve. This skill unifies authoritative real-time data, recognized domain methods, and a
continuously-updated academic knowledge base into one evidence-backed, risk-disclosed workflow.