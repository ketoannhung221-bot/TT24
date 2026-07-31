#!/usr/bin/env python3
"""
scripts/seed_chart_of_accounts.py
Utility to import chart_of_accounts_template.csv into Postgres database.
"""
import csv
import os
from sqlalchemy import create_engine, MetaData, Table, Column, String

DB_URL = os.getenv('TT24_DB_URL','postgresql://user:pass@localhost:5432/tt24')

def seed(csv_path='data/chart_of_accounts_template.csv'):
    engine = create_engine(DB_URL)
    metadata = MetaData()
    coa = Table('chart_of_accounts', metadata,
                Column('account_code', String, primary_key=True),
                Column('account_name', String),
                Column('account_type', String),
                Column('level', String),
                Column('valid_from', String),
                Column('valid_to', String),
                Column('notes', String)
                )
    metadata.create_all(engine)
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with engine.begin() as conn:
        for r in rows:
            conn.execute(coa.insert().values(**r))
    print(f"Seeded {len(rows)} chart of accounts rows")

if __name__ == '__main__':
    seed()
