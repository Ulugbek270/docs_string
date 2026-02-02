#!/usr/bin/env bash
set -e

# export OLLAMA_NO_STREAM=1

python pdf_string.py | ollama run qwen2.5:7b \
"""
Analyze the following Uzbek (Cyrillic) document.

Return ONLY valid JSON. No explanations.

JSON fields:
- author: person name 
- doc_num: number of document (ex: 01/14-1-329-son)
- from_org: organization the document is sent from, if explicitly stated
- date: copy exactly as written; do not normalize or infer()
- context: main body text only (no headers, signatures, stamps)
- adres: for ex(100170, O’zbekiston Respublikasi, Toshkent shahri,
Mirzo-Ulug’bek tumani, Mustaqillik shoh ko’chasi, 107.)
- phone_number:
- email
- code_doc: for ex: (Ҳужжат коди: MM87587866)
"""
