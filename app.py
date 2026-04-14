import streamlit as st
import random
from datetime import datetime

# ==========================================
# Configuração da Página e CSS Customizado
# ==========================================
st.set_page_config(page_title="Reclame no Ponto", page_icon="🚌", layout="centered")

# Injetando um pouco do estilo visual original para manter a identidade
st.markdown("""
    <style>
    .stApp { background-color: #F4F2EE; }
    .status-badge { padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
    .s-concluido { background-color: #E6F4EC; color: #1F7A4A; }
    .s-analise { background-color: #FEF3DC; color: #875200; }
    .s-enviado { background-color: #E8F0FB; color: #1A5FAB; }
    .lgpd-note { font-size: 12px; color: #5A5850; background: #F0EDE8; padding: 10px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Gerenciamento de Estado (Dinâmica do App)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'reclamacoes' not in st.session_state:
    st.session_state['reclamacoes'] = []

# ==========================================
# Tela de Login
# ==========================================
if not st.session_state['logged_in']:
    st.markdown("<h1 style='color: #1A5FAB; text-align: center;'>Reclame<span style='color: #1A1A1A;'>noPonto</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sua voz na melhoria do transporte público de Florianópolis.</p>", unsafe_allow_html=True)
    
    st.write("---")
    cpf_email = st.text_input("CPF ou e-mail", value="123.456.789-00")
    senha = st.text_input("Senha", type="password", value="demo1234")
    
    if st.button("Entrar", type="primary", use_container_width=True):
        st.session_state['logged_in'] = True
        st.toast("✓ Login realizado com sucesso!")
        st.rerun()
        
    st.markdown("""
        <div class="lgpd-note">
            <strong>🔒 Privacidade (LGPD):</strong> Seus dados pessoais são usados apenas para autenticação. 
            Publicações são anonimizadas. Imagens passam por IA para remoção de rostos.
        </div>
    """, unsafe_allow_html=True)
    st.stop() # Pausa a execução aqui até o login ser feito

# ==========================================
# App Principal
# ==========================================
st.markdown("<h3 style='color: #1A5FAB;'>Reclame<span style='color: #1A1A1A;'>noPonto</span></h3>", unsafe_allow_html=True)

# Criando a barra de navegação (Tabs)
tab_reclamar, tab_forum, tab_minhas = st.tabs(["📝 Reclamar", "💬 Fórum", "👤 Minhas"])

# ------------------------------------------
# ABA 1: RECLAMAR
# ------------------------------------------
with tab_reclamar:
    st.subheader("Nova reclamação")
    
    with st.form("form_reclamacao"):
        categoria = st.selectbox("Categoria do problema", [
            "⏱ Atraso / Furo (Operacional)", 
            "🚌 Lotação (Demanda)", 
            "🔧 Veículo com defeito (Estrutural)", 
            "😤 Conduta / Direção (Comportamental)", 
            "💳 Cartão / Sistema (Sistêmico)", 
            "♿ Acessibilidade (Estrutural)"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            linha = st.text_input("Número da linha", placeholder="ex: 330")
        with col2:
            onibus = st.text_input("Número do ônibus", placeholder="ex: 1042", help="Visível no app Floripa no Ponto")
            
        descricao = st.text_area("Descrição do problema", placeholder="Descreva o que aconteceu...")
        anexo = st.file_uploader("📎 Anexar foto ou vídeo (opcional) - Rostos serão ocultados por IA")
        
        st.caption("Sua postagem será publicada anonimamente.")
        submitted = st.form_submit_button("Enviar reclamação", type="primary", use_container_width=True)
        
        if submitted:
            id_req = f"#2025-0{random.randint(510, 599)}"
            st.session_state['reclamacoes'].append({
                "id": id_req,
                "linha": linha,
                "categoria": categoria,
                "status": "Enviado",
                "data": datetime.now().strftime("%d/%m/%Y")
            })
            st.success(f"Reclamação {id_req} registrada! Prazo de resposta: 10 dias úteis.")
            st.balloons()

# ------------------------------------------
# ABA 2: FÓRUM
# ------------------------------------------
with tab_forum:
    st.subheader("Fórum público e respostas oficiais")
    
    filtro = st.radio("Ordenar por:", ["★ Relevância", "🕐 Recente", "🚌 Linha", "✅ Respondidas"], horizontal=True)
    st.caption("Relevância = curtidas + frequência + vulnerabilidade social (IBGE/Censo 2022)")
    
    # Post 1
    with st.container(border=True):
        st.markdown("**Linha 330 · TICEN → Centro** | <span class='status-badge s-analise'>Atraso</span>", unsafe_allow_html=True)
        st.caption("👤 Anônimo · há 12 min · Estreito")
        st.write("Ônibus passou 25 minutos atrasado. Terceira vez essa semana. Cheguei atrasada no trabalho.")
        
        st.info("**✅ Resposta oficial — SMTT Florianópolis:** Reforço de frota programado para a Linha 330 a partir de 01/04.")
        
        col1, col2, col3 = st.columns(3)
        col1.button("▲ 47 Curtidas", key="like1")
        col3.button("↗ Compartilhar", key="share1")
        
        with st.expander("💬 Ver 8 comentários"):
            st.write("👤 **Anônimo:** Acontece toda semana nesse horário.")
            st.write("👤 **Anônimo:** Linha 330 é uma das mais movimentadas, deveria ter ônibus reserva.")
            st.text_input("Adicionar comentário anônimo...", key="com1")

    # Post 2
    with st.container(border=True):
        st.markdown("**Linha 182 · Trindade** | <span class='status-badge s-analise'>Lotação</span>", unsafe_allow_html=True)
        st.caption("👤 Anônimo · há 43 min · Trindade")
        st.write("Superlotação crônica no horário de pico. Idosos e pessoas com deficiência não conseguem embarcar.")
        
        st.warning("**⏳ Em análise — Consórcio Fênix:** Demanda encaminhada ao setor de planejamento. Prazo: 08/04/2025.")
        
        col1, col2, col3 = st.columns(3)
        col1.button("▲ 31 Curtidas", key="like2")
        col3.button("↗ Compartilhar", key="share2")
        
        with st.expander("💬 Ver 4 comentários"):
            st.write("👤 **Anônimo:** Confirmo! Todo dia às 7h40 não para pra embarcar.")
            st.text_input("Adicionar comentário anônimo...", key="com2")

    st.markdown("<div style='text-align: center;'><small>🤖 IA ativa: conteúdo sensível e rostos filtrados (LGPD)</small></div>", unsafe_allow_html=True)

# ------------------------------------------
# ABA 3: MINHAS RECLAMAÇÕES
# ------------------------------------------
with tab_minhas:
    st.subheader("Minhas reclamações")
    st.caption("Suas postagens são sempre anônimas no fórum.")
    
    # Exibir as novas reclamações criadas na sessão atual
    for req in reversed(st.session_state['reclamacoes']):
        with st.expander(f"{req['id']} - Linha {req['linha']} (Novo)"):
            st.write(f"**Status:** {req['status']}")
            st.write(f"**Categoria:** {req['categoria']}")
            st.write(f"**Data:** {req['data']}")
            st.progress(25) # Barra de progresso visual simulando a timeline
    
    # Mock de dados passados do HTML
    with st.expander("#2025-0471 - Linha 330 · Atraso / Furo", expanded=True):
        st.markdown("<span class='status-badge s-concluido'>Concluído</span>", unsafe_allow_html=True)
        st.write("---")
        st.write("**15/03/2025:** Reclamação enviada")
        st.write("**17/03/2025:** Em análise — SMTT")
        st.success("**29/03/2025 (Concluído):** SMTT Florianópolis: Reforço de frota programado para a Linha 330 a partir de 01/04.")

    with st.expander("#2025-0468 - Linha 182 · Lotação"):
        st.markdown("<span class='status-badge s-analise'>Em análise</span>", unsafe_allow_html=True)
        st.write("---")
        st.write("**26/03/2025:** Reclamação enviada")
        st.warning("**30/03/2025:** Em análise — Consórcio Fênix. Prazo: 08/04/2025")

    with st.expander("#2025-0440 - Linha 330 · Cartão / Sistema"):
        st.markdown("<span class='status-badge s-analise' style='background-color:#FDEAEA; color:#B03030;'>Não atendido</span>", unsafe_allow_html=True)
        st.write("---")
        st.write("**14/03/2025:** Reclamação enviada")
        st.error("**28/03/2025:** Prazo encerrado sem resposta. Você pode reabrir ou escalar esta demanda.")
