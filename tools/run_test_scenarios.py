"""
run_test_scenarios.py — Skill 250: base-building-trap-defense-design
====================================================================
Production-grade structural & content validator for the skill bundle.

It verifies:
  1. Required file structure (8-File Contract + tooling).
  2. Sub-skill frontmatter, sections, and real domain content.
  3. main.md harness protocol, context envelope, quality gates, degradation.
  4. Knowledge base: evidence hierarchy, verifiable references, methods.
  5. Test scenarios: coverage of gates, verdicts, and degraded modes.
  6. knowledge_updater.py pipeline integrity markers.

Exit code 0 = all checks pass; non-zero = failures (printed).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

GATES = ["U1", "U2", "U3", "U4", "U5", "U6", "G1", "G2", "G3", "G4"]
VERDICTS = ["Strong Defense", "Conditional (weak flank)", "Easily Raidable", "Inconclusive"]

checks_passed = 0
checks_failed = 0
failures = []


def ok(label, detail=""):
    global checks_passed
    checks_passed += 1


def fail(label, detail=""):
    global checks_failed
    checks_failed += 1
    failures.append(label + ": " + detail)


def require(cond, label, detail=""):
    (ok if cond else fail)(label, detail)


def read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---- 1. File structure (8-File Contract + tooling) ----
REQUIRED = [
    "CLAUDE.md", "PROJECT-detail.md", "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "README.md", "SECOND-KNOWLEDGE-BRAIN.md", "skills/main.md",
    "tools/knowledge_updater.py", "tools/test_knowledge_updater.py",
    "tools/run_test_scenarios.py", "tools/validate_project.py",
    "tests/test-scenarios.md", "tests/TEST_RESULTS.md", "LICENSE",
]
for f in REQUIRED:
    require((ROOT / f).exists(), "file present: " + f)

subs = sorted(SKILLS.glob("sub-*.md"))
expected_subs = {
    "sub-gather-requirements", "sub-evidence-collector", "sub-core-analysis",
    "sub-knowledge-updater", "sub-advisor",
}
got_subs = {s.stem for s in subs}
require(got_subs == expected_subs, "sub-skill set", "got " + str(got_subs))
require(len(subs) >= 5, "at least 5 sub-skills", "found " + str(len(subs)))

# ---- 2. Sub-skill frontmatter + required sections + real domain content ----
FM = re.compile(r"^---\s*\n(.*?\n)---", re.S)
for s in subs:
    txt = read(s)
    m = FM.search(txt)
    require(bool(m), s.name + ": frontmatter")
    if m:
        require("name:" in m.group(1) and "description:" in m.group(1), s.name + ": name+description")
    for sec in ["Role & Persona", "Workflow", "Output Format", "Quality Gates"]:
        require(sec in txt, s.name + ": section " + sec)

core = read(ROOT / "skills" / "sub-core-analysis.md")
require("L0" in core and "L5" in core, "core-analysis: defense-in-depth layers L0-L5")
require("convergence ratio" in core.lower() or "chokepoint" in core.lower(), "core-analysis: chokepoint/funneling")
require("efficiency frontier" in core.lower(), "core-analysis: efficiency frontier")
require("single-point failure" in core.lower(), "core-analysis: single-point failure")
require("TTK" in core and "EHP" in core and "DPE" in core, "core-analysis: metrics TTK/EHP/DPE")
require("coverage" in core.lower() and "raid_cost" in core, "core-analysis: coverage + raid_cost")

gather = read(ROOT / "skills" / "sub-gather-requirements.md")
require("Canonical game normalization" in gather, "gather: canonical game normalization")
require("Threat taxonomy" in gather, "gather: threat taxonomy")

evidence = read(ROOT / "skills" / "sub-evidence-collector.md")
require("degradation" in evidence.lower(), "evidence: degradation handling")

advisor = read(ROOT / "skills" / "sub-advisor.md")
for v in VERDICTS:
    require(v in advisor, "advisor: verdict " + v)
require("Disclosure" in advisor and "Evidence chain" in advisor, "advisor: disclosure + evidence chain")
require("remediation" in advisor.lower(), "advisor: remediation")

# ---- 3. main.md harness protocol, context, gates, degradation ----
main_txt = read(ROOT / "skills" / "main.md")
for sec in ["Role & Persona", "Harness Execution Protocol", "Quality Gates",
            "Graceful Degradation & Error Handling", "Output Format"]:
    require(sec in main_txt, "main.md: section " + sec)
require("Pre-Flight" in main_txt, "main.md: pre-flight language detection")
require("Context Management" in main_txt and "Context Envelope" in main_txt, "main.md: context envelope")
require("schema_version" in main_txt, "main.md: envelope schema_version")
require("degradation_level" in main_txt, "main.md: envelope degradation_level")
require("limitation" in main_txt.lower(), "main.md: limitation banner")
for g in GATES:
    require(g in main_txt, "main.md: gate " + g + " present")

# ---- 4. Knowledge base ----
brain = read(ROOT / "SECOND-KNOWLEDGE-BRAIN.md")
require("Tier 1" in brain and "Tier 4" in brain, "brain: evidence hierarchy tiers")
dois = re.findall(r"10\.\d{4,9}/[^\s|]+", brain)
require(len(dois) >= 2, "brain: >=2 DOI-cited references", "found " + str(len(dois)))
require("## 1. Core Concepts" in brain, "brain: core concepts section")
require("L0" in brain and "L5" in brain, "brain: layer model L0-L5")
require("efficiency frontier" in brain.lower(), "brain: efficiency frontier")
require("counter-play" in brain.lower() or "counter_play" in brain.lower() or "counter play" in brain.lower(), "brain: counter-play")
require("## 2. Key Research Papers" in brain, "brain: key papers section")
require("## 4. Authoritative Data Sources" in brain, "brain: data sources section")
require("## 6. Self-Update Protocol" in brain, "brain: self-update protocol")
require("## 7. Knowledge Update Log" in brain, "brain: update log section")

# ---- 5. test-scenarios ----
sc = read(ROOT / "tests" / "test-scenarios.md")
require(sc.count("Scenario") >= 5, "scenarios: >=5", "found " + str(sc.count("Scenario")))
require("degraded" in sc.lower() or "missing" in sc.lower(), "scenarios: degraded case")
require("conflict" in sc.lower() or "compare" in sc.lower() or "comparison" in sc.lower(), "scenarios: comparison/conflict case")
for g in ["G1", "G2", "G3", "G4"]:
    require(g in sc, "scenarios: gate " + g + " referenced")
for v in VERDICTS:
    require(v in sc, "scenarios: verdict " + v + " covered")

# ---- 6. knowledge_updater.py integrity markers ----
ku = read(ROOT / "tools" / "knowledge_updater.py")
require("KNOWLEDGE_CONFIG" in ku, "knowledge_updater: KNOWLEDGE_CONFIG")
require("compute_hash" in ku and "sha256" in ku, "knowledge_updater: SHA256 dedup")
require("score_entry" in ku, "knowledge_updater: scoring")
require("extract_identifier" in ku, "knowledge_updater: identifier extraction")
require("--dry-run" in ku, "knowledge_updater: dry-run flag")
require("--json-logs" in ku, "knowledge_updater: json-logs flag")
require("cs.AI" in ku and "cs.HC" in ku, "knowledge_updater: real arxiv categories")
require("rss_feeds" in ku, "knowledge_updater: RSS feeds config")
require("def main(" in ku, "knowledge_updater: main entry")

# ---- report ----
total = checks_passed + checks_failed
print("[run_test_scenarios] " + str(checks_passed) + "/" + str(total) + " checks passed")
if failures:
    for f in failures:
        print("  - FAIL " + f)
    sys.exit(1)
print("[OK] all checks passed")
sys.exit(0)