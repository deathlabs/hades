#!/bin/sh

curl -X POST http://localhost:9999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b-instruct-v0.2",
    "messages": [
      {"role": "user", "content": "Where is Pittsburgh?"}
    ],
    "temperature": 0.7,
    "max_tokens": 128
  }'

echo ""
