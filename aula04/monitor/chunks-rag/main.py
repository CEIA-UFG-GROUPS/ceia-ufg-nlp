from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Chunk:
	chunk_id: int
	start: int
	end: int
	text: str

def load_example_doc_pt() -> str:
	path = Path(__file__).with_name("example_doc_pt.txt")
	return path.read_text(encoding="utf-8")
	


def _normalize_text(text: str) -> str:
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = re.sub(r"[\t\x0b\x0c]+", " ", text)
	return text.strip()


def chunk_text_by_chars(text: str, chunk_size: int, overlap: int) -> List[Chunk]:
	if chunk_size <= 0:
		raise ValueError("chunk_size must be > 0")
	if overlap < 0:
		raise ValueError("overlap must be >= 0")
	if overlap >= chunk_size:
		raise ValueError("overlap must be < chunk_size")

	text = _normalize_text(text)
	if not text:
		return []

	chunks: List[Chunk] = []
	step = chunk_size - overlap
	start = 0
	chunk_id = 1

	while start < len(text):
		raw_end = min(len(text), start + chunk_size)
		end = _snap_to_whitespace(text, start, raw_end)
		if end <= start:
			end = raw_end

		chunk_str = text[start:end].strip()
		if chunk_str:
			chunks.append(Chunk(chunk_id=chunk_id, start=start, end=end, text=chunk_str))
			chunk_id += 1

		if end >= len(text):
			break
		start = start + step

	return chunks


def _snap_to_whitespace(text: str, start: int, end: int, window: int = 60) -> int:
	"""Move the end position to a nearby whitespace to avoid breaking words.

	Looks backwards up to `window` chars. If none found, keeps original `end`.
	"""

	if end >= len(text):
		return end
	left = max(start + 1, end - window)
	segment = text[left:end]
	match = re.search(r"\s+(?!.*\s)", segment)
	if not match:
		return end
	return left + match.start()


def retrieve_tfidf(chunks: List[Chunk], question: str, top_k: int) -> List[Tuple[Chunk, float]]:
	question = _normalize_text(question)
	if not question:
		return []
	if not chunks:
		return []

	corpus = [c.text for c in chunks]
	vectorizer = TfidfVectorizer(
		lowercase=True,
		ngram_range=(1, 2),
		max_features=50_000,
	)
	matrix = vectorizer.fit_transform(corpus)
	q_vec = vectorizer.transform([question])
	sims = cosine_similarity(q_vec, matrix).ravel()

	scored = list(zip(chunks, sims))
	scored.sort(key=lambda x: x[1], reverse=True)
	return scored[: max(1, min(top_k, len(scored)))]


def main() -> None:
	st.set_page_config(page_title="Chunks em RAG", layout="wide")
	st.title("Chunks em RAG — demo leve (retrieval + comparação de chunking)")
	st.caption(
		"Objetivo: ajustar chunk_size/overlap e ver como o top-k recuperado muda. "
		"Sem LLM: aqui o foco é *retrieval*, que é onde chunking aparece de forma bem clara."
	)

	with st.sidebar:
		st.header("Configuração")
		chunk_size = st.slider("chunk_size (caracteres)", min_value=200, max_value=1400, value=600, step=50)
		overlap = st.slider("overlap (caracteres)", min_value=0, max_value=400, value=120, step=20)
		top_k = st.slider("top_k", min_value=1, max_value=10, value=3, step=1)
		st.divider()
		st.write("Dica: teste duas configs:")
		st.code("A) chunk_size=900, overlap=50\nB) chunk_size=400, overlap=120", language="text")

	col_left, col_right = st.columns([1, 1])

	with col_left:
		st.subheader("Documento")
		doc_text = st.text_area(
			"Cole o texto aqui (ou use o exemplo):",
			value=load_example_doc_pt(),
			height=360,
		)

	with col_right:
		st.subheader("Pergunta")
		question = st.text_input(
			"Digite uma pergunta para o retrieval:",
			value="O que é overlap e qual o trade-off?",
		)
		run = st.button("Rodar retrieval", type="primary")

	if not run:
		st.info("Clique em 'Rodar retrieval' para ver os chunks e o top-k.")
		return

	try:
		chunks = chunk_text_by_chars(doc_text, chunk_size=chunk_size, overlap=overlap)
	except ValueError as e:
		st.error(str(e))
		return

	if not chunks:
		st.warning("Documento vazio (ou sem texto útil) após normalização.")
		return

	results = retrieve_tfidf(chunks, question=question, top_k=top_k)
	if not results:
		st.warning("Pergunta vazia ou sem resultados.")
		return

	st.divider()
	st.subheader("Resumo")
	st.write(
		{
			"num_chunks": len(chunks),
			"chunk_size": chunk_size,
			"overlap": overlap,
			"top_k": top_k,
		}
	)

	col_a, col_b = st.columns([1, 1])

	with col_a:
		st.subheader("Top-k chunks recuperados")
		for rank, (chunk, score) in enumerate(results, start=1):
			st.markdown(f"**#{rank} — chunk {chunk.chunk_id}** | score={score:.4f} | span=[{chunk.start}, {chunk.end})")
			st.code(chunk.text, language="text")

	with col_b:
		st.subheader("Visão geral dos chunks")
		st.caption("Use isso para ver rapidamente se as fronteiras cortaram ideias no meio.")
		preview_lines = []
		for c in chunks:
			preview = re.sub(r"\s+", " ", c.text)
			preview = (preview[:110] + "…") if len(preview) > 110 else preview
			preview_lines.append(f"{c.chunk_id:02d}. [{c.start:>4},{c.end:>4}) {preview}")
		st.code("\n".join(preview_lines), language="text")

	st.divider()
	st.subheader("Como usar na apresentação (script rápido)")
	st.markdown(
		"""
1) Rode uma pergunta com **Config A** e observe o top-k.
2) Troque para **Config B** e rode a mesma pergunta.
3) Aponte:
   - se a evidência ficou completa/incompleta
   - se ficou redundante (chunks quase iguais)
   - se ficou genérico (chunk grande demais)
"""
	)


if __name__ == "__main__":
	main()

