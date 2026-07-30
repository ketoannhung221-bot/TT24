# Functional Spec — Công cụ Chuẩn hóa Báo cáo Tài chính & Quyết toán (MVP)

Tổng quan
- Mục tiêu: Hệ thống on‑prem/hybrid để nhận file PDF/Excel, chuẩn hóa thành canonical JSON theo Thông tư 24/2024/TT‑BTC & Luật Kế toán 2015, chạy validation rules, cho phép review/approve, và xuất báo cáo chuẩn (Excel/PDF).
- Phạm vi MVP: hỗ trợ PDF quét + Excel nhiều layout, local OCR (Tesseract/PaddleOCR), lưu object trên MinIO, DB Postgres.

Kiến trúc (cao cấp)
- Frontend: React + Ant Design (upload, review queue, export, admin).
- Backend API: FastAPI (auth, upload, status, report access).
- Worker/Doc Processor: preprocessing → OCR → table extraction → IE/mapping → canonical JSON.
- Validation Engine: rules JSON/YAML (versioned) evaluated against canonical payload.
- Storage: Postgres (metadata), MinIO (raw + processed files).
- Queue: Celery + Redis (on‑prem).
- Audit: append-only audit table; store mapping_template_id & rules_version with each report.

Canonical Payload (tóm t���t)
- unit_info: unit_code, unit_name, budget_chapter, accounting_period {year, from_date, to_date}
- trial_balance_records[]: account_code, account_name, opening_debit, opening_credit, period_debit, period_credit, closing_debit, closing_credit, fund_source, budget_chapter, budget_category, budget_sub_category, budget_item, budget_sub_item, line_reference
- off_balance_records[]: account_code, account_name, opening_balance, increase_amount, decrease_amount, closing_balance
- attachments[]: file_id, file_type, original_filename, s3_path, ocr_confidence
- meta: source_file, ingested_at, processor_version, mapping_template_id

Validation Rules (tóm tắt)
- R001_unbalanced_totals (P1): kiểm tra cân đối tổng hợp (opening/period/closing)
- R002_required_fields (P1): kiểm tra trường bắt buộc
- R003_duplicate_documents (P1): phát hiện trùng lặp
- R004_reconcile_111_112 (P1): đối chiếu TK 111/112 với biên bản
- R005_tk468_continuity (P1): continuity TK 468 chuyển nguồn
- R006_balance_sheet (P1): tổng tài sản == tổng nguồn
- R007_line_items_sum (P2): dòng chi tiết == tổng
- R008_vat_check (P2): kiểm tra VAT theo loại
- R009_approval_threshold (P2): ngưỡng phê duyệt configurable
- R010_unknown_account (P3): phát hiện mã TK lạ

Rule Definition Format
- Mỗi rule là YAML/JSON với id, version, priority, category, expression, tolerance, action_on_fail, severity, message, suggested_fix.
- Rule result trả về: rule_id, passed, severity, message, fields_affected, suggested_fix, rule_version.

API Spec (cốt lõi)
- POST /api/v1/financial-reports/validate-and-standardize
  - Accept: multipart/form-data (file) OR application/json (canonical payload)
  - Response success (200): { status, code, message, data: {report_id, total_assets, total_sources, validation_passed, validation_results[], canonical_payload }}
  - Response fail (422): { status, code, message, data: {report_id, validation_passed:false, errors[] }}

Workflow (kỹ thuật & UX)
- Upload → persist raw file → enqueue job → preprocess → OCR → extract → map → validate → store canonical + validation_results
- Nếu tất cả P1 pass & no approval required → auto‑finalize + export
- Nếu có P1 fail hoặc approval required → tạo review task → user chỉnh sửa → revalidate → finalize

Audit & Versioning
- Lưu mapping_template_id, processor_version, rules_version, và mọi manual edit (user_id, timestamp, old_value, new_value, reason)

Security / On‑prem notes
- Chạy OCR/IE toàn bộ on‑prem; MinIO, Postgres on‑prem. Không gọi dịch vụ cloud cho dữ liệu nhạy cảm trừ khi được explicit phép.
- TLS internal, encryption at rest, RBAC, optional SSO (Keycloak)

Acceptance Criteria (MVP)
- Parsing Accuracy (Excel chuẩn) ≥ 90%
- Processing time (≤100 trang) ≤ 30s on 4 vCPU / 8GB RAM baseline
- Audit trail: mọi chỉnh sửa thủ công lưu log (user_id, timestamp, old/new, reason)

Dữ liệu mẫu & Yêu cầu
- Cung cấp 10–30 file mẫu: mix scanned PDFs, e‑invoices, Excel templates; chart of accounts; reconciliation files; phê duyệt thresholds.

Next steps
1. Bạn kiểm duyệt tài liệu này. Nếu OK, tôi sẽ:
   - lưu tệp sang repo hoặc nén để gửi.
   - tiếp nhận mẫu files để tiến hành PoC parser/OCR.
2. Nếu muốn, tôi có thể hiện thực scaffold repo (FastAPI + React + worker) — báo tôi biết.
