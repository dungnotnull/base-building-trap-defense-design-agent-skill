# test-scenarios.md — Skill 250: base-building-trap-defense-design

Five concrete end-to-end scenarios that exercise the full harness
(requirements -> evidence -> core analysis -> knowledge -> advice -> quality
gate). Each lists inputs, expected steps, applicable quality gates, and a
target verdict. The scenarios collectively cover every universal gate U1-U6,
every domain gate G1-G4, and every verdict category.

---

## Scenario 1: Standard analysis (object in scope)
- **Input:** a typical Base-Building Game Defense & Trap System Design case
  with complete inputs (game = Rust, mode = PvP, full trap/structure stats,
  a base-layout sketch, a sulfur budget, server wipe cycle).
- **Expected:** sub-gather-requirements normalizes the game -> sub-evidence-
  collector fetches live stats + patch notes (Level 0) -> sub-core-analysis
  produces L0-L5 layers, chokepoints, trap logic, cost-vs-coverage frontier,
  counter-play matrix, metrics (TTK/EHP/DPE/coverage/raid_cost) -> sub-
  knowledge-updater surfaces Tier-labeled citations -> sub-advisor emits a
  risk-disclosed verdict -> main quality gate.
- **Gates:** U1-U6 + G1, G2, G3, G4.
- **Verdict target:** Strong Defense.

## Scenario 2: Minimal-input analysis (defaults)
- **Input:** terse request ("design a defense for my Rust base") with minimal
  data; game inferred, mode/resources/audience defaulted.
- **Expected:** defaults applied with explicit assumption statements for every
  defaulted field; never fabricate missing values; degradation Level may rise
  if stats are unavailable.
- **Gates:** U4 (language), U6 (traceability), G1-G4 with explicit assumptions.

## Scenario 3: Comparison scenario
- **Input:** compare two base/defense layouts (or two trap plans) within the
  domain for the same game/threat profile.
- **Expected:** side-by-side scorecard (layers, metrics, cost/coverage,
  counter-play balance) + evidence-based winner; sub-core-analysis applied to
  both; a single winning verdict plus the runner-up's residual risk.
- **Gates:** U3 (evidence hierarchy), U6, G1, G2, G3, G4.
- **Verdict target:** Conditional (weak flank) for the runner-up.

## Scenario 4: Risk / feasibility or conflict scenario
- **Input:** assess risk of a borderline case, or resolve conflicting
  trap/structure actions (e.g., AoE traps that mutually trigger, or a
  defense-in-depth layer conflicting with a single concentrated layer).
- **Expected:** multi-scenario (best/base/worst) risk output; stated
  precedence (defense-in-depth > single-layer; cost-efficiency breaks ties);
  >=3 key risks with probability/impact/mitigation; disclosure before verdict.
- **Gates:** U2 (disclosure), G1, G2, G3, G4.
- **Verdict target:** Easily Raidable (decisive single-point failure) or
  Conditional (weak flank).

## Scenario 5: Degraded-mode scenario
- **Input:** primary sources unreachable (patch-note site down) OR a required
  stat (e.g., a trap's damage) is DATA UNAVAILABLE.
- **Expected:** fallback chain (official -> community wiki -> SECOND-KNOWLEDGE-
  BRAIN.md) + LIMITATION notice (degradation Level 2-3); no fabricated values;
  every missing value marked DATA UNAVAILABLE; verdict maps to Inconclusive
  when the missing stat is decisive for the balance calculation.
- **Gates:** U2, graceful-degradation levels, G1, G2, G3, G4.
- **Verdict target:** Inconclusive (decisive metric missing).

---

### Gate coverage matrix

| Gate | S1 | S2 | S3 | S4 | S5 |
|------|----|----|----|----|----|
| G1 | yes | yes | yes | yes | yes |
| G2 | yes | yes | yes | yes | yes |
| G3 | yes | yes | yes | yes | yes |
| G4 | yes | yes | yes | yes | yes |
| U1-U6 | yes | yes | yes | yes | yes |

### Verdict coverage

- Strong Defense (Scenario 1)
- Conditional (weak flank) (Scenario 3 / Scenario 4)
- Easily Raidable (Scenario 4)
- Inconclusive (Scenario 5)