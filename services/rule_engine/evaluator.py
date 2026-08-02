"""
services/rule_engine/evaluator.py

Enhanced evaluator:
- dynamic rule loader: load all rules/R*.json if no path given or when rules_dir passed
- registers helper operations from helpers and helpers_extra (if present)
- evaluate_rule/evaluate_ruleset unchanged semantics
"""
import json
import os
import glob
import logging
from typing import Dict, Any, List
from jsonlogic import jsonlogic, add_operation

logger = logging.getLogger(__name__)

# load helper maps from helpers modules
def _collect_helpers():
    helpers_map = {}
    try:
        from .helpers import helpers_map as base_map
        helpers_map.update(base_map)
    except Exception:
        logger.debug('base helpers not available')
    try:
        from .helpers_extra import _new_helpers as extra_map
        helpers_map.update(extra_map)
    except Exception:
        # helpers_extra may have merged into base already
        try:
            from .helpers import helpers_map as merged_map
            helpers_map.update(merged_map)
        except Exception:
            logger.debug('no additional helpers found')
    return helpers_map

_helpers = _collect_helpers()

# register operations
for name, fn in _helpers.items():
    try:
        add_operation(name, fn)
    except Exception as e:
        logger.exception('Failed to register helper operation %s: %s', name, e)


def load_rules(rules_path: str = None) -> List[Dict[str, Any]]:
    """Load rules. If rules_path is a file, load that file.
    If rules_path is None or a directory, load all JSON files under rules/ matching R*.json or rules_expanded.json
    Returns list of rule dicts.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    rules_dir = os.path.join(repo_root, 'rules')

    rules: List[Dict[str, Any]] = []

    if rules_path and os.path.isfile(rules_path):
        with open(rules_path, encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'rules' in data:
            rules.extend(data['rules'])
        elif isinstance(data, list):
            rules.extend(data)
        elif isinstance(data, dict):
            rules.append(data)
        return rules

    # Otherwise, load all rule files in rules_dir with prefix R or file rules_expanded.json
    pattern_files = glob.glob(os.path.join(rules_dir, 'R*.json'))
    # include rules_expanded.json if present
    expanded = os.path.join(rules_dir, 'rules_expanded.json')
    if os.path.isfile(expanded):
        pattern_files.append(expanded)

    for rf in sorted(set(pattern_files)):
        try:
            with open(rf, encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'rules' in data:
                rules.extend(data['rules'])
            elif isinstance(data, list):
                rules.extend(data)
            elif isinstance(data, dict):
                rules.append(data)
        except Exception as e:
            logger.exception('Failed to load rule file %s: %s', rf, e)
            continue
    return rules


def evaluate_rule(rule: Dict[str, Any], payload: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
    expr = rule.get('expression')
    ctx = context or {}
    data = dict(payload or {})
    data.update({'payload': payload, 'config': ctx.get('config', {})})
    try:
        result = jsonlogic(expr, data)
        passed = bool(result)
        return {
            'rule_id': rule.get('id'),
            'version': rule.get('version'),
            'passed': passed,
            'severity': rule.get('severity'),
            'details': result
        }
    except Exception as e:
        logger.exception('Error evaluating rule %s: %s', rule.get('id'), e)
        return {
            'rule_id': rule.get('id'),
            'version': rule.get('version'),
            'passed': False,
            'severity': rule.get('severity'),
            'error': str(e)
        }


def evaluate_ruleset(rules: List[Dict[str, Any]], payload: Dict[str, Any], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    results = []
    for r in rules:
        res = evaluate_rule(r, payload, context=context or {})
        results.append(res)
    return results
