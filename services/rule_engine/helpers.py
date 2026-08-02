"""
Updated helpers: add 'sum' helper and ensure helpers_map registration includes 'sum'.
"""
from typing import Any, Dict, List


def sum_field(arr, field_path):
    # field_path like 'opening_debit' relative to items in arr
    s = 0.0
    if not isinstance(arr, list):
        return 0.0
    for item in arr:
        v = None
        if isinstance(item, dict):
            v = item.get(field_path)
        if v is None:
            continue
        try:
            s += float(v)
        except Exception:
            pass
    return s


def exists_duplicate(attachments: List[Dict], keys: List[str]) -> bool:
    seen = set()
    for a in attachments or []:
        vals = tuple((a.get('meta', {}).get(k) if a.get('meta', {}).get(k) is not None else a.get(k)) for k in keys)
        if vals in seen:
            return True
        seen.add(vals)
    return False


def match_reconciliation(account_prefix_a, account_prefix_b, attachments):
    for a in attachments or []:
        fname = a.get('original_filename','').lower()
        if 'recon' in fname or 'reconc' in fname or 'doi' in fname or 'doi_chieu' in fname or 'reconciliation' in fname:
            return True
    return False


def check_continuity_account(account_code, historical_data):
    if not historical_data:
        return False
    for rec in historical_data.get('trial_balance_records',[]) or []:
        if rec.get('account_code') == account_code:
            return True
    return False


def exists_in_chart_of_accounts(account_code):
    known = {'1111','1121','211','468','501','821'}
    return account_code in known


def is_asset(record):
    code = record.get('account_code','')
    return str(code).startswith('1')


def is_liability_or_equity(record):
    c = record.get('account_code','')
    return str(c).startswith('2') or str(c).startswith('3')


def validate_vat_rates(line_items, tax_code_map):
    for li in line_items or []:
        tr = li.get('tax_rate')
        if tr is None:
            return False
        if tax_code_map and str(tr) not in tax_code_map:
            return False
    return True


def avg_ocr_confidence(attachments):
    if not attachments:
        return 1.0
    s = 0.0
    n = 0
    for a in attachments:
        v = a.get('ocr_confidence')
        if v is None:
            continue
        s += float(v)
        n += 1
    return (s/n) if n>0 else 0.0


# map of helper names to functions for registration in evaluator
helpers_map = {
    'exists_duplicate': exists_duplicate,
    'match_reconciliation': match_reconciliation,
    'check_continuity_account': check_continuity_account,
    'exists_in_chart_of_accounts': exists_in_chart_of_accounts,
    'is_asset': is_asset,
    'is_liability_or_equity': is_liability_or_equity,
    'validate_vat_rates': validate_vat_rates,
    'avg': avg_ocr_confidence,
    'sum': sum_field
}
