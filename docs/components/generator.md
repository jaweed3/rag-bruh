# Generator

LLM answer generation via Groq API.

## Model

`llama3-70b-8192` — free tier: 30 req/min, 6000 req/day.

## Prompt

System:
```
You are a librarian assistant for a campus library.
Answer based ONLY on the retrieved context below.
If the context doesn't contain the answer, say "I don't have that information."
Cite the document title for each claim.
```

User:
```
Context:
[Title1] chunk text...
[Title2] chunk text...

Question: {query}
```

## Fallback Chain

1. Groq API
2. (optional) Ollama local Llama 3.2 8B
3. (optional) OpenRouter

## Config

```yaml
groq:
  api_key: ""       # required
  model: llama3-70b-8192
  max_tokens: 1024
  temperature: 0.3
```
