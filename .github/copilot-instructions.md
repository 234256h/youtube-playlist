# GitHub Copilot Instructions for YouTube Playlist Project

## Project Overview

This is a YouTube Playlist Duration Calculator and Player - a web application that helps users calculate total playlist duration and play videos with custom start/end times.

**Key Features:**
- YouTube API integration for playlist data
- Playlist duration calculation
- Custom video player with start/end time support
- Shareable playlist links
- Top-of-hour countdown feature

## Tech Stack

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **APIs**: YouTube Data API v3, YouTube IFrame API
- **Storage**: Browser localStorage for playlist data

## Issue Tracking with bd (beads)

**CRITICAL**: This project uses **bd** for ALL task tracking. Do NOT create markdown TODO lists.

### Essential Commands

```bash
# Find work
bd ready --json                    # Unblocked issues
bd stale --days 30 --json          # Forgotten issues

# Create and manage
bd create "Title" -t bug|feature|task -p 0-4 --json
bd create "Subtask" --parent <epic-id> --json  # Hierarchical subtask
bd update <id> --status in_progress --json
bd close <id> --reason "Done" --json

# Search
bd list --status open --priority 1 --json
bd show <id> --json

# Sync (CRITICAL at end of session!)
bd sync  # Force immediate export/commit/push
```

### Workflow

1. **Check ready work**: `bd ready --json`
2. **Claim task**: `bd update <id> --status in_progress`
3. **Work on it**: Implement, test, document
4. **Discover new work?** `bd create "Found bug" -p 1 --deps discovered-from:<parent-id> --json`
5. **Complete**: `bd close <id> --reason "Done" --json`
6. **Sync**: `bd sync` (flushes changes to git immediately)

### Priorities

- `0` - Critical (security, data loss, broken functionality)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

## Project Structure

```
youtube-playlist/
├── index.html                    # Main playlist player (updated version)
├── playlist-v2.html             # Alternative playlist calculator
├── .beads/
│   ├── beads.db                 # SQLite database (DO NOT COMMIT)
│   └── issues.jsonl             # Git-synced issue storage
└── .beads-hooks/                # Git hooks for auto-sync
```

## Coding Guidelines

### HTML/CSS/JavaScript
- Keep code in single HTML files for simplicity
- Use vanilla JavaScript (no frameworks required)
- Follow existing code style and naming conventions
- Test in multiple browsers when making UI changes
- Ensure mobile responsiveness

### YouTube API
- Use existing API key or request new one if needed
- Handle API errors gracefully
- Respect rate limits
- Cache playlist data when possible

### Git Workflow
- Always commit `.beads/issues.jsonl` with code changes
- Run `bd sync` at end of work sessions
- Git hooks auto-sync on commits/merges/checkouts

## CLI Help

Run `bd <command> --help` to see all available flags for any command.
For example: `bd create --help` shows `--parent`, `--deps`, `--assignee`, etc.

## Important Rules

- ✅ Use bd for ALL task tracking
- ✅ Always use `--json` flag for programmatic use
- ✅ Run `bd sync` at end of sessions
- ✅ Test changes in browser before committing
- ✅ Run `bd <cmd> --help` to discover available flags
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems
- ❌ Do NOT commit `.beads/beads.db` (JSONL only)

---

**For detailed workflows and advanced features, see [AGENTS.md](../AGENTS.md)**

