# RAG Demo (FastAPI + Qdrant)

Demo simples de uma API RAG usando FastAPI e Qdrant, com textos curtos sobre basquete.
O gerador aqui e **intencionalmente simples** (nao usa LLM) para manter o exemplo leve e didático.

## Como rodar

```bash
cd /Users/josericardo/Developer/Repos/GdE/ceia-ufg-nlp/aula03/monitor/rag-demo
docker compose up --build
```

## Teste rapido

Health:

```bash
curl http://localhost:8000/health
```

Consulta:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "O que e uma cesta de tres pontos?", "top_k": 3}'
```

## Estrutura

- `app/main.py`: API FastAPI e logica RAG basica
- `app/data/basketball.txt`: base de textos simples
- `app/Dockerfile`: container da API
- `docker-compose.yml`: API + Qdrant

## Observacoes

- O modelo de embeddings e baixado no primeiro start do container.
- Para trocar os textos, edite `app/data/basketball.txt`.
- Se quiser usar LLM de verdade, a funcao `_simple_generator` e o lugar para trocar.
