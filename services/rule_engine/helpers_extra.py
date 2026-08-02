"""
Extend helpers with functions required by R011-R015 and expose them via helpers_map.
"""
from typing import Any, Dict, List, Optional
import logging

from . import coa

logger = logging.getLogger(__name__)

# Reuse _safe_call_default and _safe_call from helpers base if present
try:
    from .helpers import _safe_call, _safe_call_default
except Exception:
    # fallback simple implementations
    def _safe_call(fn_name, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception('helper %s failed: %s', fn_name, e)
            return None
    def _safe_call_default(fn_name):
        return None


def any_negative(trial_balance_records: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        for r in trial_balance_records or []:
            try:
                if float(r.get('closing_debit',0) or 0) < 0 or float(r.get('closing_credit',0) or 0) < 0:
                    return True
            except Exception:
                continue
    except Exception as e:
        logger.exception('any_negative error: %s', e)
    return False


def validate_account_levels(trial_balance_records: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        # if COA has level info, compare
        for r in trial_balance_records or []:
            code = r.get('account_code')
            if not code:
                return False
            rec = coa.get_account(str(code))
            if rec and rec.get('level'):
                if str(rec.get('level')) != str(r.get('level')):
                    return False
        return True
    except Exception as e:
        logger.exception('validate_account_levels error: %s', e)
        return False


def validate_fund_source(trial_balance_records: Optional[List[Dict[str, Any]]], vocab: Optional[List[str]]) -> bool:
    try:
        vocab_set = set(vocab or [])
        for r in trial_balance_records or []:
            fs = r.get('fund_source')
            if fs is None:
                return False
            if vocab_set and str(fs) not in vocab_set:
                return False
        return True
    except Exception as e:
        logger.exception('validate_fund_source error: %s', e)
        return False


def validate_currency_consistency(trial_balance_records: Optional[List[Dict[str, Any]]], attachments: Optional[List[Dict[str, Any]]]) -> bool:
    try:
        # determine currency from records if present
        rec_currencies = set([ (r.get('currency') or '').strip() for r in (trial_balance_records or []) if r.get('currency') is not None ])
        att_currencies = set([ (a.get('currency') or '').strip() for a in (attachments or []) if a.get('currency') is not None ])
        # empty sets considered consistent
        if not rec_currencies and not att_currencies:
            return True
        # if both non-empty, they must be equal and non-empty strings
        if rec_currencies and att_currencies:
            return rec_currencies == att_currencies and '' not in rec_currencies
        # if only one side present, require that present values are non-empty
        if rec_currencies:
            return '' not in rec_currencies
        if att_currencies:
            return '' not in att_currencies
        return False
    except Exception as e:
        logger.exception('validate_currency_consistency error: %s', e)
        return False


def within_tolerance(difference: Any, tolerance: Any) -> bool:
    try:
        diff = float(difference)
        tol = float(tolerance)
        return abs(diff) <= tol
    except Exception as e:
        logger.exception('within_tolerance error: %s', e)
        return False


# Expose these helpers via the helpers_map expected by evaluator
from .helpers import helpers_map as _base_helpers_map

_new_helpers = {
    'any_negative': lambda r: _safe_call('any_negative', any_negative, r),
    'validate_account_levels': lambda r: _safe_call('validate_account_levels', validate_account_levels, r),
    'validate_fund_source': lambda r, v: _safe_call('validate_fund_source', validate_fund_source, r, v),
    'validate_currency_consistency': lambda r, a: _safe_call('validate_currency_consistency', validate_currency_consistency, r, a),
    'within_tolerance': lambda d, t: _safe_call('within_tolerance', within_tolerance, d, t)
}

# merge into base helpers_map
try:
    _base_helpers_map.update(_new_helpers)
except Exception:
    # if base not importable, ignore (tests will import helpers directly)
    pass
