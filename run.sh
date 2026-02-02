#!/usr/bin/env bash
set -e

# export OLLAMA_NO_STREAM=1

python pdf_string.py | ollama run qwen2.5:7b \
"Analyze this Uzbek/Cyrillic document.
Give:
- author
- company
- date
- short summary

If text is empty, say so."
