#!/usr/bin/env python3
"""
Master E2E Test Runner Harness for CineStories (Remediated Iteration 2).
Orchestrates the complete 4-tier E2E test suite, specialized quality linters,
and adversarial stress suites with STRICT PASS/FAIL SEMANTICS by default.

Usage:
    python run_e2e_tests.py [OPTIONS]

Options:
    --tier {1,2,3,4,all}   Run specific tier or all tiers (default: all)
    --include-stress       Include adversarial carousel & viewport stress tests
    --include-amp          Include batch AMP validation via amphtml-validator
    --compliance-only      Run only the Google AdSense & Search Essentials linter
    --geo-only             Run only the Geo-Routing & I18n test suite
    --fail-fast            Exit immediately on first test failure
    --strict-compliance    Enforce strict compliance (DEFAULT: True; fails runner on any violation)
    --allow-compliance-failures
                           Run compliance linter, but permit violations without failing
                           the master runner overall status (for intermediate dev)
    --skip-compliance      Skip running the compliance linter entirely
    --json-report PATH     Path to emit structured JSON report (default: dist/e2e_report.json)
    --verbose, -v          Verbose output logging
"""

import os
import sys
import time
import json
import argparse
import unittest
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

DIST_DIR = ROOT_DIR / "dist"

from compliance_linter import ComplianceLinter
from test_geo_routing_i18n import (
    TestTier1ExplicitUserChoice,
    TestTier2EdgeCdnHeaders,
    TestTier3ClientHeuristics,
    TestTier4SafeFallback,
    TestAdversarialAndCornerCases,
    TestStaticHreflangBidirectionality,
    TestLanguageSwitcherUIAndState,
    TestHindiLocalizationIntegrity,
    TestAmpStoryComplianceForLocalizedPages,
    TestClientSideGeoScriptStructure,
)
from tests.test_e2e_4tiers import (
    Tier1FeatureCoverage,
    Tier2BoundaryCornerCases,
    Tier3CrossFeatureInteractions,
    Tier4RealWorldScenarios,
)


class E2ETestRunner:
    def __init__(
        self,
        tier: str = "all",
        include_stress: bool = False,
        include_amp: bool = False,
        compliance_only: bool = False,
        geo_only: bool = False,
        fail_fast: bool = False,
        strict_compliance: bool = True,
        allow_compliance_failures: bool = False,
        skip_compliance: bool = False,
        json_report: str = "dist/e2e_report.json",
        verbose: bool = False,
    ):
        self.tier = tier
        self.include_stress = include_stress
        self.include_amp = include_amp
        self.compliance_only = compliance_only
        self.geo_only = geo_only
        self.fail_fast = fail_fast

        # Compliance Mode Resolution:
        # Default is STRICT compliance.
        # If --allow-compliance-failures is set, strict_compliance is overridden to False.
        # If --skip-compliance is set, compliance checking is bypassed.
        if allow_compliance_failures:
            self.strict_compliance = False
            self.allow_compliance_failures = True
        else:
            self.strict_compliance = strict_compliance
            self.allow_compliance_failures = False

        self.skip_compliance = skip_compliance
        self.json_report_path = Path(json_report)
        self.verbose = verbose

        self.report_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "execution_mode": (
                "skip_compliance" if self.skip_compliance
                else ("allow_compliance_failures" if self.allow_compliance_failures else "strict")
            ),
            "summary": {},
            "tiers": {},
            "specialized_checks": {},
        }

    def run_tier_suite(self, tier_classes: list, tier_key: str) -> unittest.TestResult:
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for cls in tier_classes:
            suite.addTests(loader.loadTestsFromTestCase(cls))

        runner = unittest.TextTestRunner(verbosity=2 if self.verbose else 1, failfast=self.fail_fast)
        result = runner.run(suite)

        passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
        failed = len(result.failures) + len(result.errors)
        skipped = len(result.skipped)

        self.report_data["tiers"][tier_key] = {
            "count": result.testsRun,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
        }
        return result

    def execute(self) -> int:
        start_time = time.time()
        overall_success = True
        compliance_allowed_warning = False

        mode_str = (
            "SKIP COMPLIANCE" if self.skip_compliance
            else ("PERMISSIVE (allow-failures)" if self.allow_compliance_failures else "STRICT (default)")
        )

        print("=" * 80)
        print("          CINESTORIES MASTER E2E TEST RUNNER HARNESS          ")
        print("=" * 80)
        print(f"Start Time       : {self.report_data['timestamp']}")
        print(f"Target Directory : {DIST_DIR}")
        print(f"Compliance Mode  : {mode_str}")
        print(f"Selected Scope   : tier={self.tier}, stress={self.include_stress}, amp={self.include_amp}")
        print("-" * 80)

        # -------------------------------------------------------------
        # Mode 1: Compliance Only
        # -------------------------------------------------------------
        if self.compliance_only:
            linter = ComplianceLinter(dist_dir=DIST_DIR, verbose=self.verbose)
            linter_ok = linter.run_all(run_cli_validator=self.include_amp)
            violations_count = len(linter.violations)

            self.report_data["specialized_checks"]["compliance_linter"] = {
                "status": "PASS" if linter_ok else "FAIL",
                "violations_count": violations_count,
                "scanned_counts": linter.scanned_counts,
            }

            final_success = linter_ok or self.allow_compliance_failures
            overall_status = "PASS" if linter_ok else ("PASS_WITH_WARNINGS" if self.allow_compliance_failures else "FAIL")

            self.report_data["summary"] = {
                "overall_status": overall_status,
                "exit_code": 0 if final_success else 1,
                "duration_seconds": round(time.time() - start_time, 2),
                "compliance_status": "PASS" if linter_ok else "FAIL",
                "compliance_violations": violations_count,
            }
            self._save_report(time.time() - start_time, final_success)
            self._print_banner(final_success, overall_status, violations_count, 0, 0, 0)
            return 0 if final_success else 1

        # -------------------------------------------------------------
        # Mode 2: Geo Only
        # -------------------------------------------------------------
        if self.geo_only:
            geo_classes = [
                TestTier1ExplicitUserChoice,
                TestTier2EdgeCdnHeaders,
                TestTier3ClientHeuristics,
                TestTier4SafeFallback,
                TestAdversarialAndCornerCases,
                TestStaticHreflangBidirectionality,
                TestLanguageSwitcherUIAndState,
                TestHindiLocalizationIntegrity,
                TestAmpStoryComplianceForLocalizedPages,
                TestClientSideGeoScriptStructure,
            ]
            geo_result = self.run_tier_suite(geo_classes, "geo_routing_i18n")
            geo_ok = geo_result.wasSuccessful()
            passed = geo_result.testsRun - len(geo_result.failures) - len(geo_result.errors) - len(geo_result.skipped)
            failed = len(geo_result.failures) + len(geo_result.errors)
            skipped = len(geo_result.skipped)

            self.report_data["summary"] = {
                "overall_status": "PASS" if geo_ok else "FAIL",
                "exit_code": 0 if geo_ok else 1,
                "duration_seconds": round(time.time() - start_time, 2),
                "geo_tests": {
                    "count": geo_result.testsRun,
                    "passed": passed,
                    "failed": failed,
                    "skipped": skipped,
                },
            }
            self._save_report(time.time() - start_time, geo_ok)
            self._print_banner(geo_ok, "PASS" if geo_ok else "FAIL", 0, geo_result.testsRun, passed, failed)
            return 0 if geo_ok else 1

        # -------------------------------------------------------------
        # Standard Orchestrated Run: 4 Tiers
        # -------------------------------------------------------------
        tier_mappings = [
            ("1", "tier_1_feature_coverage", [Tier1FeatureCoverage]),
            ("2", "tier_2_boundary_corner", [Tier2BoundaryCornerCases]),
            ("3", "tier_3_cross_feature", [Tier3CrossFeatureInteractions]),
            ("4", "tier_4_real_world", [Tier4RealWorldScenarios]),
        ]

        four_tier_total = 0
        four_tier_passed = 0
        four_tier_failed = 0
        four_tier_skipped = 0
        tier_status_map = {}

        for t_id, t_key, t_classes in tier_mappings:
            if self.tier in ["all", t_id]:
                print(f"\n[RUNNING] Tier {t_id} ({t_key.replace('_', ' ').title()})...")
                res = self.run_tier_suite(t_classes, t_key)
                passed = res.testsRun - len(res.failures) - len(res.errors) - len(res.skipped)
                failed = len(res.failures) + len(res.errors)
                skipped = len(res.skipped)

                four_tier_total += res.testsRun
                four_tier_passed += passed
                four_tier_failed += failed
                four_tier_skipped += skipped
                tier_status_map[t_key] = "PASS" if res.wasSuccessful() else "FAIL"

                if not res.wasSuccessful():
                    overall_success = False
                    if self.fail_fast:
                        print(f"[FAIL-FAST] Halting execution due to failure in Tier {t_id}.")
                        break
            else:
                tier_status_map[t_key] = "SKIPPED"

        # -------------------------------------------------------------
        # Specialized Runner: Geo-Routing & I18n Suite
        # -------------------------------------------------------------
        print("\n[RUNNING] Geo-Routing & I18n Verification Suite...")
        geo_classes = [
            TestTier1ExplicitUserChoice,
            TestTier2EdgeCdnHeaders,
            TestTier3ClientHeuristics,
            TestTier4SafeFallback,
            TestAdversarialAndCornerCases,
            TestStaticHreflangBidirectionality,
            TestLanguageSwitcherUIAndState,
            TestHindiLocalizationIntegrity,
            TestAmpStoryComplianceForLocalizedPages,
            TestClientSideGeoScriptStructure,
        ]
        geo_res = self.run_tier_suite(geo_classes, "geo_routing_i18n")
        geo_ok = geo_res.wasSuccessful()
        geo_passed = geo_res.testsRun - len(geo_res.failures) - len(geo_res.errors) - len(geo_res.skipped)
        geo_failed = len(geo_res.failures) + len(geo_res.errors)
        geo_skipped = len(geo_res.skipped)

        if not geo_ok:
            overall_success = False

        self.report_data["specialized_checks"]["geo_routing_i18n"] = {
            "status": "PASS" if geo_ok else "FAIL",
            "tests_run": geo_res.testsRun,
            "passed": geo_passed,
            "failed": geo_failed,
            "skipped": geo_skipped,
        }

        # -------------------------------------------------------------
        # Specialized Runner: Compliance Linter
        # -------------------------------------------------------------
        linter_violations = 0
        compliance_status = "SKIPPED"

        if self.skip_compliance:
            print("\n[SKIPPING] Google AdSense & Search Essentials Compliance Linter (--skip-compliance)...")
            self.report_data["specialized_checks"]["compliance_linter"] = {
                "status": "SKIPPED",
                "reason": "--skip-compliance specified",
            }
        else:
            print("\n[RUNNING] Google AdSense & Search Essentials Compliance Linter...")
            linter = ComplianceLinter(dist_dir=DIST_DIR, verbose=False)
            linter_ok = linter.run_all(run_cli_validator=self.include_amp)
            linter_violations = len(linter.violations)
            compliance_status = "PASS" if linter_ok else "FAIL"

            self.report_data["specialized_checks"]["compliance_linter"] = {
                "status": compliance_status,
                "violations_count": linter_violations,
                "scanned_counts": linter.scanned_counts,
                "mode": "allow_failures" if self.allow_compliance_failures else "strict",
            }

            if not linter_ok:
                if self.allow_compliance_failures:
                    print("\n[NON-STRICT NOTICE] Compliance failures permitted via --allow-compliance-failures.")
                    compliance_allowed_warning = True
                else:
                    # STRICT COMPLIANCE BY DEFAULT: FAILS MASTER RUNNER
                    print("\n[STRICT FAILURE] Compliance linter detected violations. Runner marked as FAIL.")
                    overall_success = False

        # -------------------------------------------------------------
        # Optional: Stress Tests
        # -------------------------------------------------------------
        stress_overall = "SKIPPED"
        if self.include_stress:
            print("\n[RUNNING] Adversarial Viewport & Carousel Stress Tests...")
            stress_status = {}
            stress_ok = True
            try:
                import adversarial_carousel_stress_test
                stress_status["carousel"] = "PASS"
            except Exception as e:
                stress_status["carousel"] = f"FAIL: {e}"
                stress_ok = False
                overall_success = False

            try:
                import adversarial_viewport_text_stress_test
                stress_status["viewport_text"] = "PASS"
            except Exception as e:
                stress_status["viewport_text"] = f"FAIL: {e}"
                stress_ok = False
                overall_success = False

            stress_overall = "PASS" if stress_ok else "FAIL"
            self.report_data["specialized_checks"]["stress_tests"] = {
                "status": stress_overall,
                "details": stress_status,
            }

        # -------------------------------------------------------------
        # Optional: AMP Batch Validation
        # -------------------------------------------------------------
        amp_overall = "SKIPPED"
        if self.include_amp:
            print("\n[RUNNING] Batch AMP Validation via validator.py...")
            try:
                import validator
                passed_amp, failed_amp, amp_errors = validator.check_amp_files()
                amp_ok = (failed_amp == 0)
                amp_overall = "PASS" if amp_ok else "FAIL"
                self.report_data["specialized_checks"]["amp_validator"] = {
                    "status": amp_overall,
                    "passed": passed_amp,
                    "failed": failed_amp,
                    "errors": amp_errors,
                }
                if not amp_ok:
                    overall_success = False
            except Exception as e:
                amp_overall = "FAIL"
                self.report_data["specialized_checks"]["amp_validator"] = {
                    "status": f"ERROR: {e}"
                }
                overall_success = False

        # -------------------------------------------------------------
        # Summary & Exit Code Calculation
        # -------------------------------------------------------------
        elapsed = time.time() - start_time
        total_automated_tests = four_tier_total + geo_res.testsRun
        total_passed = four_tier_passed + geo_passed
        total_failed = four_tier_failed + geo_failed
        total_skipped = four_tier_skipped + geo_skipped

        if overall_success:
            overall_status = "PASS_WITH_WARNINGS" if compliance_allowed_warning else "PASS"
        else:
            overall_status = "FAIL"

        components_summary = {
            "tier_1_feature_coverage": tier_status_map.get("tier_1_feature_coverage", "SKIPPED"),
            "tier_2_boundary_corner": tier_status_map.get("tier_2_boundary_corner", "SKIPPED"),
            "tier_3_cross_feature": tier_status_map.get("tier_3_cross_feature", "SKIPPED"),
            "tier_4_real_world": tier_status_map.get("tier_4_real_world", "SKIPPED"),
            "geo_routing_i18n": "PASS" if geo_ok else "FAIL",
            "compliance_linter": compliance_status,
            "stress_tests": stress_overall,
            "amp_validator": amp_overall,
        }

        self.report_data["summary"] = {
            "overall_status": overall_status,
            "exit_code": 0 if overall_success else 1,
            "duration_seconds": round(elapsed, 2),
            "mode": (
                "skip_compliance" if self.skip_compliance
                else ("allow_compliance_failures" if self.allow_compliance_failures else "strict")
            ),
            "four_tier_tests": {
                "count": four_tier_total,
                "passed": four_tier_passed,
                "failed": four_tier_failed,
                "skipped": four_tier_skipped,
            },
            "geo_routing_tests": {
                "count": geo_res.testsRun,
                "passed": geo_passed,
                "failed": geo_failed,
                "skipped": geo_skipped,
            },
            "total_automated_tests": total_automated_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "compliance_violations": linter_violations,
            "components": components_summary,
        }

        self._save_report(elapsed, overall_success)
        self._print_summary(
            overall_status=overall_status,
            overall_success=overall_success,
            elapsed=elapsed,
            components=components_summary,
            four_tier=(four_tier_total, four_tier_passed, four_tier_failed, four_tier_skipped),
            geo=(geo_res.testsRun, geo_passed, geo_failed, geo_skipped),
            compliance_violations=linter_violations,
            compliance_allowed=compliance_allowed_warning,
        )

        return 0 if overall_success else 1

    def _save_report(self, elapsed: float, overall_success: bool):
        try:
            self.json_report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.json_report_path, "w", encoding="utf-8") as f:
                json.dump(self.report_data, f, indent=2)
            print(f"\n[REPORT] Saved structured report to: {self.json_report_path}")
        except Exception as e:
            print(f"[REPORT ERROR] Could not save JSON report: {e}", file=sys.stderr)

    def _print_summary(
        self,
        overall_status: str,
        overall_success: bool,
        elapsed: float,
        components: Dict[str, str],
        four_tier: tuple,
        geo: tuple,
        compliance_violations: int,
        compliance_allowed: bool,
    ):
        print("\n" + "=" * 80)
        print("                      E2E TEST EXECUTION SUMMARY                      ")
        print("=" * 80)
        print("Component Status Breakdown:")
        for comp, status in components.items():
            disp_name = comp.replace("_", " ").title()
            print(f"  - {disp_name:<32}: [{status}]")
        print("-" * 80)
        print(f"4-Tier Test Suite     : {four_tier[0]} run ({four_tier[1]} passed, {four_tier[2]} failed, {four_tier[3]} skipped)")
        print(f"Geo-Routing & I18n    : {geo[0]} run ({geo[1]} passed, {geo[2]} failed, {geo[3]} skipped)")
        total_run = four_tier[0] + geo[0]
        total_p = four_tier[1] + geo[1]
        total_f = four_tier[2] + geo[2]
        total_s = four_tier[3] + geo[3]
        print(f"Combined Automated    : {total_run} run ({total_p} passed, {total_f} failed, {total_s} skipped)")
        print(f"Compliance Violations : {compliance_violations}")
        print(f"Execution Duration    : {elapsed:.2f} seconds")
        print(f"Strict Compliance     : {'DISABLED (--allow-compliance-failures)' if compliance_allowed else ('DISABLED (--skip-compliance)' if self.skip_compliance else 'ENABLED (Default)')}")
        print("-" * 80)

        if overall_status == "PASS":
            print(">>> OVERALL STATUS: [PASS] All executed suites and checks PASSED cleanly! <<<")
        elif overall_status == "PASS_WITH_WARNINGS":
            print(f">>> OVERALL STATUS: [PASS_WITH_WARNINGS] Test suites passed; {compliance_violations} compliance violations permitted via --allow-compliance-failures. <<<")
        else:
            print(">>> OVERALL STATUS: [FAIL] One or more test suites or compliance checks FAILED! <<<")
        print("=" * 80)

    def _print_banner(self, success: bool, status: str, violations: int, total: int, passed: int, failed: int):
        print("\n" + "=" * 80)
        print(f">>> OVERALL STATUS: [{status}] (success={success}) <<<")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="CineStories Master E2E Test Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all", help="Tier to run")
    parser.add_argument("--include-stress", action="store_true", help="Include stress test suites")
    parser.add_argument("--include-amp", action="store_true", help="Include batch AMP validation")
    parser.add_argument("--compliance-only", action="store_true", help="Run only compliance linter")
    parser.add_argument("--geo-only", action="store_true", help="Run only geo-routing & i18n suite")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")
    parser.add_argument(
        "--strict-compliance",
        action="store_true",
        default=True,
        help="Enforce strict compliance (DEFAULT: True; fails runner on any compliance violation)"
    )
    parser.add_argument(
        "--allow-compliance-failures",
        action="store_true",
        default=False,
        help="Run compliance linter, record violations, but do not fail overall runner status if violations are found"
    )
    parser.add_argument(
        "--skip-compliance",
        action="store_true",
        default=False,
        help="Skip running compliance linter entirely"
    )
    parser.add_argument("--json-report", default="dist/e2e_report.json", help="Report output path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose test logging")
    args = parser.parse_args()

    runner = E2ETestRunner(
        tier=args.tier,
        include_stress=args.include_stress,
        include_amp=args.include_amp,
        compliance_only=args.compliance_only,
        geo_only=args.geo_only,
        fail_fast=args.fail_fast,
        strict_compliance=args.strict_compliance,
        allow_compliance_failures=args.allow_compliance_failures,
        skip_compliance=args.skip_compliance,
        json_report=args.json_report,
        verbose=args.verbose,
    )
    sys.exit(runner.execute())


if __name__ == "__main__":
    main()
