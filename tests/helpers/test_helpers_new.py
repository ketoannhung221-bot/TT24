"""
Unit tests for new helper functions attached to R011-R015 rules.
"""
from services.rule_engine import helpers
from services.rule_engine import coa
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
COA_PATH = os.path.join(REPO_ROOT, 'data', 'chart_of_accounts_template.csv')


def test_any_negative():
    assert helpers.any_negative([{'closing_debit':0,'closing_credit':0}]) is False
    assert helpers.any_negative([{'closing_debit':-1,'closing_credit':0}]) is True


def test_validate_account_levels():
    coa.load_chart_of_accounts([COA_PATH])
    assert helpers.validate_account_levels([{'account_code':'1111','level':'4'}]) is True
    assert helpers.validate_account_levels([{'account_code':'9999','level':'1'}]) is False


def test_validate_fund_source():
    vocab = ['11','12']
    assert helpers.validate_fund_source([{'fund_source':'11'}], vocab) is True
    assert helpers.validate_fund_source([{'fund_source':'99'}], vocab) is False


def test_validate_currency_consistency():
    assert helpers.validate_currency_consistency([{'currency':'VND'}],[{'currency':'VND'}]) is True
    assert helpers.validate_currency_consistency([{'currency':'USD'}],[{'currency':'VND'}]) is False


def test_within_tolerance():
    assert helpers.within_tolerance(0, 0) is True
    assert helpers.within_tolerance(500, 1000) is True
    assert helpers.within_tolerance(1500, 1000) is False
    assert helpers.within_tolerance('abc', 'def') is False
