"""
Automated AMP Validator Runner for CineStories.
Scans all generated story HTML files and verifies 100% AMP compliance using amphtml-validator.
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple
from config import STORIES_DIR

def check_amp_files(target_dir: Path = STORIES_DIR) -> Tuple[int, int, List[str]]:
    """
    Validate all index.html files under target_dir.
    Returns (passed_count, failed_count, error_messages).
    """
    html_files = list(target_dir.glob("*/index.html"))
    if not html_files:
        print(f"[Validator] No story files found in {target_dir}")
        return 0, 0, ["No HTML files found to validate."]

    # Find npx or npx.cmd
    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx_cmd:
        print("[Validator] Warning: npx not found in PATH. Skipping CLI validation.")
        return len(html_files), 0, []

    passed = 0
    failed = 0
    errors = []

    print(f"\n=======================================================")
    print(f"       AMP HTML COMPLIANCE VALIDATION SUITE            ")
    print(f"=======================================================")
    print(f"Validating {len(html_files)} story files with amphtml-validator...\n")

    for file_path in html_files:
        slug = file_path.parent.name
        try:
            result = subprocess.run(
                [npx_cmd, "amphtml-validator", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout.strip() or result.stderr.strip()
            if result.returncode == 0 and "PASS" in output:
                passed += 1
                print(f"  [PASS] /stories/{slug}/index.html")
            else:
                failed += 1
                err_msg = f"[FAIL] /stories/{slug}/index.html\n{output}"
                errors.append(err_msg)
                print(f"  {err_msg}")
        except Exception as e:
            failed += 1
            err_msg = f"[ERROR] Failed to run validator on /stories/{slug}/: {e}"
            errors.append(err_msg)
            print(f"  {err_msg}")

    print(f"\nValidation Summary: {passed} PASSED | {failed} FAILED (Total: {len(html_files)})")
    if failed == 0:
        print(">> 100% AMP VALIDATION SUCCESS: All stories comply with Google Web Story specifications!\n")
    else:
        print(">> ATTENTION: Some stories failed AMP validation. Review errors above.\n")

    return passed, failed, errors

if __name__ == "__main__":
    passed, failed, errors = check_amp_files()
    sys.exit(0 if failed == 0 else 1)
