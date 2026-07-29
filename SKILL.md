---
name: base-building-trap-defense-design
description: Trap & Defense System Design for Base-Building Games — evidence-backed analysis harness with layered defense (L0-L5), trap-synergy chains, cost-coverage efficiency frontier, and PvP counter-play reasoning. Trigger on: base defense, trap systems, raid protection, chokepoint design, funneling, base layout analysis, PvP defense, fortification, raidability assessment, game defense optimization.
version: 2.1.0
---

# SKILL REGISTRY — base-building-trap-defense-design

## Skill Registration

### Primary Skill
- **Name:** `base-building-trap-defense-design`
- **Version:** 2.1.0
- **Type:** Domain Analysis Harness
- **Domain:** Base-Building Game Defense & Trap System Design
- **Trigger Phrases:** "base defense", "trap system", "raid protection", "chokepoint", "funneling", "base layout", "PvP defense", "fortification", "raidability", "defense design"
- **Entry Point:** `skills/main.md`

### Sub-Skills

| Sub-Skill | Version | Type | Entry Point |
|-----------|---------|------|-------------|
| `sub-gather-requirements` | 2.1.0 | Intake Specialist | `skills/sub-gather-requirements.md` |
| `sub-evidence-collector` | 2.1.0 | Data Librarian | `skills/sub-evidence-collector.md` |
| `sub-core-analysis` | 2.1.0 | Defense Analyst | `skills/sub-core-analysis.md` |
| `sub-knowledge-updater` | 2.1.0 | Research Librarian | `skills/sub-knowledge-updater.md` |
| `sub-advisor` | 2.1.0 | Senior Advisor | `skills/sub-advisor.md` |

---

## Execution Protocols

### Main Harness Flow

```
USER INPUT
    │
    ├─> [PRE-FLIGHT] Language Detection
    │   └─> Set LANG (vi|en)
    │
    ├─> [HOOK] lifecycle-pre-exec
    │   ├─> Environment validation
    │   ├─> Context envelope validation
    │   └─> Prerequisite check
    │
    ├─> [STEP 1] sub-gather-requirements
    │   ├─> Input: Raw user message
    │   ├─> Output: Structured requirements → envelope.steps.requirements
    │   └─> Gate: Object + game confirmed
    │
    ├─> [HOOK] state-sync
    │   └─> Validate envelope state transition
    │
    ├─> [STEP 2] sub-evidence-collector
    │   ├─> Input: envelope.steps.requirements
    │   ├─> Output: Evidence bundle → envelope.steps.evidence
    │   ├─> Sets: degradation_level
    │   └─> Gate: Current data + 1 authoritative doc
    │
    ├─> [HOOK] state-sync
    │   └─> Validate envelope state transition
    │
    ├─> [HOOK] token-optimize (if budget exceeded)
    │   └─> Prune context by tier and recency
    │
    ├─> [STEP 3] sub-core-analysis
    │   ├─> Input: envelope.steps.{requirements, evidence}
    │   ├─> Output: Layers, chokepoints, trap logic, cost/coverage, counter-play → envelope.steps.analysis
    │   └─> Gate: Layers (≥3) + chokepoints (≥1) + trap logic + cost/coverage + counter-play
    │
    ├─> [HOOK] state-sync
    │   └─> Validate envelope state transition
    │
    ├─> [STEP 4] sub-knowledge-updater
    │   ├─> Input: envelope.steps.analysis
    │   ├─> Output: Citations + gaps + coverage → envelope.steps.knowledge
    │   └─> Gate: ≥1 academic source + coverage rating
    │
    ├─> [HOOK] state-sync
    │   └─> Validate envelope state transition
    │
    ├─> [STEP 5] sub-advisor
    │   ├─> Input: envelope.steps.{analysis, evidence, knowledge}
    │   ├─> Output: Verdict + scenarios + risks + evidence chain + remediation → envelope.steps.advice
    │   └─> Gate: Verdict is valid category + disclosure before conclusion
    │
    ├─> [HOOK] state-sync
    │   └─> Validate envelope state transition
    │
    ├─> [QUALITY GATE] Main Harness
    │   ├─> Verify U1-U6 + G1-G4
    │   ├─> Auto-fix where possible
    │   └─> Record gate_results
    │
    ├─> [HOOK] lifecycle-post-exec
    │   ├─> Result finalization
    │   ├─> Performance logging
    │   ├─> Context envelope freeze
    │   └─> Resource cleanup
    │
    └─> OUTPUT DELIVERY
        └─> Final report with disclosure
```

### Hook Execution Points

| Hook | Execution Point | Purpose |
|------|-----------------|---------|
| lifecycle-pre-exec | Before Step 1 | Environment and envelope validation |
| state-sync | After every step | Envelope integrity verification |
| token-optimize | Before Step 3 (conditional) | Context pruning if budget exceeded |
| lifecycle-post-exec | After Quality Gate | Finalization and cleanup |
| event-emit | On every significant event | Monitoring and observability |
| error-classify | On any error | Error categorization |
| error-recover | After classification | Recovery execution |

---

## Input/Output Schemas

### Context Envelope Schema (v1.0)

```json
{
  "type": "object",
  "required": ["schema_version", "session_id", "lang", "degradation_level", "steps", "gate_results"],
  "properties": {
    "schema_version": {"type": "string", "enum": ["1.0"]},
    "session_id": {"type": "string", "format": "uuid"},
    "lang": {"type": "string", "enum": ["vi", "en"]},
    "degradation_level": {"type": "integer", "minimum": 0, "maximum": 4},
    "flags": {"type": "array", "items": {"type": "string"}},
    "steps": {
      "type": "object",
      "properties": {
        "requirements": {
          "type": "object",
          "properties": {
            "object": {"type": "string"},
            "scope": {"type": "string"},
            "timeframe": {"type": "string"},
            "available_inputs": {"type": "array"},
            "target_audience": {"type": "string"},
            "language": {"type": "string"},
            "analysis_type": {"type": "string"},
            "game": {"type": "string"},
            "game_mode": {"type": "string", "enum": ["pvp", "pve", "hybrid"]},
            "threat_types": {"type": "array"},
            "resources_budget": {"type": ["object", "null"]},
            "status": {"type": "string", "enum": ["pending", "complete", "blocked"]}
          }
        },
        "evidence": {
          "type": "object",
          "properties": {
            "current_data": {"type": "array"},
            "authoritative_docs": {"type": "array"},
            "recent_news": {"type": "array"},
            "reference_benchmarks": {"type": "array"},
            "sources": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {"type": "string"},
                  "label": {"type": "string"},
                  "url": {"type": "string", "format": "uri"},
                  "date": {"type": "string", "format": "date"},
                  "tier": {"type": "integer", "minimum": 1, "maximum": 4},
                  "accessed": {"type": "string", "format": "date-time"}
                }
              }
            },
            "status": {"type": "string", "enum": ["pending", "complete", "degraded"]}
          }
        },
        "analysis": {
          "type": "object",
          "properties": {
            "layers": {"type": "array"},
            "chokepoints": {"type": "array"},
            "trap_logic": {"type": "array"},
            "cost_coverage": {"type": "object"},
            "counter_play": {"type": "object"},
            "scenarios": {
              "type": "object",
              "properties": {
                "best": {"type": "object"},
                "base": {"type": "object"},
                "worst": {"type": "object"}
              }
            },
            "metrics": {
              "type": "object",
              "properties": {
                "ttk": {"type": "number"},
                "ehp": {"type": "number"},
                "dpe": {"type": "number"},
                "coverage": {"type": "number"},
                "raid_cost": {"type": "number"}
              }
            },
            "status": {"type": "string", "enum": ["pending", "complete"]}
          }
        },
        "knowledge": {
          "type": "object",
          "properties": {
            "citations": {"type": "array"},
            "gaps": {"type": "array"},
            "coverage_rating": {"type": "string", "enum": ["Strong", "Moderate", "Weak"]},
            "status": {"type": "string", "enum": ["pending", "complete"]}
          }
        },
        "advice": {
          "type": "object",
          "properties": {
            "verdict": {"type": "string", "enum": ["Strong Defense", "Conditional", "Easily Raidable", "Inconclusive"]},
            "scenarios": {"type": "object"},
            "key_risks": {"type": "array"},
            "evidence_chain": {"type": "array"},
            "remediation": {"type": "array"},
            "disclosure": {"type": "string"},
            "status": {"type": "string", "enum": ["pending", "complete"]}
          }
        }
      }
    },
    "gate_results": {
      "type": "object",
      "properties": {
        "U1": {"type": ["boolean", "null"]},
        "U2": {"type": ["boolean", "null"]},
        "U3": {"type": ["boolean", "null"]},
        "U4": {"type": ["boolean", "null"]},
        "U5": {"type": ["boolean", "null"]},
        "U6": {"type": ["boolean", "null"]},
        "G1": {"type": ["boolean", "null"]},
        "G2": {"type": ["boolean", "null"]},
        "G3": {"type": ["boolean", "null"]},
        "G4": {"type": ["boolean", "null"]}
      }
    },
    "retries": {"type": "object"},
    "performance": {
      "type": "object",
      "properties": {
        "start_time": {"type": "string", "format": "date-time"},
        "end_time": {"type": "string", "format": "date-time"},
        "total_duration_ms": {"type": "integer"},
        "total_tokens": {"type": "integer"},
        "steps": {"type": "array"},
        "token_budget": {"type": "object"}
      }
    }
  }
}
```

### Quality Gates Schema

```json
{
  "type": "object",
  "properties": {
    "gate_id": {"type": "string"},
    "gate_name": {"type": "string"},
    "check": {"type": "string"},
    "auto_fix": {"type": "string"},
    "enforcement_logic": {"type": "string"},
    "result": {"type": "boolean"},
    "retry_attempt": {"type": "integer"},
    "max_retries": {"type": "integer"}
  }
}
```

---

## Quality Gates

### Universal Gates (U1-U6)

| Gate | Check | Auto-Fix | Enforcement |
|------|-------|----------|-------------|
| U1 | ≥3 sources cited, ≥1 academic/authoritative | Fetch from KB/evidence | Append before delivery |
| U2 | Disclosure/limitations before recommendation | Prepend disclosure | Block until present |
| U3 | Evidence hierarchy (Tier 1-4) per source | Tag tiers | Label each source |
| U4 | Language matches user preference | Translate output | Detect in pre-flight |
| U5 | Output uses declared template | Reformat | Check sections |
| U6 | Every claim traceable to source or flagged | Flag unsupported | Link claim to source |

### Domain Gates (G1-G4)

| Gate | Check | Auto-Fix | Enforcement |
|------|-------|----------|-------------|
| G1 | Layered defense & chokepoints (≥3 layers, ≥1 chokepoint) | Design layers | Append missing |
| G2 | Trap synergy/trigger logic specified | Specify logic | Append block |
| G3 | Cost-vs-coverage balanced (cost table + coverage %) | Balance | Append table |
| G4 | Counter-play (PvP) evaluated (raid tools + weak spots) | Evaluate | Append matrix |

---

## Dependencies

### Internal Dependencies

```
main.md
├── sub-gather-requirements (no dependencies)
├── sub-evidence-collector → requires: sub-gather-requirements
├── sub-core-analysis → requires: sub-gather-requirements, sub-evidence-collector
├── sub-knowledge-updater → requires: sub-core-analysis
└── sub-advisor → requires: sub-evidence-collector, sub-core-analysis, sub-knowledge-updater
```

### External Dependencies

**Required Tools:**
- WebSearch (MCP server)
- WebFetch (MCP server)
- Read (file system)
- Write (file system)
- Bash (shell commands)
- Skill (sub-skill invocation)

**Required Files:**
- `SECOND-KNOWLEDGE-BRAIN.md` (knowledge base)
- `config/default.json` (configuration)
- `hooks/**/*.md` (hook definitions)

**Optional Files:**
- `config/production.json` (production overrides)
- `.env` (environment variables)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-07-27 | Added hooks system, token optimization, structured logging, configuration management |
| 2.0.0 | 2026-07-13 | Production release with all 6 phases complete |
| 1.0.0 | 2026-07-10 | Initial release with basic harness |

---

## Compatibility Matrix

| Component | Version | Compatible With |
|-----------|---------|-----------------|
| main.md | 2.1.0 | sub-skills 2.1.0, hooks 2.1.0 |
| sub-gather-requirements | 2.1.0 | main.md 2.1.0 |
| sub-evidence-collector | 2.1.0 | main.md 2.1.0 |
| sub-core-analysis | 2.1.0 | main.md 2.1.0 |
| sub-knowledge-updater | 2.1.0 | main.md 2.1.0 |
| sub-advisor | 2.1.0 | main.md 2.1.0 |
| hooks/* | 2.1.0 | main.md 2.1.0 |
| config/* | 2.1.0 | main.md 2.1.0 |

---

## Configuration

Configuration is loaded from:
1. `config/default.json` (base configuration)
2. `config/production.json` (production overrides, if environment=production)
3. Environment variables (override file settings)

**Priority:** Environment variables > production.json > default.json

---

## Monitoring & Observability

### Event Streams
- `logs/events-<session_id>.jsonl` — All events during execution
- `logs/performance-<session_id>.json` — Token consumption and timing
- `logs/envelopes/<session_id>.json` — Context envelope snapshots

### Metrics
- Total tokens per session
- Duration per step
- Cache hit rate
- Degradation level changes
- Quality gate pass/fail rates

### Alerts
- Degradation level ≥2 (WARN)
- Critical gate failure (ERROR)
- All sources unavailable (CRITICAL)
- Context envelope corrupted (CRITICAL)
