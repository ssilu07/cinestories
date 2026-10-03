"""
Automated AMP Validator Runner for CineStories.
Scans all generated story HTML files and verifies 100% AMP compliance using amphtml-validator.
"""

import sys
import subprocess
import shutil
import os
import re
from pathlib import Path
from typing import List, Tuple
from config import STORIES_DIR

def check_amp_files(target_dir: Path = STORIES_DIR) -> Tuple[int, int, List[str]]:
    """
    Validate all index.html files under target_dir in high-speed batches.
    Returns (passed_count, failed_count, error_messages).
    """
    html_files = list(target_dir.glob("*/index.html"))
    if not html_files:
        print(f"[Validator] No story files found in {target_dir}", flush=True)
        return 0, 0, ["No HTML files found to validate."]

    # Find npx or npx.cmd
    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx_cmd:
        print("[Validator] Warning: npx not found in PATH. Skipping CLI validation.", flush=True)
        return len(html_files), 0, []

    passed = 0
    failed = 0
    errors = []

    print(f"\n=======================================================", flush=True)
    print(f"       AMP HTML COMPLIANCE VALIDATION SUITE            ", flush=True)
    print(f"=======================================================", flush=True)
    print(f"Validating {len(html_files)} story files with amphtml-validator...\n", flush=True)

    file_paths = [str(f) for f in html_files]
    is_windows = (os.name == "nt")

    try:
        # Run all files in a single fast batch
        cmd = [npx_cmd, "--yes", "amphtml-validator"] + file_paths
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=is_windows,
            timeout=120
        )
        raw_output = result.stdout + "\n" + result.stderr
        # Strip ANSI terminal escape sequences
        clean_output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', raw_output)

        lines = clean_output.strip().splitlines()
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            if ": PASS" in line_str or line_str.endswith("PASS"):
                passed += 1
                parts = line_str.rsplit(":", 1)
                file_rel = Path(parts[0]).as_posix()
                if "stories/" in file_rel:
                    file_rel = "/stories/" + file_rel.split("stories/")[-1]
                print(f"  [PASS] {file_rel}", flush=True)
            elif ": FAIL" in line_str or "ERROR" in line_str:
                failed += 1
                errors.append(line_str)
                print(f"  [FAIL] {line_str}", flush=True)
    except Exception as e:
        print(f"[Validator] Error running amphtml-validator batch: {e}", flush=True)
        errors.append(str(e))
        failed = len(html_files)

    print(f"\nValidation Summary: {passed} PASSED | {failed} FAILED (Total: {len(html_files)})", flush=True)
    if failed == 0 and passed > 0:
        print(">> 100% AMP VALIDATION SUCCESS: All stories comply with Google Web Story specifications!\n", flush=True)
    else:
        print(">> ATTENTION: Some stories failed AMP validation. Review errors above.\n", flush=True)

    return passed, failed, errors

if __name__ == "__main__":
    passed, failed, errors = check_amp_files()
    sys.exit(0 if failed == 0 else 1)
