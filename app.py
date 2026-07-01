"""
Chaves Premium Concierge – Chatbot exclusivo sobre a cidade de Chaves, Portugal.
Usa a API gratuita da Groq (modelo Llama 3) através da biblioteca OpenAI.
Interface profissional construída com Streamlit e CSS personalizado.
"""

import streamlit as st
from openai import OpenAI

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Chaves Premium Concierge",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS PERSONALIZADO – VISUAL CORPORATIVO
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

    /* Ocultar menu e rodapé do Streamlit (opcional) */
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
# PROMPT DE SISTEMA – BLINDAGEM RÍGIDA
# =============================================================================
SYSTEM_PROMPT = """
Você é o 'Chaves Premium Concierge', um assistente virtual exclusivo da cidade de Chaves, Portugal.
A sua única missão é fornecer informações precisas, úteis e encantadoras sobre Chaves, incluindo:
- História, património (Castelo, Ponte de Trajano, etc.)
- Termas e águas termais
- Gastronomia (Pastéis de Chaves, presunto, vinhos, restaurantes)
- Alojamento, turismo rural, hotéis
- Eventos culturais, festas e tradições
- Roteiros, sugestões de visita, curiosidades

**REGRAS INQUEBRÁVEIS:**
- NUNCA responda a perguntas que não estejam diretamente relacionadas com Chaves.
- Se o utilizador perguntar sobre programação, matemática, política, culinária geral, outras cidades ou qualquer tópico alheio, recuse educadamente usando EXATAMENTE a frase:
  "Como assistente exclusivo da cidade de Chaves, estou programado para responder apenas a questões turísticas, históricas ou culturais da nossa região."
- Mesmo que o utilizador insista, mantenha sempre a mesma resposta padrão.
- Responda sempre em português de Portugal, com um tom acolhedor e profissional.
"""

# =============================================================================
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# =============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# =============================================================================
# BARRA LATERAL
# =============================================================================
with st.sidebar:
    st.title("🏰 Chaves Premium Concierge")
    st.markdown(
        "O seu assistente pessoal para descobrir a encantadora cidade de Chaves, Portugal. "
        "Pergunte-me sobre o que visitar, onde comer ou as melhores termas!"
    )
    st.markdown("---")

    # Botão para limpar histórico (mantém o system prompt)
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
    # Cada botão adiciona a sugestão como mensagem do utilizador
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

# =============================================================================
# ÁREA PRINCIPAL DO CHAT
# =============================================================================
st.header("Conversa com o Concierge de Chaves")

# Mostrar histórico de mensagens (exceto a mensagem de sistema)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Entrada de texto do utilizador
if prompt := st.chat_input("Faça uma pergunta sobre Chaves..."):
    # Adiciona e mostra a mensagem do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Geração de resposta automática sempre que a última mensagem for do utilizador
if st.session_state.messages[-1]["role"] == "user":
    # Obter chave da API da Groq (segura via Streamlit Secrets)
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error(
            "⚠️ Chave da API Groq não configurada. "
            "Para usar a aplicação, adicione `GROQ_API_KEY` nos segredos do Streamlit Cloud "
            "ou no ficheiro `.streamlit/secrets.toml` local."
        )
        st.stop()

    # Criar cliente OpenAI apontado para a Groq
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_api_key,
    )

    with st.chat_message("assistant"):
        try:
            # Chamada à API com streaming
            stream = client.chat.completions.create(
                model="llama3-8b-8192",  # Modelo gratuito da Groq (também disponível: llama3-70b-8192)
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
            )
            # Efeito de "streaming" (palavras a aparecer)
            response = st.write_stream(stream)
        except Exception as e:
            response = f"Lamento, ocorreu um erro inesperado: {str(e)}"
            st.write(response)

    # Guardar a resposta do assistente no histórico
    st.session_state.messages.append({"role": "assistant", "content": response})
