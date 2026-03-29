import streamlit as st
from datetime import datetime

# 1. Configuração de Estilo Visual (CSS Mobile-First & Anti-Dark Mode)
st.set_page_config(page_title="Reclama no Ponto", page_icon="🚌", layout="centered")

# Inicializa a lista de reclamações no estado da sessão se não existir
if 'minhas_reclamacoes' not in st.session_state:
    st.session_state.minhas_reclamacoes = [
        {"protocolo": "#RP-2026-001", "linha": "135", "status": "Concluído", "data": "25/03/2026", "cat": "Operacional"},
        {"protocolo": "#RP-2026-015", "linha": "231", "status": "Em Análise", "data": "27/03/2026", "cat": "Demanda"}
    ]

st.markdown("""
    <style>
    /* FUNDO GERAL CLARO */
    .stApp { background-color: #f8f9fa !important; }

    /* TÍTULOS EM AZUL */
    h1, h2, h3 { color: #007bff !important; text-align: center; }

    /* TEXTOS SEMPRE PRETOS E VISÍVEIS */
    label, p, [data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* INPUTS E SELECTBOXES - AZUL CLARINHO (SEM FUNDO PRETO) */
    div[data-baseweb="select"] > div, input, textarea {
        background-color: #e8f0fe !important;
        color: #000000 !important;
        border: 1px solid #ced4da !important;
        border-radius: 12px !important;
    }

    /* FORÇAR TEXTO PRETO AO DIGITAR */
    input, textarea { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }

    /* BOTÃO ENVIAR E BUSCAR - AZUL DO ÍCONE (FORMATO PILL) */
    .stButton>button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        border: none !important;
        height: 3.5em !important;
        width: 100% !important;
        box-shadow: 0px 4px 10px rgba(0,123,255,0.2) !important;
    }

    /* CAIXA DE UPLOAD DE FOTOS - CLARA */
    div[data-testid="stFileUploadDropzone"] {
        background-color: #e8f0fe !important;
        border: 2px dashed #007bff !important;
        color: black !important;
    }
    div[data-testid="stFileUploadDropzone"] button {
        background-color: #007bff !important;
        color: white !important;
    }

    /* CAIXA BRANCA DOS FORMS E CARDS */
    div[data-testid="stForm"], .card-reclamacao {
        background-color: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05) !important;
        border: 1px solid #eee !important;
        margin-bottom: 15px;
    }

    /* ESTILO DOS STATUS */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }

    /* Esconder menus do Streamlit */
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DADOS ---
categorias = {
    "Operacional": {"foco": "Cumprimento de metas", "exemplo": "Atrasos e furos de escala."},
    "Estrutural": {"foco": "Estado do veículo", "exemplo": "Elevador quebrado ou falta de ar-condicionado."},
    "Comportamental": {"foco": "Conduta humana", "exemplo": "Direção perigosa ou grosseria."},
    "Demanda": {"foco": "Fluxo de passageiros", "exemplo": "Superlotação crônica."},
    "Sistêmica": {"foco": "Tecnologia e Créditos", "exemplo": "Erros no cartão de passagens."}
}

# --- INTERFACE ---
st.markdown("<h1>🚌 Reclama no Ponto</h1>", unsafe_allow_html=True)

# NAVEGAÇÃO NO TOPO
aba = st.selectbox("Menu do Aplicativo:", ["📝 Fazer Reclamação", "💬 Fórum da Comunidade", "🔍 Minhas Reclamações"])
st.markdown("---")

# --- PÁGINA 1: RECLAMAÇÃO ---
if aba == "📝 Fazer Reclamação":
    st.markdown("<h3>Nova Reclamação</h3>", unsafe_allow_html=True)
    escolha_cat = st.selectbox("Selecione a categoria do problema:", list(categorias.keys()))
    info = categorias[escolha_cat]
    st.info(f"💡 **Foco:** {info['foco']}\n\n*Ex: {info['exemplo']}*")

    with st.form("form_celular"):
        linha = st.selectbox("Número da Linha:", ["100", "135", "138", "165", "210", "231", "410"])
        placa = st.text_input("Placa do Ônibus (Opcional):", placeholder="Ex: ABC-1234")
        descricao = st.text_area("Descrição do ocorrido:", placeholder="Conte detalhes para nos ajudar...")
        foto = st.file_uploader("Anexar foto (Opcional):")
        
        btn_enviar = st.form_submit_button("ENVIAR RECLAMAÇÃO")
        
        if btn_enviar:
            if not descricao:
                st.warning("⚠️ Descreva o problema.")
            else:
                # Salva a reclamação na lista global da sessão
                novo_p = f"#RP-2026-{len(st.session_state.minhas_reclamacoes) + 1:03d}"
                st.session_state.minhas_reclamacoes.append({
                    "protocolo": novo_p,
                    "linha": linha,
                    "status": "Recebido",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "cat": escolha_cat
                })
                st.success(f"✅ Protocolo {novo_p} registrado!")
                st.balloons()

# --- PÁGINA 2: FÓRUM ---
elif aba == "💬 Fórum da Comunidade":
    st.markdown("<h3>Ocorrências em Tempo Real</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 12px; border-left: 5px solid #007bff; color: black; margin-bottom: 10px;">
            <strong>Linha 135 - Volta ao Morro</strong><br>
            <small>📍 UDESC - Há 5 min</small><br>
            "Atraso no horário das 16:15."
        </div>
    """, unsafe_allow_html=True)

# --- PÁGINA 3: SITUAÇÃO (MINHAS RECLAMAÇÕES) ---
else:
    st.markdown("<h3>Suas Reclamações</h3>", unsafe_allow_html=True)
    st.write("Acompanhe aqui o andamento de todos os seus chamados:")

    if not st.session_state.minhas_reclamacoes:
        st.write("Você ainda não fez nenhuma reclamação.")
    else:
        # Mostra as reclamações da mais recente para a mais antiga
        for rec in reversed(st.session_state.minhas_reclamacoes):
            cor_status = "#ffa500" if rec['status'] == "Em Análise" else "#28a745" if rec['status'] == "Concluído" else "#007bff"
            
            st.markdown(f"""
                <div class="card-reclamacao">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #007bff; font-weight: bold;">{rec['protocolo']}</span>
                        <span class="status-badge" style="background-color: {cor_status};">{rec['status']}</span>
                    </div>
                    <div style="margin-top: 10px; color: #333;">
                        <b>Linha:</b> {rec['linha']} | <b>Tipo:</b> {rec['cat']}<br>
                        <small>📅 Data: {rec['data']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

