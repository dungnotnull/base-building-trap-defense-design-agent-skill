#!/usr/bin/env python3
"""
base-building-trap-defense-design - Environment Validation Script
Version: 2.1.0

This Python script validates the runtime environment including:
- Python version and packages
- Configuration file integrity
- Knowledge base existence
- Skill file availability
- Directory permissions
"""

import sys
import os
import json
import pathlib
from typing import List, Tuple

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def log_info(message: str) -> None:
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")

def log_warn(message: str) -> None:
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {message}")

def log_error(message: str) -> None:
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def check_python_version() -> bool:
    """Check if Python version is 3.8 or higher."""
    log_info("Checking Python version...")
    version = sys.version_info
    if version >= (3, 8):
        log_info(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        log_error(f"Python 3.8+ required, found {version.major}.{version.minor}.{version.micro}")
        return False

def check_packages() -> bool:
    """Check if required Python packages are installed."""
    log_info("Checking Python packages...")
    required = ['json', 'hashlib', 're', 'datetime', 'pathlib', 'typing']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        log_error(f"Missing packages: {', '.join(missing)}")
        return False
    else:
        log_info("All required packages present")
        return True

def check_config(project_root: pathlib.Path) -> bool:
    """Check if configuration files exist and are valid."""
    log_info("Checking configuration files...")
    config_file = project_root / 'config' / 'default.json'
    schema_file = project_root / 'config' / 'schema.json'

    if not config_file.exists():
        log_error(f"Configuration file not found: {config_file}")
        return False

    if not schema_file.exists():
        log_warn(f"Schema file not found: {schema_file}")

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        log_info("Configuration file is valid JSON")

        # Validate required fields
        required_fields = ['version', 'environment', 'context_window', 'quality_gates']
        for field in required_fields:
            if field not in config:
                log_error(f"Missing required config field: {field}")
                return False

        log_info("Configuration file has all required fields")
        return True
    except json.JSONDecodeError as e:
        log_error(f"Configuration file is invalid JSON: {e}")
        return False

def check_skill_files(project_root: pathlib.Path) -> bool:
    """Check if skill files exist."""
    log_info("Checking skill files...")
    skills_dir = project_root / 'skills'
    required_files = [
        'main.md',
        'sub-gather-requirements.md',
        'sub-evidence-collector.md',
        'sub-core-analysis.md',
        'sub-knowledge-updater.md',
        'sub-advisor.md'
    ]

    missing = []
    for file in required_files:
        if not (skills_dir / file).exists():
            missing.append(file)

    if missing:
        log_error(f"Missing skill files: {', '.join(missing)}")
        return False
    else:
        log_info("All skill files present")
        return True

def check_knowledge_base(project_root: pathlib.Path) -> bool:
    """Check if knowledge base exists."""
    log_info("Checking knowledge base...")
    kb_file = project_root / 'SECOND-KNOWLEDGE-BRAIN.md'

    if not kb_file.exists():
        log_warn("Knowledge base not found - run knowledge updater")
        return False
    else:
        log_info("Knowledge base found")
        return True

def check_directories(project_root: pathlib.Path) -> bool:
    """Check if required directories exist and are writable."""
    log_info("Checking directories...")
    required_dirs = ['logs', 'temp', 'config', 'skills', 'tools', 'hooks']

    all_ok = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            log_warn(f"Directory not found: {dir_name}")
            all_ok = False
        elif not os.access(dir_path, os.W_OK):
            log_error(f"Directory not writable: {dir_name}")
            all_ok = False

    if all_ok:
        log_info("All required directories present and writable")
    return all_ok

def check_hooks(project_root: pathlib.Path) -> bool:
    """Check if hook files exist."""
    log_info("Checking hooks...")
    hooks_dir = project_root / 'hooks'

    if not hooks_dir.exists():
        log_warn("Hooks directory not found")
        return False

    required_hooks = [
        'lifecycle/pre-exec.md',
        'lifecycle/post-exec.md',
        'state/sync.md',
        'state/validate.md',
        'event/emit.md',
        'event/subscribe.md',
        'token/track.md',
        'token/optimize.md',
        'error/classify.md',
        'error/recover.md'
    ]

    missing = []
    for hook in required_hooks:
        if not (hooks_dir / hook).exists():
            missing.append(hook)

    if missing:
        log_warn(f"Missing hooks: {', '.join(missing)}")
        return False
    else:
        log_info("All hooks present")
        return True

def main() -> int:
    """Main validation flow."""
    print("=" * 50)
    print("Base Building Trap Defense Design - Environment Validation")
    print("Version: 2.1.0")
    print("=" * 50)
    print()

    # Get project root
    script_dir = pathlib.Path(__file__).parent
    project_root = script_dir.parent.parent

    # Run all checks
    checks = [
        check_python_version(),
        check_packages(),
        check_config(project_root),
        check_skill_files(project_root),
        check_knowledge_base(project_root),
        check_directories(project_root),
        check_hooks(project_root)
    ]

    passed = sum(checks)
    total = len(checks)

    print()
    print("=" * 50)
    if passed == total:
        log_info(f"All checks passed ({passed}/{total})")
        return 0
    else:
        log_warn(f"Some checks failed ({passed}/{total} passed)")
        return 1

if __name__ == '__main__':
    sys.exit(main())
