"""
Stress test that constructs a payload with >=100,000 trial_balance_records to simulate heavy evaluation.
This is intended to be run on a machine with sufficient memory and CPU.
"""
import time
from services.rule_engine.evaluator import load_rules, evaluate_ruleset

RULES_FILE = 'rules/rules_expanded.json'


def make_record(i):
    return {
        'account_code': str(1000 + (i % 9999)),
        'account_name': f'Acct {i}',
        'closing_debit': float(i % 1000),
        'closing_credit': 0.0
    }


def run_stress(n_records=100000):
    rules = load_rules(RULES_FILE)
    payload = {
        'unit_info': {'unit_code':'ST0001','accounting_period':{'year':2026,'from_date':'2026-01-01','to_date':'2026-12-31'}},
        'trial_balance_records': [ make_record(i) for i in range(n_records) ]
    }
    start = time.time()
    results = evaluate_ruleset(rules, payload, context={'config':{}})
    elapsed = time.time() - start
    print(f'Stress test: records={n_records}, elapsed_seconds={elapsed:.3f}')
    return results, elapsed


if __name__ == '__main__':
    run_stress()
