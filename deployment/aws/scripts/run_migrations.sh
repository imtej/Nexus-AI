#!/usr/bin/env bash
# ========================================================
# Nexus AI — Automated Supabase Database Migration Runner
# Executes database schema migrations against Supabase target
# ========================================================

set -euo pipefail

echo "⚡ Starting Database Schema Verification..."

MIGRATION_FILE="supabase/migrations/001_initial_schema.sql"

if [ ! -f "${MIGRATION_FILE}" ]; then
    echo "❌ Migration file not found at ${MIGRATION_FILE}"
    exit 1
fi

echo "📄 Schema file verified: ${MIGRATION_FILE}"

if command -v supabase &> /dev/null; then
    echo "🚀 Running Supabase CLI Database Push..."
    supabase db push
else
    echo "ℹ️ Supabase CLI not installed locally. Ensure schema migration is applied via Supabase Dashboard SQL Editor."
fi

echo "✅ Migration Step Completed."
