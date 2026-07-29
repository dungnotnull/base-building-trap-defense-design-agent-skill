# Architectural Enhancement Plan — base-building-trap-defense-design

## Executive Summary

This document outlines the architectural enhancements to upgrade the `base-building-trap-defense-design` skill from production-ready (v2.0.0) to **bulletproof, production-grade, open-source standard** with flexible agent/skill architecture, specialized system elements, and real-world best practices.

---

## Current State Assessment

### Strengths (Already in Place)
- ✅ Complete 8-File Contract (CLAUDE.md, PROJECT-detail.md, PDPT, README.md, skills/*.md, SECOND-KNOWLEDGE-BRAIN.md, tools/)
- ✅ 6-phase development completed (100%)
- ✅ 5 sub-skills with quality gates (U1-U6 + G1-G4)
- ✅ Context Envelope for robust inter-step handoff
- ✅ Graceful degradation (levels 0-4)
- ✅ Knowledge crawl pipeline (ArXiv + Semantic Scholar + RSS)
- ✅ Test scenarios and validators

### Gaps to Address
- ❌ No modular directories (/scripts, /references, /assets, /config)
- ❌ No SKILL.md skill registry documentation
- ❌ No hooks system for lifecycle/state/events
- ❌ No rich tool definitions with schemas
- ❌ No production-grade logging
- ❌ No configuration management system
- ❌ No context window optimization
- ❌ No token consumption tracking
- ❌ Sub-skills are static (no dynamic routing/chain-of-thought)

---

## Architectural Enhancements

### 1. Flexible Agent & Skill Architecture

#### Current Architecture
```
main.md → [sub-gather-requirements → sub-evidence-collector → sub-core-analysis → sub-knowledge-updater → sub-advisor] → Quality Gate
```
Linear execution; all sub-skills invoked in order.

#### Enhanced Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                            │
│  (route, chain-of-thought, parallel execution, retry logic)      │
└────────────┬────────────────────────────────────┬───────────────┘
             │                                    │
    ┌────────▼────────┐                   ┌──────▼──────┐
    │  Skill Registry │                   │ Hook System │
    │  (SKILL.md)      │                   │ (lifecycle) │
    └─────────────────┘                   └─────────────┘
             │
    ┌────────▼──────────────────────────────────────────┐
    │            Sub-Skills (Dynamic Routing)            │
    ├─────────────┬──────────────┬──────────────┬────────┤
    │ Requirements│  Evidence    │   Core       │Knowledge│
    │   Agent     │   Collector  │  Analyst    │ Updater │
    └─────────────┴──────────────┴──────────────┴────────┘
             │
    ┌────────▼──────────────────────────────────────────┐
    │              Context Envelope (v2.0)                │
    │  + Token tracking, optimization flags, metadata      │
    └─────────────────────────────────────────────────────┘
             │
    ┌────────▼──────────────────────────────────────────┐
    │          Tool Definitions (with Schemas)          │
    │  WebSearch, WebFetch, Read, Write, Bash, Skill    │
    └────────────────────────────────────────────────────┘
```

#### Implementation Strategy

**1.1 Agent Orchestrator (`skills/agent-orchestrator.md`)**
- Route requests to appropriate sub-skills based on context
- Chain-of-thought reasoning for complex scenarios
- Parallel execution of independent sub-skills
- Intelligent retry with fallback strategies
- Context window optimization (prune outdated data)

**1.2 Skill Registry (`SKILL.md`)**
- Central registry of all skills and sub-skills
- Input/output JSON schemas for each skill
- Trigger conditions and routing logic
- Version tracking and compatibility matrix
- Dependencies between skills

**1.3 Dynamic Sub-Skill Routing**
- Sub-skills can invoke other sub-skills as needed
- Conditional execution based on degradation level
- Early exit patterns when requirements are met
- Caching of expensive operations

---

### 2. Specialized System Elements

#### 2.1 Hooks & Tools

**Hooks System (`hooks/` directory)**

| Hook Type | Purpose | Trigger Points |
|-----------|---------|----------------|
| `lifecycle` | Manage skill lifecycle (init, pre-exec, post-exec, cleanup) | Before/after each step |
| `state` | Synchronize state between agents | Context envelope updates |
| `event` | Emit events for external monitoring | Gate failures, degradation |
| `token` | Track and optimize token usage | Every LLM call |
| `error` | Centralized error handling | Any exception |

**Hook Implementation:**
```yaml
hooks/
├── lifecycle/
│   ├── pre-exec.md      # Before any skill execution
│   └── post-exec.md     # After skill completes
├── state/
│   ├── sync.md          # Synchronize context envelope
│   └── validate.md      # Validate envelope integrity
├── event/
│   ├── emit.md          # Event emission protocol
│   └── subscribe.md     # Event subscription handlers
├── token/
│   ├── track.md         # Token counting per operation
│   └── optimize.md      # Pruning and compression
└── error/
    ├── classify.md      # Error classification system
    └── recover.md       # Recovery strategies
```

**Tool Definitions (with Schemas)**

Define rich tool schemas for type safety and validation:
```json
{
  "tool": "WebSearch",
  "schema": {
    "input": {
      "query": {"type": "string", "min": 3, "max": 500},
      "domain_filter": {"type": "array", "items": {"type": "string"}},
      "recency_filter": {"type": "string", "enum": ["oneDay", "oneWeek", "oneMonth", "noLimit"]}
    },
    "output": {
      "results": {"type": "array", "items": {"title": "string", "url": "string", "summary": "string"}}
    },
    "errors": ["timeout", "no_results", "rate_limited"]
  }
}
```

#### 2.2 Modular Directories

**Directory Structure:**
```
250-base-building-trap-defense-design/
├── assets/
│   ├── diagrams/           # System architecture diagrams
│   │   ├── harness-flow.svg
│   │   ├── context-envelope.svg
│   │   └── degradation-levels.svg
│   ├── schemas/            # JSON schemas for validation
│   │   ├── context-envelope.json
│   │   ├── gates.json
│   │   └── output-template.json
│   └── templates/          # Output format templates
│       ├── report-vi.md
│       └── report-en.md
├── config/
│   ├── default.json        # Default configuration
│   ├── production.json     # Production overrides
│   └── schema.json         # Configuration schema
├── hooks/                  # Lifecycle and state hooks
│   ├── lifecycle/
│   ├── state/
│   ├── event/
│   ├── token/
│   └── error/
├── references/             # Domain knowledge and prompts
│   ├── domain/             # Base-building game defense concepts
│   ├── frameworks/         # Analytical frameworks (L0-L5, metrics)
│   └── prompts/            # Base prompt templates
├── scripts/                # Automation and setup routines
│   ├── setup/              # Installation and initialization
│   ├── database/           # Data seeding and migration
│   ├── ingestion/          # Data ingestion from external sources
│   └── maintenance/        # Cleanup and optimization
└── tools/                  # Existing tools (knowledge_updater, validators)
```

#### 2.3 SKILL.md (Skill Registry)

Comprehensive documentation covering:
- Skill registration and resolution
- Input/output JSON schemas
- Execution protocols
- Validation rules
- Version compatibility
- Dependency management

---

### 3. Execution & Quality Standards

#### 3.1 Context Window Optimization

**Strategies:**
1. **Pruning by Tier**: Lower-tier evidence pruned before higher-tier
2. **Recency Bidding**: Older entries pruned first within same tier
3. **Compression**: Summarize long context blocks while preserving citations
4. **Token Budgeting**: Allocate fixed budgets per step
5. **Checkpointing**: Save intermediate results to disk

**Implementation:**
```yaml
context_management:
  max_tokens: 128000
  budgets:
    requirements: 2000
    evidence: 15000
    analysis: 40000
    knowledge: 8000
    advice: 3000
  pruning:
    strategy: "tier_then_recency"
    preserve_sources: true
    compression_threshold: 0.8  # Prune when 80% full
```

#### 3.2 Token Consumption Tracking

Track tokens at every operation:
```json
{
  "operation": "sub-core-analysis",
  "tokens": {
    "input": 15234,
    "output": 8742,
    "total": 23976,
    "cached": 4521
  },
  "duration_ms": 12345,
  "timestamp": "2026-07-27T10:30:00Z"
}
```

#### 3.3 Production-Grade Error Handling

**Error Classification System:**
```yaml
error_types:
  recoverable:
    - timeout
    - rate_limited
    - temporary_unavailable
  non_recoverable:
    - invalid_input
    - authentication_failed
    - resource_not_found
  critical:
    - knowledge_base_corrupted
    - context_envelope_invalid
    - all_sources_unavailable
```

**Recovery Strategies:**
- Fallback chains with explicit degradation
- Circuit breaker for repeated failures
- Dead letter queue for failed operations
- Structured error logging (see below)

#### 3.4 Structured Logging

**Log Schema:**
```json
{
  "timestamp": "ISO8601",
  "level": "DEBUG|INFO|WARN|ERROR",
  "component": "sub-skill-name",
  "session_id": "uuid",
  "operation": "operation-name",
  "status": "success|failure|partial",
  "data": {},
  "error": {
    "type": "",
    "message": "",
    "stack_trace": "",
    "context": {}
  },
  "performance": {
    "duration_ms": 0,
    "tokens_used": 0
  }
}
```

**Log Rotation & Retention:**
- Daily rotation
- 30-day retention for INFO logs
- 90-day retention for ERROR logs
- Compression for archived logs

---

### 4. No Placeholders Policy

**Implementation Checklist:**
- [ ] All functions have real implementations
- [ ] No TODO comments without ticket numbers
- [ ] No stubbed return values
- [ ] No "implement later" placeholders
- [ ] All error paths have explicit handling
- [ ] All edge cases are documented and handled

**Validation:**
```bash
# Scan for placeholders
grep -r "TODO\|FIXME\|XXX\|HACK\|STUB" --exclude-dir=node_modules scripts/ hooks/ references/

# Scan for empty functions
grep -r "pass$\|# Placeholder" --exclude-dir=node_modules scripts/ hooks/ references/
```

---

### 5. Configuration Management

**Type-Safe Configuration:**
```json
{
  "$schema": "./config/schema.json",
  "version": "2.0.0",
  "environment": "production",
  "context_window": {
    "max_tokens": 128000,
    "pruning_strategy": "tier_then_recency",
    "compression_enabled": true
  },
  "knowledge_sources": {
    "arxiv": {
      "enabled": true,
      "categories": ["cs.AI", "cs.HC"],
      "max_results": 50
    },
    "semantic_scholar": {
      "enabled": true,
      "api_key": "${SEMANTIC_SCHOLAR_API_KEY}",
      "timeout_ms": 30000
    }
  },
  "quality_gates": {
    "enforcement": "strict",
    "max_retries": 2,
    "auto_fix_enabled": true
  },
  "logging": {
    "level": "INFO",
    "structured": true,
    "rotation": "daily"
  }
}
```

**Environment Variable Support:**
```bash
# .env file template
CONTEXT_WINDOW_MAX_TOKENS=128000
SEMANTIC_SCHOLAR_API_KEY=your_key_here
LOG_LEVEL=INFO
DEGRADATION_THRESHOLD=2
```

---

### 6. Documentation Standards

**SKILL.md Structure:**
```markdown
---
name: base-building-trap-defense-design
description: ...
version: 2.1.0
---

## Skill Registration
## Execution Protocols
## Input/Output Schemas
## Quality Gates
## Dependencies
## Version History
```

**README Enhancements:**
- Architecture diagrams (SVG)
- Quick start guide
- Configuration reference
- Troubleshooting guide
- Contributing guidelines

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create modular directories (/scripts, /references, /assets, /config)
- [ ] Implement hooks system (lifecycle, state, event, token, error)
- [ ] Create SKILL.md with full registry
- [ ] Set up configuration management

### Phase 2: Agent Architecture (Week 2)
- [ ] Implement agent orchestrator
- [ ] Add dynamic sub-skill routing
- [ ] Implement context window optimization
- [ ] Add token consumption tracking

### Phase 3: Production Hardening (Week 3)
- [ ] Implement structured logging
- [ ] Add error classification and recovery
- [ ] Implement circuit breakers
- [ ] Add monitoring hooks

### Phase 4: Documentation & Testing (Week 4)
- [ ] Create architecture diagrams
- [ ] Write comprehensive documentation
- [ ] Implement integration tests
- [ ] Performance testing and optimization

### Phase 5: Validation (Week 5)
- [ ] Run all validators
- [ ] Security audit
- [ ] Performance benchmarks
- [ ] Production readiness checklist

---

## Success Criteria

- [ ] All modular directories created with appropriate content
- [ ] Hooks system fully functional with test coverage
- [ ] SKILL.md comprehensive and up-to-date
- [ ] Configuration management type-safe and validated
- [ ] Context window optimization reducing token usage by 20%
- [ ] Structured logging with rotation and retention
- [ ] Zero placeholders in codebase
- [ ] All validators passing
- [ ] Documentation complete with diagrams
- [ ] Performance benchmarks within acceptable ranges

---

## Open Questions & Decisions Needed

1. **Hook Execution Model**: Should hooks be synchronous or asynchronous? (Recommend: async for non-blocking)
2. **Token Tracking Granularity**: Track at skill-level or operation-level? (Recommend: operation-level for accuracy)
3. **Configuration Priority**: Environment variables vs config file? (Recommend: config file with env override)
4. **Log Storage**: Local files or external service? (Recommend: local with rotation, optional external)

---

## References

- D:\972026\SKILL-STANDARD.md — Library-wide standard
- D:\972026\250-base-building-trap-defense-design\CLAUDE.md — Current skill documentation
- D:\972026\250-base-building-trap-defense-design\PROJECT-detail.md — Technical specification
