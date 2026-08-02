"""
services/rule_engine/__init__.py

Expose evaluator load_rules and helpers_map plus provide a convenience function to reload helpers
"""
from .evaluator import load_rules, evaluate_rule, evaluate_ruleset

# expose helper maps
try:
    from .helpers import helpers_map as helpers_map
except Exception:
    helpers_map = {}

# try to merge extra helpers if present
try:
    from .helpers_extra import _new_helpers as _extra
    if isinstance(helpers_map, dict):
        helpers_map.update(_extra)
except Exception:
    pass
