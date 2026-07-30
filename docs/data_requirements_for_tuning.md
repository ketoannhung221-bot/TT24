# Minimal Sample Data List for Tuning (detailed)

Mục tiêu: liệt kê các dữ liệu tối thiểu cần để tiến hành tuning OCR/Parser và hiệu chỉnh rules sau khi hoàn thiện KB/Rule/Mapping engines. Mỗi mục nêu rõ mục đích sử dụng.

1) Báo cáo tài chính chính thức (Excel) — 15 files
   - Mục đích: tuning Excel Parser, header normalization, column mapping, numeric/date parsing.
   - Yêu cầu: đa dạng layout từ các phần mềm (MISA, Fast, Bravo), có sheet tên khác nhau.

2) Bảng cân đối phát sinh tài khoản (trial balance) — 20 files
   - Mục đích: kiểm tra aggregate rules, balance checks, account code normalization.
   - Yêu cầu: include examples with TK 111/112/468 and various fund_source values.

3) Báo cáo PDF (in từ phần mềm, text-based) — 10 files
   - Mục đích: PDF table extraction without OCR — test pdfplumber/Camelot.

4) PDF quét (scanned images) — 20 files
   - Mục đích: OCR tuning (Tesseract/PaddleOCR), cleaning heuristics, layout detection.

5) Biên bản đối chiếu tiền gửi ngân hàng/kho bạc — 5 files
   - Mục đích: reconciliation helper testing (match_reconciliation).

6) Mẫu chứng từ, hóa đơn (scan) — 20 files
   - Mục đích: duplicate detection, VAT parsing, line item extraction.

7) Chart of Accounts (CSV/Excel) — 1 file (complete)
   - Mục đích: mapping validation, unknown account rule testing.

8) Data history (năm trước) — optional 1–3 years
   - Mục đích: TK468 continuity checks, year-over-year validations.

9) Template export forms (Excel/PDF) — 2–3 mẫu
   - Mục đích: kiểm thử xuất báo cáo theo mẫu Phụ lục.

Ghi chú: trước khi gửi, hãy ẩn danh hoá (mask) dữ liệu nhạy cảm nếu cần. Sau khi nhận dữ liệu đã ẩn danh, tôi sẽ tiến hành tuning theo priority: Excel parser → trial balance rules → PDF text extraction → OCR for scanned PDFs.

---

File liên quan: docs/data_requirements_for_tuning.md
