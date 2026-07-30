# Mapping Engine Design — Ánh xạ nhiều layout về Canonical Payload

Mục tiêu: xây engine ánh xạ linh hoạt, hỗ trợ nhiều template Excel/PDF, heuristics cho PDF scans, và fallback cho khi không có template phù hợp.

1) Kiến trúc
- Template Registry: lưu mapping_template files (JSON) với id, supported_formats, priority, sample_hashes.
- Parser Modules:
  - Excel Parser: uses pandas/openpyxl to read sheets, normalize headers, run column mapping and transforms.
  - PDF Parser: uses pdfplumber/Camelot for table extraction, OCR fallback for scanned images.
  - Heuristic Matcher: for noisy layouts, uses header similarity, column name fuzzy matching, positional heuristics.
- Mapping Runner: given input file, select candidate templates (by classifier or heuristics), apply mapping, produce canonical JSON with confidence scores per field.

2) Template format
- mapping_template.json includes: template_id, parser_engine, sheet_selector (for excel), header_mappings, column_transforms, required_fields, post_processing.

3) Fuzzy mapping & confidence
- Use normalization: lowercasing, strip punctuation, unify diacritics.
- Fuzzy matcher: Levenshtein distance and token similarity to match source column names to target fields.
- Confidence scoring: each mapped field has confidence (0..1) derived from exact match, fuzzy match distance, parsing success.
- Fields with confidence < threshold flagged for human review.

4) Fallback strategies
- If no template: run auto-mapper that attempts to detect columns by keywords, header heuristics, and generate provisional mapping requiring review.
- If multiple candidate templates: pick highest confidence; allow user to switch template in UI and re-run mapping.

5) Normalization rules
- Numeric parsing: strip thousand separators, handle different decimal separators, negative formats (parens, leading -).
- Date parsing: try multiple formats; fall back to ISO parsing; if ambiguous, flag.
- Account codes: normalize to canonical format (pad zeros, remove dots) via `normalize_account_code` function.

6) Post-processing
- Aggregation and deduplication of rows; apply currency conversion if needed; round to configured decimal places.
- Produce canonical_payload with per-field confidence and source_reference (sheet,row,col).

7) Testing
- Each template must include sample file and expected canonical output for unit testing.

---

File liên quan: docs/mapping_engine_design.md
