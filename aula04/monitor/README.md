# Aula 04 — Monitor (Guia: Chunks em RAG)

Este README é um **guia conceitual** para o monitor sobre o que são **chunks em RAG**, por que existem e quais decisões importam.

---

## 1. O que é um “chunk” em RAG?

- **Chunk** é um trecho do documento que vira uma **unidade indexável e recuperável**.
- No pipeline de RAG, você não indexa “o PDF inteiro” como uma coisa só; você indexa vários chunks.
- Na hora da pergunta, o retrieval retorna **top-k chunks**, e o LLM responde a partir deles.

Frase-guia:
> “O RAG não responde do documento; ele responde dos chunks que o retrieval traz.”

---

## 2. Onde chunking entra no pipeline

1) Ingestão (parse/limpeza)
2) **Chunking** (dividir em trechos)
3) Embeddings (vetor por chunk)
4) Indexação (armazenar vetores + metadados)
5) Consulta (embedding da pergunta)
6) Retrieval (top-k chunks)
7) Prompt (montar contexto)
8) Geração (LLM)

Chunking é a ponte entre “documento bruto” e “contexto recuperável”.

---

## 3. Decisões de chunking (conceitos)

### 3.1 Tamanho do chunk (`chunk_size`)

- Chunk grande: mais contexto interno, porém o embedding tende a “misturar tópicos” e o ranking pode perder foco.
- Chunk pequeno: mais precisão, porém aumenta risco de quebrar a ideia (definição sem condição/exceção).

### 3.2 Overlap (`chunk_overlap`)

- Overlap = repetir um pedaço do final de um chunk no começo do próximo.
- Serve para reduzir perdas em fronteiras (transições, definições que atravessam parágrafos).

Trade-off:
- + Aumenta recall em perguntas que cruzam parágrafos.
- − Aumenta redundância e custo (mais texto e chunks “parecidos” no top-k).

### 3.3 Delimitadores / estrutura

- Em vez de cortar “no meio da frase”, usar limites naturais melhora coesão:
  - parágrafos
  - headings/seções
  - bullets/listas
  - blocos de código

Ideia central: chunks “bons” tendem a ser **coerentes** (um tema por chunk) e **autossuficientes** (não dependem do vizinho para fazer sentido).

### 3.4 Metadados por chunk

Mesmo quando o texto do chunk é bom, metadados dão rastreabilidade:
- `source` (arquivo/URL)
- `section_title`
- `page` (PDF)
- `doc_id`

Isso ajuda a:
- depurar retrieval
- citar evidência
- aplicar filtros (por documento, por seção)

---

## 4. O que chunking “resolve” e o que ele não resolve

- Chunking melhora a chance de o retrieval encontrar **o pedaço certo**.
- Chunking não corrige:
  - documento mal parseado (texto fora de ordem, tabelas quebradas)
  - embeddings ruins
  - prompt que não obriga usar contexto
  - perguntas ambíguas sem fonte clara

---

## 5. Sinais de chunking ruim (para diagnosticar)

- Top-k traz chunks longos e genéricos (muitos tópicos no mesmo trecho).
- Top-k traz chunks quase idênticos (overlap alto ou documento repetido).
- O chunk recuperado menciona o assunto, mas não contém a evidência completa.
- A resposta do LLM “parece certa” mas não dá para apontar onde está no contexto.

---

## 6. Heurísticas simples 

- Se as perguntas costumam ser **definições curtas**, chunks menores tendem a funcionar bem.
- Se as respostas exigem **parágrafo + parágrafo**, um pouco de overlap ajuda.
- Se o documento tem **headings claros**, chunk por seção/subseção costuma ser melhor que “tamanho fixo”.
- Se o top-k está redundante, reduza overlap ou aumente diversidade (ex.: MMR, quando disponível).

---



