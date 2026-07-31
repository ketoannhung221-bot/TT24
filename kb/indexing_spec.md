# KB Indexing & AI Retrieval Spec

Purpose: define how KB entries are tokenized and indexed for later AI retrieval (on‑prem). The index will not leave the internal network.

Index fields
- kb_key (e.g., KB::TT24::article_3)
- title
- full_text (extracted from uploaded PDFs)
- citations (article/clause/point)
- related_rules (list of rule IDs)
- last_updated

Index storage
- Use a lightweight vector index (FAISS or Annoy) on-premise in a dedicated service, or a simple inverted index (SQLite + FTS5) depending on resource availability.

Retrieval API
- /kb/search?q=... returns top-N KB entries with scores and citations.

Privacy
- Indexing runs locally; no outbound network.
