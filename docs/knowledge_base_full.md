# Knowledge Base (KB) — Full (KB_v1.1)

This Knowledge Base is the canonical source for legal placeholders, Chart of Accounts template, canonical report templates, data dictionary, canonical data model and indexing information for AI retrieval. All legal citations are placeholders and must be updated when official PDFs are provided.

KB Manifest
- kb_version: KB_v1.1
- created_at: 2026-07-31
- created_by: copilot
- legal_citations: placeholders (replace with official documents)

Sections included
1) Legal sources (placeholders)
   - KB::TT24::placeholder
   - KB::LAW_ACCT_2015::placeholder
   - KB::CIRCULARS::placeholder

2) Chart of Accounts
   - File: data/chart_of_accounts_template.csv (versioned)

3) Canonical report templates
   - Folder: report_template_defs/ (balance_sheet, income_statement, cash_flow, decision_report)

4) Data Dictionary & Canonical Data Model
   - Files: docs/data_dictionary.md, canonical/canonical_data_model.json

5) KB indexing & AI retrieval spec
   - File: kb/indexing_spec.md

6) Change log
   - File: kb/change_log.md

Usage guidance
- Rules reference `legal_basis` keys (e.g. KB::TT24::placeholder::article_x). After legal PDFs are provided, update KB entries with exact citations and link to PDF pages.

Governance
- KB is versioned. Changes must be committed via PR with changelog entries. The KB manifest must be updated on each change.
