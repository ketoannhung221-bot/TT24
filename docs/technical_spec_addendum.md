# Technical Spec Addendum

Tóm tắt các thành phần kỹ thuật bổ sung và interface chi tiết cần hoàn thiện trước giai đoạn tuning.

1) Components & Interfaces
- API (FastAPI): upload endpoint, canonical submit, report retrieval, templates management.
- Processor Worker: subscribes to queue, runs mapping engine, invokes rule engine, persists results.
- Rule Engine: HTTP/GRPC service with /evaluate endpoint accepting canonical JSON and returning rule results.
- Mapping Engine: library used by processor; exposes map(file, template_id?) -> canonical_json.

2) DB Schema (high-level)
- users, uploads, reports, validation_runs, rules_meta, mapping_templates, audit_logs.

3) Security
- Internal network only for processing services. Service accounts for worker.
- Access control for templates and rules: only admin can activate rules.

4) CI/CD
- CI validates: lint rules, run rule test cases, run mapping unit tests.

5) Observability
- Metrics: processing time per file, OCR confidence distribution, rule pass rates.
- Logging: structured logs; Sentry for exceptions.

File liên quan: docs/technical_spec_addendum.md
