# Materiais de Estudo — Técnicas de Parsing em Documentos

Materiais para embasar a aula sobre **parsing/ingestão**: transformar PDF/HTML/DOCX/imagens em **texto + estrutura + metadados** de boa qualidade para NLP/RAG.

---

## Parsing Estrutural de Documentos

- **DocParser: Hierarchical Structure Parsing of Document Renderings**  
  https://arxiv.org/abs/1911.01702  
  *Parsing hierárquico end-to-end de documentos renderizados (ex.: PDFs).*

- **HRDoc: Dataset and Baseline for Hierarchical Document Structure Reconstruction**  
  https://arxiv.org/abs/2303.13839  
  *Dataset e baselines para reconstrução de estrutura hierárquica de documentos multi-página.*

- **Detect-Order-Construct: Tree Construction Approach for Document Structure**  
  https://arxiv.org/abs/2401.11874  
  *Pipeline baseado em detecção, ordenação e construção de árvores estruturais.*


## 🧠 Recuperação / RAG 

- Jurafsky & Martin — *Speech and Language Processing (SLP3)*
	https://web.stanford.edu/~jurafsky/slp3/

- Chapter 11 — *Information Retrieval and Retrieval-Augmented Generation*
	https://web.stanford.edu/~jurafsky/slp3/11.pdf

---

## 🧰 Ferramentas e Docs (Parsing na prática)

### PDF (texto e layout)

- `pypdf` (extração básica de texto)
	https://pypdf.readthedocs.io/

- `pdfplumber` (extração + tabelas + inspeção de layout)
	https://github.com/jsvine/pdfplumber

- `pdfminer.six` (extração detalhada)
	https://github.com/pdfminer/pdfminer.six

- Apache Tika (extração para múltiplos formatos)
	https://tika.apache.org/

### OCR

- Tesseract OCR
	https://github.com/tesseract-ocr/tesseract

- PaddleOCR
	https://github.com/PaddlePaddle/PaddleOCR

### HTML (boilerplate removal)

- Beautiful Soup
	https://www.crummy.com/software/BeautifulSoup/

- readability-lxml (extrair “conteúdo principal”)
	https://github.com/buriy/python-readability

### Ingestão para RAG (pipelines)

- LangChain — Document Loaders
	https://python.langchain.com/docs/concepts/document_loaders/

- LangChain — Text Splitters
	https://python.langchain.com/docs/concepts/text_splitters/

- LlamaIndex — Data Loading / Node Parsers
	https://docs.llamaindex.ai/en/stable/module_guides/loading/

---

## 📊 Tópicos importantes

- **Ordem de leitura em PDF**: colunas, caixas de texto e quebras de linha
- **Header/footer**: ruído repetido dominando embeddings e retrieval
- **Tabelas**: texto “sopa” vs estrutura (CSV/JSON) vs texto descritivo
- **Metadados por chunk**: `source`, `page`, `section_title`, `doc_id`
- **Deduplicação e versões**: mesmo conteúdo repetido em várias páginas/arquivos
- **Qualidade de OCR**: resolução, idioma, ruído, skew



