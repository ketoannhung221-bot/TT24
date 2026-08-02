"""
Benchmark harness for Rule Engine evaluation.
Generates synthetic canonical payloads and measures average evaluation time per rule.
"""
import time
import random
from services.rule_engine.evaluator import load_rules, evaluate_ruleset

RULES_FILE = 'rules/rules_expanded.json'


def make_record(i):
    return {
        'account_code': str(1000 + (i % 9999)),
        'account_name': f'Acct {i}',
        'closing_debit': float(random.randint(0,10000)),
        'closing_credit': 0.0
    }


def make_payload(n_records=1000):
    return {
        'unit_info': {'unit_code':'ST0001','accounting_period':{'year':2026,'from_date':'2026-01-01','to_date':'2026-12-31'}},
        'trial_balance_records': [ make_record(i) for i in range(n_records) ]
    }


def run_benchmark(n_records=1000, iterations=5):
    rules = load_rules(RULES_FILE)
    payload = make_payload(n_records)
    # warmup
    _ = evaluate_ruleset(rules, payload, context={'config':{}})
    times = []
    for _ in range(iterations):
        start = time.time()
        _ = evaluate_ruleset(rules, payload, context={'config':{}})
        end = time.time()
        times.append(end-start)
    avg = sum(times)/len(times)
    print(f'Benchmark: records={n_records}, iterations={iterations}, avg_seconds={avg:.4f}')


if __name__ == '__main__':
    run_benchmark(n_records=1000, iterations=5)
