# Chunks em RAG — Demo leve (local)

Aplicação simples para demonstrar, na hora da apresentação, como `chunk_size` e `overlap` mudam o **top‑k recuperado**.

- Leve: não usa LLM e não precisa de banco vetorial.
- Foco: **retrieval** (TF‑IDF + similaridade cosseno) + visualização dos chunks.

## Como rodar (Windows / PowerShell)

Na pasta do projeto:

```powershell
cd .\aula04\monitor\chunks-rag
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r .\requirements.txt
streamlit run .\main.py
```

Abra o browser no endereço que o Streamlit mostrar (geralmente `http://localhost:8501`).

## Como usar na apresentação

1. Cole um documento (ou use o texto exemplo).
2. Faça uma pergunta.
3. Rode o retrieval com uma config A (chunk grande, overlap baixo).
4. Troque para uma config B (chunk menor, overlap moderado) e rode de novo.
5. Compare:
   - quais chunks entraram no top‑k
   - se a evidência ficou completa/incompleta
   - se apareceu redundância (chunks quase iguais)

## Dicas de configs (para demonstrar diferenças)

- **A:** `chunk_size=900`, `overlap=50`
- **B:** `chunk_size=400`, `overlap=120`

## Observação

Como a demo é TF‑IDF (não embedding neural), ela é intencionalmente simples e didática: o objetivo é visualizar o efeito do chunking no retrieval, não maximizar qualidade SOTA.
