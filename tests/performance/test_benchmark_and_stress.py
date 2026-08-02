"""
Unit tests for benchmark and stress harness. These tests ARE NOT intended to run the full stress load during CI.
They validate the harness functions at small scale.
"""
from scripts.benchmark_rule_engine import make_payload, run_benchmark
from scripts.stress_test_rule_engine import run_stress


def test_benchmark_small():
    payload = make_payload(10)
    assert payload and isinstance(payload.get('trial_balance_records'), list)


def test_stress_small():
    results, elapsed = run_stress(n_records=1000)
    assert isinstance(results, list)
    assert elapsed >= 0
