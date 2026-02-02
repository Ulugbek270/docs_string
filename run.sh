#!/usr/bin/env bash
set -e

# export OLLAMA_NO_STREAM=1

python pdf_string.py | ollama run qwen2.5:7b \
"""You are analyzing a document written in Uzbek (Cyrillic).

Return ONLY valid JSON.
Do NOT include explanations, markdown, code fences, or any extra text.

Extract information ONLY if it is explicitly present in the document text.
If a field is not present or cannot be determined from the text, use null.
Do NOT guess. Do NOT infer. Do NOT use external knowledge.

JSON schema (must match exactly):
{
"author": string | null,
"doc_author": string | null,
"from_org": string | null,
"date": string | null,
"context": string,
"language": "uz_cyrl" | "unknown",
"page_count": number | null,
"extraction_method": "text" | "ocr" | "mixed",
"confidence": {
"author": "high" | "low" | "none",
"doc_author": "high" | "low" | "none",
"date": "high" | "low" | "none"
}
}

Field definitions:

* "author": the person who signed the document or is explicitly named as the author (person name).
* "doc_author": the entity that issued the document (organization, ministry, company) if explicitly stated.
* "from_org": the sender organization if explicitly stated; if not stated, set null. (Do NOT copy doc_author unless the text clearly indicates it.)
* "date": copy the date exactly as written in the document; do not normalize or reformat.
* "context": the main body text only. Remove headers/footers, page numbers, stamps, signatures, and contact blocks if present.

Confidence rules:

* "high": explicitly written and clear.
* "low": partially written / ambiguous / incomplete.
* "none": not present (field is null).

System-provided metadata (do NOT guess these from text):

* "language": use the provided value: uz_cyrl
* "page_count": use the provided value: {PAGE_COUNT}
* "extraction_method": use the provided value: {EXTRACTION_METHOD}

If the document text is empty or unreadable, return exactly:
{
"author": null,
"doc_author": null,
"from_org": null,
"date": null,
"context": "",
"language": "uz_cyrl",
"page_count": {PAGE_COUNT},
"extraction_method": "{EXTRACTION_METHOD}",
"confidence": { "author": "none", "doc_author": "none", "date": "none" }
}
"""
