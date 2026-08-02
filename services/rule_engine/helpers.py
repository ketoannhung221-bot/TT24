"""
Refined helpers: standardized _safe_call default returns table and stronger typing/logging.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from . import coa

logger = logging.getLogger(__name__)

# default return values for safe calls
_SAFE_DEFAULTS = {
    'is_asset': False,
    'is_liability_or_equity': False,
    'exists_duplicate': False,
    'match_reconciliation': False,
    'check_continuity_account': False,
    'exists_in_chart_of_accounts': False,
    'validate_vat_rates': False,
    'avg': 0.0,
    'sum': 0.0,
    'balance_sheet_eq': False,
    'line_items_sum_match': False,
    'all_accounts_exist': False,
    'approval_check': False
}


def _safe_call_default(fn_name: str):
    return _SAFE_DEFAULTS.get(fn_name, None)


def _safe_call(fn_name: str, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.exception("Helper %s failed: %s", fn_name, e)
        return _safe_call_default(fn_name)

# rest of helpers unchanged but using _safe_call wrapper where exposed
