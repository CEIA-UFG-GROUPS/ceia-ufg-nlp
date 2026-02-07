# Aula 03 — RAG (Retrieval-Augmented Generation) em Aplicações de NLP

## README do Apresentador

Este documento organiza a apresentação da aula e serve como **guia conceitual** para o expositor.
A estrutura abaixo deve ser seguida para garantir clareza, progressão logica e alinhamento com o grupo.

---

## 1. Motivação

### 1.1 Por que RAG existe?

- LLMs isolados tem conhecimento **congelado** no treino
- Podem **alucinar** com confiança
- Muitas tarefas exigem **informação atualizada e verificável**

### 1.2 O que o RAG resolve na pratica

- Conecta o LLM a uma **base externa** (docs, FAQs, artigos, dados internos)
- Respostas mais **precisas e contextualizadas**
- Reduz alucinacoes ao exigir **evidencias**

### 1.3 Exemplos de impacto

- Chatbots corporativos com respostas baseadas em documentos oficiais
- QA em bases tecnicas e cientificas
- Busca semantica que entende **significado** e nao so palavras

---

## 2. Como Funciona

### 2.1 Conceitos fundamentais

- **Base de conhecimento**: corpus de documentos que o sistema consulta
- **Embeddings**: representações vetoriais de textos
- **Base vetorial**: armazenamento e busca eficiente de vetores
- **Retrieval**: recuperação dos trechos mais relevantes
- **LLM**: gera a resposta usando o contexto recuperado

### 2.2 Pipeline RAG basico (visao geral)

1. **Chunking** de documentos
2. **Indexação**: gerar embeddings e armazenar na base vetorial
3. **Consulta**: embedding da pergunta e busca dos top-k trechos
4. **Contexto**: montar prompt com trechos recuperados
5. **Geração**: LLM responde com base no contexto

### 2.3 Boas praticas essenciais

- Qualidade da base de conhecimento (garbage in, garbage out)
- Instruções claras no prompt: **responder apenas com o contexto**
- Avaliar retrieval e resposta (relevância + qualidade)
- Manter base atualizada e com metadados

---

## 3. Quickstart (para a aula)

### 3.1 Explicação em 1 minuto

- RAG = **recuperar** trechos relevantes + **gerar** resposta
- Vantagem: respostas **fundamentadas** e com menor risco de erro

### 3.2 Mini-demo conceitual

- Mostrar pergunta sem RAG: resposta genérica ou errada
- Mostrar a mesma pergunta com RAG: resposta ancorada nos docs

### 3.3 Exemplo de pipeline (pseudo-código)

```python
consulta = "Quais sao os sintomas da diabetes tipo 2?"

# 1) Recuperação
trechos = base_vetorial.buscar(consulta, top_k=3)

# 2) Montagem do prompt
contexto = "\n".join([f"- {t}" for t in trechos])
prompt = f"Contexto:\n{contexto}\n\nPergunta: {consulta}\nResposta:"

# 3) Geração
resposta = llm.gerar_texto(prompt)
print(resposta)
```

### 3.4 Atividades sugeridas

- Comparar LLM puro vs RAG em 2 ou 3 perguntas
- Mini-QA em grupos com base pequena de documentos
- Discussão: RAG vs fine-tuning (trade-offs)

---

## 4. Pontos de Reflexao para conduzir a discussao

- O RAG reduz alucinacoes, mas **nao elimina** erros se a fonte estiver ruim
- O que fazer quando o documento certo **nao esta** na base?
- Como garantir que o LLM **use** o contexto recuperado?
- Quais métricas usar para avaliar retrieval e resposta?
- Responsabilidade e ética: dados sensíveis e confiabilidade das fontes

---

## 5. Referencias (para citar rapidamente)

- Lewis et al. (2020): artigo seminal do RAG
- Wang et al. (2024): melhores praticas
- Google Cloud AI Blog (2024): avaliação e tuning
- OpenAI Knowledge Retrieval Blueprint (2023)
- Ferramentas: LangChain, Haystack, FAISS, Qdrant, Weaviate, Milvus
