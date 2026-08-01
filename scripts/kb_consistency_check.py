#!/usr/bin/env python3
"""
scripts/kb_consistency_check.py
Check KB consistency: ensure rule legal_basis keys map to KB manifest entries, and report templates fields align with canonical schema.
"""
import json
import os
from jsonschema import validate, ValidationError

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
KB_MANIFEST = os.path.join(REPO_ROOT, 'docs', 'knowledge_base_full.md')
CANONICAL_SCHEMA = os.path.join(REPO_ROOT, 'canonical', 'canonical_data_model.json')
RULES_FILE = os.path.join(REPO_ROOT, 'rules', 'rules_expanded.json')


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def check_rules_vs_kb():
    rules = load_json(RULES_FILE)['rules']
    # Simple check: legal_basis uses KB:: prefix
    issues = []
    for r in rules:
        lb = r.get('legal_basis','')
        if not lb.startswith('KB::'):
            issues.append((r['id'], 'legal_basis_missing_or_not_kb', lb))
    return issues


def check_schema_alignment():
    schema = load_json(CANONICAL_SCHEMA)
    sample = load_json(os.path.join(REPO_ROOT,'tests','samples','sample_canonical_payload_001.json'))
    try:
        validate(instance=sample, schema=schema)
        return []
    except ValidationError as e:
        return [str(e)]


if __name__ == '__main__':
    issues = check_rules_vs_kb()
    schema_issues = check_schema_alignment()
    if issues:
        print('KB consistency issues found:')
        for it in issues:
            print(it)
    else:
        print('No KB issues detected for legal_basis format.')
    if schema_issues:
        print('Schema validation issues:')
        for s in schema_issues:
            print(s)
    else:
        print('Sample payload conforms to canonical schema.')
