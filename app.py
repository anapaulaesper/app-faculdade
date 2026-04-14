import streamlit as st
import random
import time

# Configuração da página para simular uma visualização mobile-friendly
st.set_page_config(page_title="Reclame no Ponto", page_icon="🚌", layout="centered")

# Estilo customizado (opcional, para esconder menus padrão do Streamlit)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho do App
st.title("🚌 Reclame no Ponto")
st.caption("Sua voz na melhoria do transporte público de Florianópolis.")

# Criando as abas de navegação
tab_reclamar, tab_forum, tab_minhas = st.tabs(["📝 Reclamar", "💬 Fórum", "👤 Minhas"])

# ==========================================
# ABA 1: RECLAMAR
# ==========================================
with tab_reclamar:
    st.subheader("Nova Reclamação")
    
    with st.form("form_reclamacao"):
        categoria = st.selectbox("Categoria do problema", 
            ["Atraso / Furo (Operacional)", "Lotação (Demanda)", "Veículo com defeito (Estrutural)", 
             "Conduta / Direção (Comportamental)", "Cartão / Sistema (Sistêmico)", "Acessibilidade (Estrutural)"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            linha = st.text_input("Número da linha", placeholder="ex: 330")
        with col2:
            onibus = st.text_input("Número do ônibus", placeholder="ex: 1042", help="Visível no app Floripa no Ponto")
            
        descricao = st.text_area("Descrição do problema", placeholder="Descreva o que aconteceu...")
        
        anexo = st.file_uploader("Anexar foto ou vídeo (opcional)", help="Rostos serão ocultados por IA (LGPD)")
        
        st.caption("Sua postagem será publicada anonimamente.")
        enviado = st.form_submit_button("Enviar reclamação", type="primary")
        
        if enviado:
            if linha and descricao:
                num_protocolo = f"#2025-0{random.randint(500, 999)}"
                st.success(f"Reclamação registrada com sucesso! Protocolo: {num_protocolo}")
                st.info("Prazo de resposta: 10 dias úteis.")
            else:
                st.error("Por favor, preencha a linha e a descrição.")

# ==========================================
# ABA 2: FÓRUM
# ==========================================
with tab_forum:
    st.subheader("Fórum Público")
    st.caption("Relevância = curtidas + frequência + vulnerabilidade social")
    
    # Mock de Post 1
    with st.container(border=True):
        st.markdown("**Linha 330 · TICEN → Centro** ⏱️ *Atraso*")
        st.caption("Anônimo · há 12 min · Estreito")
        st.write("Ônibus passou 25 minutos atrasado. Terceira vez essa semana. Cheguei atrasada no trabalho.")
        
        st.button("▲ 47 Curtidas", key="like1")
        
        st.success("**✅ Resposta oficial — SMTT Florianópolis:** Reforço de frota programado para a Linha 330 a partir de 01/04.")

    # Mock de Post 2
    with st.container(border=True):
        st.markdown("**Linha 182 · Trindade** 🚌 *Lotação*")
        st.caption("Anônimo · há 43 min · Trindade")
        st.write("Superlotação crônica no horário de pico. Idosos e pessoas com deficiência não conseguem embarcar.")
        
        st.button("▲ 31 Curtidas", key="like2")
        
        st.warning("**⏳ Em análise — Consórcio Fênix:** Demanda encaminhada ao setor de planejamento. Prazo: 08/04/2025.")

    st.caption("🤖 IA ativa: conteúdo sensível e rostos filtrados (LGPD)")

# ==========================================
# ABA 3: MINHAS RECLAMAÇÕES
# ==========================================
with tab_minhas:
    st.subheader("Meu Histórico")
    st.caption("Acompanhe o status das suas solicitações.")
    
    with st.expander("✅ #2025-0471 - Linha 330 (Concluído)"):
        st.write("**Motivo:** Atraso / Furo")
        st.write("**Data:** 15/03/2025")
        st.write("---")
        st.write("📍 **15/03:** Reclamação enviada")
        st.write("📍 **17/03:** Em análise — SMTT")
        st.write("📍 **29/03:** Respondido e concluído")
        st.success("**SMTT Florianópolis:** Reforço de frota programado para a Linha 330 a partir de 01/04.")

    with st.expander("⏳ #2025-0468 - Linha 182 (Em análise)"):
        st.write("**Motivo:** Lotação")
        st.write("**Data:** 26/03/2025")
        st.write("---")
        st.write("📍 **26/03:** Reclamação enviada")
        st.write("📍 **30/03:** Em análise — Consórcio Fênix (Prazo: 08/04/2025)")
        st.write("⌛ Aguardando resposta final...")

    with st.expander("❌ #2025-0440 - Linha 330 (Não atendido)"):
        st.write("**Motivo:** Cartão / Sistema")
        st.write("**Data:** 14/03/2025")
        st.write("---")
        st.write("📍 **14/03:** Reclamação enviada")
        st.error("Prazo encerrado sem resposta em 28/03/2025. Você pode escalar esta demanda.")
