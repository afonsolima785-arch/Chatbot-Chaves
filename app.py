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
# CSS BASE – VISUAL CORPORATIVO (Sem nenhuma f-string ou lógica complexa)
# =============================================================================
st.markdown(
    """
<style>
    /* Fundo geral da página */
    .stApp {
        background-color: #F0F4F8;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0A2540;
        color: white;
        padding: 2rem 1rem;
    }
    section[data-testid="stSidebar"] .stButton>button {
        background-color: #2B4C7E;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #1E3A5F;
        transform: scale(1.02);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    /* Mensagens do chat */
    div[data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        line-height: 1.5;
    }

    /* Mensagem do utilizador */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="user"]) {
        background-color: #1E3A5F;
        color: white;
    }

    /* Mensagem do assistente */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="assistant"]) {
        background-color: #FFFFFF;
        border: 1px solid #D1D9E0;
    }

    /* Campo de input do chat */
    div[data-testid="stChatInput"] textarea {
        border-radius: 20px !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Ocultar menus e rodapés antigos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Ajustes para ecrãs pequenos */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            padding: 1rem 0.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# BARRA LATERAL (Construção da Interface)
# =============================================================================
with st.sidebar:
    st.title("🏰 Chaves Sigmabot")
    st.markdown(
        "O seu assistente pessoal para descobrir a encantadora cidade de Chaves, Portugal. "
        "Pergunte-me sobre o que visitar, onde comer ou as melhores termas!"
    )
    st.markdown("---")

    # PROMPT DE SISTEMA – BLINDAGEM RÍGIDA
    SYSTEM_PROMPT = """
    Você é o 'Chaves Sigmabot', um assistente virtual exclusivo da cidade de Chaves, Portugal.
    A sua única missão é fornecer informações precisas, úteis e encantadoras sobre Chaves.
    Responda sempre em português de Portugal.
    """

    # Inicialização básica do histórico se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Botão para limpar histórico
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    st.subheader("💡 Sugestões Rápidas")
    suggestions = [
        "Roteiro de 1 dia em Chaves",
        "Onde comer os melhores Pastéis de Chaves?",
        "Quais as termas disponíveis em Chaves?",
        "História do Castelo de Chaves",
        "Melhores hotéis no centro histórico",
        "O que visitar com crianças em Chaves?",
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

    # -------------------------------------------------------------------------
    # SECÇÃO DA PASSWORD (Simples e direta)
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🔒 Área do Proprietário")
    
    # Caixa de texto normal para a password
    senha_digitada = st.text_input("Chave Admin", type="password")
    eh_admin = (senha_digitada == "Liljuice13..")
    
    if eh_admin:
        st.success("Modo Admin Ativo! 🛠️")


# =============================================================================
# INJEÇÃO DO BLOQUEIO DO BOTÃO MANAGE APP (Apenas se NÃO for o dono correto)
# =============================================================================
if not eh_admin:
    st.markdown(
        """
    <style>
        /* Desativa por completo o botão preto Manage App do ecrã público */
        [data-testid="stStatusWidget"], .viewerBadge_link__1S16K, [class^="viewerBadge"], iframe[title="Manage app"], iframe[src*="manage"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            width: 0px !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

# =============================================================================
# ÁREA PRINCIPAL DO CHAT
# =============================================================================
st.header("Conversa Sigmabot")

# Mostrar histórico de mensagens (exceto a mensagem de sistema)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Entrada de texto do utilizador
if prompt := st.chat_input("Faça uma pergunta sobre Chaves..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Geração de resposta automática sempre que a última mensagem for do utilizador
if st.session_state.messages[-1]["role"] == "user":
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("⚠️ Chave da API Groq não configurada nos Secrets do Streamlit Cloud.")
        st.stop()

    client = OpenAI(
        base_url="https://groq.com",
        api_key=groq_api_key,
    )

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
            response = f"Lamento, ocorreu um erro inesperado: {str(e)}"
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


# =============================================================================
# PAINEL DE GESTÃO EXCLUSIVO (Apenas aparece quando digitas a password certa)
# =============================================================================
if eh_admin:
    st.markdown("---")
    st.subheader("🛠️ Painel de Gestão e Monitorização (Exclusivo)")
    st.write("Bem-vindo, Afonso. Este painel está oculto para todos os utilizadores comuns.")
    
    if st.checkbox("👁️ Ver Logs/Histórico Completo da Conversa Atual"):
        st.json(st.session_state.messages)
