#!/usr/bin/env python3
"""
CostPilot Demo Progress Tracker

This script scans checklist.md for completed tasks and updates the progress bar.
Usage: python tools/update_progress.py
"""

import re
import sys
from pathlib import Path
from datetime import datetime


def count_checkboxes(content: str) -> tuple[int, int]:
    """
    Count total and completed checkboxes in markdown content.
    
    Returns:
        tuple: (completed_count, total_count)
    """
    # Match checked boxes: - [x] or - [X]
    checked = len(re.findall(r'^- \[[xX]\]', content, re.MULTILINE))
    
    # Match all boxes: - [ ] and - [x]/[X]
    total = len(re.findall(r'^- \[[ xX]\]', content, re.MULTILINE))
    
    return checked, total


def calculate_percentage(completed: int, total: int) -> float:
    """Calculate completion percentage."""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 1)


def generate_progress_bar(completed: int, total: int) -> str:
    """
    Generate HTML progress bar with gradient.
    
    Args:
        completed: Number of completed tasks
        total: Total number of tasks
        
    Returns:
        str: HTML progress bar markup
    """
    percentage = calculate_percentage(completed, total)
    
    # Choose color gradient based on progress
    if percentage < 33:
        gradient = "linear-gradient(90deg,#dc2626,#ea580c,#f59e0b)"  # Red to orange
    elif percentage < 66:
        gradient = "linear-gradient(90deg,#f59e0b,#eab308,#84cc16)"  # Orange to yellow
    else:
        gradient = "linear-gradient(90deg,#84cc16,#22c55e,#10b981)"  # Yellow to green
    
    progress_bar = f'''<div role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{int(percentage)}" style="width:94%; background:#e6eef0; border-radius:8px; padding:6px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.04);">
  <div style="width:{percentage}%; background:{gradient}; color:#fff; padding:10px 12px; text-align:right; border-radius:6px; font-weight:700; transition:width 0.5s ease;">
    <span style="display:inline-block; background:rgba(0,0,0,0.12); padding:4px 8px; border-radius:999px; font-size:0.95em;">{percentage}% · {completed}/{total}</span>
  </div>
</div>'''
    
    return progress_bar


def update_checklist(file_path: Path) -> bool:
    """
    Update the progress bar in checklist.md.
    
    Args:
        file_path: Path to checklist.md
        
    Returns:
        bool: True if update was successful
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Count checkboxes
        completed, total = count_checkboxes(content)
        percentage = calculate_percentage(completed, total)
        
        # Generate new progress bar
        new_progress_bar = generate_progress_bar(completed, total)
        
        # Replace old progress bar with new one
        # Match the entire progress bar div
        pattern = r'<div role="progressbar"[^>]*>.*?</div>\s*</div>'
        updated_content = re.sub(
            pattern,
            new_progress_bar,
            content,
            count=1,
            flags=re.DOTALL
        )
        
        # Update the "Last Updated" timestamp
        today = datetime.now().strftime('%Y-%m-%d')
        updated_content = re.sub(
            r'\*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}',
            f'**Last Updated:** {today}',
            updated_content
        )
        
        # Update summary section
        summary_pattern = r'\*\*Total Tasks:\*\* \d+\s+\*\*Completed:\*\* \d+\s+\*\*Remaining:\*\* \d+\s+\*\*Progress:\*\* [\d.]+%'
        summary_replacement = f'''**Total Tasks:** {total}  
**Completed:** {completed}  
**Remaining:** {total - completed}  
**Progress:** {percentage}%'''
        
        updated_content = re.sub(
            summary_pattern,
            summary_replacement,
            updated_content
        )
        
        # Write updated content back
        file_path.write_text(updated_content, encoding='utf-8')
        
        return True
        
    except Exception as e:
        print(f"Error updating checklist: {e}", file=sys.stderr)
        return False


def print_report(completed: int, total: int):
    """Print a progress report to console."""
    percentage = calculate_percentage(completed, total)
    remaining = total - completed
    
    print("=" * 60)
    print("CostPilot Demo Progress Report")
    print("=" * 60)
    print(f"Total Tasks:      {total}")
    print(f"Completed:        {completed}")
    print(f"Remaining:        {remaining}")
    print(f"Progress:         {percentage}%")
    print("=" * 60)
    
    # ASCII progress bar
    bar_width = 50
    filled = int((completed / total) * bar_width) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_width - filled)
    print(f"[{bar}]")
    print("=" * 60)
    
    if percentage == 100:
        print("🎉 All tasks completed! Ready for launch! 🚀")
    elif percentage >= 75:
        print("💪 Almost there! Keep pushing!")
    elif percentage >= 50:
        print("👍 Halfway done! Great progress!")
    elif percentage >= 25:
        print("🏃 Good start! Keep going!")
    else:
        print("🌱 Just getting started!")
    
    print("=" * 60)


def main():
    """Main entry point."""
    # Locate checklist.md
    repo_root = Path(__file__).parent.parent
    checklist_path = repo_root / "docs/checklist.md"
    
    if not checklist_path.exists():
        print(f"Error: checklist.md not found at {checklist_path}", file=sys.stderr)
        sys.exit(1)
    
    # Count current progress
    content = checklist_path.read_text(encoding='utf-8')
    completed, total = count_checkboxes(content)
    
    # Print report
    print_report(completed, total)
    
    # Update checklist
    print("\nUpdating checklist.md...")
    if update_checklist(checklist_path):
        print("✅ Progress bar updated successfully!")
        sys.exit(0)
    else:
        print("❌ Failed to update progress bar", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
