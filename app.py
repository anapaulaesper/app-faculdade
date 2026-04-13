import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Reclame no Ponto", page_icon="🚌", layout="centered")

# ── ESTADO DA SESSÃO ─────────────────────────────────────
if 'minhas_reclamacoes' not in st.session_state:
    st.session_state.minhas_reclamacoes = [
        {
            "protocolo": "#RP-2026-001", "grupo": "🔄 Circulares e Transversais",
            "linha": "135", "status": "Concluído", "data": "25/03/2026",
            "cat": "⏱️ Operacional", "placa": "ABC-1234",
            "descricao": "Ônibus atrasou mais de 40 minutos no horário das 17h.",
            "resposta": "Identificamos falha operacional. O motorista foi notificado e o horário reforçado a partir de 01/04/2026."
        },
        {
            "protocolo": "#RP-2026-015", "grupo": "🔗 Troncais (Inter-terminais)",
            "linha": "231", "status": "Em Análise", "data": "27/03/2026",
            "cat": "👥 Demanda", "placa": "",
            "descricao": "Superlotação constante nos horários de pico. Passageiros ficam para trás.",
            "resposta": "Reclamação em avaliação pelo setor de planejamento. Previsão: 15/04/2026."
        },
    ]
if 'rec_detalhe'     not in st.session_state: st.session_state.rec_detalhe     = None
if 'forum_apoios'    not in st.session_state: st.session_state.forum_apoios    = {}
if 'forum_coments'   not in st.session_state: st.session_state.forum_coments   = {}
if 'forum_expandido' not in st.session_state: st.session_state.forum_expandido = None

categorias = {
    "⏱️ Operacional":    {"foco": "Cumprimento de metas",   "exemplo": "Atrasos e furos de escala.",                     "cor": "#3b82f6"},
    "🔧 Estrutural":     {"foco": "Estado do veículo",       "exemplo": "Elevador quebrado ou falta de ar-condicionado.", "cor": "#f59e0b"},
    "🚨 Comportamental": {"foco": "Conduta humana",           "exemplo": "Direção perigosa ou grosseria.",                 "cor": "#ef4444"},
    "👥 Demanda":        {"foco": "Fluxo de passageiros",    "exemplo": "Superlotação crônica.",                          "cor": "#8b5cf6"},
    "💳 Sistêmica":      {"foco": "Tecnologia e Créditos",   "exemplo": "Erros no cartão de passagens.",                  "cor": "#10b981"},
}

grupos_linhas = {
    "🔗 Troncais (Inter-terminais)":        {"desc": "Conectam terminais entre si — espinha dorsal do sistema.",   "linhas": ["210","221","230","231","233","311","320","330","331","332","333","410","430","840","841","843","845","847"]},
    "🏘️ Alimentadoras Norte (TICAN/TISAN)": {"desc": "Ligam bairros do Norte ao terminal TICAN.",                  "linhas": ["260","264","267","271","272","281"]},
    "🌊 Alimentadoras Leste (TILAG)":        {"desc": "Ligam bairros do Leste ao terminal TILAG.",                  "linhas": ["360","362","363","364"]},
    "🏖️ Alimentadoras Sul (TIRIO)":          {"desc": "Ligam bairros do Sul ao terminal TIRIO.",                    "linhas": ["462","562","563","564","565"]},
    "🌿 Bacia do Itacorubi (TITRI)":         {"desc": "Ligam bairros do Itacorubi ao terminal TITRI.",              "linhas": ["164","165","176"]},
    "🌉 Alimentadoras Continente":           {"desc": "Atendem a região continental de Florianópolis.",             "linhas": ["631","661","663","670"]},
    "🔄 Circulares e Transversais":          {"desc": "Volta ao Morro (UFSC/UDESC) e conexões entre praias.",       "linhas": ["134","135","136","137","138","294"]},
    "🌟 Executivos (Amarelinhos)":           {"desc": "Micro-ônibus com ar-condicionado e tarifa diferenciada.",    "linhas": ["1112","1120","1121","1123","1125","4120","4123","4124","2120"]},
    "🌙 Madrugadão (00h–05h)":              {"desc": "Linhas que operam na madrugada.",                            "linhas": ["100","102","200","201","300","500","501","600","604"]},
}

FORUM_POSTS = [
    {"id":"f1","linha":"134","rota":"TITRI – TICEN via Beira-Mar",       "local":"Terminal TITRI",       "tempo":"8 min",  "cat":"⏱️","texto":"Furo de viagem no horário das 7h30. Fiquei esperando 50 minutos."},
    {"id":"f2","linha":"221","rota":"TICAN – TICEN via Mauro Ramos",      "local":"TICAN",                "tempo":"15 min", "cat":"👥","texto":"Superlotação absurda todo dia às 18h. Passageiros prensados."},
    {"id":"f3","linha":"233","rota":"TICAN – TITRI via UFSC",             "local":"UFSC",                 "tempo":"22 min", "cat":"🔧","texto":"Ar-condicionado quebrado faz dias. Calor insuportável."},
    {"id":"f4","linha":"311","rota":"TILAG – TICEN Direto",               "local":"Lagoa da Conceição",   "tempo":"40 min", "cat":"🚨","texto":"Motorista xingou passageiro que pediu para diminuir velocidade."},
    {"id":"f5","linha":"320","rota":"TILAG – TICEN via Beira-Mar",        "local":"Av. Beira-Mar",        "tempo":"1 hora", "cat":"⏱️","texto":"Linha passou 35 min atrasada sem aviso no app."},
    {"id":"f6","linha":"330","rota":"TILAG – TICEN via Mauro Ramos",      "local":"TICEN",                "tempo":"2 horas","cat":"👥","texto":"Dois ônibus lotados seguidos, terceiro vazio depois de 40 min."},
    {"id":"f7","linha":"333","rota":"TILAG – TITRI via Madre Benvenuta",  "local":"Madre Benvenuta",      "tempo":"3 horas","cat":"🔧","texto":"Elevador para cadeirantes não funciona há mais de uma semana."},
    {"id":"f8","linha":"430","rota":"TIRIO – TICEN via Costeira",         "local":"Costeira do Pirajubaé","tempo":"5 horas","cat":"💳","texto":"Cartão debitou duas vezes na mesma viagem."},
    {"id":"f9","linha":"845","rota":"TILAG – TITRI via Córrego Grande",   "local":"Córrego Grande",       "tempo":"6 horas","cat":"⏱️","texto":"Horário das 19h simplesmente não apareceu. Furo total."},
]

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif !important; box-sizing: border-box; }
.stApp { background-color: #f0f4ff !important; }
#MainMenu, footer, header { visibility: hidden !important; }

.block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 100px !important;   /* espaço para a nav no rodapé */
    max-width: 480px !important;
    margin: 0 auto !important;
}

/* ════════════════════════════════════════
   TABS NO RODAPÉ — move a barra para baixo
   ════════════════════════════════════════ */
[data-testid="stTabs"] {
    display: flex;
    flex-direction: column-reverse;   /* conteúdo em cima, barra embaixo */
}
[data-testid="stTabList"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
    background: white !important;
    border-top: 2px solid #e8eeff !important;
    border-bottom: none !important;
    box-shadow: 0 -4px 20px rgba(30,86,219,0.13) !important;
    padding: 4px 6px 14px 6px !important;
    gap: 4px !important;
    justify-content: space-around !important;
}
/* Cada tab */
button[data-baseweb="tab"] {
    flex: 1 !important;
    font-size: 0.7rem !important;
    font-weight: 900 !important;
    color: #94a3b8 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 8px 4px !important;
    min-height: 54px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 3px !important;
    transition: all .15s !important;
    white-space: pre-line !important;
}
button[data-baseweb="tab"]:hover,
button[data-baseweb="tab"]:active {
    background: #eef2ff !important;
    color: #1a56db !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #eef2ff !important;
    color: #1a56db !important;
    border-bottom: none !important;
    border-top: 3px solid #1a56db !important;
}
/* Remove o indicador padrão do Streamlit */
[data-testid="stTabList"] > div[role="presentation"] { display: none !important; }
[data-testid="stTabPanel"] { padding: 0 !important; }

/* ── TEXTOS ── */
h1, h2, h3 { color: #1a56db !important; text-align: center; }
label, p, [data-testid="stWidgetLabel"] p, .stMarkdown p {
    color: #1e293b !important; font-weight: 700 !important;
}

/* ── INPUTS ── */
div[data-baseweb="select"]>div, input[type="text"], textarea {
    background: #fff !important; color: #1e293b !important;
    border: 2px solid #c7d7fc !important; border-radius: 14px !important;
    font-size: .95rem !important;
}
input, textarea { color: #1e293b !important; -webkit-text-fill-color: #1e293b !important; }

/* ── UPLOAD ── */
[data-testid="stFileUploaderDropzone"] {
    background: white !important;
    border: 2px dashed #1a56db !important;
    border-radius: 14px !important;
}

/* ── BOTÕES ── */
.stButton > button {
    border-radius: 50px !important; font-size: .9rem !important;
    font-weight: 800 !important; height: 2.6em !important; width: 100% !important;
    border: 1.5px solid #e8eeff !important; background: #f8faff !important; color: #334155 !important;
}
.stButton > button:hover { background: #eef2ff !important; color: #1a56db !important; }
.btn-enviar .stButton > button {
    background: linear-gradient(135deg,#1a56db,#3b82f6) !important;
    color: white !important; border: none !important;
    height: 3.2em !important; font-size: 1rem !important;
    box-shadow: 0 4px 18px rgba(26,86,219,.35) !important; margin-top: 6px !important;
}
.btn-voltar .stButton > button { background: #eef2ff !important; color: #1a56db !important; border: none !important; }

/* ── SEÇÕES ── */
.secao { background: white; padding: 16px 18px; border-radius: 18px; box-shadow: 0 2px 12px rgba(30,86,219,.08); border: 1px solid #e8eeff; margin-bottom: 14px; }
.secao-titulo { font-size: .72rem; font-weight: 900; color: #94a3b8; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 10px; }
.cat-card { border-radius: 12px; padding: 12px 14px; margin-top: 10px; border-left: 5px solid; }
.cat-foco    { font-size: .82rem; font-weight: 700; color: #475569; margin-top: 3px; }
.cat-exemplo { font-size: .8rem; font-style: italic; color: #64748b; font-weight: 600; margin-top: 2px; }
.grupo-desc  { background: #eef2ff; border-radius: 10px; padding: 9px 13px; font-size: .82rem; color: #1e3a8a !important; font-weight: 700 !important; margin: 9px 0 7px; }

/* ── CARDS ── */
.card { background: white; padding: 16px 18px; border-radius: 18px; box-shadow: 0 2px 12px rgba(30,86,219,.08); border: 1px solid #e8eeff; margin-bottom: 12px; }
.status-badge { padding: 4px 12px; border-radius: 20px; font-size: .78rem; font-weight: 900; color: white; display: inline-block; }
.detalhe-box { background: #f8faff; border-radius: 13px; padding: 14px 16px; margin-top: 11px; border: 1px solid #dbe8ff; }
.detalhe-label { font-size: .72rem; font-weight: 900; color: #94a3b8; letter-spacing: .8px; text-transform: uppercase; margin-bottom: 8px; }
.detalhe-placa { font-size: .88rem; font-weight: 700; color: #64748b; margin-bottom: 7px; }
.detalhe-texto { font-size: .92rem; color: #334155; font-weight: 600; line-height: 1.6; }
.resposta-box { background: #ecfdf5; border-radius: 13px; padding: 14px 16px; margin-top: 12px; border-left: 5px solid #10b981; }
.resposta-titulo { font-size: .72rem; font-weight: 900; color: #059669; letter-spacing: .8px; text-transform: uppercase; margin-bottom: 7px; }
.resposta-texto { font-size: .92rem; color: #065f46; font-weight: 600; line-height: 1.6; }
.aguardando-box { background: #fafafa; border-radius: 12px; padding: 14px; margin-top: 12px; border: 1px dashed #cbd5e1; text-align: center; }
.aguardando-txt { font-size: .85rem; color: #94a3b8; font-weight: 700; }

/* ── APP HEADER ── */
.app-header { text-align: center; margin-bottom: 14px; padding-top: 4px; }
.app-header h1 { font-size: 1.4rem !important; font-weight: 900 !important; margin: 0 !important; }
.app-header p  { font-size: .82rem !important; color: #64748b !important; margin: 2px 0 0 !important; font-weight: 700 !important; }

/* ── FÓRUM ── */
.forum-card { background: white; padding: 14px 16px; border-radius: 16px; box-shadow: 0 2px 8px rgba(30,86,219,.07); border: 1px solid #e8eeff; margin-bottom: 10px; }
.forum-linha { font-weight: 900; font-size: 1rem; color: #1a56db; }
.forum-rota  { font-size: .8rem; color: #64748b; font-weight: 700; }
.forum-meta  { font-size: .75rem; color: #94a3b8; margin: 3px 0 7px; font-weight: 700; }
.forum-texto { font-size: .9rem; color: #334155; font-style: italic; font-weight: 600; margin-bottom: 10px; }
.coment-item { background: #f8faff; border-radius: 10px; padding: 9px 13px; margin-top: 7px; }
.coment-autor { font-weight: 900; color: #1a56db; font-size: .8rem; }
.coment-texto { font-size: .87rem; color: #334155; font-weight: 600; }

div[data-testid="stAlert"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-header"><h1>🚌 Reclama no Ponto</h1><p>Transporte público de Florianópolis</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝  Reclamar", "💬  Fórum", "🔍  Meus Chamados"])

# ════════════════════════════════════════════════════════
# TAB 1 — RECLAMAÇÃO
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="secao"><div class="secao-titulo">1 · Tipo do problema</div>', unsafe_allow_html=True)
    escolha_cat = st.selectbox("Categoria:", list(categorias.keys()), key="sel_cat", label_visibility="collapsed")
    ic = categorias[escolha_cat]
    st.markdown(
        f'<div class="cat-card" style="background:{ic["cor"]}15;border-color:{ic["cor"]};">'
        f'<div style="font-size:.95rem;font-weight:900;color:{ic["cor"]};">{escolha_cat}</div>'
        f'<div class="cat-foco">🎯 Foco: {ic["foco"]}</div>'
        f'<div class="cat-exemplo">💬 Ex: {ic["exemplo"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="secao"><div class="secao-titulo">2 · Linha do ônibus</div>', unsafe_allow_html=True)
    escolha_grupo = st.selectbox("Grupo:", list(grupos_linhas.keys()), key="sel_grupo", label_visibility="collapsed")
    gi = grupos_linhas[escolha_grupo]
    st.markdown(f'<div class="grupo-desc">🗺️ {gi["desc"]}</div>', unsafe_allow_html=True)
    linha = st.selectbox("Número:", gi["linhas"], key="sel_linha", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="secao"><div class="secao-titulo">3 · Detalhes</div>', unsafe_allow_html=True)
    placa     = st.text_input("Placa (Opcional):", placeholder="Ex: ABC-1234", key="inp_placa")
    descricao = st.text_area("Descrição:", placeholder="Descreva o que aconteceu...", height=95, key="inp_desc")
    st.file_uploader("📎 Foto (Opcional):", key="inp_foto", label_visibility="visible")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-enviar">', unsafe_allow_html=True)
    if st.button("🚀  ENVIAR RECLAMAÇÃO", key="btn_enviar"):
        if not descricao:
            st.warning("⚠️ Descreva o problema antes de enviar.")
        else:
            novo_p = f"#RP-2026-{len(st.session_state.minhas_reclamacoes)+1:03d}"
            st.session_state.minhas_reclamacoes.append({
                "protocolo": novo_p, "grupo": escolha_grupo, "linha": linha,
                "status": "Recebido", "data": datetime.now().strftime("%d/%m/%Y"),
                "cat": escolha_cat, "placa": placa, "descricao": descricao, "resposta": "",
            })
            st.success(f"✅ Protocolo **{novo_p}** registrado!")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 2 — FÓRUM
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown("<p style='text-align:center;color:#64748b;font-size:.88rem;margin-bottom:14px;'>Apoie ou comente ocorrências de outros usuários</p>", unsafe_allow_html=True)

    for post in FORUM_POSTS:
        pid       = post["id"]
        apoios    = st.session_state.forum_apoios.get(pid, 0)
        coments   = st.session_state.forum_coments.get(pid, [])
        expandido = st.session_state.forum_expandido == pid

        st.markdown(
            f'<div class="forum-card">'
            f'<div class="forum-linha">Linha {post["linha"]}</div>'
            f'<div class="forum-rota">{post["rota"]}</div>'
            f'<div class="forum-meta">📍 {post["local"]} · Há {post["tempo"]} · {post["cat"]}</div>'
            f'<div class="forum-texto">"{post["texto"]}"</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        ca, cb = st.columns(2)
        with ca:
            lbl_a = f"👍 Apoiar ({apoios})" if apoios else "👍 Apoiar"
            if st.button(lbl_a, key=f"apoio_{pid}", use_container_width=True):
                st.session_state.forum_apoios[pid] = apoios + 1
                st.rerun()
        with cb:
            lbl_c = f"💬 Ver ({len(coments)})" if coments else "💬 Comentar"
            if st.button(lbl_c, key=f"toggle_{pid}", use_container_width=True):
                st.session_state.forum_expandido = None if expandido else pid
                st.rerun()

        if expandido:
            for c in coments:
                st.markdown(
                    f'<div class="coment-item">'
                    f'<div class="coment-autor">{c["autor"]}</div>'
                    f'<div class="coment-texto">{c["texto"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            novo_c = st.text_input("", key=f"inp_c_{pid}", placeholder="Escreva seu comentário...")
            if st.button("✉️ Enviar comentário", key=f"send_c_{pid}"):
                if novo_c.strip():
                    st.session_state.forum_coments.setdefault(pid, []).append({"autor": "Você", "texto": novo_c.strip()})
                    st.session_state.forum_expandido = pid
                    st.rerun()
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 3 — MEUS CHAMADOS
# ════════════════════════════════════════════════════════
with tab3:
    if st.session_state.rec_detalhe is not None:
        idx = st.session_state.rec_detalhe
        rec = st.session_state.minhas_reclamacoes[idx]
        cor = "#f59e0b" if rec['status'] == "Em Análise" else "#10b981" if rec['status'] == "Concluído" else "#1a56db"
        grupo_curto = rec.get('grupo', '').split("(")[0].strip()

        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("← Voltar", key="btn_voltar"):
            st.session_state.rec_detalhe = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Card resumo
        st.markdown(
            f'<div class="card">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
            f'<span style="color:#1a56db;font-weight:900;font-size:1rem;">{rec["protocolo"]}</span>'
            f'<span class="status-badge" style="background:{cor};">{rec["status"]}</span>'
            f'</div>'
            f'<div style="color:#334155;font-size:.92rem;font-weight:700;">🚌 Linha <b>{rec["linha"]}</b></div>'
            f'<div style="color:#64748b;font-size:.82rem;font-weight:700;margin-top:3px;">{grupo_curto}</div>'
            f'<div style="color:#94a3b8;font-size:.82rem;font-weight:700;margin-top:5px;">{rec["cat"]} · 📅 {rec["data"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Detalhes — sem f-string condicional, tudo separado
        st.markdown('<div class="detalhe-box"><div class="detalhe-label">📋 Detalhes</div>', unsafe_allow_html=True)
        if rec.get('placa'):
            st.markdown(f'<div class="detalhe-placa">🚗 Placa: {rec["placa"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detalhe-texto">{rec.get("descricao", "—")}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Resposta da empresa
        resposta = rec.get('resposta', '')
        if resposta:
            st.markdown('<div class="resposta-box">', unsafe_allow_html=True)
            st.markdown('<div class="resposta-titulo">✅ Resposta da Empresa</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="resposta-texto">{resposta}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="aguardando-box"><div class="aguardando-txt">⏳ Aguardando resposta da empresa</div></div>', unsafe_allow_html=True)

    else:
        st.markdown("<p style='text-align:center;color:#64748b;font-size:.88rem;margin-bottom:14px;'>Toque para ver os detalhes de cada chamado</p>", unsafe_allow_html=True)

        if not st.session_state.minhas_reclamacoes:
            st.markdown('<div class="card" style="text-align:center;padding:32px;"><div style="font-size:2.8rem;">📭</div><p style="color:#64748b;margin-top:10px;">Nenhuma reclamação ainda.</p></div>', unsafe_allow_html=True)
        else:
            for i, rec in enumerate(reversed(st.session_state.minhas_reclamacoes)):
                idx_real = len(st.session_state.minhas_reclamacoes) - 1 - i
                cor = "#f59e0b" if rec['status'] == "Em Análise" else "#10b981" if rec['status'] == "Concluído" else "#1a56db"
                grupo_curto = rec.get('grupo', '').split("(")[0].strip()
                icone_resp  = " 💬" if rec.get('resposta') else ""

                st.markdown(
                    f'<div class="card">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;">'
                    f'<span style="color:#1a56db;font-weight:900;font-size:.95rem;">{rec["protocolo"]}</span>'
                    f'<span class="status-badge" style="background:{cor};">{rec["status"]}</span>'
                    f'</div>'
                    f'<div style="color:#334155;font-size:.9rem;font-weight:700;">🚌 Linha <b>{rec["linha"]}</b>{icone_resp}</div>'
                    f'<div style="color:#64748b;font-size:.8rem;font-weight:700;margin-top:2px;">{grupo_curto}</div>'
                    f'<div style="color:#94a3b8;font-size:.8rem;font-weight:700;margin-top:4px;">{rec["cat"]} · 📅 {rec["data"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if st.button("Ver detalhes →", key=f"det_{idx_real}", use_container_width=True):
                    st.session_state.rec_detalhe = idx_real
                    st.rerun()
