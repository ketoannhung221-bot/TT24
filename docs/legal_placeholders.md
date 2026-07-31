# Legal Placeholders — Usage & Update Guide

This document explains how legal placeholders are used in rules and KB, and how to replace placeholders with official citations.

Placeholder format
- KB::<DOC_KEY>::placeholder::<section>
  - Examples: KB::TT24::placeholder::article_1, KB::LAW_ACCT_2015::placeholder::article_5

How to update
1. Upload official PDF to repo or internal storage (recommended: kb/legal_pdfs/).
2. Add a KB entry mapping placeholder to exact citation: {doc_key, page, article, clause, excerpt}.
3. Update the applicable rule's `legal_basis` value to point to the full citation entry.
4. Update KB manifest and change_log.

Permissions
- Only admin or designated legal owner should update legal citations.
