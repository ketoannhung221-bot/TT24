"""
Refined helpers with type hints, logging, use of COA service and robust exception handling.
All helper functions swallow internal exceptions and return safe defaults to avoid crashing
the rule evaluation engine.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from . import coa

logger = logging.getLogger(__name__)


def _safe_call(fn_name: str, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.exception("Helper %s failed: %s", fn_name, e)
        # safe default values
        if fn_name.startswith('is_'):
            return False
        if fn_name.startswith('validate') or fn_name.endswith('_match'):
            return False
        if fn_name in ('sum',):
            return 0.0
        return None


def sum_field(arr: Optional[List[Dict[str, Any]]], field_path: str) -> float:
    if arr is None:
        return 0.0
    s = 0.0
    for item in arr:
        try:
            v = item.get(field_path) if isinstance(item, dict) else None
            if v is None:
                continue
            s += float(v)
        except Exception:
            logger.debug('Non-numeric value in sum_field: %r', v)
            continue
    return s


def exists_duplicate(attachments: Optional[List[Dict[str, Any]]], keys: List[str]) -> bool:
    try:
        seen = set()
        for a in attachments or []:
            vals = tuple((a.get('meta', {}).get(k) if a.get('meta', {}).get(k) is not None else a.get(k)) for k in keys)
            if vals in seen:
                return True
            seen.add(vals)
    except Exception as e:
        logger.exception('exists_duplicate error: %s', e)
    return False


def match_reconciliation(account_prefix_a: str, account_prefix_b: str, attachments: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        for a in attachments or []:
            fname = (a.get('original_filename') or '').lower()
            if any(k in fname for k in ('recon', 'reconc', 'doi', 'doi_chieu', 'reconciliation')):
                return True
    except Exception as e:
        logger.exception('match_reconciliation error: %s', e)
    return False


def check_continuity_account(account_code: str, historical_data: Optional[Dict[str, Any]]) -> bool:
    try:
        if not historical_data:
            return False
        for rec in historical_data.get('trial_balance_records', []) or []:
            if rec.get('account_code') == account_code:
                return True
    except Exception as e:
        logger.exception('check_continuity_account error: %s', e)
    return False


def exists_in_chart_of_accounts(account_code: Optional[str]) -> bool:
    try:
        if not account_code:
            return False
        return coa.exists_in_coa(str(account_code))
    except Exception as e:
        logger.exception('exists_in_chart_of_accounts error: %s', e)
        return False


def get_account_type(account_code: Optional[str]) -> Optional[str]:
    try:
        if not account_code:
            return None
        return coa.get_account_type(str(account_code))
    except Exception as e:
        logger.exception('get_account_type error: %s', e)
        return None


def is_asset_by_coa(record: Dict[str, Any]) -> bool:
    try:
        code = record.get('account_code')
        atype = get_account_type(code)
        if atype:
            return atype.lower() == 'asset'
        # fallback heuristic
        return str(code).startswith('1')
    except Exception as e:
        logger.exception('is_asset_by_coa error: %s', e)
        return False


def is_liability_or_equity_by_coa(record: Dict[str, Any]) -> bool:
    try:
        code = record.get('account_code')
        atype = get_account_type(code)
        if atype:
            return atype.lower() in ('liability', 'equity')
        return str(code).startswith('2') or str(code).startswith('3')
    except Exception as e:
        logger.exception('is_liability_or_equity_by_coa error: %s', e)
        return False


def validate_vat_rates(line_items: Optional[List[Dict[str, Any]]], tax_code_map: Optional[Dict[str, Any]]) -> bool:
    try:
        for li in line_items or []:
            tr = li.get('tax_rate')
            if tr is None:
                return False
            if tax_code_map and str(tr) not in tax_code_map:
                return False
    except Exception as e:
        logger.exception('validate_vat_rates error: %s', e)
        return False
    return True


def avg_ocr_confidence(attachments: Optional[List[Dict[str, Any]]]) -> float:
    try:
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
    except Exception as e:
        logger.exception('avg_ocr_confidence error: %s', e)
        return 0.0


def balance_sheet_eq(trial_balance_records: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        assets = 0.0
        others = 0.0
        for r in trial_balance_records or []:
            try:
                debit = float(r.get('closing_debit', 0) or 0)
                credit = float(r.get('closing_credit', 0) or 0)
            except Exception:
                debit = 0.0
                credit = 0.0
            total = debit + credit
            if is_asset_by_coa(r):
                assets += total
            elif is_liability_or_equity_by_coa(r):
                others += total
            else:
                others += total
        return abs(assets - others) < 1e-6
    except Exception as e:
        logger.exception('balance_sheet_eq error: %s', e)
        return False


def line_items_sum_match(detail_reports: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        for d in detail_reports or []:
            total = 0.0
            for li in d.get('line_items') or []:
                try:
                    total += float(li.get('amount') or 0)
                except Exception:
                    pass
            if abs(total - float(d.get('report_total') or 0)) > 1e-6:
                return False
        return True
    except Exception as e:
        logger.exception('line_items_sum_match error: %s', e)
        return False


def all_accounts_exist(trial_balance_records: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        for r in trial_balance_records or []:
            code = r.get('account_code')
            if not exists_in_chart_of_accounts(code):
                return False
        return True
    except Exception as e:
        logger.exception('all_accounts_exist error: %s', e)
        return False


def approval_check(report_total: Any, approval_threshold: Any) -> bool:
    try:
        rt = float(report_total or 0)
    except Exception:
        rt = 0.0
    try:
        th = float(approval_threshold)
    except Exception:
        return False
    return rt > th


# export map
helpers_map = {
    'exists_duplicate': lambda a, k: _safe_call('exists_duplicate', exists_duplicate, a, k),
    'match_reconciliation': lambda a, b, c: _safe_call('match_reconciliation', match_reconciliation, a, b, c),
    'check_continuity_account': lambda a, b: _safe_call('check_continuity_account', check_continuity_account, a, b),
    'exists_in_chart_of_accounts': lambda a: _safe_call('exists_in_chart_of_accounts', exists_in_chart_of_accounts, a),
    'is_asset': lambda r: _safe_call('is_asset', is_asset_by_coa, r),
    'is_liability_or_equity': lambda r: _safe_call('is_liability_or_equity', is_liability_or_equity_by_coa, r),
    'validate_vat_rates': lambda a, b: _safe_call('validate_vat_rates', validate_vat_rates, a, b),
    'avg': lambda a: _safe_call('avg', avg_ocr_confidence, a),
    'sum': lambda arr, field: _safe_call('sum', sum_field, arr, field),
    'balance_sheet_eq': lambda r: _safe_call('balance_sheet_eq', balance_sheet_eq, r),
    'line_items_sum_match': lambda r: _safe_call('line_items_sum_match', line_items_sum_match, r),
    'all_accounts_exist': lambda r: _safe_call('all_accounts_exist', all_accounts_exist, r),
    'approval_check': lambda rt, th: _safe_call('approval_check', approval_check, rt, th)
}
