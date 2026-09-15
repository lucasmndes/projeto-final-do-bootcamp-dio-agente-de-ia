"""Núcleo local e explicável do assistente de conformidade."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_KB = BASE_DIR / "data" / "base_conhecimento.json"
DEFAULT_SOURCES = BASE_DIR / "data" / "fontes_publicas.json"

OUT_OF_SCOPE = {
    "clima", "tempo amanha", "previsao do tempo", "futebol", "receita", "filme", "musica", "viagem"
}
SENSITIVE_PATTERNS = (
    r"\bsenha\b", r"\btoken\b", r"\bchave privada\b", r"\bcodigo de autenticacao\b",
    r"\bdados? (?:do|de um) cliente\b", r"\blista de clientes\b", r"\bcpf\b.*\bcliente\b"
)
INJECTION_PATTERNS = (
    r"ignore (?:as|todas as|suas) instrucoes", r"revele (?:o|seu) prompt",
    r"mostre (?:as|suas) regras internas", r"modo desenvolvedor"
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", normalize(text)) if len(token) > 2}


@dataclass(frozen=True)
class SearchResult:
    topic: dict
    score: float


class ComplianceAssistant:
    """Recupera conteúdo aprovado e responde sem depender de serviço externo."""

    def __init__(self, kb_path: Path = DEFAULT_KB, sources_path: Path = DEFAULT_SOURCES):
        self.knowledge = json.loads(kb_path.read_text(encoding="utf-8"))
        sources = json.loads(sources_path.read_text(encoding="utf-8"))["fontes"]
        self.source_urls = {item["titulo"].split(" — ")[0]: item["url"] for item in sources}

    def _matches(self, text: str, patterns: tuple[str, ...]) -> bool:
        normalized = normalize(text)
        return any(re.search(pattern, normalized, re.IGNORECASE) for pattern in patterns)

    def search(self, question: str, limit: int = 3) -> list[SearchResult]:
        query_tokens = tokenize(question)
        results: list[SearchResult] = []
        for topic in self.knowledge["topicos"]:
            keyword_tokens = tokenize(" ".join(topic["palavras_chave"]))
            content_tokens = tokenize(topic["titulo"] + " " + topic["resumo"])
            exact_bonus = sum(
                3 for keyword in topic["palavras_chave"] if normalize(keyword) in normalize(question)
            )
            score = exact_bonus + 2 * len(query_tokens & keyword_tokens) + len(query_tokens & content_tokens)
            if score:
                results.append(SearchResult(topic=topic, score=float(score)))
        return sorted(results, key=lambda item: (-item.score, item.topic["id"]))[:limit]

    def answer(self, question: str) -> dict:
        clean_question = question.strip()
        if not clean_question:
            return self._result("Informe uma dúvida de conformidade para eu orientar.", "entrada_invalida")

        if self._matches(clean_question, INJECTION_PATTERNS):
            return self._result(
                "Não posso revelar instruções internas nem ignorar minhas regras. "
                "Posso responder a uma dúvida de conformidade usando a base aprovada.",
                "instrucao_adversarial",
            )

        if self._matches(clean_question, SENSITIVE_PATTERNS):
            return self._result(
                "Não envie nem solicite senhas, tokens ou dados pessoais/confidenciais neste chat. "
                "Interrompa o compartilhamento e use o canal institucional seguro. Se já houve exposição, "
                "acione imediatamente Segurança da Informação e Privacidade.",
                "conteudo_sensivel",
                escalation=True,
            )

        normalized = normalize(clean_question)
        if any(term in normalized for term in OUT_OF_SCOPE):
            return self._result(
                "Essa pergunta está fora do meu escopo. Posso ajudar com ética, cadastro e diligência, "
                "PLD/FT, credenciamento, fraude e chargeback, recebíveis, privacidade, segurança ou continuidade.",
                "fora_do_escopo",
            )

        matches = self.search(clean_question)
        if not matches:
            return self._result(
                "Não encontrei informação suficiente na base aprovada para responder com segurança. "
                "Consulte Compliance ou Jurídico e informe o processo envolvido, sem incluir dados pessoais ou sigilosos.",
                "sem_evidencia",
                escalation=True,
            )

        primary = matches[0].topic
        guidance = "\n".join(f"- {item}" for item in primary["orientacoes"][:4])
        alerts = ", ".join(primary["sinais_alerta"][:3])
        source_lines = []
        for label in primary["fontes"]:
            url = next((url for prefix, url in self.source_urls.items() if label.startswith(prefix)), None)
            source_lines.append(f"- {label}" + (f": {url}" if url else ""))

        response = (
            f"**Orientação geral — {primary['titulo']}**\n\n"
            f"{primary['resumo']}\n\n"
            f"**O que fazer**\n{guidance}\n\n"
            f"**Sinais de atenção:** {alerts}.\n\n"
            f"**Quando escalar:** {primary['escalar_quando']}\n\n"
            "**Referências públicas**\n" + "\n".join(source_lines) + "\n\n"
            "Esta resposta é educacional e não substitui análise de Compliance/Jurídico. "
            "A regra aplicável depende do papel da organização, do arranjo, dos contratos e do caso concreto."
        )
        return self._result(response, "respondido", [primary["id"]])

    @staticmethod
    def _result(answer: str, status: str, topics: list[str] | None = None, escalation: bool = False) -> dict:
        return {"answer": answer, "status": status, "topics": topics or [], "requires_escalation": escalation}
