"""Interface Streamlit do ConformidadePay."""

from pathlib import Path
import sys

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assistente import ComplianceAssistant  # noqa: E402


st.set_page_config(page_title="ConformidadePay", page_icon="🛡️", layout="centered")

st.title("🛡️ ConformidadePay")
st.caption("Orientações gerais de compliance para o ecossistema de pagamentos")

with st.sidebar:
    st.subheader("Escopo")
    st.write("Ética, diligência, PLD/FT, credenciamento, fraude, recebíveis, privacidade, segurança e continuidade.")
    st.warning("Não insira dados pessoais, segredos, credenciais ou informações de casos reais.")
    st.info("O protótipo é educacional e não substitui Compliance, Jurídico ou a análise do caso concreto.")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Olá! Descreva uma dúvida geral de conformidade, sem dados pessoais ou confidenciais."
    }]

assistant = ComplianceAssistant()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex.: quais cuidados tomar ao credenciar um estabelecimento?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    result = assistant.answer(prompt)
    with st.chat_message("assistant"):
        st.markdown(result["answer"])
        if result["requires_escalation"]:
            st.error("Este cenário requer validação humana pelo canal institucional apropriado.")
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
