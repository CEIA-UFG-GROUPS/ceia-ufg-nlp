from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable, Literal, Optional

import streamlit as st
from bs4 import BeautifulSoup
from pypdf import PdfReader


InputKind = Literal["Texto", "HTML", "PDF"]


@dataclass(frozen=True)
class ParsedDocument:
	kind: InputKind
	source_name: str
	raw_text: str
	clean_text: str
	notes: tuple[str, ...]


def _read_local_text_file(filename: str) -> str:
	path = Path(__file__).with_name(filename)
	return path.read_text(encoding="utf-8")
	


def load_example_text_pt() -> str:
	return _read_local_text_file("example_text_pt.txt")


def load_example_html_pt() -> str:
	return _read_local_text_file("example_html_pt.html")


def _normalize_newlines(text: str) -> str:
	return text.replace("\r\n", "\n").replace("\r", "\n")


def _collapse_whitespace(text: str) -> str:
	text = re.sub(r"[\t\x0b\x0c]+", " ", text)
	text = re.sub(r"[ ]{2,}", " ", text)
	# mantém quebras de linha; remove excesso em linhas vazias
	text = re.sub(r"\n{3,}", "\n\n", text)
	return text.strip()


def _dehyphenate_linebreaks(text: str) -> str:
	"""Une palavras quebradas por hifenização de final de linha.

	Ex.: "informa-\nção" -> "informação".
	"""
	return re.sub(r"(?i)(\w)-\n(\w)", r"\1\2", text)


def _remove_lines_matching(text: str, patterns: Iterable[str]) -> tuple[str, int]:
	compiled = [re.compile(p) for p in patterns if p.strip()]
	if not compiled:
		return text, 0

	removed = 0
	out_lines: list[str] = []
	for line in _normalize_newlines(text).split("\n"):
		if any(r.search(line) for r in compiled):
			removed += 1
			continue
		out_lines.append(line)

	return "\n".join(out_lines), removed


def parse_plain_text(
	text: str,
	*,
	dehyphenate: bool,
	collapse_ws: bool,
	remove_regex: list[str],
) -> tuple[str, tuple[str, ...]]:
	notes: list[str] = []
	text = _normalize_newlines(text)

	if dehyphenate:
		text = _dehyphenate_linebreaks(text)
		notes.append("De-hifenização aplicada")

	text, removed = _remove_lines_matching(text, remove_regex)
	if removed:
		notes.append(f"Linhas removidas por regex: {removed}")

	if collapse_ws:
		text = _collapse_whitespace(text)
		notes.append("Normalização de espaços/linhas aplicada")

	return text, tuple(notes)


def extract_text_from_html(
	html: str,
	*,
	strip_boilerplate_tags: bool,
) -> tuple[str, tuple[str, ...]]:
	notes: list[str] = []
	soup = BeautifulSoup(html, "html.parser")

	# remove conteúdo que quase sempre é ruído
	for tag in soup(["script", "style", "noscript"]):
		tag.decompose()

	if strip_boilerplate_tags:
		for tag in soup(["nav", "header", "footer", "aside"]):
			tag.decompose()
		notes.append("Remoção de tags boilerplate (nav/header/footer/aside)")

	text = soup.get_text("\n")
	text = _normalize_newlines(text)
	text = _collapse_whitespace(text)
	return text, tuple(notes)


def extract_text_from_pdf(
	pdf_bytes: bytes,
	*,
	page_separator: str,
) -> tuple[str, tuple[str, ...]]:
	reader = PdfReader(BytesIO(pdf_bytes))
	pages: list[str] = []
	for idx, page in enumerate(reader.pages, start=1):
		page_text = page.extract_text() or ""
		page_text = _normalize_newlines(page_text).strip()
		pages.append(f"[Página {idx}]\n{page_text}".strip())

	notes = (f"PDF com {len(reader.pages)} página(s)",)
	return page_separator.join(pages).strip(), notes


def _stats(text: str) -> dict:
	text = _normalize_newlines(text)
	lines = [ln for ln in text.split("\n")]
	non_empty_lines = [ln for ln in lines if ln.strip()]
	return {
		"chars": len(text),
		"lines": len(lines),
		"non_empty_lines": len(non_empty_lines),
	}


def run() -> None:
	st.set_page_config(page_title="Parsing em documentos ", layout="wide")
	st.title("Técnicas de parsing em documentos")
	st.caption(
		"Objetivo: comparar extração bruta vs texto tratado para indexação (NLP/RAG). "
		"Suporta HTML/PDF/texto e aplica limpezas comuns (boilerplate, regex, de-hifenização, normalização)."
	)

	with st.sidebar:
		st.header("Entrada")
		kind: InputKind = st.radio("Tipo de documento", ["Texto", "HTML", "PDF"], horizontal=False)
		uploaded = None
		if kind == "PDF":
			uploaded = st.file_uploader("Envie um PDF", type=["pdf"])
		elif kind == "HTML":
			uploaded = st.file_uploader("Envie um HTML (opcional)", type=["html", "htm"])
		else:
			uploaded = st.file_uploader("Envie um .txt (opcional)", type=["txt", "md"])

		st.divider()
		st.header("Tratamento")
		collapse_ws = st.checkbox("Normalizar espaços/linhas", value=True)
		dehyphenate = st.checkbox("De-hifenizar quebras de linha (PDF/texto)", value=True)
		remove_regex_raw = st.text_area(
			"Remover linhas por regex (1 por linha)",
			value="^HEADER.*$\n^FOOTER.*$",
			height=90,
		)
		remove_regex = [ln.strip() for ln in remove_regex_raw.split("\n") if ln.strip()]

		strip_boilerplate_tags = False
		if kind == "HTML":
			strip_boilerplate_tags = st.checkbox(
				"Remover boilerplate HTML (nav/header/footer/aside)",
				value=True,
			)

		page_separator = "\n\n---\n\n"
		if kind == "PDF":
			page_separator = st.text_input("Separador entre páginas", value=page_separator)

		st.divider()
		top_n = st.slider("Prévia: top N linhas", min_value=20, max_value=200, value=60, step=10)

	st.subheader("Documento")
	if kind == "PDF":
		st.write("Para PDF, use upload (não há exemplo embutido aqui para manter leve).")
	else:
		if uploaded is not None:
			content = uploaded.getvalue().decode("utf-8", errors="replace")
			default_value = content
		else:
			default_value = load_example_html_pt() if kind == "HTML" else load_example_text_pt()
		doc_text = st.text_area(
			"Cole o conteúdo aqui (ou use o exemplo):",
			value=default_value,
			height=280,
		)

	run_btn = st.button("Rodar parsing", type="primary")
	if not run_btn:
		st.info("Clique em 'Rodar parsing' para ver extração bruta vs tratada.")
		return

	source_name = uploaded.name if uploaded is not None else "(entrada manual)"

	# 1) Extração bruta
	if kind == "PDF":
		if uploaded is None:
			st.error("Envie um PDF para continuar.")
			return
		raw, raw_notes = extract_text_from_pdf(uploaded.getvalue(), page_separator=page_separator)
		raw = _normalize_newlines(raw)
	else:
		raw = _normalize_newlines(doc_text)
		raw_notes = ("Entrada em texto",)

	# 2) Tratamento / parsing
	clean_notes: list[str] = []
	clean: str
	if kind == "HTML":
		clean, notes = extract_text_from_html(raw, strip_boilerplate_tags=strip_boilerplate_tags)
		clean_notes.extend(notes)
		# pós-processamento comum
		clean, removed = _remove_lines_matching(clean, remove_regex)
		if removed:
			clean_notes.append(f"Linhas removidas por regex: {removed}")
		if collapse_ws:
			clean = _collapse_whitespace(clean)
			clean_notes.append("Normalização de espaços/linhas aplicada")
	elif kind == "PDF":
		clean, notes = parse_plain_text(
			raw,
			dehyphenate=dehyphenate,
			collapse_ws=collapse_ws,
			remove_regex=remove_regex,
		)
		clean_notes.extend(notes)
	else:
		clean, notes = parse_plain_text(
			raw,
			dehyphenate=dehyphenate,
			collapse_ws=collapse_ws,
			remove_regex=remove_regex,
		)
		clean_notes.extend(notes)

	parsed = ParsedDocument(
		kind=kind,
		source_name=source_name,
		raw_text=raw,
		clean_text=clean,
		notes=tuple(raw_notes) + tuple(clean_notes),
	)

	st.divider()
	st.subheader("Resultado")
	st.write({
		"kind": parsed.kind,
		"source": parsed.source_name,
		"raw_stats": _stats(parsed.raw_text),
		"clean_stats": _stats(parsed.clean_text),
		"notes": list(parsed.notes),
	})

	col_a, col_b = st.columns(2)
	with col_a:
		st.markdown("**Extração bruta**")
		preview = "\n".join(_normalize_newlines(parsed.raw_text).split("\n")[:top_n])
		st.code(preview, language="text")

	with col_b:
		st.markdown("**Texto tratado (pronto para chunking/indexação)**")
		preview = "\n".join(_normalize_newlines(parsed.clean_text).split("\n")[:top_n])
		st.code(preview, language="text")

	st.download_button(
		"Baixar texto tratado (.txt)",
		data=parsed.clean_text.encode("utf-8"),
		file_name="parsed_clean.txt",
		mime="text/plain",
	)

	st.divider()
	st.subheader("Como apresentar")
	st.markdown(
		"""
1) Pegue um PDF ou HTML real e rode com as opções padrão.
2) Mostre como a **extração bruta** vem com ruído (boilerplate/linhas quebradas).
3) Ative/desative:
   - regex de remoção (header/footer)
   - de-hifenização
   - remoção de boilerplate HTML
"""
	)


if __name__ == "__main__":
	run()

