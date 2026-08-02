"""Chart of Accounts service

Provides in-memory cache of one or more COA CSV files. Supports reload-on-change based
on mtime and sha256 hash. No hardcoded paths; paths configured at runtime.
"""
from __future__ import annotations
import csv
import hashlib
import logging
import os
import threading
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger(__name__)
_lock = threading.RLock()

# internal cache structure
_COA_CACHE: Dict[str, Dict[str, Any]] = {}
_COA_META: Dict[str, Dict[str, Any]] = {}


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def load_chart_of_accounts(paths: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """Load one or more COA CSV files into in-memory cache.
    paths: list of filesystem paths. If None, returns current cache (no-op).
    Returns combined COA dict mapping account_code -> row dict.
    """
    global _COA_CACHE, _COA_META
    if not paths:
        return _COA_CACHE
    combined: Dict[str, Dict[str, Any]] = {}
    for p in paths:
        if not os.path.isfile(p):
            logger.warning("COA path not found: %s", p)
            continue
        try:
            mtime = os.path.getmtime(p)
            h = _file_hash(p)
            meta = _COA_META.get(p)
            if meta and meta.get('mtime') == mtime and meta.get('hash') == h:
                # file unchanged; we may reuse existing entries for this path
                logger.debug("COA file unchanged: %s", p)
                # merge entries from previous cache for this path
                prev = meta.get('entries') or {}
                combined.update(prev)
                continue
            # (re)load file
            entries: Dict[str, Dict[str, Any]] = {}
            with open(p, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    code = (r.get('account_code') or '').strip()
                    if not code:
                        continue
                    entries[code] = r
            # update meta and combined
            _COA_META[p] = {'mtime': mtime, 'hash': h, 'entries': entries}
            combined.update(entries)
            logger.info("Loaded COA file %s with %d entries", p, len(entries))
        except Exception as e:
            logger.exception("Failed to load COA file %s: %s", p, e)
            continue
    with _lock:
        _COA_CACHE = combined
    return _COA_CACHE


def get_account(account_code: str) -> Optional[Dict[str, Any]]:
    if not account_code:
        return None
    with _lock:
        return _COA_CACHE.get(str(account_code))


def exists_in_coa(account_code: str) -> bool:
    if not account_code:
        return False
    with _lock:
        return str(account_code) in _COA_CACHE


def get_account_type(account_code: str) -> Optional[str]:
    rec = get_account(account_code)
    if not rec:
        return None
    return (rec.get('account_type') or '').strip()


def reload_if_changed(paths: Optional[List[str]] = None) -> Tuple[int, List[str]]:
    """Reload COA files if they changed. Returns (count_entries, list_paths_loaded)."""
    loaded = load_chart_of_accounts(paths)
    return len(loaded), list(_COA_META.keys())
