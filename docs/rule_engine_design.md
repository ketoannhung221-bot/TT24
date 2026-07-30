# Rule Engine Design — Kiến trúc & Định dạng quy tắc

Mục tiêu: xây Rule Engine linh hoạt, có thể mở rộng (add/update rule) mà không cần thay đổi mã nguồn, hỗ trợ phân loại severity và lifecycle quản trị.

1) Yêu cầu chức năng
- Hỗ trợ rule definition bằng YAML/JSON (human readable) hoặc JSONLogic.
- Hỗ trợ các loại rule: aggregate checks, per-record checks, cross-report checks, temporal checks (liên tục giữa các năm), external checks (reconciliation documents).
- Rule versioning, activation flag, author, created_at, updated_at.
- Rule evaluation trả về: {rule_id, version, passed, severity, message, fields_affected, details}.
- Rule management UI: list, enable/disable, edit (only metadata), upload new rule file.

2) Định dạng mẫu (YAML)
- Sử dụng biểu diễn đơn giản như đã mô tả: id, version, priority, category, expression, tolerance_vnd, action_on_fail, severity, message, suggested_fix.
- Expression có thể là JSONLogic hoặc custom mini-DSL; engine sẽ hỗ trợ cả hai (trước tiên JSONLogic).

3) Severity mapping
- Critical (BLOCKER / P1) — không được phép finalize báo cáo; require human fix.
- Major (P2) — cảnh báo/require approval; may block auto-finalize depending config.
- Minor (P3) — ghi nhận warning; allow finalize but log.

4) Rule lifecycle
- Draft → Review → Active → Deprecated
- Rules stored in Git-backed store (repo/rules) for auditing. Rule changes require commit with message and optional approval.

5) Implementation notes
- Rule evaluator service (Python): loads active rules (cache), compiles expression to executable checks, runs on canonical payload, returns results.
- Use sandboxed evaluation (no arbitrary code exec). Prefer JSONLogic engine with host functions (sum, filter, exists, match_reconciliation).
- For complex functions (e.g., match_reconciliation, check_continuity_account), implement as built-in helpers callable from rules: helper functions accept parameters and return boolean/details.

6) Storage & Observability
- Store rule run result per report in DB table `validation_runs` with run_id, report_id, rule_id, result_json, run_time, engine_version.
- Metrics: rule pass-rate, time per rule, most-failed rules.

7) Governance
- Changes to rules must reference legal_basis and test_case(s). Each rule commit triggers CI validation: run rule against test_cases to verify expected behavior.

---

File liên quan: docs/rule_engine_design.md
