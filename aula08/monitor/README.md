# 📘 Aula 08 — Agentes em NLP (com foco em Produção)
## Material de Estudo Prévio (Monitor)

Este material tem como objetivo **preparar o monitor para a aula de Agentes em NLP**, oferecendo uma base conceitual sólida para acompanhar, complementar e aprofundar a discussão conduzida pelo apresentador.

⚠️ **Este conteúdo não é um guia de instruções para o monitor**, mas sim um **material de estudo prévio**, alinhado ao modelo colaborativo do Grupo de Estudos em MLOps do CEIA/UFG.

Recomenda-se fortemente a leitura dos links e documentações de referência mais abaixo. Elas explicam muito bem os fundamentos, padrões de design e desafios reais de agents em produção. Se for para começar, leia a documentação do LangGraph e do LangSmith — são as mais práticas e atualizadas para 2026.

---

## 🎯 Objetivo da Aula

Ao final desta aula, espera-se que os participantes compreendam:

- O que são agentes em NLP e como diferem de chatbots tradicionais ou chains simples
- Componentes principais: LLM como raciocínio, tools, memory, planning e reflection
- Padrões comuns: ReAct, Plan-and-Execute, Multi-Agent Collaboration
- Desafios de produção: non-determinism, safety, latência, custo e loops infinitos
- Melhores práticas de MLOps para agents (testing, monitoring, iteration, guardrails)
- Frameworks populares (LangGraph, CrewAI, AutoGen) e quando usar cada um
- Como integrar agents com RAG, embeddings e bancos vetoriais
- Como avaliar e iterar agents em cenários reais de NLP

---

## 🧠 Contexto: Evolução dos Agentes em NLP

### Breve História

**Pré-LLM (até ~2022):**
- Chatbots rule-based ou ML clássico (RASA, Dialogflow)
- Limitações: fluxos fixos, sem raciocínio multi-step

**Era LLM Inicial (2022–2023):**
- LangChain chains + tools → primeiros agents (MRKL, ReAct)
- Auto-GPT, BabyAGI → prova de conceito de autonomia

**Era Moderna (2024–2026):**
- LangGraph → workflows stateful e graph-based
- CrewAI, AutoGen → multi-agent systems colaborativos
- Reflexion, Self-Consistency, Tree-of-Thoughts → reflection e planning avançado
- Integração nativa com RAG, function calling e guardrails

**Por que Agentes Importam Agora?**
- LLMs sozinhos alucinam ou falham em tarefas complexas
- Agents quebram tarefas em steps, usam tools e corrigem erros
- Essenciais para aplicações enterprise: análise de documentos, suporte ao cliente, automação de workflows NLP

> **"Um bom agent é um LLM que sabe quando parar de pensar e começar a agir"** — Princípio chave em produção

---

## 📋 Conceitos Fundamentais de Agentes em NLP

### O que é um Agente?

**Definição:** Sistema autônomo que usa LLM para perceber ambiente, planejar ações, executar tools e refletir sobre resultados para atingir um objetivo.

**Componentes principais:**
- **LLM / Brain**: raciocínio, decision making, parsing de outputs
- **Tools / Actions**: funções externas (busca web, DB query, calculator, API calls)
- **Memory**: short-term (contexto atual), long-term (vector store + retrieval)
- **Planning**: decomposition (break task), reflection (critique own output)
- **Executor / Controller**: loop de decisão (ReAct, Plan-and-Solve)

### Padrões de Design Populares

1. **ReAct** (Reason + Act) — pensa, age, observa, repete
2. **Plan-and-Execute** — planeja passos completos antes de executar
3. **Reflection / Self-Critique** — agent avalia e melhora sua própria resposta
4. **Multi-Agent** — vários agents colaboram (ex.: researcher + writer + reviewer)
5. **Graph-based** (LangGraph) — estado explícito, branching, human-in-the-loop

### Desafios em Produção

**Principais problemas:**
- Non-determinism → outputs variam mesmo com mesma input
- Loops infinitos ou tool overuse
- Alta latência e custo (múltiplas chamadas LLM)
- Safety: alucinações, prompt injection, dados sensíveis
- Debugging difícil: traces longos e complexos

**Checklist de produção:**
- Tem guardrails (Nemo Guardrails, LlamaGuard)?
- Latency aceitável por step?
- Custo médio por query monitorado?
- Existe fallback para falhas?
- Traces salvos e analisáveis?

### Melhores Práticas MLOps para Agentes

**1. Testing**
- Golden datasets de tarefas NLP
- Unit tests para tools
- E2E evaluation com métricas (BLEU, ROUGE, faithfulness)

**2. Monitoring**
- LangSmith / Phoenix para traces completos
- Prometheus + Grafana: latência por step, tool usage, error rate
- Drift detection em prompts e tool outputs

**3. Iteration**
- A/B testing de prompts e models
- Human feedback loop (RLHF-like para agents)
- Versionamento de graphs e tools

**4. Safety & Guardrails**
- Input/output validation
- Topic restrictions
- Rate limiting por usuário

**Importância:**
> **"Agents em produção não são sobre inteligência máxima, mas sobre confiabilidade máxima"**

---

## 🤖 Frameworks Recomendados para Produção (2026)

### Top 4 para NLP em Produção

1. **LangGraph** — workflows stateful, human-in-the-loop, production-ready
2. **CrewAI** — multi-agent simples e colaborativo (bom para equipes)
3. **AutoGen** (Microsoft) — conversas multi-agent, pesquisa acadêmica forte
4. **LlamaIndex Workflows / Agents** — integrado com RAG e data querying

### Quando Usar Cada Um?

**LangGraph** — quando precisa de controle fino, estado persistente e deploy robusto  
**CrewAI** — quando quer orquestrar múltiplos agents rapidamente  
**AutoGen** — quando foco em colaboração conversacional entre agents  
**LlamaIndex** — quando o core é RAG + querying de dados

---

## ⚖️ Comparação: Frameworks de Agentes em Produção

| Framework     | Stateful? | Multi-Agent? | Human-in-loop? | Tracing Nativo | Facilidade | Produção Readiness | Recomendado para          |
|---------------|-----------|--------------|----------------|----------------|------------|--------------------|----------------------------|
| LangGraph    | Sim      | Sim         | Sim           | LangSmith     | Média-Alta | Alta              | Workflows complexos NLP   |
| CrewAI       | Parcial  | Sim         | Limitado      | Básico        | Alta       | Média-Alta        | Colaboração rápida        |
| AutoGen      | Sim      | Sim         | Sim           | Bom           | Média      | Média-Alta        | Pesquisa / conversacional |
| LlamaIndex   | Sim      | Limitado    | Sim           | Integrado     | Alta       | Alta              | RAG-heavy agents          |

### Princípio: Começar Simples

> **"Start with ReAct single-agent, scale to multi-agent when complexity demands"**

1. Comece com chain + tools simples
2. Evolua para ReAct agent
3. Adicione memory e reflection
4. Só multi-agent se tarefa exigir colaboração
5. Sempre monitore traces desde o início

---

## 🛠️ Frameworks e Ferramentas

### LangGraph

**O que é:**
- Biblioteca para construir agents como graphs dirigidos
- Estado explícito, persistência e branching

**Vantagens:**
- Controle total sobre fluxo
- Integração com LangSmith para debugging
- Suporte a streaming e async

### LangSmith

**O que é:**
- Plataforma de observability para LangChain/LangGraph
- Traces completos, datasets de teste, evaluation

**Vantagens:**
- Visualização de decisões passo a passo
- A/B testing de prompts
- Exportação de traces para análise

### CrewAI

**O que é:**
- Framework para orquestrar múltiplos agents colaborativos
- Foco em roles e tarefas

**Vantagens:**
- Sintaxe simples e intuitiva
- Bom para prototipagem multi-agent

### Outras Ferramentas

**Nemo Guardrails / LlamaGuard** — safety layers  
**Phoenix / Arize** — tracing alternativo  
**MLflow** — registry de agents e prompts  
**FastAPI / Litestar** — servir agents como API  
**Kubernetes / Modal** — escalabilidade de agents

---

## 💡 Boas Práticas

### Versionamento e Reprodutibilidade
- Versione graphs, prompts e tools individualmente
- Use LangSmith Projects para separar ambientes
- Fixe versões de LLMs e dependências

### Monitoring em Produção
- Latência por step e total por query
- Tool usage frequency e errors
- Success rate por tarefa NLP
- Human feedback collection
- Alerta para loops longos (>10 steps)

### Evitar Problemas Comuns
- Sempre implementar max_iterations ou token limits
- Usar structured output (JSON mode) para tool calls
- Testar com adversarial inputs
- Implementar fallbacks (ex.: "desculpe, não entendi")
- Loggar todos os intermediate thoughts

### Conexão com MLOps
- Agents são composable systems → cada mudança afeta o todo
- CI/CD deve incluir E2E tests de agents
- Custo por query deve ser rastreado (LLM + tools)
- Use observability desde o dia 1 — debugging retroativo é caro

---

## 💬 Pontos para Reflexão Pré-Aula

Como monitor, reflita sobre:

1. **Por que agents são mais difíceis de colocar em produção do que chains ou RAG simples?**
   - Qual o maior risco em produção?

2. **Como medir o sucesso de um agent em tarefas de NLP?**
   - Quais métricas além de accuracy (ex.: faithfulness, tool efficiency)?

3. **Quando vale a pena multi-agent vs single-agent mais poderoso?**
   - Custo vs benefício em latência e complexidade?

4. **Como lidar com non-determinism em produção?**
   - Estratégias para reproducibilidade parcial?

5. **Qual o papel de guardrails e safety em agents enterprise?**
   - Quando bloquear vs permitir liberdade?

6. **Como iterar agents com feedback de usuários reais?**
   - Integração de human-in-the-loop em escala?

Esses pontos são fundamentais para enriquecer a discussão durante o encontro.

---

## 📚 Referências

### Documentação e Recursos Online

1. **LangGraph Documentation**  
   https://langchain-ai.github.io/langgraph/

2. **LangSmith Observability**  
   https://docs.smith.langchain.com/

3. **CrewAI Documentation**  
   https://docs.crewai.com/

4. **AutoGen (Microsoft)**  
   https://microsoft.github.io/autogen/

5. **LlamaIndex Agents & Workflows**  
   https://docs.llamaindex.ai/en/stable/module_guides/agent/

### Artigos e Blog Posts

6. **"Building Reliable Agents in 2025"**  
   https://blog.langchain.dev/reliable-agents-2025/

7. **"Production Patterns for LLM Agents"**  
   https://www.philschmid.de/production-llm-agents

8. **"Agent Safety & Guardrails"**  
   https://www.nvidia.com/en-us/ai-data-science/nemo-guardrails/

### Exemplos Práticos e Repositórios

9. **LangGraph Tutorials**  
   https://langchain-ai.github.io/langgraph/tutorials/

10. **CrewAI Examples**  
    https://github.com/crewAIInc/crewAI-examples

11. **AutoGen Gallery**  
    https://microsoft.github.io/autogen/docs/Use-Cases/

12. **LangChain Agent Benchmarks**  
    https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/agents