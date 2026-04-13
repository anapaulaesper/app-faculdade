import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Reclama no Ponto", page_icon="🚌", layout="centered")

# ── ESTADO DA SESSÃO ─────────────────────────────────────
if 'minhas_reclamacoes' not in st.session_state:
    st.session_state.minhas_reclamacoes = [
        {
            "protocolo": "#RP-2026-001", "grupo": "🔄 Circulares e Transversais",
            "linha": "135", "status": "Concluído", "data": "25/03/2026",
            "cat": "⏱️ Operacional", "placa": "ABC-1234",
            "descricao": "Ônibus atrasou mais de 40 minutos no horário das 17h.",
            "resposta": "Identificamos falha operacional naquela escala. O motorista responsável foi notificado e o horário foi reforçado a partir de 01/04/2026."
        },
        {
            "protocolo": "#RP-2026-015", "grupo": "🔗 Troncais (Inter-terminais)",
            "linha": "231", "status": "Em Análise", "data": "27/03/2026",
            "cat": "👥 Demanda", "placa": "",
            "descricao": "Superlotação constante nos horários de pico. Passageiros ficam para trás.",
            "resposta": "Sua reclamação está sendo avaliada pelo setor de planejamento operacional. Previsão de retorno: 15/04/2026."
        },
    ]
if 'aba_ativa'       not in st.session_state: st.session_state.aba_ativa       = "reclamacao"
if 'rec_detalhe'     not in st.session_state: st.session_state.rec_detalhe     = None
if 'forum_apoios'    not in st.session_state: st.session_state.forum_apoios    = {}
if 'forum_coments'   not in st.session_state: st.session_state.forum_coments   = {}
if 'forum_expandido' not in st.session_state: st.session_state.forum_expandido = None

# ── CATEGORIAS ───────────────────────────────────────────
categorias = {
    "⏱️ Operacional":    {"foco": "Cumprimento de metas",   "exemplo": "Atrasos e furos de escala.",                     "cor": "#3b82f6"},
    "🔧 Estrutural":     {"foco": "Estado do veículo",       "exemplo": "Elevador quebrado ou falta de ar-condicionado.", "cor": "#f59e0b"},
    "🚨 Comportamental": {"foco": "Conduta humana",           "exemplo": "Direção perigosa ou grosseria.",                 "cor": "#ef4444"},
    "👥 Demanda":        {"foco": "Fluxo de passageiros",    "exemplo": "Superlotação crônica.",                          "cor": "#8b5cf6"},
    "💳 Sistêmica":      {"foco": "Tecnologia e Créditos",   "exemplo": "Erros no cartão de passagens.",                  "cor": "#10b981"},
}

# ── LINHAS POR GRUPO ─────────────────────────────────────
grupos_linhas = {
    "🔗 Troncais (Inter-terminais)": {
        "desc": "Conectam terminais entre si — espinha dorsal do sistema.",
        "linhas": ["210","221","230","231","233","311","320","330","331","332","333","410","430","840","841","843","845","847"],
    },
    "🏘️ Alimentadoras Norte (TICAN/TISAN)": {
        "desc": "Ligam bairros do Norte ao terminal TICAN.",
        "linhas": ["260","264","267","271","272","281"],
    },
    "🌊 Alimentadoras Leste (TILAG)": {
        "desc": "Ligam bairros do Leste ao terminal TILAG.",
        "linhas": ["360","362","363","364"],
    },
    "🏖️ Alimentadoras Sul (TIRIO)": {
        "desc": "Ligam bairros do Sul ao terminal TIRIO.",
        "linhas": ["462","562","563","564","565"],
    },
    "🌿 Bacia do Itacorubi (TITRI)": {
        "desc": "Ligam bairros do Itacorubi ao terminal TITRI.",
        "linhas": ["164","165","176"],
    },
    "🌉 Alimentadoras Continente": {
        "desc": "Atendem a região continental de Florianópolis.",
        "linhas": ["631","661","663","670"],
    },
    "🔄 Circulares e Transversais": {
        "desc": "Volta ao Morro (UFSC/UDESC) e conexões entre praias.",
        "linhas": ["134","135","136","137","138","294"],
    },
    "🌟 Executivos (Amarelinhos)": {
        "desc": "Micro-ônibus com ar-condicionado e tarifa diferenciada.",
        "linhas": ["1112","1120","1121","1123","1125","4120","4123","4124","2120"],
    },
    "🌙 Madrugadão (00h–05h)": {
        "desc": "Linhas que operam na madrugada.",
        "linhas": ["100","102","200","201","300","500","501","600","604"],
    },
}

# ── POSTS DO FÓRUM ────────────────────────────────────────
FORUM_POSTS = [
    {"id":"f1","linha":"134","rota":"TITRI – TICEN via Beira-Mar",          "local":"Terminal TITRI",     "tempo":"8 min",  "cat":"⏱️ Operacional",   "texto":"Furo de viagem no horário das 7h30. Fiquei esperando 50 minutos."},
    {"id":"f2","linha":"221","rota":"TICAN – TICEN via Mauro Ramos",         "local":"TICAN",              "tempo":"15 min", "cat":"👥 Demanda",        "texto":"Superlotação absurda todo dia às 18h. Passageiros prensados."},
    {"id":"f3","linha":"233","rota":"TICAN – TITRI via UFSC",                "local":"UFSC",               "tempo":"22 min", "cat":"🔧 Estrutural",    "texto":"Ar-condicionado quebrado faz dias. Calor insuportável."},
    {"id":"f4","linha":"311","rota":"TILAG – TICEN Direto",                  "local":"Lagoa da Conceição", "tempo":"40 min", "cat":"🚨 Comportamental","texto":"Motorista xingou passageiro que pediu para diminuir a velocidade."},
    {"id":"f5","linha":"320","rota":"TILAG – TICEN via Beira-Mar",           "local":"Av. Beira-Mar",      "tempo":"1 hora", "cat":"⏱️ Operacional",   "texto":"Linha passou com 35 min de atraso sem aviso no app."},
    {"id":"f6","linha":"330","rota":"TILAG – TICEN via Mauro Ramos",         "local":"TICEN",              "tempo":"2 horas","cat":"👥 Demanda",        "texto":"Dois ônibus seguidos lotados, terceiro veio vazio depois de 40 min."},
    {"id":"f7","linha":"333","rota":"TILAG – TITRI via Madre Benvenuta",     "local":"Madre Benvenuta",    "tempo":"3 horas","cat":"🔧 Estrutural",    "texto":"Elevador para cadeirantes não funciona há mais de uma semana."},
    {"id":"f8","linha":"430","rota":"TIRIO – TICEN via Costeira",            "local":"Costeira do Pirajubaé","tempo":"5 horas","cat":"💳 Sistêmica",   "texto":"Cartão debitou duas vezes na mesma viagem."},
    {"id":"f9","linha":"845","rota":"TILAG – TITRI via Córrego Grande",      "local":"Córrego Grande",     "tempo":"6 horas","cat":"⏱️ Operacional",   "texto":"Horário das 19h simplesmente não apareceu. Furo total."},
]

aba = st.session_state.aba_ativa

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif !important; box-sizing: border-box; }
.stApp { background-color: #f0f4ff !important; }
#MainMenu, footer, header { visibility: hidden !important; }

/* Espaço para a nav bar fixa */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 110px !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

/* Textos acessíveis - fonte maior */
h1,h2,h3 { color:#1a56db !important; text-align:center; }
label, p, [data-testid="stWidgetLabel"] p, .stMarkdown p {
    color:#1e293b !important; font-weight:700 !important; font-size:1rem !important;
}

/* Inputs maiores para facilitar toque */
div[data-baseweb="select"] > div, input[type="text"], textarea {
    background:#fff !important; color:#1e293b !important;
    border:2px solid #c7d7fc !important; border-radius:14px !important;
    font-size:1rem !important; min-height:52px !important;
}
input, textarea { color:#1e293b !important; -webkit-text-fill-color:#1e293b !important; }

/* ═══════════════════════════════════════
   BARRA NAV INFERIOR — FIXA NO RODAPÉ
   CSS targeta o ÚLTIMO bloco horizontal
   ═══════════════════════════════════════ */
[data-testid="stHorizontalBlock"]:last-of-type {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: white !important;
    border-top: 2px solid #e8eeff !important;
    box-shadow: 0 -4px 24px rgba(30,86,219,0.13) !important;
    z-index: 9999 !important;
    padding: 6px 8px 16px 8px !important;
    margin: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    gap: 4px !important;
}

/* Botões da nav bar */
[data-testid="stHorizontalBlock"]:last-of-type .stButton > button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #94a3b8 !important;
    font-size: 0.72rem !important;
    font-weight: 900 !important;
    height: 60px !important;
    width: 100% !important;
    border-radius: 12px !important;
    white-space: pre-line !important;
    line-height: 1.3 !important;
    padding: 6px 4px !important;
}
[data-testid="stHorizontalBlock"]:last-of-type .stButton > button:hover,
[data-testid="stHorizontalBlock"]:last-of-type .stButton > button:focus {
    background: #eef2ff !important;
    color: #1a56db !important;
}

/* Aba ativa na nav */
.nav-ativo button {
    background: #eef2ff !important;
    color: #1a56db !important;
}

/* Botão principal ENVIAR */
.btn-enviar .stButton > button {
    background: linear-gradient(135deg,#1a56db,#3b82f6) !important;
    color: white !important; border-radius: 50px !important;
    font-weight: 900 !important; font-size: 1.05rem !important;
    border: none !important; height: 3.4em !important; width: 100% !important;
    box-shadow: 0 4px 18px rgba(26,86,219,0.35) !important;
    margin-top: 8px !important;
}

/* Botão voltar */
.btn-voltar .stButton > button {
    background: #eef2ff !important; color: #1a56db !important;
    border: none !important; border-radius: 50px !important;
    font-weight: 900 !important; height: 2.8em !important;
    font-size: 1rem !important;
}

/* Seções com espaçamento generoso */
.secao {
    background: white;
    padding: 18px 20px;
    border-radius: 20px;
    box-shadow: 0 2px 14px rgba(30,86,219,0.09);
    border: 1px solid #e8eeff;
    margin-bottom: 16px;   /* espaço claro entre blocos */
}
.secao-titulo {
    font-size: .78rem; font-weight:900; color:#94a3b8;
    letter-spacing:1.2px; text-transform:uppercase; margin-bottom:12px;
}

/* Card da categoria */
.cat-card {
    border-radius: 14px; padding: 14px 16px;
    margin-top: 12px; border-left: 6px solid;
    display:flex; flex-direction:column; gap:5px;
}
.cat-foco    { font-size:.85rem; font-weight:700; color:#475569; }
.cat-exemplo { font-size:.83rem; font-style:italic; color:#64748b; font-weight:600; }

/* Desc do grupo de linha */
.grupo-desc {
    background: #eef2ff; border-radius: 12px; padding: 10px 14px;
    font-size: .85rem; color: #1e3a8a !important;
    font-weight: 700 !important; margin: 10px 0 8px 0;
}

/* Cards de reclamação */
.card {
    background:white; padding:18px 20px; border-radius:18px;
    box-shadow:0 2px 12px rgba(30,86,219,0.08);
    border:1px solid #e8eeff; margin-bottom:14px;
}
.status-badge {
    padding:5px 14px; border-radius:20px;
    font-size:.8rem; font-weight:900; color:white; display:inline-block;
}

/* Detalhe da reclamação */
.detalhe-box {
    background:#f8faff; border-radius:14px; padding:16px 18px;
    margin-top:12px; border:1px solid #dbe8ff;
}
.resposta-box {
    background:#ecfdf5; border-radius:14px; padding:16px 18px;
    margin-top:14px; border-left:5px solid #10b981;
}
.resposta-titulo {
    font-size:.75rem; font-weight:900; color:#059669;
    letter-spacing:.8px; text-transform:uppercase; margin-bottom:8px;
}

/* Upload */
div[data-testid="stFileUploadDropzone"] {
    background-color:#eef2ff !important; border:2px dashed #1a56db !important; border-radius:14px !important;
}
div[data-testid="stFileUploadDropzone"] button { background-color:#1a56db !important; color:white !important; }

/* App header */
.app-header { text-align:center; margin-bottom:18px; }
.app-header h1 { font-size:1.5rem !important; font-weight:900 !important; margin:0 !important; color:#1a56db !important; }
.app-header p  { font-size:.88rem !important; color:#64748b !important; margin:4px 0 0 0 !important; font-weight:700 !important; }

/* Forum cards */
.forum-card {
    background:white; padding:16px 18px; border-radius:18px;
    box-shadow:0 2px 10px rgba(30,86,219,0.07);
    border:1px solid #e8eeff; margin-bottom:12px;
}
.forum-linha { font-weight:900; font-size:1.05rem; color:#1a56db; }
.forum-rota  { font-size:.82rem; color:#64748b; font-weight:700; }
.forum-meta  { font-size:.78rem; color:#94a3b8; margin:4px 0 8px; font-weight:700; }
.forum-texto { font-size:.92rem; color:#334155; font-style:italic; font-weight:600; margin-bottom:12px; }

/* Botões apoiar/comentar no fórum */
[data-testid="stHorizontalBlock"]:not(:last-of-type) .stButton > button {
    border-radius: 50px !important;
    font-size: .85rem !important;
    font-weight: 800 !important;
    height: 2.4em !important;
    border: 1.5px solid #e8eeff !important;
    background: #f8faff !important;
    color: #334155 !important;
}
[data-testid="stHorizontalBlock"]:not(:last-of-type) .stButton > button:hover {
    background: #eef2ff !important; color: #1a56db !important;
    border-color: #c7d7fc !important;
}

/* Comentários */
.coment-item { background:#f8faff; border-radius:10px; padding:10px 14px; margin-top:8px; }
.coment-autor { font-weight:900; color:#1a56db; font-size:.82rem; }
.coment-texto { font-size:.88rem; color:#334155; font-weight:600; }

div[data-testid="stAlert"] { border-radius:14px !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 1 — RECLAMAÇÃO
# ════════════════════════════════════════════════════════
if aba == "reclamacao":
    st.markdown('<div class="app-header"><h1>🚌 Reclama no Ponto</h1><p>Relate problemas no transporte público</p></div>', unsafe_allow_html=True)

    # BLOCO 1
    st.markdown('<div class="secao"><div class="secao-titulo">1 · Tipo do problema</div>', unsafe_allow_html=True)
    escolha_cat = st.selectbox("Categoria:", list(categorias.keys()), key="sel_cat", label_visibility="collapsed")
    ic = categorias[escolha_cat]
    st.markdown(f"""
    <div class="cat-card" style="background:{ic['cor']}15;border-color:{ic['cor']};">
        <div style="font-size:1rem;font-weight:900;color:{ic['cor']};">{escolha_cat}</div>
        <div class="cat-foco">🎯 Foco: {ic['foco']}</div>
        <div class="cat-exemplo">💬 Exemplo: {ic['exemplo']}</div>
    </div>
    </div>""", unsafe_allow_html=True)

    # BLOCO 2 — separado visualmente
    st.markdown('<div class="secao"><div class="secao-titulo">2 · Linha do ônibus</div>', unsafe_allow_html=True)
    escolha_grupo = st.selectbox("Grupo:", list(grupos_linhas.keys()), key="sel_grupo", label_visibility="collapsed")
    gi = grupos_linhas[escolha_grupo]
    st.markdown(f'<div class="grupo-desc">🗺️ {gi["desc"]}</div>', unsafe_allow_html=True)
    linha = st.selectbox("Número da linha:", gi["linhas"], key="sel_linha", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # BLOCO 3
    st.markdown('<div class="secao"><div class="secao-titulo">3 · Detalhes da ocorrência</div>', unsafe_allow_html=True)
    placa     = st.text_input("Placa do Ônibus (Opcional):", placeholder="Ex: ABC-1234", key="inp_placa")
    descricao = st.text_area("Descrição:", placeholder="Descreva o que aconteceu...", height=100, key="inp_desc")
    foto      = st.file_uploader("📎 Anexar foto (Opcional):", key="inp_foto")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-enviar">', unsafe_allow_html=True)
    if st.button("🚀  ENVIAR RECLAMAÇÃO", key="btn_enviar"):
        if not descricao:
            st.warning("⚠️ Por favor, descreva o problema antes de enviar.")
        else:
            novo_p = f"#RP-2026-{len(st.session_state.minhas_reclamacoes) + 1:03d}"
            st.session_state.minhas_reclamacoes.append({
                "protocolo": novo_p, "grupo": escolha_grupo, "linha": linha,
                "status": "Recebido", "data": datetime.now().strftime("%d/%m/%Y"),
                "cat": escolha_cat, "placa": placa, "descricao": descricao, "resposta": "",
            })
            st.success(f"✅ Reclamação enviada! Protocolo: **{novo_p}**")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 2 — FÓRUM
# ════════════════════════════════════════════════════════
elif aba == "forum":
    st.markdown("<h3>💬 Fórum da Comunidade</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b;font-size:.9rem;'>Apoie ou comente ocorrências de outros usuários</p>", unsafe_allow_html=True)

    for post in FORUM_POSTS:
        pid      = post["id"]
        apoios   = st.session_state.forum_apoios.get(pid, 0)
        coments  = st.session_state.forum_coments.get(pid, [])
        expandido = st.session_state.forum_expandido == pid

        st.markdown(f"""
        <div class="forum-card">
            <div class="forum-linha">Linha {post['linha']}</div>
            <div class="forum-rota">{post['rota']}</div>
            <div class="forum-meta">📍 {post['local']} &nbsp;·&nbsp; Há {post['tempo']} &nbsp;·&nbsp; {post['cat']}</div>
            <div class="forum-texto">"{post['texto']}"</div>
        </div>
        """, unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            txt_apoio = f"👍  Apoiar   ({apoios})" if apoios > 0 else "👍  Apoiar"
            if st.button(txt_apoio, key=f"apoio_{pid}", use_container_width=True):
                st.session_state.forum_apoios[pid] = apoios + 1
                st.rerun()
        with cb:
            txt_coment = f"💬  Comentários ({len(coments)})" if coments else "💬  Comentar"
            if st.button(txt_coment, key=f"toggle_{pid}", use_container_width=True):
                st.session_state.forum_expandido = None if expandido else pid
                st.rerun()

        if expandido:
            for c in coments:
                st.markdown(f"""
                <div class="coment-item">
                    <div class="coment-autor">{c['autor']}</div>
                    <div class="coment-texto">{c['texto']}</div>
                </div>""", unsafe_allow_html=True)
            novo_c = st.text_input("Seu comentário:", key=f"inp_c_{pid}", placeholder="Escreva seu comentário...", label_visibility="collapsed")
            if st.button("✉️  Enviar comentário", key=f"send_c_{pid}"):
                if novo_c.strip():
                    if pid not in st.session_state.forum_coments:
                        st.session_state.forum_coments[pid] = []
                    st.session_state.forum_coments[pid].append({"autor": "Você", "texto": novo_c.strip()})
                    st.session_state.forum_expandido = pid
                    st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 3 — MINHAS RECLAMAÇÕES
# ════════════════════════════════════════════════════════
else:
    # TELA DE DETALHE
    if st.session_state.rec_detalhe is not None:
        idx = st.session_state.rec_detalhe
        rec = st.session_state.minhas_reclamacoes[idx]
        cor = "#f59e0b" if rec['status']=="Em Análise" else "#10b981" if rec['status']=="Concluído" else "#1a56db"
        grupo_curto = rec.get('grupo','').split("(")[0].strip()

        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("← Voltar para Meus Chamados", key="btn_voltar"):
            st.session_state.rec_detalhe = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:#1a56db;font-weight:900;font-size:1.1rem;">{rec['protocolo']}</span>
                <span class="status-badge" style="background:{cor};">{rec['status']}</span>
            </div>
            <div style="color:#334155;font-size:.95rem;font-weight:700;">🚌 Linha <b>{rec['linha']}</b></div>
            <div style="color:#64748b;font-size:.85rem;font-weight:700;margin-top:4px;">{grupo_curto}</div>
            <div style="color:#94a3b8;font-size:.85rem;font-weight:700;margin-top:6px;">{rec['cat']} &nbsp;·&nbsp; 📅 {rec['data']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detalhe-box">
            <div style="font-size:.75rem;font-weight:900;color:#94a3b8;letter-spacing:.8px;text-transform:uppercase;margin-bottom:10px;">📋 Detalhes da Ocorrência</div>
            {'<div style="font-size:.88rem;font-weight:700;color:#64748b;margin-bottom:8px;">🚗 Placa: ' + rec['placa'] + '</div>' if rec.get('placa') else ''}
            <div style="font-size:.95rem;color:#334155;font-weight:600;line-height:1.6;">{rec.get('descricao','—')}</div>
        </div>
        """, unsafe_allow_html=True)

        resposta = rec.get('resposta','')
        if resposta:
            st.markdown(f"""
            <div class="resposta-box">
                <div class="resposta-titulo">✅ Resposta da Empresa Responsável</div>
                <div style="font-size:.95rem;color:#065f46;font-weight:600;line-height:1.6;">{resposta}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#fafafa;border-radius:14px;padding:16px 18px;margin-top:14px;border:1px dashed #cbd5e1;text-align:center;">
                <div style="font-size:.88rem;color:#94a3b8;font-weight:700;">⏳ Aguardando resposta da empresa responsável</div>
            </div>
            """, unsafe_allow_html=True)

    # LISTA DE RECLAMAÇÕES
    else:
        st.markdown("<h3>🔍 Meus Chamados</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#64748b;font-size:.9rem;'>Toque em uma reclamação para ver os detalhes</p>", unsafe_allow_html=True)

        if not st.session_state.minhas_reclamacoes:
            st.markdown('<div class="card" style="text-align:center;padding:36px;"><div style="font-size:3rem;">📭</div><p style="color:#64748b;margin-top:12px;font-size:1rem;">Você ainda não fez nenhuma reclamação.</p></div>', unsafe_allow_html=True)
        else:
            for i, rec in enumerate(reversed(st.session_state.minhas_reclamacoes)):
                idx_real = len(st.session_state.minhas_reclamacoes) - 1 - i
                cor = "#f59e0b" if rec['status']=="Em Análise" else "#10b981" if rec['status']=="Concluído" else "#1a56db"
                grupo_curto = rec.get('grupo','').split("(")[0].strip()
                icone_resp  = " 💬" if rec.get('resposta') else ""

                st.markdown(f"""
                <div class="card" style="cursor:pointer;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="color:#1a56db;font-weight:900;font-size:1rem;">{rec['protocolo']}</span>
                        <span class="status-badge" style="background:{cor};">{rec['status']}</span>
                    </div>
                    <div style="color:#334155;font-size:.92rem;font-weight:700;">🚌 Linha <b>{rec['linha']}</b>{icone_resp}</div>
                    <div style="color:#64748b;font-size:.82rem;font-weight:700;margin-top:3px;">{grupo_curto}</div>
                    <div style="color:#94a3b8;font-size:.82rem;font-weight:700;margin-top:5px;">{rec['cat']} &nbsp;·&nbsp; 📅 {rec['data']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Ver detalhes  →", key=f"det_{idx_real}", use_container_width=True):
                    st.session_state.rec_detalhe = idx_real
                    st.rerun()

# ════════════════════════════════════════════════════════
# BARRA DE NAVEGAÇÃO INFERIOR — colunas reais do Streamlit
# CSS acima torna este último bloco horizontal em nav fixa
# ════════════════════════════════════════════════════════
def nav_cls(nome):
    return "nav-ativo" if aba == nome else ""

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="{nav_cls("reclamacao")}">', unsafe_allow_html=True)
    if st.button("📝\nReclamar", key="nav_rec", use_container_width=True):
        st.session_state.aba_ativa   = "reclamacao"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="{nav_cls("forum")}">', unsafe_allow_html=True)
    if st.button("💬\nFórum", key="nav_for", use_container_width=True):
        st.session_state.aba_ativa   = "forum"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="{nav_cls("minhas")}">', unsafe_allow_html=True)
    if st.button("🔍\nMeus\nChamados", key="nav_min", use_container_width=True):
        st.session_state.aba_ativa   = "minhas"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
