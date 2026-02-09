# Aula 04 — Chunks em RAG (Chunking, Overlap e Recuperação)

## README do Apresentador

Este documento organiza a apresentação da aula e serve como **guia teórico + prático** para o expositor.
O foco é mostrar como **chunking** afeta diretamente o retrieval (recall/precisão), a qualidade do contexto e o risco de alucinações.

---

## 1. Objetivo da aula (abrir com isso)

- Fazer o grupo entender o que é um **chunk** no RAG e por que ele é uma decisão de projeto (não um detalhe).
- Apresentar as principais estratégias: **tamanho**, **overlap**, **delimitadores**, **hierarquia**, **metadados**.
- Rodar uma prática simples comparando configurações de chunking e observando impacto no **top-k recuperado** e na **resposta**.

---

## 2. Parte teórica

### 2.1 O que é “chunking” no RAG?

- Chunking = dividir documentos longos em **trechos menores** antes de gerar embeddings e indexar.
- O LLM não “lê o documento” inteiro: ele vê apenas os **chunks recuperados**.

Mensagem-chave: **o RAG responde com base em chunks**, então chunking define o “vocabulário” de contexto que o sistema consegue trazer.

### 2.2 Por que chunking importa (intuição)

- Se o chunk é **grande demais**, ele dilui sinal semântico (embedding “médio”), piora o ranking e pode estourar contexto.
- Se o chunk é **pequeno demais**, ele perde informação essencial (definições incompletas, referências quebradas), e o LLM fica sem suporte para inferir.
- Chunking também afeta custo: mais chunks ⇒ mais embeddings ⇒ mais armazenamento e latência.

### 2.3 Tamanho do chunk e overlap

- **Chunk size** (por tokens ou caracteres): “quanto cabe” em cada pedaço.
- **Overlap**: repetição de uma janela do final no começo do próximo chunk.

Trade-off do overlap:
- + Ajuda a capturar conceitos que atravessam fronteiras (títulos, definições, listas).
- − Aumenta redundância, custo e risco de recuperar “quase o mesmo chunk” várias vezes.

Regra prática para comunicar:
- Comece com chunk “médio” + overlap “pequeno/moderado”, e **meça**.

### 2.4 Como chunking afeta retrieval (o que observar)

1) **Recall**: o chunk certo aparece no top-k?
2) **Precisão do contexto**: os chunks recuperados são “focados” na pergunta?
3) **Coerência**: o chunk contém o pedaço completo (definição + condição + exceção)?
4) **Redundância**: top-k traz chunks repetidos?

### 2.5 Estratégias comuns de chunking

1) **Por tamanho fixo** (caracteres/tokens)
- Simples, mas pode quebrar frases e seções.

2) **Por delimitadores** (parágrafos, headings, bullets)
- Mantém estrutura; geralmente melhora recuperabilidade.

3) **Semântico/híbrido**
- Usa limites estruturais, mas ajusta tamanho para manter coesão.

4) **Hierárquico** (seções → subseções → parágrafos)
- Permite recuperar em diferentes granularidades.

5) **Com metadados**
- Salvar `source`, `section`, `title`, `page`, `timestamp` ajuda filtering e explicação.

### 2.6 Erros clássicos (para provocar discussão)

- Chunking “cego” que mistura tópicos diferentes no mesmo chunk.
- Não guardar metadados: depois você não sabe “de onde veio”.
- Overlap alto demais gerando top-k redundante.
- Avaliar só a resposta do LLM e ignorar o retrieval (quando dá errado, quase sempre começa no retrieval).

---

## 3. Parte prática (para a aula)

### 3.1 O que a prática precisa demonstrar

Comparar 2 ou 3 configurações e observar:
- Quais chunks entram no top-k.
- Se o chunk recuperado “contém a evidência” necessária.
- Se a resposta final melhora/piora.

Sugestão de configs (mínimo viável):
- **A:** chunks maiores, overlap baixo
- **B:** chunks menores, overlap moderado
- **C (opcional):** chunking por parágrafos/headings

### 3.2 Mini-demo (roteiro rápido)

1) Escolha um texto com uma definição + detalhes (ex.: artigo curto, manual, política interna fake).
2) Faça 3 perguntas:
   - Uma pergunta “direta” (a definição literal).
   - Uma pergunta “que cruza frases” (depende de 2 parágrafos).
   - Uma pergunta “parecida” (para testar confusão/ambiguidade).
3) Rode o retrieval com top-k=3 e mostre os chunks.
4) Rode a geração instruindo: **responda apenas com base no contexto**.

### 3.3 Checklist de avaliação (durante a prática)

- O chunk recuperado tem a frase exata que responde?
- A resposta cita/usa o conteúdo ou “viaja”?
- O top-k veio redundante?
- Se deu errado: foi chunking? embedding? ranking? prompt?

---

## 4. Exemplo de pseudo-código (para explicar o loop)

Use como quadro mental (não precisa executar assim):

```python
configs = [
	{"name": "A_grande_pouco_overlap", "chunk_size": 800, "overlap": 50},
	{"name": "B_medio_overlap_moderado", "chunk_size": 400, "overlap": 100},
]

pergunta = "..."

for cfg in configs:
	chunks = chunk_documento(texto, chunk_size=cfg["chunk_size"], overlap=cfg["overlap"])
	index = indexar_embeddings(chunks)
	top_chunks = index.buscar(pergunta, top_k=3)

	contexto = "\n\n".join(top_chunks)
	prompt = (
		"Use apenas o CONTEXTO para responder. "
		"Se não houver informação suficiente, diga que não sabe.\n\n"
		f"CONTEXTO:\n{contexto}\n\n"
		f"PERGUNTA: {pergunta}\nRESPOSTA:"
	)
	resposta = llm.gerar(prompt)

	print(cfg["name"], "\nTop chunks:\n", top_chunks, "\nResposta:\n", resposta)
```

---

## 5. Atividades sugeridas (apenas um exemplo)

### 5.1 Atividade 1 — Encontrar o “melhor chunking”

- escolhe 2 configurações (size/overlap) e 3 perguntas.
- Objetivo: maximizar “chunk certo no top-3” e minimizar redundância.
- Compartilhar rapidamente: o que mudou e por quê.

### 5.2 Atividade 2 — Diagnóstico de falhas

- Dê um caso onde o RAG “falha”.
- Pergunta-guia: o erro vem de chunking, retrieval ou geração?
- Peça para justificarem com o top-k recuperado.

---

## 6. Pontos de reflexão (fechamento)

- Chunking é um **trade-off** entre coesão semântica, custo e recuperabilidade.
- Não existe tamanho perfeito universal: depende do domínio, do tipo de pergunta e do modelo.
- O “certo” é o que melhora métricas de retrieval e reduz respostas sem evidência.

---

## 7. Referências rápidas (para citar)

- Conceitos gerais de RAG (Lewis et al., 2020)
- Práticas de chunking e avaliação de retrieval (guias técnicos de ferramentas e blogs de engenharia)
- Ferramentas onde chunking é explícito: LangChain (TextSplitters), Haystack, LlamaIndex

