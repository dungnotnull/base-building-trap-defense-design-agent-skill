# SECOND-KNOWLEDGE-BRAIN.md — Skill 250: base-building-trap-defense-design

> **Living Knowledge Base** — updated by `tools/knowledge_updater.py` on a weekly
> schedule (academic, Mondays 08:00) and daily (news, 07:00). All entries are
> date-stamped; new entries are appended at the bottom of Section 7.
> Evidence hierarchy: Systematic Review > Meta-Analysis > Peer-reviewed/RCT > Cohort > Expert Consensus > News.
> Tier definitions: Tier 1 systematic/standard, Tier 2 peer-reviewed, Tier 3 industry/book/guideline, Tier 4 news/blog/vendor.

---

## 1. Core Concepts & Frameworks

### 1.1 Defense-in-depth layering (base-building games)

A base defense is modeled as concentric layers L0..L5. Each layer has a stated purpose, a structure set, an overlap field-of-fire with the next layer, and a target breach time. The defense is robust when no single layer's loss collapses the whole (no single-point failure) and each layer buys time for the inner layer.

| Layer | Purpose | Typical structures | Breach-time goal |
|-------|---------|--------------------|------------------|
| L0 Outer detection | early warning, decoys, twig tripwires | twig spikes, alarm traps, camera/detection | alert + deter |
| L1 Perimeter | deny easy approach, slow pathing | outer stone wall, barricades, barbed wire | slow > approach |
| L2 Funneling chokepoints | force pathing into kill zones | wall gaps, doorway funnels, stairs-as-choke | route control |
| L3 Kill zones | concentrated overlapping fire + traps | trap field, turrets, shotgun/flame traps | maximize TTK |
| L4 Inner keep | protect loot + TC | honeycomb, sheet-metal/blast doors | survive > raid window |
| L5 TC core | last stand; most armored | HQM box, armored doors | deny TC destruction |

### 1.2 Chokepoints & funneling

Chokepoints are deliberate path-narrowing geometries that route enemy AI/raiders through a kill zone. Design rules:
- **Convergence ratio**: entrance width / exit width. A ratio >= 3 produces strong funneling; the exit must align with the primary kill-zone overlap.
- **No alternative path**: any gap that bypasses the choke invalidates it. Walls/foundations must seal flanks.
- **A\* awareness**: enemy AI typically pathfinds by lowest-cost route. A choke is only effective if the funneled route is the lowest-cost option (cheaper than breaching walls). Raise the cost of alternate routes (armor grade, height) so the intended path wins.
- **Trigger-to-exit timing**: a trap in the choke must fire before the enemy exits the kill radius. Verify trigger_delay + traversal_time_through_zone > 0 with margin.

### 1.3 Trap synergy & trigger logic

Traps combine via trigger chains rather than raw stacking. The canonical chain is **CC (slow/disable) -> damage -> finish**:
- CC trap (flame, slow, stun) reduces traversal speed, extending the time enemies spend in the damage zone.
- Damage traps (shotgun trap, spike, dart) exploit the extended dwell time.
- AoE traps must not mutually trigger or destroy each other; place them with >= their blast radius apart or stagger their trigger timers.
- Multi-phase: for wave or multi-breach scenarios, the plan must re-arm or fall back to a deeper layer after the first trigger.

Trap template: `trap | trigger=proximity|contact|timer|tripwire|manual | delay=s | radius=m | dmg=n | cooldown=s | chain=prev|next | notes`.

### 1.4 Cost vs coverage & the efficiency frontier

- **Coverage %** = (covered area)/(threat-zone area). Target >= 70% of the primary threat zone before adding redundancy.
- **Defensive value** = (structure HP + trap damage contribution) weighted by threat-zone coverage.
- **Efficiency** = defensive_value / total_material_cost. Rank structures; drop any dominated by another (higher value at <= cost) — this is the **efficiency frontier**.
- **Redundancy rule**: add redundancy only after the frontier is met and a single-point failure exists.

### 1.5 Counter-play & PvP balance

The defender-attacker balance is a sulfur/cost ratio, not a binary "strong":
- **Defender cost** = total materials invested in the protected axis.
- **Attacker raid cost** = explosives + tooling to reach the TC core (sulfur equivalent).
- **Net balance**: defender-favored when defender_cost < attacker_raid_cost AND breach_time > response_window; attacker-favored otherwise.
- **Single-point failure**: a structure whose loss collapses a layer — must be eliminated with redundancy.
- **Online vs offline**: offline raids remove the response_window, so balance must hold on attacker_raid_cost alone (cost-denial), not time.

### 1.6 Threat zoning (PvE / PvP / hybrid)

- **PvE zones**: timed hordes/waves follow predictable pathing — funneling and TTK maximization dominate.
- **PvP zones**: raiders choose approach vectors — detection, redundancy, and cost-denial dominate.
- **Hybrid**: PvE threats compound with PvP raiders (e.g., a horde during a raid); design must handle both pathing funnels and human flankers.

### 1.7 Metric definitions (used across sub-skills)

| Metric | Definition | Source axis |
|--------|-----------|-------------|
| TTK | time-to-kill a typical attacker in the primary kill zone (s) | L3 trap/turret DPS |
| EHP | effective HP of the protected core vs the dominant raid tool = HP / (explosive_dmg * efficiency) | L4/L5 + raid tool stats |
| DPE | damage per explosive for the attacker (inverse of EHP) — compares raid cost | raid tool stats |
| coverage | % of threat zone covered by overlapping fire/traps | cost-coverage table |
| raid_cost | total attacker resource cost to reach the TC core (sulfur/currency) | counter-play matrix |

### 1.8 Evidence hierarchy (this domain)

- **Tier 1**: Systematic review / meta-analysis / official standard.
- **Tier 2**: Peer-reviewed academic paper / foundational method.
- **Tier 3**: Industry report / professional book / guideline.
- **Tier 4**: News / blog / vendor / wiki.
---

## 2. Key Research Papers & Standards

| # | Title | Authors | Year | Venue | Identifier | Tier |
|---|------|---------|------|-------|------------|------|
| 1 | A Formal Basis for the Heuristic Determination of Minimum Cost Paths | P. Hart, N. Nilsson, B. Raphael | 1968 | IEEE Trans. Systems Science and Cybernetics | DOI 10.1109/TSSC.1968.300133 | 2 |
| 2 | Does Gamification Work? — A Literature Review of Empirical Studies on Gamification | J. Hamari, J. Koivisto, H. Sarsa | 2014 | Hawaii Int. Conf. on System Sciences (HICSS) | DOI 10.1109/HICSS.2014.377 | 2 |
| 3 | The Art of Game Design: A Book of Lenses | J. Schell | 2008 | CRC Press | ISBN 978-0123694966 | 3 |
| 4 | Patterns in Game Design | S. Bjork, J. Holopainen | 2005 | Charles River Media | ISBN 1-58450-354-8 | 3 |
| 5 | Game Mechanics: Advanced Game Design | E. Adams, J. Dormans | 2012 | New Riders | ISBN 978-0321820273 | 3 |
| 6 | A Theory of Fun for Game Design | R. Koster | 2004 | Paraglyph Press | ISBN 1-932117-06-1 | 3 |
| 7 | Rules of Play: Game Design Fundamentals | K. Salen, E. Zimmerman | 2003 | MIT Press | ISBN 978-0262240451 | 3 |

**Coverage note:** entries 1 anchors pathfinding/funneling (chokepoint cost routing); 2 anchors engagement/balance evaluation methodology; 3-7 anchor general game-design mechanics, pattern language, and balance discipline. Domain-specific base-defense literature is sparse; the crawl pipeline targets CHI PLAY, IEEE Trans. Games, and Entertainment Computing to grow Tier-1/2 coverage (see Section 7 log).

Authoritative venues registered for crawling:
- Proceedings of CHI PLAY (ACM)
- IEEE Transactions on Games
- Entertainment Computing (Elsevier)
- Computers in Human Behavior (Elsevier)
- Simulation & Gaming (SAGE)
- Journal of Game Design & Development Education

---

## 3. State-of-the-Art Methods & Tools

State of the art in base-building defense & trap design:
- **AI-pathfinding-aware trap placement** — place traps along the lowest-cost A\* route so enemy AI is forced through kill zones (Hart/Nilsson/Raphael is the foundational method).
- **ML raid prediction** — learn raider approach vectors from replay/community data to prioritize coverage.
- **Tower-defense balance simulation** — Monte-Carlo breaching to tune trap damage vs enemy HP and cooldowns.
- **Community base-sharing & analytics** — Rust Labs / community wikis surface real structure/trap stats and meta shifts.
- **Procedural defense layouts** — auto-generate layer geometries satisfying the convergence-ratio and overlap constraints.

Crawl targets for SOTA growth: CHI PLAY, IEEE Trans. Games, Entertainment Computing, Simulation & Gaming, plus community stat feeds (patch notes, wiki APIs).

---

## 4. Authoritative Data Sources

### 4.1 Domain authoritative sources (Tier 3-4, verified per-run)
- Official patch notes per resolved game (Rust, 7DTD, Fortnite STW, ARK, Valheim, Conan, Palworld) — Tier 3.
- Official game wikis (Facepunch wiki, etc.) — Tier 3.
- Community stat wikis (Rust Labs, 7DTD wiki, etc.) — Tier 4 (verify against patch notes).
- Datamined stat sheets — Tier 4 (verify per patch).

### 4.2 Academic & research sources (Tier 1-2)
- Proceedings of CHI PLAY (ACM)
- IEEE Transactions on Games
- Entertainment Computing (Elsevier)
- Computers in Human Behavior (Elsevier)
- Simulation & Gaming (SAGE)
- Journal of Game Design & Development Education

### 4.3 Standards/methods references
- A\* pathfinding (Hart, Nilsson, Raphael 1968) — foundational routing method for funneling analysis.
- Game-design pattern language (Bjork & Holopainen; Adams & Dormans) — trap/structure pattern catalog.

---

## 5. Analytical Frameworks

Knowledge categories applied by the sub-skills:
- **Defense layers & chokepoints** (sub-core-analysis 2.2) — L0..L5 model, convergence ratio, overlap fields of fire.
- **Trap synergy & trigger logic** (sub-core-analysis 2.3) — CC -> damage -> finish chains, AoE stacking, trigger-to-exit timing.
- **Pathing & funneling enemy AI** (sub-core-analysis 2.2) — A\* lowest-cost routing, alternate-route cost raising.
- **Resource cost vs defensive value** (sub-core-analysis 2.4) — coverage %, efficiency frontier, redundancy rule.
- **Counter-play (PvP raid) & balance** (sub-core-analysis 2.5) — sulfur ratio, net balance, single-point failure, online vs offline.
- **Spatial layout & threat zoning** (sub-core-analysis 2.1) — PvE/PvP/hybrid zone mapping.

Cross-reference the workflows in `skills/*.md` for the exact method applied at each step. The fixed bookends (requirements -> evidence -> knowledge -> synthesis -> quality gate) are mandatory; the core-analysis sub-skill implements the domain-specific methods above.
---

## 6. Self-Update Protocol

- **Crawl pipeline:** `tools/knowledge_updater.py`
- **Schedule:** weekly academic (Mondays 08:00) + daily news (07:00); documented in `CLAUDE.md`
- **Dedup:** SHA256 of DOI/URL/ISBN (case/whitespace-insensitive)
- **Scoring:** composite 0-10 = recency(0.4) + keyword_relevance(0.4) + citation_count(0.2)
- **Crawl targets:** ArXiv categories `cs.AI`, `cs.HC` (game/AI/HCI); Semantic Scholar keyword clusters; RSS feeds (game design blogs / patch-watch feeds)
- **Gap-fill:** sub-knowledge-updater flags missing coverage as crawl queries; the next pipeline run consumes them via `--keywords`
- **Append rule:** new entries appended under Section 7 with date stamp + relevance score; never overwrite Section 1-6 baseline
- **Integrity:** the pipeline never fabricates; a source without a verifiable identifier is rejected; runs are idempotent via SHA256 dedup

---

## 7. Knowledge Update Log

_(Appended automatically by the crawl pipeline. Baseline seeded with the references in Section 2. The log below is empty until the first scheduled run; manual runs are safe via `python tools/knowledge_updater.py --dry-run`.)_

| Date | Title | Authors | Year | Venue | DOI/URL | Tier | Score | Source |
|------|-------|---------|------|-------|---------|------|-------|--------|
_(no automated entries yet — run `python tools/knowledge_updater.py` to populate)_