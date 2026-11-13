#!/usr/bin/env python3
"""
Empirical Challenge & Mutation Testing Harness for CineStories E2E Test Suite.
Authored by challenger_e2e_2.
Performs adversarial stress testing, fault injection / mutation analysis,
execution profiling, and concurrency/race-condition verification.
"""

import os
import sys
import time
import json
import shutil
import unittest
import tracemalloc
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

DIST_DIR = ROOT_DIR / "dist"

from compliance_linter import ComplianceLinter
import test_geo_routing_i18n
from test_geo_routing_i18n import GeoRoutingSimulator
import tests.test_e2e_4tiers as e2e_tiers

def run_suite(suite):
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    return runner.run(suite)

def get_geo_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for tc in [
        test_geo_routing_i18n.TestTier1ExplicitUserChoice,
        test_geo_routing_i18n.TestTier2EdgeCdnHeaders,
        test_geo_routing_i18n.TestTier3ClientHeuristics,
        test_geo_routing_i18n.TestTier4SafeFallback,
        test_geo_routing_i18n.TestAdversarialAndCornerCases,
        test_geo_routing_i18n.TestStaticHreflangBidirectionality,
        test_geo_routing_i18n.TestLanguageSwitcherUIAndState,
        test_geo_routing_i18n.TestHindiLocalizationIntegrity,
        test_geo_routing_i18n.TestAmpStoryComplianceForLocalizedPages,
        test_geo_routing_i18n.TestClientSideGeoScriptStructure,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(tc))
    return suite

def get_4tiers_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for tc in [
        e2e_tiers.Tier1FeatureCoverage,
        e2e_tiers.Tier2BoundaryCornerCases,
        e2e_tiers.Tier3CrossFeatureInteractions,
        e2e_tiers.Tier4RealWorldScenarios,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(tc))
    return suite

# ===========================================================================
# 1. MUTATION & FAULT INJECTION TESTING
# ===========================================================================
def test_simulator_mutations():
    print("\n--- 1. SIMULATOR MUTATION & FAULT DETECTION TESTS ---")
    mutations = [
        ("M1: Invert Tier 1 simulate_geo=IN -> en",
         lambda orig: (lambda *args, **kwargs: {"lang": "en", "tier": 1, "reason": "mutated", "is_manual": False, "should_redirect": False, "target_path": "/"} if (kwargs.get("query_params") or {}).get("simulate_geo", "").upper() == "IN" else orig(*args, **kwargs))),
        ("M2: Ignore manual switcher storage override",
         lambda orig: (lambda *args, **kwargs: orig(*args, **{**kwargs, "local_storage": {k: v for k, v in (kwargs.get("local_storage") or {}).items() if k != "cinestories_lang_manual"}}))),
        ("M3: Invert Tier 2 CF-IPCountry=IN -> en",
         lambda orig: (lambda *args, **kwargs: {"lang": "en", "tier": 2, "reason": "mutated", "is_manual": False, "should_redirect": False, "target_path": "/"} if (kwargs.get("edge_headers") or {}).get("CF-IPCountry", "").upper() == "IN" else orig(*args, **kwargs))),
        ("M4: Break Tier 3 Indian timezone detection",
         lambda orig: (lambda *args, **kwargs: {"lang": "en", "tier": 4, "reason": "mutated_tz", "is_manual": False, "should_redirect": False, "target_path": "/"} if (kwargs.get("client_heuristics") or {}).get("timezone") in {"Asia/Kolkata", "Asia/Calcutta", "IST"} else orig(*args, **kwargs))),
        ("M5: Invert Tier 4 default fallback -> hi",
         lambda orig: (lambda *args, **kwargs: {"lang": "hi", "tier": 4, "reason": "mutated_fallback", "is_manual": False, "should_redirect": True, "target_path": "/hi"} if not kwargs.get("query_params") and not kwargs.get("cookies") and not kwargs.get("local_storage") and not kwargs.get("edge_headers") and not kwargs.get("client_heuristics") else orig(*args, **kwargs))),
    ]

    original_func = GeoRoutingSimulator.resolve_language

    results = []
    for name, mutator in mutations:
        mutated_func = mutator(original_func)
        GeoRoutingSimulator.resolve_language = classmethod(mutated_func)
        test_geo_routing_i18n.GeoRoutingSimulator.resolve_language = classmethod(mutated_func)
        e2e_tiers.GeoRoutingSimulator.resolve_language = classmethod(mutated_func)

        # Run test_geo_routing_i18n
        res_geo = run_suite(get_geo_suite())
        geo_caught = len(res_geo.failures) + len(res_geo.errors)

        # Run tests/test_e2e_4tiers.py
        res_e2e = run_suite(get_4tiers_suite())
        e2e_caught = len(res_e2e.failures) + len(res_e2e.errors)

        results.append({
            "mutation": name,
            "geo_routing_suite_caught_failures": geo_caught,
            "geo_routing_suite_passed": res_geo.wasSuccessful(),
            "e2e_4tiers_caught_failures": e2e_caught,
            "e2e_4tiers_passed": res_e2e.wasSuccessful()
        })
        print(f"[{'CAUGHT' if geo_caught > 0 or e2e_caught > 0 else 'MISSED'}] {name}")
        print(f"   -> test_geo_routing_i18n: {geo_caught} failures")
        print(f"   -> test_e2e_4tiers:       {e2e_caught} failures")

    # Restore original
    GeoRoutingSimulator.resolve_language = original_func
    test_geo_routing_i18n.GeoRoutingSimulator.resolve_language = original_func
    e2e_tiers.GeoRoutingSimulator.resolve_language = original_func
    return results

# ===========================================================================
# 2. STATIC ASSET MUTATION / CORRUPTION FAULT DETECTION
# ===========================================================================
def test_static_asset_mutations():
    print("\n--- 2. STATIC ASSET MUTATION / CORRUPTION TESTS ---")
    results = []

    # Test H1: Corrupt title/description in dist/about/index.html
    about_file = DIST_DIR / "about" / "index.html"
    if about_file.exists():
        backup = about_file.read_text(encoding="utf-8")
        try:
            # Corrupt: remove title and description
            corrupted = backup.replace("<title>", "<!--").replace("</title>", "-->").replace('name="description"', 'name="x-desc"')
            about_file.write_text(corrupted, encoding="utf-8")

            linter = ComplianceLinter(dist_dir=DIST_DIR, verbose=False)
            linter.check_rule_1_policy_pages()
            caught_linter = any(v.file_path == "about/index.html" or "about" in v.file_path for v in linter.violations)

            res_e2e = run_suite(get_4tiers_suite())
            caught_e2e = not res_e2e.wasSuccessful()

            results.append({
                "test": "H1: Strip title & description in dist/about/index.html",
                "compliance_linter_caught": caught_linter,
                "e2e_4tiers_caught": caught_e2e,
            })
            print(f"[{'CAUGHT' if caught_linter else 'MISSED'}] H1: Strip title & description in dist/about/index.html")
            print(f"   -> compliance_linter caught: {caught_linter}")
            print(f"   -> e2e_4tiers caught:        {caught_e2e}")
        finally:
            about_file.write_text(backup, encoding="utf-8")

    # Test H2: Inject broken link into dist/index.html
    home_file = DIST_DIR / "index.html"
    if home_file.exists():
        backup = home_file.read_text(encoding="utf-8")
        try:
            corrupted = backup.replace("</body>", '<a href="/nonexistent-dead-link-12345/">Dead Link</a></body>')
            home_file.write_text(corrupted, encoding="utf-8")

            linter = ComplianceLinter(dist_dir=DIST_DIR, verbose=False)
            linter.check_rule_7_internal_links()
            caught_linter = any("nonexistent-dead-link-12345" in v.message for v in linter.violations)

            res_e2e = run_suite(get_4tiers_suite())
            caught_e2e = not res_e2e.wasSuccessful()

            results.append({
                "test": "H2: Inject broken internal link in dist/index.html",
                "compliance_linter_caught": caught_linter,
                "e2e_4tiers_caught": caught_e2e,
            })
            print(f"[{'CAUGHT' if caught_linter else 'MISSED'}] H2: Inject broken internal link in dist/index.html")
            print(f"   -> compliance_linter caught: {caught_linter}")
            print(f"   -> e2e_4tiers caught:        {caught_e2e}")
        finally:
            home_file.write_text(backup, encoding="utf-8")

    # Test H3: Inject banned placeholder 'TODO' in contact page
    contact_file = DIST_DIR / "contact" / "index.html"
    if contact_file.exists():
        backup = contact_file.read_text(encoding="utf-8")
        try:
            corrupted = backup.replace("</body>", "<p>TODO: update this address</p></body>")
            contact_file.write_text(corrupted, encoding="utf-8")

            linter = ComplianceLinter(dist_dir=DIST_DIR, verbose=False)
            linter.check_rule_2_ownership_and_contact()
            caught_linter = any("TODO" in v.message for v in linter.violations)

            res_e2e = run_suite(get_4tiers_suite())
            caught_e2e = not res_e2e.wasSuccessful()

            results.append({
                "test": "H3: Inject 'TODO' placeholder in dist/contact/index.html",
                "compliance_linter_caught": caught_linter,
                "e2e_4tiers_caught": caught_e2e,
            })
            print(f"[{'CAUGHT' if caught_linter else 'MISSED'}] H3: Inject 'TODO' placeholder in dist/contact/index.html")
            print(f"   -> compliance_linter caught: {caught_linter}")
            print(f"   -> e2e_4tiers caught:        {caught_e2e}")
        finally:
            contact_file.write_text(backup, encoding="utf-8")

    return results

# ===========================================================================
# 3. PERFORMANCE & MEMORY PROFILING
# ===========================================================================
def profile_performance():
    print("\n--- 3. PERFORMANCE & MEMORY BENCHMARKING ---")
    benchmarks = {}

    # Benchmark 1: test_geo_routing_i18n.py
    tracemalloc.start()
    t0 = time.time()
    res_geo = run_suite(get_geo_suite())
    cur, peak_geo = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    benchmarks["test_geo_routing_i18n"] = {
        "tests_run": res_geo.testsRun,
        "elapsed_seconds": round(time.time() - t0, 3),
        "peak_memory_mb": round(peak_geo / 1048576, 2)
    }

    # Benchmark 2: tests/test_e2e_4tiers.py
    tracemalloc.start()
    t0 = time.time()
    res_e2e = run_suite(get_4tiers_suite())
    cur, peak_e2e = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    benchmarks["test_e2e_4tiers"] = {
        "tests_run": res_e2e.testsRun,
        "elapsed_seconds": round(time.time() - t0, 3),
        "peak_memory_mb": round(peak_e2e / 1048576, 2)
    }

    # Benchmark 3: compliance_linter rules
    linter_bench = {}
    for r in range(1, 9):
        tracemalloc.start()
        t0 = time.time()
        l = ComplianceLinter(dist_dir=DIST_DIR, verbose=False)
        l.run_all(rules_to_run=[r], run_cli_validator=False)
        cur, peak_r = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        linter_bench[f"Rule_{r}"] = {
            "elapsed_seconds": round(time.time() - t0, 3),
            "peak_memory_mb": round(peak_r / 1048576, 2),
            "violations": len(l.violations)
        }
    benchmarks["compliance_linter_rules"] = linter_bench

    for suite_name, data in benchmarks.items():
        if "tests_run" in data:
            print(f"Suite: {suite_name:<25} | Tests: {data['tests_run']:<4} | Time: {data['elapsed_seconds']:<6}s | Peak RAM: {data['peak_memory_mb']} MB")
        else:
            print(f"Compliance Linter Rules Breakdown:")
            total_time = 0
            for r_name, r_data in data.items():
                total_time += r_data['elapsed_seconds']
                print(f"   {r_name:<10}: Time: {r_data['elapsed_seconds']:<6}s | Peak RAM: {r_data['peak_memory_mb']:<6} MB | Violations: {r_data['violations']}")
            print(f"   TOTAL COMPLIANCE TIME: {total_time:.2f}s")

    return benchmarks

# ===========================================================================
# 4. CONCURRENCY & RACE CONDITIONS
# ===========================================================================
def test_concurrency():
    print("\n--- 4. CONCURRENCY & RACE CONDITION STRESS TEST ---")
    threads = 10
    iterations = 20

    def concurrent_geo_task(worker_id):
        # Stress resolve_language with varying inputs across threads
        errors = 0
        for i in range(iterations):
            # Alternating requests
            if i % 3 == 0:
                res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "IN"})
                if res["lang"] != "hi":
                    errors += 1
            elif i % 3 == 1:
                res = GeoRoutingSimulator.resolve_language(
                    edge_headers={"CF-IPCountry": "IN"},
                    local_storage={"cinestories_lang": "en", "cinestories_lang_manual": "true"}
                )
                if res["lang"] != "en":
                    errors += 1
            else:
                res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "Asia/Kolkata"})
                if res["lang"] != "hi":
                    errors += 1
        return errors

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(concurrent_geo_task, i) for i in range(threads)]
        total_errors = sum(f.result() for f in futures)
    elapsed = time.time() - t0

    print(f"Ran {threads * iterations} concurrent geo resolutions across {threads} threads in {elapsed:.3f}s.")
    print(f"Race condition errors detected: {total_errors}")

    return {
        "threads": threads,
        "iterations_per_thread": iterations,
        "total_operations": threads * iterations,
        "elapsed_seconds": round(elapsed, 3),
        "errors": total_errors,
        "thread_safe": total_errors == 0
    }

def main():
    print("=" * 70)
    print("      CINESTORIES EMPIRICAL CHALLENGE & STRESS HARNESS       ")
    print("=" * 70)

    sim_mut_results = test_simulator_mutations()
    static_mut_results = test_static_asset_mutations()
    perf_results = profile_performance()
    concurrency_results = test_concurrency()

    summary = {
        "simulator_mutations": sim_mut_results,
        "static_asset_mutations": static_mut_results,
        "performance": perf_results,
        "concurrency": concurrency_results
    }

    report_path = ROOT_DIR / "tests" / "empirical_challenge_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print(f"Empirical results written to: {report_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
