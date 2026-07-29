# Defense Metrics Framework

## Overview

This framework defines standardized metrics for evaluating base defense effectiveness in base-building games. Metrics enable quantitative comparison, optimization, and communication of defensive quality.

## Core Metrics

### TTK: Time To Kill (seconds)
**Definition:** Average time from attacker engagement to elimination
**Formula:** Sum of kill times / number of attackers
**Target:** Minimize (lower is better)
**Context:** Measured from breach of first perimeter layer

**Factors:**
- Trap density and placement
- Chokepoint effectiveness
- Layer depth
- Damage output

### EHP: Effective Health Points (hit points)
**Definition:** Total damage required to breach all defensive layers
**Formula:** Sum of (structure HP * armor modifier) across all layers
**Target:** Maximize (higher is better)
**Context:** Includes walls, traps, and defensive structures

**Factors:**
- Material quality (wood, stone, metal, armored)
- Structure upgrade levels
- Armor effectiveness
- Layer count

### DPE: Damage Per Expenditure (damage per resource unit)
**Definition:** Defensive damage output per resource cost
**Formula:** Total trap damage / total resource cost
**Target:** Maximize (higher is better)
**Context:** Measures efficiency of defensive investment

**Factors:**
- Trap selection and synergy
- Resource optimization
- Trap trigger reliability
- Placement effectiveness

### Coverage (%)
**Definition:** Percentage of base footprint protected by active defense
**Formula:** Protected area / total area * 100
**Target:** Maximize (higher is better, diminishing returns >85%)
**Context:** Includes trap coverage, TC coverage, and kill zone coverage

**Factors:**
- Trap positioning
- Tool cupboard radius
- Kill zone overlap
- Blind spots

### Raid Cost (resource units)
**Definition:** Estimated cost for attackers to successfully raid
**Formula:** Breach tools cost + expected losses / success probability
**Target:** Maximize (higher is better)
**Context:** Deters low-resource raiders

**Factors:**
- Breach difficulty
- Defense effectiveness
- Asset value
- Counter-measures

## Secondary Metrics

### Convergence Ratio
**Definition:** Ratio of chokepoint width to entrance width
**Formula:** (Sum of chokepoint widths) / (Sum of entrance widths)
**Target:** < 0.3 (70% funneling efficiency)
**Context:** Measures funnel effectiveness

### Trap Synergy Multiplier
**Definition:** Effectiveness multiplier from trap combinations
**Formula:** Actual kills / (Sum of individual trap kills)
**Target:** > 1.0 (synergy exists)
**Context:** Chains, combos, and overlapping effects

### Response Time (seconds)
**Definition:** Time from detection to defender response
**Formula:** Average response time across alert events
**Target:** Minimize (lower is better)
**Context:** Enabled by detection systems

### Asset Protection Rate (%)
**Definition:** Percentage of assets protected in worst-case scenario
**Formula:** (Asset value in sanctuary) / (Total asset value)
**Target:** Maximize (higher is better)
**Context:** Critical for resource-heavy bases

## Metric Relationships

```
TTK ←→ EHP (higher EHP increases TTK)
TTK ←→ Coverage (better coverage reduces TTK)
DPE ←→ Raid Cost (higher DPE increases raid cost)
Coverage ←→ Convergence Ratio (better funneling improves coverage)
Raid Cost ←→ EHP (higher EHP increases raid cost)
```

## Optimization Frontier

Plot cost vs. effectiveness to identify optimal investment points:
- **Diminishing Returns:** Beyond 85% coverage, additional investment yields minimal benefit
- **Sweet Spot:** Typically 60-80% coverage with balanced TTK and DPE
- **Over-Investment:** >95% coverage rarely justifies cost

## Measurement Protocols

### Data Collection
- Simulate attacks with varied resource levels
- Record TTK for each attack path
- Calculate EHP from structure inventories
- Measure coverage from base blueprints

### Analysis
- Compare metrics against game-specific benchmarks
- Identify weak spots (low coverage, low TTK areas)
- Optimize by reallocating resources from low-DPE to high-DPE areas

### Reporting
- Present metrics in scorecard format
- Include best/base/worst scenarios
- Highlight optimization opportunities

## References

- Game balance theory: Economics of PvP defense
- Military metrics: Force effectiveness measures
- Security assessment: Quantitative risk analysis

---

*This framework reference is part of the base-building-trap-defense-design knowledge base.*
