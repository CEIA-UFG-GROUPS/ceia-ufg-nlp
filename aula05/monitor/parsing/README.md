# Demo — Técnicas de parsing em documentos (Streamlit)

Aplicação leve para demonstrar **parsing de documentos** (HTML/PDF/texto) com comparação entre:
- **extração bruta** (o que você normalmente “pega do arquivo”)
- **texto tratado** (mais adequado para chunking/indexação em NLP/RAG)

A demo foca em práticas comuns:
- remoção de boilerplate (HTML: `nav/header/footer/aside`)
- normalização de espaços e quebras de linha
- de-hifenização (`informa-\nção` → `informação`)
- remoção de linhas por regex (útil para header/footer)

## Como rodar (Windows / PowerShell)

Na pasta desta demo:

```powershell
cd .\aula05\monitor\parsing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run main.py
```

Abra o link que o Streamlit mostrar (normalmente `http://localhost:8501`).

## Como usar na apresentação

1) Suba um PDF simples (digital) ou cole um HTML.
2) Mostre a coluna **Extração bruta** e a coluna **Texto tratado**.
3) Ajuste as opções na sidebar (regex/header/footer, de-hifenização, boilerplate HTML).
4) Conclusão: *parsing ruim = índice ruim = retrieval ruim*.

## Dicas

- Para testar regex de remoção, edite o campo "Remover linhas por regex" (uma expressão por linha).
- PDFs escaneados (imagem) não terão texto via `pypdf` (precisaria OCR). Para manter leve, esta demo não faz OCR.
