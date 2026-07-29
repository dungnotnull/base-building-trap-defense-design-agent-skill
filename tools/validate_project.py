"""
validate_project.py - Skill 250: base-building-trap-defense-design
==================================================================
8-File Contract validator + project metadata consistency check.

Verifies that every file required by the skill standard is present,
non-empty, UTF-8 (no BOM), uses LF line endings, and that cross-file
references are consistent (version, phase status, verdict set, etc.).

Exit code 0 = contract satisfied; non-zero = violations (printed).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The 8-File Contract (core deliverables) + supporting artifacts.
CONTRACT = [
    "CLAUDE.md",
    "PROJECT-detail.md",
    "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "README.md",
    "SECOND-KNOWLEDGE-BRAIN.md",
    "skills/main.md",
    "skills/sub-gather-requirements.md",
    "skills/sub-evidence-collector.md",
    "skills/sub-core-analysis.md",
    "skills/sub-knowledge-updater.md",
    "skills/sub-advisor.md",
    "tools/knowledge_updater.py",
    "tools/test_knowledge_updater.py",
    "tools/run_test_scenarios.py",
    "tests/test-scenarios.md",
    "tests/TEST_RESULTS.md",
    "LICENSE",
]

VERDICTS = ["Strong Defense", "Conditional (weak flank)", "Easily Raidable", "Inconclusive"]

_passed = 0
_failed = 0
violations = []


def ok(*_):
    global _passed
    _passed += 1


def fail(label):
    global _failed
    _failed += 1
    violations.append(label)


def require(cond, label):
    (ok if cond else fail)(label)


def read(path):
    p = Path(path)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def is_utf8_no_bom(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def is_lf(path):
    raw = Path(path).read_bytes()
    return b"\r\n" not in raw


# ---- 1. Presence + non-empty + encoding ----
for f in CONTRACT:
    p = ROOT / f
    require(p.exists() and p.stat().st_size > 0, "missing/empty: " + f)
    if p.exists():
        require(is_utf8_no_bom(p), "encoding (UTF-8 no BOM): " + f)
        require(is_lf(p), "line endings (LF): " + f)

# ---- 2. progression.json (metadata artifact) ----
prog_path = ROOT / "progression.json"
require(prog_path.exists(), "missing: progression.json")
if prog_path.exists():
    try:
        prog = json.loads(prog_path.read_text(encoding="utf-8"))
        require(isinstance(prog, dict), "progression.json: object root")
        require(str(prog.get("skill")) == "base-building-trap-defense-design", "progression.json: skill id")
        require(str(prog.get("status", "")).lower() in ("complete", "production ready", "done"), "progression.json: status")
        require(prog.get("percent_complete") == 100, "progression.json: percent_complete == 100")
    except (ValueError, TypeError) as ex:
        require(False, "progression.json: valid JSON (" + str(ex) + ")")

# ---- 3. CLAUDE.md reflects production-ready state ----
claude = read(ROOT / "CLAUDE.md") or ""
require("base-building-trap-defense-design" in claude, "CLAUDE.md: skill name")
require("knowledge_updater.py" in claude, "CLAUDE.md: tool reference")

# ---- 4. README has install/usage/license ----
readme = read(ROOT / "README.md") or ""
require("Usage" in readme or "usage" in readme.lower(), "README: usage section")
require("MIT" in readme, "README: MIT license reference")
require("Phase 5" in readme or "Phase 0" in readme, "README: phase roadmap")

# ---- 5. PROJECT-detail has harness architecture + Vietnamese idea ----
pd = read(ROOT / "PROJECT-detail.md") or ""
require("Harness Architecture" in pd, "PROJECT-detail: harness architecture")
require("Idea (Vietnamese)" in pd or "Idea" in pd, "PROJECT-detail: idea section")
require("Context Envelope" in pd or "context" in pd.lower(), "PROJECT-detail: context management mention")

# ---- 6. PDPT marks 100% complete across all phases ----
pdpt = read(ROOT / "PROJECT-DEVELOPMENT-PHASE-TRACKING.md") or ""
require("100%" in pdpt, "PDPT: 100% markers")
for phase in ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]:
    require(phase in pdpt, "PDPT: " + phase)
complete_count = pdpt.lower().count("100% complete")
require(complete_count >= 6, "PDPT: all 6 phases 100% complete", )
require("PRODUCTION READY" in pdpt.upper() or "production ready" in pdpt.lower(), "PDPT: production ready")

# ---- 7. main.md + advisor verdict consistency ----
main_txt = read(ROOT / "skills" / "main.md") or ""
for v in VERDICTS:
    require(v in main_txt, "main.md: verdict " + v)
adv = read(ROOT / "skills" / "sub-advisor.md") or ""
for v in VERDICTS:
    require(v in adv, "advisor: verdict " + v)

# ---- 8. Knowledge base verifiable references ----
brain = read(ROOT / "SECOND-KNOWLEDGE-BRAIN.md") or ""
dois = re.findall(r"10\.\d{4,9}/[^\s|]+", brain)
require(len(dois) >= 2, "brain: >=2 verifiable DOIs", )
isbns = re.findall(r"ISBN\s*[0-9Xx\-]{10,17}", brain)
require(len(isbns) >= 2, "brain: >=2 ISBNs", )

# ---- report ----
total = _passed + _failed
print("[validate_project] " + str(_passed) + "/" + str(total) + " contract checks passed")
if violations:
    for v in violations:
        print("  - VIOLATION " + v)
    sys.exit(1)
print("[OK] 8-File Contract satisfied; project production-ready")
sys.exit(0)