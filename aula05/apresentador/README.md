# Aula 05 — Técnicas de Parsing em Documentos (para NLP/RAG)

## README do Apresentador

Este documento organiza a apresentação da aula e serve como **guia teórico + prático**.
O foco é parsing como etapa de **ingestão**: transformar PDFs/HTML/Docs em texto e estrutura confiáveis para indexação, chunking e retrieval.

---

## 1. Objetivo da apresentação (abrir com isso)

- Explicar o que significa “parsing de documentos” no contexto de NLP/RAG.
- Mostrar que muitos erros do RAG vêm de **ingestão ruim** (texto quebrado, tabelas bagunçadas, metadados perdidos).
- Apresentar técnicas e trade-offs: **extração**, **limpeza**, **estrutura**, **tabelas**, **OCR**, **deduplicação**.
- Fazer uma prática rápida: comparar saídas de parsing e ver o impacto nos chunks/retrieval.

---

## 2. Parte teórica

### 2.1 O que é “parsing” de documentos?

- Converter um arquivo (PDF, HTML, DOCX, PPTX, imagens escaneadas) em:
	- **texto** (conteúdo)
	- **estrutura** (títulos, seções, listas, tabelas)
	- **metadados** (fonte, página, seção, data)

Mensagem-chave: parsing não é só “extrair texto”; é **preservar sinal útil** para busca e para o LLM citar evidências.

### 2.2 Por que parsing é crítico em RAG

- RAG depende de recuperação: se o texto extraído está ruim, o embedding representa ruído.
- Perder estrutura (títulos, seções, tabelas) torna:
	- chunking menos coerente
	- retrieval menos preciso
	- respostas menos confiáveis

Sintomas típicos de parsing ruim:
- palavras coladas ou quebradas (hifenização errada)
- ordem de leitura trocada (colunas)
- cabeçalhos/rodapés repetidos dominando o índice
- tabelas virando “sopa de números”
- páginas escaneadas virando texto vazio (sem OCR)

### 2.3 Tipos de documentos e desafios

1) **HTML**
- Fácil extrair texto, mas precisa filtrar nav/menus/ads.
- Preservar headings (h1/h2), listas e links costuma ajudar.

2) **PDF digital (com camada de texto)**
- Extração pode vir com ordem errada, quebras e hifenização.
- Tabelas e multi-coluna são os maiores desafios.

3) **PDF escaneado / imagem**
- Precisa de **OCR** (qualidade depende de resolução, ruído, língua).

4) **DOCX/PPTX**
- Geralmente melhor para estrutura (títulos e bullets), mas pode ter caixas de texto.

### 2.4 Técnicas de parsing (blocos de construção)

**A) Extração (converter para texto/estrutura)**
- HTML: selecionar o “main content” e remover boilerplate.
- PDF: extrair texto por página e tentar reconstruir ordem.
- OCR: reconhecer texto em imagem + (opcional) layout.

**B) Limpeza e normalização**
- Remover headers/footers repetidos.
- Consertar hifenização de fim de linha (quando aplicável).
- Normalizar espaços, quebras de linha e bullets.
- Remover duplicatas (mesmo parágrafo repetido em versões).

**C) Preservação de estrutura**
- Capturar hierarquia: documento → seção → subseção → parágrafo.
- Marcar listas e títulos explicitamente (melhora chunking e citação).

**D) Parsing de tabelas**
- Escolher estratégia:
	- tabela → **CSV/JSON** (boa para precisão)
	- tabela → **texto descritivo** (boa para leitura do LLM)
- Sempre guardar referência: página, título da tabela, coluna/cabeçalho.

**E) Metadados (essenciais para debugging e confiança)**
- `source` (arquivo/URL), `page`, `section_title`, `doc_id`, `timestamp`.

### 2.5 Heurísticas práticas (para orientar o grupo)

- Se a pergunta do usuário costuma citar “na seção X”, preserve headings.
- Se o conteúdo tem muitas tabelas, trate tabelas como objetos próprios.
- Se o PDF é multi-coluna, desconfie da ordem de leitura.
- Sempre faça uma inspeção visual do texto extraído antes de indexar.

### 2.6 Avaliação: como saber se o parsing está bom?

- **Fidelidade**: o texto bate com o documento?
- **Coesão**: parágrafos fazem sentido ou misturam colunas?
- **Ruído**: muito header/footer/padrões repetidos?
- **Cobertura**: páginas/tabelas importantes foram extraídas?

---

## 3. Parte prática (exemplos)

### 3.1 Objetivo da prática

Comparar 2 ou 3 saídas de parsing (ou 2 configurações) e observar:
- diferenças de legibilidade e estrutura
- presença de ruído (header/footer)
- preservação de tabelas/listas
- impacto esperado no chunking e retrieval

### 3.2 Roteiro de prática (um exemplo de prática apenas)

1) Separe 2 documentos pequenos (ideal):
	 - um HTML/Markdown (bem estruturado)
	 - um PDF com tabela OU um PDF escaneado
2) Para cada documento, faça:
	 - extração “crua” (sem limpeza)
	 - extração “tratada” (com limpeza e metadados)
3) Compare lado a lado:
	 - 15–30 linhas do texto resultante
	 - quais campos de metadados vocês guardaram
4) (Opcional) Gere chunks e verifique se títulos e tabelas ficaram “inteiros”.

### 3.3 Checklist de comparação (para guiar a discussão)

- O texto está na ordem certa?
- Os títulos aparecem como títulos (ou se perderam)?
- Listas viraram uma linha só?
- Tabelas:
	- foram extraídas?
	- viraram texto útil ou bagunça?
- Há header/footer repetido contaminando o texto?
- Metadados permitem rastrear a origem (página/seção)?

---

## 4. Mini-demo conceitual (para apresentar em 5–8 min)

### 4.1 Cenário

- Mesma pergunta, mesmo RAG.
- Só muda a qualidade do parsing.

### 4.2 Script do apresentador

1) Mostre um trecho “ruim” (com header/footer, colunas misturadas, tabela quebrada).
2) Pergunte: “Esse texto indexado, como vai recuperar certo?”
3) Mostre a versão “tratada” com:
	 - headings preservados
	 - tabelas representadas (CSV/JSON ou texto limpo)
	 - metadados
4) Conclusão: parsing é **pré-requisito** para chunking e retrieval bons.

---

## 5. Pseudo-código (pipeline mental de ingestão)

```python
docs = carregar_arquivos(["doc.pdf", "pagina.html", "scan.png"])

for doc in docs:
		bruto = extrair(doc)  # pdf/html/ocr
		limpo = limpar(bruto, remover_headers=True, corrigir_hifenizacao=True)

		estrutura = detectar_estrutura(limpo)  # headings, listas, tabelas
		tabelas = extrair_tabelas(doc)         # opcional, dependendo do formato

		registros = montar_registros(
				texto=estrutura.texto,
				metadados={
						"source": doc.nome,
						"page": estrutura.page,
						"section": estrutura.section_title,
				},
				tabelas=tabelas,
		)

		chunks = chunkar(registros, estrategia="por_secoes", overlap=...)  # apresentação anterior pode ajudar
		indexar(chunks)
```

---

## 6. Pontos de reflexão (fechamento)

- “RAG bom” começa na ingestão: parsing é onde a base ganha (ou perde) qualidade.
- Estrutura e metadados não são luxo: são o que permite debugar e confiar.
- O melhor parsing depende do tipo de documento (HTML vs PDF vs scan).

---

## 7. Referências rápidas (para citar)

- Conceitos de extração/limpeza e pipelines de ingestão em RAG (documentação de ferramentas)
- Termos para pesquisa: boilerplate removal, PDF layout parsing, table extraction, OCR, document structure extraction
- Ferramentas (exemplos): BeautifulSoup/Readability (HTML), pdfminer/pypdf/pdfplumber (PDF), Tesseract (OCR)

