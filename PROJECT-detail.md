# PROJECT-detail.md — Skill 250: base-building-trap-defense-design

## Executive Summary

`base-building-trap-defense-design` is a professional-grade harness for Claude Code targeting the
**Base-Building Game Defense & Trap System Design** domain. It transforms Claude into a domain expert that delivers
structured, evidence-backed outputs by combining real-time data aggregation, recognized domain methods
(defense-in-depth layering, chokepoint funneling, trap-synergy chains, cost-vs-coverage efficiency frontier, PvP
counter-play balance), and academic research into a single orchestrated workflow ending in a risk/limitation-disclosed
recommendation.

---

## Problem Statement

Practitioners in this domain face three structural gaps:
1. **Data fragmentation**: authoritative data scattered across wikis, patch notes, and datamine sheets.
2. **Methodology gaps**: most advice lacks systematic, evidence-graded methods (layering, cost-efficiency, counter-play).
3. **No self-improvement**: static tools don't learn from new research or balance patches.

This skill addresses all three via real-time aggregation, professional frameworks, and a continuously-updated knowledge
crawl pipeline.

---

## Target Users & Use Cases

| User | Trigger Example | Skill Response |
|------|----------------|----------------|
| Practitioner | "Analyze my Rust base defense against offline raids" | Full evidenced report with L0-L5 layers, metrics, counter-play |
| Researcher | "What methods apply to trap-synergy balance?" | Method-grounded guidance with citations |
| Decision-maker | "Assess raidability of this base layout" | Risk-disclosed assessment with best/base/worst scenarios |
| Learner | "Explain defense-in-depth in this domain" | Educational framing with evidence |

---

## Harness Architecture

```
USER INPUT
    |
    v
[main.md — base-building-trap-defense-design]
    |  (typed Context Envelope flows between every step)
    +--> sub-gather-requirements.md  -> normalized object/game/mode/threats/resources
    +--> sub-evidence-collector.md   -> live trap/structure stats + patch notes (degradation level set)
    +--> sub-core-analysis.md        -> L0-L5 layers, chokepoints, trap logic, cost/coverage, counter-play, metrics
    +--> sub-knowledge-updater.md    -> Tier-labeled citations + crawl-gap flags
    +--> sub-advisor.md              -> risk-disclosed verdict + evidence chain + remediation

    \--> [QUALITY GATE — main.md]
            U1 >=3 sources cited (>=1 academic)
            U2 disclosure before recommendation
            U3 evidence hierarchy (Tier 1-4) per source
            U4 language matches user preference
            U5 declared template (all sections)
            U6 every claim traceable to a source or flagged
            G1 layered defense & chokepoints (>=3 layers, >=1 chokepoint)
            G2 trap synergy/trigger logic specified
            G3 cost-vs-coverage balanced (frontier + coverage %)
            G4 counter-play (PvP) evaluated (matrix + net balance)
```

---

## Context Management (Robust Inter-Step Handoff)

The harness uses a single typed **Context Envelope** (JSON) that flows step-to-step. Each sub-skill reads its inputs
from the envelope, writes its outputs back, and never relies on conversational memory alone. This guarantees
traceability and prevents context loss in long sessions. The envelope carries: `schema_version`, `lang`,
`degradation_level`, `flags[]`, `steps.{requirements,evidence,analysis,knowledge,advice}`, `gate_results`, and
`retries`. See `skills/main.md` → Context Management for the full schema and integrity rules.

---

## Full Sub-Skill Catalog

### 1. `sub-gather-requirements.md`
- **Purpose:** Clarify/normalize the object, game, game-mode, threat types, resource budget, constraints, timeframe, available inputs, target audience, and language before any data fetching.
- **Role:** intake specialist.
- **Inputs:** Raw user message + any provided materials/inputs.
- **Outputs:** Structured requirements written into `steps.requirements`.
- **Tools:** Conversation only.
- **Quality Gate:** At least one object + canonical game confirmed; every defaulted field carries an explicit assumption.

### 2. `sub-evidence-collector.md`
- **Purpose:** Fetch authoritative real-time and reference data: current trap/structure stats, authoritative game wikis/patch notes, and recent balance changes/meta developments.
- **Role:** data librarian; sets degradation level.
- **Inputs:** `steps.requirements`.
- **Outputs:** Evidence bundle (current_data, authoritative_docs, recent_news, reference_benchmarks, sources) written into `steps.evidence`.
- **Tools:** WebSearch, WebFetch, Read (SECOND-KNOWLEDGE-BRAIN.md).
- **Quality Gate:** At least current data + 1 authoritative document retrieved, or an explicit limitation flag.

### 3. `sub-core-analysis.md`
- **Purpose:** Design layered defense (L0-L5), chokepoints, trap synergy/trigger logic, cost-vs-coverage frontier, PvP counter-play, and metrics.
- **Role:** base-defense & trap-system designer.
- **Inputs:** `steps.requirements` + `steps.evidence`.
- **Outputs:** Layers, chokepoints, trap_logic, cost_coverage, counter_play, scenarios, metrics (TTK/EHP/DPE/coverage/raid_cost) into `steps.analysis`.
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN.md), WebFetch (if a stat is missing), reasoning/layout.
- **Quality Gate:** Layers (>=3) + chokepoints (>=1) + trap logic + cost/coverage frontier + counter-play matrix + metrics.

### 4. `sub-knowledge-updater.md`
- **Purpose:** Query SECOND-KNOWLEDGE-BRAIN.md; surface Tier-labeled citations; flag crawl gaps.
- **Role:** research librarian.
- **Inputs:** Topic keywords from `steps.analysis`.
- **Outputs:** 3-5 citations with Tier labels + flagged gaps + coverage rating into `steps.knowledge`.
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN.md), WebSearch (gap-fill, max 2).
- **Quality Gate:** At least 1 academic/authoritative source surfaced; coverage rating provided.

### 5. `sub-advisor.md`
- **Purpose:** Synthesize a risk-disclosed conclusion with a full evidence chain and recommended actions.
- **Role:** senior advisor.
- **Inputs:** `steps.analysis` + `steps.evidence` + `steps.knowledge`.
- **Outputs:** Verdict (exactly one of the declared categories) + scenarios + key risks + evidence chain + remediation + disclosure into `steps.advice`.
- **Tools:** Reasoning/synthesis; optional sub-knowledge-updater.
- **Quality Gate:** Verdict is one of Strong Defense / Conditional (weak flank) / Easily Raidable / Inconclusive; disclosure appears before the conclusion.

---

## Skill File Format Specification

```markdown
---
name: {skill-name}
description: {one-line summary}
---
## Role & Persona
## Workflow (Harness Flow)
## Sub-skills Available   (main.md only)
## Tools
## Output Format
## Quality Gates
```

---

## E2E Execution Flow

```
1. User invokes /base-building-trap-defense-design [query]
2. Pre-Flight language detection -> LANG
3. main.md -> sub-gather-requirements -> structured requirements
4. sub-evidence-collector -> data bundle (+ degradation level)
5. sub-core-analysis -> layers/chokepoints/trap logic/cost/coverage/counter-play/metrics
6. sub-knowledge-updater -> academic evidence entries
7. sub-advisor -> final draft (disclosure before verdict)
8. main.md Quality Gate -> verify U1-U6 + G1-G4, auto-fix, deliver
```

**Error handling:** primary sources fail -> fallback chain -> knowledge base -> explicit limitation flag; never
silently proceed with stale data. Degradation Levels 0-4 with explicit LIMITATION banners.

---

## SECOND-KNOWLEDGE-BRAIN Integration

- **Sources crawled:** ArXiv (cs.AI, cs.HC) + Semantic Scholar + ArXiv RSS feeds
- **Crawl config:** `KNOWLEDGE_CONFIG` in `tools/knowledge_updater.py`
- **Dedup:** SHA256 of DOI/URL/ISBN (case/whitespace-insensitive)
- **Scoring:** composite 0-10 = recency(0.4) + keyword_relevance(0.4) + citation_count(0.2)
- **Gap-fill:** sub-knowledge-updater flags missing coverage as crawl queries

---

## Quality Gates Definition

Universal gates U1-U6 plus the domain gates G1, G2, G3, G4 (defined in `skills/main.md`).

---

## Test Scenarios

See `tests/test-scenarios.md` for 5 concrete scenario tests covering all gates and all verdict categories.

---

## Key Design Decisions

1. Domain sub-skills kept separate (distinct methods/data).
2. Authoritative domain sources as primary; global fallback secondary.
3. Disclosure enforced at the quality-gate level, not optional.
4. SECOND-KNOWLEDGE-BRAIN as living memory updated by crawl pipeline.
5. Typed Context Envelope between steps prevents context loss (robust context management).
6. Graceful degradation with explicit LIMITATION banners; no fabricated values.
7. Defense-in-depth layering outranks single concentrated layers when conflicts arise; cost-efficiency breaks ties.

---

## Idea (Vietnamese)

> Tạo skill phân tích và thiết kế hệ thống bẫy, cơ chế phòng thủ trong các tựa game xây dựng căn cứ (Base Building/Tower Defense),
> việc đánh giá và đưa đề xuất phải dựa trên các phương pháp đánh giá uy tín trên thế giới và đưa ra các đề xuất, giải pháp cải tiến,
> không ngừng đi crawl data từ các sơ đồ phòng thủ tối ưu của cộng đồng hoặc document uy tín liên quan để cập nhật kiến thức cho skill
> ngày càng tốt hơn, xu hướng hơn.