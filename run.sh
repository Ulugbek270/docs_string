#!/usr/bin/env bash
set -e

# export OLLAMA_NO_STREAM=1

python pdf_string.py | ollama run qwen2.5:7b \
"""
Analyze the following Uzbek (Cyrillic) document.

Return ONLY valid JSON. No explanations.

Extract ONLY what is explicitly written in the text.
If a field is missing or unclear, use null. Do NOT guess.

JSON fields:
- author: person name if explicitly stated
- from_org: organization the document is sent from, if explicitly stated
- doc_author: organization that issued the document, if explicitly stated
- date: copy exactly as written; do not normalize or infer
- context: main body text only (no headers, signatures, stamps)

If the document text is empty, return all fields as null except context = "".



"""
