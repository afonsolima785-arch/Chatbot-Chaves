"""
Chaves Sigmabot – Chatbot exclusivo sobre a cidade de Chaves, Portugal.
Usa a API gratuita da Groq (modelo Llama 3) através da biblioteca OpenAI.
Interface profissional construída com Streamlit e CSS personalizado.
"""

import streamlit as st
from openai import OpenAI

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Chaves Sigmabot",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS PERSONALIZADO DO CHAT (Apenas o visual, sem mexer em botões da plataforma)
# =============================================================================
st.markdown(
    """
<style>
    .stApp { background-color: #F0F4F8; }
    section[data-testid="stSidebar"] { background-color: #0A2540; color: white; padding: 2rem 1rem; }
    section[data-testid="stSidebar"] .stButton>button {
        background-color: #2B4C7E; color: white; border-radius: 10px; border: none; padding: 0.5rem 1rem; font-weight: bold;
    }
    section[data-testid="stSidebar"] .stMarkdown { color: white; }
    div[data-testid="stChatMessage"] { border-radius: 15px; padding: 1rem; margin-bottom: 0.8rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="user"]) { background-color: #1E3A5F; color: white; }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="assistant"]) { background-color: #FFFFFF; border: 1px solid #D1D9E0; }
    div[data-testid="stChatInput"] textarea { border-radius: 20px !important; border: 1px solid #CBD5E1 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# PROMPT DE SISTEMA
# =============================================================================
SYSTEM_PROMPT = """
Você é o 'Chaves Sigmabot', um assistente virtual exclusivo da cidade de Chaves, Portugal.
A sua única missão é fornecer informações precisas sobre Chaves. Responda sempre em português de Portugal.
"""

# Inicialização do histórico
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# =============================================================================
# BARRA LATERAL
# =============================================================================
with st.sidebar:
    st.title("🏰 Chaves Sigmabot")
    st.markdown("O seu assistente pessoal para descobrir a cidade de Chaves.")
    st.markdown("---")

    # Botão para limpar histórico
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    st.subheader("💡 Sugestões Rápidas")
    suggestions = [
        "Roteiro de 1 dia em Chaves",
        "Onde comer os melhores Pastéis de Chaves?",
        "Quais as termas disponíveis em Chaves?",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

    # -------------------------------------------------------------------------
    # TRANCA DE ADMIN (Sem CSS inventado para não quebrar o servidor)
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🔒 Área do Proprietário")
    senha = st.text_input("Chave Admin", type="password")
    
    eh_admin = (senha == "Liljuice13..")
    if eh_admin:
        st.success("Modo Admin Ativo!")

# =============================================================================
# ÁREA PRINCIPAL DO CHAT
# =============================================================================
st.header("Conversa Sigmabot")

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Faça uma pergunta sobre Chaves..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages[-1]["role"] == "user":
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("⚠️ GROQ_API_KEY não configurada nos Secrets do Streamlit.")
        st.stop()

    client = OpenAI(base_url="https://groq.com", api_key=groq_api_key)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
            )
            response = st.write_stream(stream)
        except Exception as e:
            response = f"Erro: {str(e)}"
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# =============================================================================
# PAINEL DE GESTÃO EXCLUSIVO AFONSO
# =============================================================================
if eh_admin:
    st.markdown("---")
    st.subheader("🛠️ Painel de Gestão (Apenas o Afonso vê)")
    if st.checkbox("👁️ Ver Logs da Conversa Atual"):
        st.json(st.session_state.messages)
