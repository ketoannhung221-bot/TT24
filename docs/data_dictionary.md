# Data Dictionary (expanded)

This document provides extended descriptions, allowed values, and examples for canonical fields.

Field: unit_info.unit_code
- Type: string
- Example: "ST01234"
- Notes: must match registered unit codes. Validation rule R030_missing_unit_info applies.

Field: trial_balance_records[].account_code
- Type: string
- Pattern: numeric codes e.g., "1111" or hierarchical "1.1.01"
- Mapping: normalize dots and leading zeros.

Field: trial_balance_records[].fund_source
- Type: string
- Allowed: see Chart of Accounts Fund sources list (external file)

Field: attachments[].ocr_confidence
- Type: decimal (0..1)
- Usage: used by R027_attachment_ocr_confidence

Provenance structure (per-field):
- value
- confidence
- source_reference: {file_id, sheet, page, row, col, bbox}
- transforms: list

