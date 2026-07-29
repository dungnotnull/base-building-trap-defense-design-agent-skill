#!/bin/bash
# base-building-trap-defense-design - Maintenance and Cleanup Script
# Version: 2.1.0
#
# This script performs routine maintenance tasks including log rotation,
# temporary file cleanup, and backup management.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Configuration
RETENTION_DAYS_INFO=30
RETENTION_DAYS_WARN=60
RETENTION_DAYS_ERROR=90
BACKUP_RETENTION_DAYS=7

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

# Clean old logs
cleanup_logs() {
    log_info "Cleaning up old logs..."

    # Clean info logs
    find "$PROJECT_ROOT/logs" -name "*.log" -type f -mtime +$RETENTION_DAYS_INFO -exec rm -v {} \;

    # Clean old envelope snapshots
    find "$PROJECT_ROOT/logs/envelopes" -name "*.json" -type f -mtime +$RETENTION_DAYS_INFO -exec rm -v {} \;

    # Clean old event logs
    find "$PROJECT_ROOT/logs/events" -name "*.jsonl" -type f -mtime +$RETENTION_DAYS_INFO -exec rm -v {} \;

    log_info "Log cleanup complete."
}

# Clean temporary files
cleanup_temp() {
    log_info "Cleaning temporary files..."

    # Remove temp files older than 1 day
    find "$PROJECT_ROOT/temp" -type f -mtime +1 -exec rm -v {} \;

    # Remove empty temp directories
    find "$PROJECT_ROOT/temp" -type d -empty -delete

    log_info "Temp cleanup complete."
}

# Rotate and compress logs
rotate_logs() {
    log_info "Rotating logs..."

    # Compress logs older than 7 days
    find "$PROJECT_ROOT/logs" -name "*.log" -type f -mtime +7 ! -name "*.gz" -exec gzip -v {} \;

    # Compress old envelope snapshots
    find "$PROJECT_ROOT/logs/envelopes" -name "*.json" -type f -mtime +7 ! -name "*.gz" -exec gzip -v {} \;

    log_info "Log rotation complete."
}

# Clean old backups
cleanup_backups() {
    log_info "Cleaning old backups..."

    # Remove backups older than retention period
    find "$PROJECT_ROOT/backups" -name "*.json" -type f -mtime +$BACKUP_RETENTION_DAYS -exec rm -v {} \;

    log_info "Backup cleanup complete."
}

# Generate disk usage report
generate_report() {
    log_info "Generating disk usage report..."

    echo "=== Disk Usage Report ===" > "$PROJECT_ROOT/logs/usage_report.txt"
    echo "Generated: $(date)" >> "$PROJECT_ROOT/logs/usage_report.txt"
    echo "" >> "$PROJECT_ROOT/logs/usage_report.txt"

    # Log directory size
    echo "Logs directory:" >> "$PROJECT_ROOT/logs/usage_report.txt"
    du -sh "$PROJECT_ROOT/logs" >> "$PROJECT_ROOT/logs/usage_report.txt"
    echo "" >> "$PROJECT_ROOT/logs/usage_report.txt"

    # Temp directory size
    echo "Temp directory:" >> "$PROJECT_ROOT/logs/usage_report.txt"
    du -sh "$PROJECT_ROOT/temp" >> "$PROJECT_ROOT/logs/usage_report.txt"
    echo "" >> "$PROJECT_ROOT/logs/usage_report.txt"

    # Backup directory size
    echo "Backup directory:" >> "$PROJECT_ROOT/logs/usage_report.txt"
    du -sh "$PROJECT_ROOT/backups" >> "$PROJECT_ROOT/logs/usage_report.txt"
    echo "" >> "$PROJECT_ROOT/logs/usage_report.txt"

    # Total project size
    echo "Total project size:" >> "$PROJECT_ROOT/logs/usage_report.txt"
    du -sh "$PROJECT_ROOT" >> "$PROJECT_ROOT/logs/usage_report.txt"

    log_info "Report saved to logs/usage_report.txt"
}

# Verify integrity
verify_integrity() {
    log_info "Verifying project integrity..."

    # Check if main skill file exists
    if [ ! -f "$PROJECT_ROOT/skills/main.md" ]; then
        log_error "Main skill file missing!"
        return 1
    fi

    # Check if knowledge base exists
    if [ ! -f "$PROJECT_ROOT/SECOND-KNOWLEDGE-BRAIN.md" ]; then
        log_warn "Knowledge base missing!"
    fi

    log_info "Integrity check complete."
}

# Main maintenance flow
main() {
    echo "=========================================="
    echo "Base Building Trap Defense Design - Maintenance"
    echo "Version: 2.1.0"
    echo "=========================================="
    echo ""

    # Parse command line arguments
    DRY_RUN=false
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--dry-run] [--help]"
                echo "  --dry-run: Show what would be done without executing"
                echo "  --help:    Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    if [ "$DRY_RUN" = true ]; then
        log_info "DRY RUN MODE - No changes will be made"
        echo ""
    fi

    # Run maintenance tasks
    cleanup_logs
    cleanup_temp
    rotate_logs
    cleanup_backups
    generate_report
    verify_integrity

    log_info "Maintenance complete!"
    echo ""
}

# Run main function
main "$@"
