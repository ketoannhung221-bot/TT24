# Knowledge Base — Căn cứ pháp lý, danh mục, cấu trúc báo cáo

Mục đích: tổng hợp và chuẩn hóa tất cả căn cứ pháp lý, danh mục tài khoản, cấu trúc báo cáo tài chính và báo cáo quyết toán để phục vụ Rule Engine và Mapping Engine.

1) Căn cứ pháp lý (nguồn tham chiếu chính)
- Thông tư 24/2024/TT-BTC (Phụ lục, biểu mẫu, quy định ghi sổ, thời điểm, chứng từ)
- Luật Kế toán 2015 (quy định chung về hạch toán, chứng từ, báo cáo)
- Các văn bản hướng dẫn có hiệu lực liên quan (circulars, guidelines) — tham chiếu theo số và ngày ban hành.

Ghi chú: để mã hóa rule chính xác, cần file PDF/HTML chính thức của Thông tư 24/2024 và Luật Kế toán 2015; các điều khoản sẽ được trích dẫn khi chuyển thành rule.

2) Chuẩn hóa Danh mục tài khoản (Chart of Accounts)
- Lưu trữ danh mục mã tài khoản dạng bảng: `account_code`, `account_name`, `account_type` (asset/liability/equity/revenue/expense), `level` (1..n), `valid_from`, `valid_to`, `notes`.
- Cách ánh xạ: mapping engine sử dụng lookup Table `chart_of_accounts.csv` (được versioned).

3) Chuẩn hóa cấu trúc Báo cáo
- Định nghĩa canonical forms cho các báo cáo bắt buộc theo Thông tư 24 (Bảng cân đối, Báo cáo kết quả hoạt động, Báo cáo quyết toán, Phụ lục III/IV): tên trường, kiểu, thứ tự, bắt buộc/tuỳ chọn.
- Mỗi mẫu báo cáo có `report_template_id`, `fields[]` (field_id, label, datatype, required, mapping_rules).

4) Chuẩn hóa Quy tắc nghiệp vụ
- Mỗi quy tắc nghiệp vụ được biểu diễn bằng một record: `rule_id`, `title`, `legal_basis` (tham chiếu điều/khoản), `severity`, `expression` (DSL / JSONLogic), `parameters`, `suggested_fix`, `example`.
- Quy trình chuyển đổi văn bản luật → rule: (1) trích xuất điều khoản, (2) xác định input fields, (3) viết expression trong DSL, (4) tạo test case (input canonical JSON + expected outcome).

5) Phiên bản & Traceability
- Knowledge Base versioned (KB_v1, KB_v2...) — mỗi rule/template mapping refer tới KB version.

---

File liên quan: docs/knowledge_base.md
