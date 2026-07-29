#!/bin/bash
# base-building-trap-defense-design - Initialization Script
# Version: 2.1.0
#
# This script initializes the skill environment by creating necessary directories,
# setting up configuration files, and verifying prerequisites.

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."

    mkdir -p "$PROJECT_ROOT/logs"
    mkdir -p "$PROJECT_ROOT/logs/envelopes"
    mkdir -p "$PROJECT_ROOT/logs/events"
    mkdir -p "$PROJECT_ROOT/logs/performance"
    mkdir -p "$PROJECT_ROOT/temp"
    mkdir -p "$PROJECT_ROOT/backups"

    log_info "Directory structure created."
}

# Verify prerequisites
verify_prerequisites() {
    log_info "Verifying prerequisites..."

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        log_info "Python found: $PYTHON_VERSION"
    else
        log_error "Python 3 is required but not installed."
        exit 1
    fi

    # Check required Python packages
    log_info "Checking Python packages..."
    python3 -c "import json, hashlib, re, datetime" 2>/dev/null || {
        log_error "Required Python packages missing. Run: pip3 install -r requirements.txt"
        exit 1
    }
    log_info "Python packages OK."

    # Check configuration files
    if [ ! -f "$PROJECT_ROOT/config/default.json" ]; then
        log_error "Configuration file not found: config/default.json"
        exit 1
    fi
    log_info "Configuration files found."

    # Check skill files
    if [ ! -f "$PROJECT_ROOT/skills/main.md" ]; then
        log_error "Main skill file not found: skills/main.md"
        exit 1
    fi
    log_info "Skill files found."

    # Check knowledge base
    if [ ! -f "$PROJECT_ROOT/SECOND-KNOWLEDGE-BRAIN.md" ]; then
        log_warn "Knowledge base not found: SECOND-KNOWLEDGE-BRAIN.md"
        log_warn "Run knowledge updater to populate."
    else
        log_info "Knowledge base found."
    fi
}

# Set permissions
set_permissions() {
    log_info "Setting permissions..."

    # Make scripts executable
    find "$PROJECT_ROOT/scripts" -type f -name "*.sh" -exec chmod +x {} \;

    # Ensure logs directory is writable
    chmod 755 "$PROJECT_ROOT/logs"

    log_info "Permissions set."
}

# Generate session ID
generate_session_id() {
    python3 -c "import uuid; print(uuid.uuid4())"
}

# Run basic validation
run_validation() {
    log_info "Running basic validation..."

    if [ -f "$PROJECT_ROOT/tools/validate_project.py" ]; then
        python3 "$PROJECT_ROOT/tools/validate_project.py" || {
            log_warn "Validation failed. Review and fix issues."
        }
    else
        log_warn "Validator not found. Skipping validation."
    fi
}

# Main initialization flow
main() {
    echo "=========================================="
    echo "Base Building Trap Defense Design - Init"
    echo "Version: 2.1.0"
    echo "=========================================="
    echo ""

    # Check if already initialized
    if [ -f "$PROJECT_ROOT/.initialized" ]; then
        log_warn "Project already initialized."
        read -p "Re-initialize? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Exiting."
            exit 0
        fi
    fi

    # Run initialization steps
    create_directories
    verify_prerequisites
    set_permissions
    run_validation

    # Mark as initialized
    date > "$PROJECT_ROOT/.initialized"
    echo "Session ID format: UUID" >> "$PROJECT_ROOT/.initialized"

    log_info "Initialization complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review configuration in config/default.json"
    echo "2. Run knowledge updater: python3 tools/knowledge_updater.py"
    echo "3. Test the harness with sample queries"
    echo ""
}

# Run main function
main "$@"
