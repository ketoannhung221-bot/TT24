"""Chart of Accounts service (thread-safe improvements)

Improvements:
- Use RLock around all reads/writes to _COA_CACHE/_COA_META.
- reload_if_changed now checks per-file mtime/hash and only reloads changed files.
- Exposes get_cache_snapshot() for safe read-only access in other threads.
- Supports multiple configured paths; does not hardcode paths.
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


def _load_file_into_entries(p: str) -> Dict[str, Dict[str, Any]]:
    entries: Dict[str, Dict[str, Any]] = {}
    with open(p, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            code = (r.get('account_code') or '').strip()
            if not code:
                continue
            entries[code] = r
    return entries


def load_chart_of_accounts(paths: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """Load one or more COA CSV files into in-memory cache.
    Only reload files whose mtime/hash changed.
    paths: list of filesystem paths. If None, returns current cache (no-op).
    Returns combined COA dict mapping account_code -> row dict.
    """
    global _COA_CACHE, _COA_META
    if not paths:
        # no input; just return snapshot
        with _lock:
            return dict(_COA_CACHE)

    combined: Dict[str, Dict[str, Any]] = {}
    loaded_paths: List[str] = []

    for p in paths:
        if not os.path.isfile(p):
            logger.warning("COA path not found: %s", p)
            continue
        try:
            mtime = os.path.getmtime(p)
            h = _file_hash(p)
            meta = _COA_META.get(p)
            # if file exists previously and both mtime/hash equal, reuse previous entries
            if meta and meta.get('mtime') == mtime and meta.get('hash') == h and meta.get('entries'):
                entries = meta.get('entries')
                logger.debug("Reusing cached entries for %s", p)
            else:
                entries = _load_file_into_entries(p)
                with _lock:
                    _COA_META[p] = {'mtime': mtime, 'hash': h, 'entries': entries}
                logger.info("Loaded COA file %s with %d entries", p, len(entries))
            combined.update(entries)
            loaded_paths.append(p)
        except Exception as e:
            logger.exception("Failed to load COA file %s: %s", p, e)
            continue

    with _lock:
        _COA_CACHE = combined
    return dict(_COA_CACHE)


def get_cache_snapshot() -> Dict[str, Dict[str, Any]]:
    with _lock:
        return dict(_COA_CACHE)


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
    """Reload only files that have changed since last load. Returns (count_entries, loaded_paths).
    If paths None, checks current _COA_META for file changes and reloads them.
    """
    global _COA_CACHE, _COA_META
    reloaded_paths: List[str] = []
    combined: Dict[str, Dict[str, Any]] = {}

    paths_to_check = paths or list(_COA_META.keys())

    for p in paths_to_check:
        if not os.path.isfile(p):
            logger.warning("COA path not found during reload check: %s", p)
            continue
        try:
            mtime = os.path.getmtime(p)
            h = _file_hash(p)
            meta = _COA_META.get(p)
            if meta and meta.get('mtime') == mtime and meta.get('hash') == h and meta.get('entries'):
                entries = meta.get('entries')
                logger.debug("No change in COA file: %s", p)
            else:
                entries = _load_file_into_entries(p)
                with _lock:
                    _COA_META[p] = {'mtime': mtime, 'hash': h, 'entries': entries}
                reloaded_paths.append(p)
                logger.info("Reloaded COA file: %s (%d entries)", p, len(entries))
            combined.update(entries)
        except Exception as e:
            logger.exception("Error while reloading COA file %s: %s", p, e)
            continue

    with _lock:
        _COA_CACHE = combined
    return len(_COA_CACHE), reloaded_paths
