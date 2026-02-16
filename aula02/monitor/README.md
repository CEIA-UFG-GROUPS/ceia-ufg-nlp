# Aula 02 — LLMs com APIs

## Material de Estudo Prévio (Monitor)

Este material prepara o monitor para a aula sobre **LLMs com APIs** e como consumir modelos de linguagem de forma programática. Serve como **estudo prévio**, alinhado ao modelo colaborativo do Grupo de Estudos em NLP do CEIA/UFG.

---

## Objetivo da Aula

Ao final desta aula, espera-se que os participantes compreendam:

- O que são **APIs de LLM** e por que são a forma mais comum de usar modelos de linguagem em produção.
- A **anatomia de uma chamada de API**: endpoints, autenticação, payload e resposta.
- Os **parâmetros de configuração** (temperature, max_tokens, top_p, etc.) e como eles afetam o comportamento do modelo.
- Os **principais provedores** (OpenAI, Anthropic, Google, etc.) e suas diferenças.
- **Boas práticas** de segurança, custos e otimização.
- Atividades práticas usando repositórios de referência da comunidade.

---

## Contexto: Por que usar APIs de LLM?

### O Problema

Modelos de linguagem de grande porte (LLMs) como GPT-4 ou Claude requerem:
- **Hardware especializado** (GPUs de alto custo)
- **Infraestrutura complexa** (servidores, balanceamento, monitoramento)
- **Expertise técnica** para deploy e manutenção

Para a maioria dos casos de uso, hospedar um modelo localmente é **impraticável** ou **economicamente inviável**.

### A Solução: APIs

APIs de LLM oferecem:
- **Acesso imediato** a modelos de ponta sem infraestrutura própria
- **Escalabilidade automática** gerenciada pelo provedor
- **Atualizações contínuas** sem esforço do usuário
- **Modelo de pagamento por uso** (pay-as-you-go)

> **"APIs democratizam o acesso a LLMs"** — você não precisa treinar, hospedar ou manter o modelo. Basta fazer uma requisição HTTP.

### Trade-offs

| Vantagem | Desvantagem |
|----------|-------------|
| Sem necessidade de GPU | Dependência de terceiros |
| Acesso a modelos SOTA | Custos podem escalar |
| Escalabilidade automática | Latência de rede |
| Manutenção zero | Dados enviados para fora |

---

## Conceitos Fundamentais

### 1. Tokens

- **Token** é a unidade básica de processamento do LLM
- Não é exatamente uma palavra: pode ser parte de palavra, pontuação, espaço
- Regra aproximada: 1 token ≈ 4 caracteres em inglês, ~3 em português
- APIs cobram por **tokens de entrada + tokens de saída**

Exemplo:
```
"Olá, mundo!" → ["Ol", "á", ",", " mundo", "!"] → 5 tokens
```

### 2. Context Window

- **Janela de contexto** = limite máximo de tokens que o modelo processa
- Inclui: prompt + histórico + resposta
- Modelos modernos: 8K, 32K, 128K, até 1M tokens
- Se exceder o limite, a API retorna erro ou trunca

### 3. Temperature

- Controla a **aleatoriedade** da geração
- `temperature=0`: determinístico, sempre escolhe o token mais provável
- `temperature=1`: amostragem padrão, mais variado
- `temperature>1`: mais criativo/caótico

Quando usar:
- **Baixa (0-0.3)**: extração de dados, classificação, tarefas factuais
- **Média (0.5-0.7)**: conversação, assistentes
- **Alta (0.8-1.2)**: escrita criativa, brainstorming

### 4. Max Tokens

- Limite máximo de tokens na **resposta**
- Não afeta qualidade, apenas comprimento
- Se a resposta for cortada, `finish_reason` será `"length"`

### 5. Top-p (Nucleus Sampling)

- Alternativa a temperature
- Considera apenas os tokens cuja probabilidade acumulada ≤ p
- `top_p=0.1`: considera apenas os 10% mais prováveis
- `top_p=1.0`: considera todos os tokens

Dica: use **ou** temperature **ou** top_p, não ambos.

### 6. Stop Sequences

- Strings que interrompem a geração quando encontradas
- Útil para formatar saída ou evitar texto extra
- Exemplo: `stop=["\n\n", "FIM"]`

### 7. Penalties

- `presence_penalty`: penaliza tokens que já apareceram (evita repetição de tópicos)
- `frequency_penalty`: penaliza tokens proporcionalmente à frequência (evita repetição de palavras)
- Valores: -2.0 a 2.0 (positivo = mais penalidade)

---

## Pipeline de uma Chamada de API

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Cliente   │────▶│   API LLM   │────▶│   Modelo    │
│  (seu app)  │◀────│  (servidor) │◀────│   (GPT-4)   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      │  1. Request        │  2. Processa       │
      │  (prompt +         │  autenticação      │
      │   parâmetros)      │                    │
      │                    │  3. Envia para     │
      │                    │  o modelo          │
      │                    │                    │
      │  6. Response       │  5. Retorna        │  4. Gera
      │  (completion +     │  resposta          │  resposta
      │   metadata)        │                    │
      └────────────────────┴────────────────────┘
```

### Estrutura da Request (OpenAI)

```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "Você é um assistente útil."},
    {"role": "user", "content": "O que é machine learning?"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

### Estrutura da Response

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Machine learning é..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  }
}
```

---

## Boas Práticas e Segurança

### Gerenciamento de API Keys

**NUNCA faça isso:**
```python
# ❌ ERRADO: API key hardcoded
api_key = "sk-abc123..."
```

**Faça isso:**
```python
# ✅ CERTO: variável de ambiente
import os
api_key = os.getenv("OPENAI_API_KEY")
```

Outras opções:
- **dotenv**: arquivo `.env` local (não commitar!)
- **Vault**: gerenciador de secrets empresarial
- **AWS Secrets Manager / GCP Secret Manager**: para cloud

### Tratamento de Erros

Erros comuns:
- `401 Unauthorized`: API key inválida
- `429 Too Many Requests`: rate limit excedido
- `500 Internal Server Error`: problema no servidor

Implementar **retry com backoff exponencial**:
```python
import time

def call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** i  # 1, 2, 4 segundos
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

### Controle de Custos

- Definir **limites de uso** no dashboard do provedor
- Monitorar **tokens consumidos** por requisição
- Usar **modelos menores** quando possível (GPT-3.5 vs GPT-4)
- Implementar **caching** para perguntas repetidas

---

## Repositórios de Referência para Prática

Como a parte prática desta aula utiliza repositórios externos validados, aqui estão as principais referências:

### Repositórios Oficiais

1. **OpenAI Cookbook**
   - https://github.com/openai/openai-cookbook
   - Notebooks oficiais com exemplos de chat, embeddings, function calling
   - Ideal para aprender a API da OpenAI

2. **Anthropic Cookbook**
   - https://github.com/anthropics/anthropic-cookbook
   - Exemplos oficiais de uso da API Claude
   - Cobre prompting, tool use, vision

### Repositórios da Comunidade

3. **LangChain Tutorial**
   - https://github.com/tiagonpsilva/genai-langchain-tutorial
   - Tutorial prático com LangChain, FastAPI e Streamlit
   - Bom para ver integração de APIs em aplicações reais

4. **ChatGPT Cases**
   - https://github.com/marlosb/ChatGPT_cases
   - Exemplos simples de uso da API no Azure OpenAI
   - Notebooks Jupyter bem estruturados em 2 partes

---

## Pontos para Reflexão Pré-Aula

Como monitor, reflita sobre:

1. **Quando usar API vs modelo local?**
   - Considere: custo, latência, privacidade, escala
   - APIs são melhores para prototipagem e produção leve
   - Modelos locais para dados sensíveis ou alto volume

2. **Como escolher entre provedores?**
   - OpenAI: mais popular, melhor documentação
   - Anthropic: foco em segurança, contexto longo
   - Google: integração com ecossistema
   - Open-source: controle total, sem dependência

3. **Quais os riscos de segurança?**
   - Vazamento de API keys
   - Dados sensíveis enviados para terceiros
   - Prompt injection (usuário manipulando o modelo)
   - Custos inesperados

4. **Como otimizar custos em produção?**
   - Caching de respostas
   - Escolha de modelo adequado ao caso
   - Limites de tokens
   - Monitoramento contínuo

5. **Qual o impacto da escolha de parâmetros?**
   - Temperature muito alta pode gerar nonsense
   - Max_tokens muito baixo pode cortar respostas
   - System prompt mal feito pode confundir o modelo

---

## Referências

### Documentação Oficial
- OpenAI API: https://platform.openai.com/docs
- Anthropic API: https://docs.anthropic.com
- Google AI: https://ai.google.dev/docs

### Papers
- Brown et al. (2020) — *Language Models are Few-Shot Learners*
- Ouyang et al. (2022) — *Training language models to follow instructions*

### Ferramentas
- LangChain: https://python.langchain.com
- LiteLLM: https://docs.litellm.ai (interface unificada para múltiplas APIs)


