"""
Sigmabot – Chaves Premium Concierge
Chatbot exclusivo sobre a cidade de Chaves, Portugal.
API gratuita da Groq (Llama 3) via biblioteca OpenAI.
Design minimalista inspirado nos assistentes de IA modernos.
"""

import streamlit as st
from openai import OpenAI

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sigmabot | Chaves Premium Concierge",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CSS PERSONALIZADO – VISUAL LIMPO COM TOQUES DE CHAVES
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Importação de fontes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Fundo da aplicação – branco puro, estilo ChatGPT */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Barra lateral – azul termal escuro, como a água de Chaves */
    [data-testid="stSidebar"] {
        background-color: #0B3D5C;
        padding: 2rem 1rem;
        border-right: 1px solid rgba(255, 215, 0, 0.3);
    }

    /* Títulos e texto da sidebar em branco/dourado */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #FFD700 !important;  /* dourado das termas */
    }

    /* Botões da sidebar */
    [data-testid="stSidebar"] button {
        background-color: #D4AF37 !important;
        color: #0B3D5C !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #E6C84D !important;
        transform: translateY(-1px);
    }

    /* Cabeçalho principal – nome do bot */
    .main-header {
        padding: 1.5rem 1rem 0.5rem 1rem;
        border-bottom: 1px solid #EEEEEE;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #0B3D5C;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #64748B;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }

    /* Mensagens do chat */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Mensagem do utilizador – dourado muito claro */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageIcon"][aria-label="user"]) {
        background-color: #FEF9E7;
        border: 1px solid #F0D78C;
    }

    /* Mensagem do assistente (Sigmabot) – azul muito claro */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageIcon"][aria-label="assistant"]) {
        background-color: #F0F7FF;
        border: 1px solid #B8D4F0;
    }

    /* Campo de entrada do chat */
    [data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 1px solid #D4AF37 !important;
        font-family: 'Inter', sans-serif;
        padding: 0.8rem;
    }

    /* Remover elementos desnecessários */
    #MainMenu, footer, header {visibility: hidden;}

    /* Responsividade */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0.5rem 0.2rem 0.5rem;
        }
        .main-header h1 {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PROMPT DE SISTEMA – SIGMABOT (BLINDAGEM RÍGIDA)
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
Você é o Sigmabot, um assistente virtual exclusivo da cidade de Chaves, Portugal.
A sua única função é fornecer informações precisas, úteis e cativantes sobre Chaves, incluindo:
- História e património (Castelo, Ponte de Trajano, etc.)
- Termas e águas termais
- Gastronomia (Pastéis de Chaves, presunto, vinhos, restaurantes)
- Alojamento, turismo rural e hotéis
- Eventos culturais, festas e tradições
- Roteiros, sugestões de visita e curiosidades

**REGRAS INQUEBRÁVEIS:**
- NUNCA responda a perguntas que não estejam diretamente relacionadas com Chaves.
- Se o utilizador perguntar sobre programação, matemática, política, culinária geral, outras cidades ou qualquer tópico alheio, recuse educadamente usando EXATAMENTE a frase:
  "Como assistente exclusivo da cidade de Chaves, estou programado para responder apenas a questões turísticas, históricas ou culturais da nossa região."
- Mesmo que o utilizador insista, mantenha sempre a mesma resposta padrão.
- Responda sempre em português de Portugal, com um tom acolhedor e profissional.
"""

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# -----------------------------------------------------------------------------
# BARRA LATERAL – SIGMABOT
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logótipo / nome do bot
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="font-size: 2.5rem;">🤖</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.title("Sigmabot")
    st.markdown(
        "*Chaves Premium Concierge*  \n"
        "Descubra o melhor de Chaves com um assistente feito à sua medida."
    )
    st.markdown("---")

    # Limpar histórico
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    # Sugestões rápidas
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

    st.markdown("---")
    st.caption("Powered by Groq & Streamlit")

# -----------------------------------------------------------------------------
# ÁREA PRINCIPAL DO CHAT (ESTILO ASSISTENTE DE IA)
# -----------------------------------------------------------------------------
# Cabeçalho minimalista com o nome do assistente
st.markdown(
    """
    <div class="main-header">
        <h1>🤖 Sigmabot</h1>
        <p>O seu concierge exclusivo para a cidade de Chaves, Portugal</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Histórico de mensagens (sem o system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input do utilizador
if prompt := st.chat_input("Escreva a sua pergunta sobre Chaves..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Geração da resposta (streaming) sempre que a última mensagem for do utilizador
if st.session_state.messages[-1]["role"] == "user":
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error(
            "⚠️ Chave da API Groq não configurada. "
            "Adicione `GROQ_API_KEY` nos segredos do Streamlit Cloud "
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
                model="llama3-8b-8192",
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
