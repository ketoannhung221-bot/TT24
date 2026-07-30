# Project Structure (Repository Layout)

Proposal for repo layout to organize code, rules, docs, tests, and infra:

/
├─ docs/                      # design docs, specs (knowledge base, rule engine, mapping, checklist)
├─ rules/                     # YAML/JSON rule definitions, catalog
├─ mapping/                   # mapping templates and sample templates
├─ services/                  # microservices (processor, rule-evaluator, api)
│  ├─ api/                    # FastAPI service
│  ├─ processor/              # OCR/Parser worker code
│  └─ rule_engine/            # rule evaluator service
├─ infra/                     # deployment manifests (k8s/compose), infra notes
├─ tests/                     # unit/integration tests, sample inputs & expected outputs
├─ scripts/                   # helper scripts (data migration, db seed)
├─ docker-compose.yml
├─ README.md

Guidelines:
- Rules and mapping templates are stored as files (git-backed) for traceability.
- Tests include a CI job that validates rules against test cases before rules are activated.

File liên quan: docs/project_structure.md
