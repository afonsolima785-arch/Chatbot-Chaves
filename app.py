"""
Chaves Premium Concierge – Chatbot exclusivo sobre a cidade de Chaves, Portugal.
Design inspirado nas cores e símbolos da cidade: azul termal, dourado do granito e verde minhoto.
Usa a API gratuita da Groq (Llama 3) através da biblioteca OpenAI.
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
# CSS PERSONALIZADO – INSPIRAÇÃO EM CHAVES
# =============================================================================
st.markdown(
    """
<style>
    /* ---------- GOOGLE FONT (opcional, para um toque mais premium) ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@400;600&display=swap');

    /* Corpo geral */
    .stApp {
        background: linear-gradient(135deg, #EAF4FC 0%, #F8F9FA 100%);
    }

    /* Barra lateral - evoca os azulejos e a água termal */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A3D62 0%, #0C4A7A 100%);
        color: #FFFFFF;
        padding: 2rem 1rem;
        border-right: 2px solid #D4AF37;
    }

    /* Título da sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #FFD700;
    }

    /* Texto na sidebar */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #F0F0F0;
        font-family: 'Inter', sans-serif;
    }

    /* Botões da sidebar */
    section[data-testid="stSidebar"] .stButton>button {
        background-color: #D4AF37;
        color: #0A3D62;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #E6C84D;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Área principal – cabeçalho com imagem de fundo */
    .main .block-container {
        padding-top: 0rem;
    }

    /* Cartão de boas-vindas (apenas decorativo, colocado no corpo do chat) */
    .welcome-banner {
        background: url('https://images.unsplash.com/photo-1598367203959-88c1f5d8f6c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') center/cover no-repeat;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    .welcome-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(10, 61, 98, 0.7);
        border-radius: 20px;
    }
    .welcome-banner h1,
    .welcome-banner p {
        position: relative;
        color: white;
        font-family: 'Playfair Display', serif;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }

    /* Mensagens do chat */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }

    /* Mensagem do utilizador - dourado suave */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="user"]) {
        background: linear-gradient(145deg, #F5E7C6 0%, #EED9A0 100%);
        color: #2C3E50;
        border-left: 4px solid #D4AF37;
    }

    /* Mensagem do assistente - azul termal */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageIcon"][aria-label="assistant"]) {
        background: #FFFFFF;
        border: 1px solid #C5D3E8;
        border-left: 4px solid #0A3D62;
    }

    /* Campo de input */
    div[data-testid="stChatInput"] textarea {
        border-radius: 24px !important;
        border: 1px solid #D4AF37 !important;
        padding: 0.8rem 1rem;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stChatInput"] button {
        background-color: #0A3D62 !important;
        color: white !important;
        border-radius: 24px;
    }

    /* Ocultar elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Ecrãs pequenos */
    @media (max-width: 768px) {
        .welcome-banner {
            padding: 1rem;
        }
        section[data-testid="stSidebar"] {
            padding: 1rem 0.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# PROMPT DE SISTEMA – BLINDAGEM RÍGIDA (INALTERADA)
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
# INICIALIZAÇÃO DO ESTADO
# =============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# =============================================================================
# BARRA LATERAL – MAIS BONITA E TEMÁTICA
# =============================================================================
with st.sidebar:
    # Logo / ícone estilizado
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="font-size: 3rem;">🏰</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.title("Chaves Premium")
    st.markdown(
        "O seu **concierge exclusivo** para descobrir a cidade termal mais encantadora de Portugal."
    )
    st.markdown("---")

    # Botão Limpar Histórico
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    # Secção de Sugestões Rápidas
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

    # Rodapé discreto na sidebar
    st.markdown("---")
    st.markdown(
        "<small style='color: #CCC;'>Powered by Groq & Streamlit</small>",
        unsafe_allow_html=True,
    )

# =============================================================================
# CABEÇALHO E BOAS-VINDAS NO CORPO DO CHAT
# =============================================================================
# Exibe um banner estilizado apenas se o histórico estiver "vazio" (apenas system prompt)
if len(st.session_state.messages) == 1:
    st.markdown(
        """
        <div class="welcome-banner">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Bem-vindo a Chaves</h1>
            <p style="font-size: 1.2rem; max-width: 600px;">
                Descubra as termas, o castelo, a ponte de Trajano e os famosos pastéis.
                <br>Pergunte-me o que quiser sobre esta cidade histórica!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Área do chat
st.header("Conversa com o Concierge")

# Mostrar histórico (exceto mensagem de sistema)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Entrada do utilizador
if prompt := st.chat_input("Faça uma pergunta sobre Chaves..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Geração da resposta quando a última mensagem for do utilizador
if st.session_state.messages[-1]["role"] == "user":
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error(
            "⚠️ Chave da API Groq não configurada. "
            "Para usar a aplicação, adicione `GROQ_API_KEY` nos segredos do Streamlit Cloud "
            "ou no ficheiro `.streamlit/secrets.toml` local."
        )
        st.stop()

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
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
