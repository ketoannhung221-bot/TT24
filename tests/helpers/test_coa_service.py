"""
Unit tests for COA service behaviors: caching, reload on change, multiple files support.
"""
import os
import time
from pathlib import Path
from services.rule_engine import coa

REPO_ROOT = Path(__file__).resolve().parents[2]
COA_PATH = REPO_ROOT / 'data' / 'chart_of_accounts_template.csv'


def test_load_and_exists():
    coa.load_chart_of_accounts([str(COA_PATH)])
    assert coa.exists_in_coa('1111')
    assert coa.get_account_type('1111') is not None


def test_reload_on_change(tmp_path):
    # create a temp COA file
    p = tmp_path / 'coa.csv'
    content = 'account_code,account_name,account_type\nT1,Test1,asset\n'
    p.write_text(content, encoding='utf-8')
    coa.load_chart_of_accounts([str(p)])
    assert coa.exists_in_coa('T1')
    # modify file
    time.sleep(0.1)
    p.write_text('account_code,account_name,account_type\nT1,Test1,asset\nT2,Test2,liability\n', encoding='utf-8')
    # reload
    count, paths = coa.reload_if_changed([str(p)])
    assert 'T2' in coa.load_chart_of_accounts([str(p)])


def test_multiple_files(tmp_path):
    p1 = tmp_path / 'coa1.csv'
    p2 = tmp_path / 'coa2.csv'
    p1.write_text('account_code,account_name,account_type\nA1,A One,asset\n', encoding='utf-8')
    p2.write_text('account_code,account_name,account_type\nB1,B One,liability\n', encoding='utf-8')
    combined = coa.load_chart_of_accounts([str(p1), str(p2)])
    assert 'A1' in combined and 'B1' in combined
