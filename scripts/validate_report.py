#!/usr/bin/env python3
"""Check audit output STRUCTURE, not whether scholarly citations are true."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REQUIRED_HEADERS = (
    'Research question',
    'One-paragraph conclusion',
    'Novelty Audit',
    'Claim-level decision',
    'Prior art and evidence',
    'Adversarial',
    'Cheapest discriminating experiments',
    'Search log',
    'Suggested contribution wording',
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path, help='Path to novelty-audit.md')
    parser.add_argument('--strict', action='store_true', help='Require prior-art.csv and search-log.csv alongside the report')
    args = parser.parse_args()
    if not args.report.is_file():
        print(f'MISSING: {args.report}', file=sys.stderr)
        return 2
    content = args.report.read_text(encoding='utf-8')
    errors = []
    for label in REQUIRED_HEADERS:
        if not any(label.lower() in line.lower() for line in re.findall(r'^#{1,5}\s+.*$', content, re.M)):
            errors.append(f'Missing section heading containing: {label}')
    for text in ('Closest Prior Work', 'Known Findings', 'Research Gap', 'Claimed Contribution', 'Strongest Objection', 'Fallback Contribution'):
        if text not in content:
            errors.append(f'Missing six-question audit item: {text}')
    if not re.search(r'(?i)https?://|doi\.org/', content):
        errors.append('No source URLs; real audit requires independently checked citations')
    if re.search(r'\[(working title|yyyy-mm-dd|exact title|working paper|what is already known)\]', content, re.I):
        errors.append('Template placeholders remain; replace with substantiated audit details')

    expected = {
        'prior-art.csv': {'paper_id', 'title', 'year', 'doi_or_url', 'claim_id', 'verification_level', 'overlap_type', 'evidence_location'},
        'search-log.csv': {'date', 'worker', 'database', 'query', 'screened_count', 'limitations'},
    }
    for filename, fields in expected.items():
        path = args.report.parent / filename
        if not path.exists():
            if args.strict:
                errors.append(f'Missing {filename}')
            continue
        with path.open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            missing = fields - set(reader.fieldnames or [])
            if missing:
                errors.append(f'{filename}: missing fields {sorted(missing)}')
            rows = list(reader)
            if not rows:
                errors.append(f'{filename}: no entries')
            if filename == 'prior-art.csv':
                for n, row in enumerate(rows, 2):
                    if not row.get('doi_or_url', '').strip().startswith(('https://', 'http://')):
                        errors.append(f'{filename} row {n}: source URL missing or invalid')
                    if not row.get('verification_level', '').strip():
                        errors.append(f'{filename} row {n}: verification level missing')

    if errors:
        for e in errors:
            print('ERROR:', e, file=sys.stderr)
        print('These checks DO NOT verify whether research sources or quotes are genuine.', file=sys.stderr)
        return 1
    print('Structural checks passed. Reminder: source content, DOI metadata, and novelty judgments still require independent verification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
