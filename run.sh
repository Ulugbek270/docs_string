#!/usr/bin/env bash
set -e

# export OLLAMA_NO_STREAM=1

python pdf_string.py | ollama run qwen2.5:7b \
"Extract document metadata from this Uzbek text as JSON:
{
  \"author\": \"name from signature\",
  \"doc_num\": \"document number\",
  \"from_org\": \"sending organization name\",
  \"date\": \"date as written\",
  \"context\": \"main text body only\",
  \"adres\": \"full address\",
  \"phone_number\": \"phone\",
  \"email\": \"email\",
  \"code_doc\": \"document code if present\"
}
Return only valid JSON, no other text."