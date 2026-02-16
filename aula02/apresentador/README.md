# Aula 02 — LLMs com APIs (Consumindo Modelos de Linguagem via API)

## README do Apresentador

Este documento organiza a apresentação da aula e serve como **guia teórico + prático** para o expositor.
O foco é mostrar como **consumir LLMs via API**, entender os parâmetros de configuração e as boas práticas de integração.

---

## 1. Objetivo da aula (abrir com isso)

- Fazer o grupo entender **o que é uma API de LLM** e por que ela é a forma mais comum de usar modelos de linguagem em produção.
- Apresentar os **principais provedores** (OpenAI, Anthropic, Google, etc.) e suas diferenças.
- Explicar os **parâmetros de configuração** (temperature, max_tokens, top_p, etc.) e como eles afetam a resposta.
- Rodar uma prática simples fazendo chamadas de API e observando o impacto dos parâmetros.

---

## 2. Parte teórica

### 2.1 O que é uma API de LLM?

- **API (Application Programming Interface)**: interface que permite que seu código "converse" com um serviço externo.
- No caso de LLMs, a API recebe um **prompt** (texto de entrada) e retorna uma **completion** (texto gerado).
- Vantagens de usar API vs rodar modelo local:
  - Não precisa de hardware potente (GPU)
  - Acesso a modelos de ponta (GPT-4, Claude, Gemini)
  - Escalabilidade e manutenção gerenciadas pelo provedor

Mensagem-chave: **APIs democratizam o acesso a LLMs** — você não precisa treinar ou hospedar o modelo.

### 2.2 Anatomia de uma chamada de API

Uma chamada típica tem:

1. **Endpoint**: URL do serviço (ex.: `https://api.openai.com/v1/chat/completions`)
2. **Headers**: metadados da requisição, incluindo autenticação
3. **Body**: payload JSON com o prompt e parâmetros
4. **Response**: JSON com a resposta gerada

Exemplo de estrutura (OpenAI):

```python
import openai

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Explique o que é machine learning."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 2.3 Parâmetros importantes (o que explicar)

| Parâmetro | O que faz | Valores típicos |
|-----------|-----------|-----------------|
| `temperature` | Controla aleatoriedade. Baixo = determinístico, alto = criativo | 0.0 a 2.0 (padrão: 1.0) |
| `max_tokens` | Limite máximo de tokens na resposta | 100 a 4096+ |
| `top_p` | Amostragem por núcleo (alternativa a temperature) | 0.0 a 1.0 |
| `stop` | Sequências que interrompem a geração | Lista de strings |
| `presence_penalty` | Penaliza repetição de tópicos já mencionados | -2.0 a 2.0 |
| `frequency_penalty` | Penaliza repetição de tokens específicos | -2.0 a 2.0 |

Dica para comunicar:
- `temperature=0` para tarefas que precisam de consistência (ex.: extração de dados)
- `temperature=0.7-1.0` para tarefas criativas (ex.: escrita, brainstorming)

### 2.4 Principais provedores de API

| Provedor | Modelos principais | Diferencial |
|----------|-------------------|-------------|
| **OpenAI** | GPT-4, GPT-4o, GPT-3.5 | Mais popular, boa documentação |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | Foco em segurança e contexto longo |
| **Google** | Gemini Pro, Gemini Ultra | Integração com ecossistema Google |
| **Groq** | LLaMA, Mixtral | Inferência ultra-rápida |
| **Together AI** | Modelos open-source | Variedade de modelos, preços competitivos |
| **Mistral AI** | Mistral Large, Mixtral | Modelos europeus, bom custo-benefício |

### 2.5 Autenticação e segurança

- **API Key**: chave secreta que identifica sua conta
- **NUNCA** commitar API keys no código ou repositório
- Usar **variáveis de ambiente** ou gerenciadores de secrets

```bash
# Exemplo: exportar variável de ambiente
export OPENAI_API_KEY="sk-..."
```

```python
import os
api_key = os.getenv("OPENAI_API_KEY")
```

### 2.6 Custos e otimização

- APIs cobram por **tokens** (entrada + saída)
- 1 token ≈ 4 caracteres em inglês, ~3 caracteres em português
- Estratégias de otimização:
  - Usar modelos menores quando possível (GPT-3.5 vs GPT-4)
  - Limitar `max_tokens` ao necessário
  - Implementar **caching** para perguntas repetidas
  - Usar **batching** para múltiplas requisições

### 2.7 Erros comuns (para provocar discussão)

- Expor API key em código público
- Não tratar erros de rate limit (429)
- Ignorar custos e estourar orçamento
- Não validar/sanitizar entrada do usuário
- Confiar cegamente na resposta do modelo

---

## 3. Parte prática (para a aula)

### 3.1 Repositórios de referência para prática

Para a parte prática, recomendamos usar repositórios já validados pela comunidade:

**Opção 1 — OpenAI Cookbook (Oficial)**
- https://github.com/openai/openai-cookbook
- Notebooks oficiais da OpenAI com exemplos de uso da API
- Cobre: chat completions, embeddings, function calling, assistants

**Opção 2 — Anthropic Cookbook (Oficial)**
- https://github.com/anthropics/anthropic-cookbook
- Exemplos oficiais de uso da API Claude
- Cobre: prompting, tool use, vision, embeddings

**Opção 3 — LangChain Tutorial (Comunidade)**
- https://github.com/tiagonpsilva/genai-langchain-tutorial
- Tutorial prático com LangChain, FastAPI e Streamlit
- Bom para ver integração de APIs em aplicações reais

**Opção 4 — ChatGPT Cases (Comunidade)**
- https://github.com/marlosb/ChatGPT_cases
- Exemplos simples de uso da API no Azure OpenAI
- Notebooks Jupyter bem estruturados

### 3.2 O que a prática precisa demonstrar

1. **Fazer uma chamada básica** e ver a resposta
2. **Variar temperature** e observar diferença na criatividade
3. **Testar diferentes prompts** (system message vs user message)
4. **Comparar modelos** (se possível, GPT-3.5 vs GPT-4 ou Claude)

### 3.3 Roteiro sugerido para demo ao vivo

1. Mostrar uma chamada simples no terminal ou notebook
2. Variar `temperature` de 0 para 1.5 e comparar respostas
3. Adicionar `system message` e ver como muda o comportamento
4. Mostrar o JSON de resposta completo (tokens usados, finish_reason)
5. Demonstrar tratamento de erro (ex.: API key inválida)

### 3.4 Atividades sugeridas

**Atividade 1 — Explorar parâmetros**
- Cada participante escolhe uma pergunta
- Testar com temperature=0, 0.5, 1.0, 1.5
- Compartilhar: qual configuração deu melhor resultado?

**Atividade 2 — Comparar provedores**
- Mesma pergunta para OpenAI e Anthropic (ou outro)
- Discutir: diferenças de estilo, velocidade, custo

**Atividade 3 — System prompts**
- Criar diferentes "personas" via system message
- Ex.: "Você é um professor", "Você é um poeta", "Você é um revisor técnico"
- Observar como a mesma pergunta gera respostas diferentes

---

## 4. Pontos de reflexão (fechamento)

- APIs são a forma mais acessível de usar LLMs de ponta, mas têm **custos** e **dependência** de terceiros.
- Entender os **parâmetros** é essencial para controlar o comportamento do modelo.
- **Segurança** (API keys, dados sensíveis) deve ser prioridade desde o início.
- O mercado de APIs está em constante evolução — novos modelos e provedores surgem frequentemente.

---

## 5. Referências rápidas (para citar)

- Documentação OpenAI: https://platform.openai.com/docs
- Documentação Anthropic: https://docs.anthropic.com
- Documentação Google AI: https://ai.google.dev/docs
- OpenAI Cookbook: https://github.com/openai/openai-cookbook
- Anthropic Cookbook: https://github.com/anthropics/anthropic-cookbook


