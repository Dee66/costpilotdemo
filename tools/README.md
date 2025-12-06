# Tools Directory

This directory contains utility scripts for the CostPilot demo repository.

## Available Tools

### `update_progress.py`

Automatically scans `checklist.md` and updates the progress bar based on completed tasks.

**Usage:**
```bash
python3 tools/update_progress.py
```

**Features:**
- Counts checked (`[x]`) vs unchecked (`[ ]`) checkboxes
- Updates the HTML progress bar with dynamic gradient colors
- Updates the timestamp
- Updates the summary section
- Displays a console progress report with ASCII art

**Progress Colors:**
- 0-33%: Red to Orange gradient 🔴
- 34-66%: Orange to Yellow gradient 🟡
- 67-100%: Yellow to Green gradient 🟢

**Example Output:**
```
============================================================
CostPilot Demo Progress Report
============================================================
Total Tasks:      151
Completed:        45
Remaining:        106
Progress:         29.8%
============================================================
[██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
============================================================
🏃 Good start! Keep going!
============================================================
```

### `reset_demo.sh`

Reset script for restoring the demo environment to its baseline state.

**Status:** Placeholder (to be implemented)

**Planned Features:**
- Restore baseline infrastructure
- Regenerate all snapshots
- Regenerate mapping
- Regenerate trend history
- Validate deterministic hashes
- Fail if drift is detected

---

## Development

To add a new tool:
1. Create the script in this directory
2. Make it executable: `chmod +x tools/your_script.sh`
3. Document it in this README
4. Add any dependencies to the project documentation
