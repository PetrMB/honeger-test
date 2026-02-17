#!/usr/bin/env python3
"""
backup-memory.py — Záloha paměti (MEMORY.md + daily notes) do backup/memory/

Kdy: Každý den v 23:55 (cron job)
"""
import os
import shutil
from pathlib import Path
from datetime import datetime


def backup_memory():
    workspace = Path("~/.openclaw/workspace").expanduser()
    backup_dir = workspace / "backup" / "memory"
    memory_dir = workspace / "memory"
    
    # Vytvoř backup složku
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Zkopíruj MEMORY.md
    src_memory = workspace / "MEMORY.md"
    if src_memory.exists():
        dst_memory = backup_dir / f"MEMORY-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
        shutil.copy2(src_memory, dst_memory)
        print(f"✅ Zálohováno: MEMORY.md → {dst_memory.name}")
    
    # Zkopíruj daily notes
    if memory_dir.exists():
        for md_file in memory_dir.glob("*.md"):
            if md_file.name != "MEMORY.md":
                dst = backup_dir / f"{md_file.name}"
                shutil.copy2(md_file, dst)
                print(f"✅ Zálohováno: {md_file.name}")
    
    print(f"✅ Záloha dokončena: {len(list(backup_dir.glob('*.md')))} souborů")  


if __name__ == "__main__":
    backup_memory()
