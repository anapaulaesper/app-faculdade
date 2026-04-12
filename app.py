

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

# ── POSTS DO FÓRUM (com as novas linhas) ─────────────────
FORUM_POSTS = [
    {"id":"f1","linha":"134","rota":"TITRI – TICEN via Beira-Mar","local":"Terminal TITRI","tempo":"8 min",  "cat":"⏱️ Operacional",   "texto":"Furo de viagem no horário das 7h30. Fiquei esperando 50 minutos."},
    {"id":"f2","linha":"221","rota":"TICAN – TICEN via Mauro Ramos","local":"TICAN","tempo":"15 min", "cat":"👥 Demanda",        "texto":"Superlotação absurda todo dia às 18h. Passageiros prensados."},
    {"id":"f3","linha":"233","rota":"TICAN – TITRI via UFSC","local":"UFSC","tempo":"22 min", "cat":"🔧 Estrutural",    "texto":"Ar-condicionado quebrado faz dias. Calor insuportável."},
    {"id":"f4","linha":"311","rota":"TILAG – TICEN Direto","local":"Lagoa da Conceição","tempo":"40 min", "cat":"🚨 Comportamental","texto":"Motorista xingou passageiro que pediu para diminuir a velocidade."},
    {"id":"f5","linha":"320","rota":"TILAG – TICEN via Beira-Mar","local":"Av. Beira-Mar","tempo":"1 hora","cat":"⏱️ Operacional",   "texto":"Linha passou com 35 min de atraso sem aviso no app."},
    {"id":"f6","linha":"330","rota":"TILAG – TICEN via Mauro Ramos","local":"TICEN","tempo":"2 horas","cat":"👥 Demanda",        "texto":"Dois ônibus seguidos lotados, terceiro veio vazio depois de 40 min."},
    {"id":"f7","linha":"333","rota":"TILAG – TITRI via Madre Benvenuta","local":"Madre Benvenuta","tempo":"3 horas","cat":"🔧 Estrutural","texto":"Elevador para cadeirantes não funciona há mais de uma semana."},
    {"id":"f8","linha":"430","rota":"TIRIO – TICEN via Costeira","local":"Costeira do Pirajubaé","tempo":"5 horas","cat":"💳 Sistêmica","texto":"Cartão debitou duas vezes na mesma viagem, terminal não reconheceu."},
    {"id":"f9","linha":"845","rota":"TILAG – TITRI via Córrego Grande","local":"Córrego Grande","tempo":"6 horas","cat":"⏱️ Operacional","texto":"Horário das 19h simplesmente não apareceu. Furo total."},
]

aba = st.session_state.aba_ativa

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif !important; }
.stApp { background-color: #f0f4ff !important; }
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding-top:1rem !important; padding-bottom:100px !important; max-width:500px !important; margin:0 auto !important; }
h1,h2,h3 { color:#1a56db !important; text-align:center; }
label,p,[data-testid="stWidgetLabel"] p,.stMarkdown p { color:#1e293b !important; font-weight:700 !important; }
div[data-baseweb="select"]>div, input[type="text"], textarea {
    background:#fff !important; color:#1e293b !important;
    border:1.5px solid #c7d7fc !important; border-radius:14px !important;
    box-shadow:0 1px 4px rgba(30,86,219,.06) !important;
}
input,textarea { color:#1e293b !important; -webkit-text-fill-color:#1e293b !important; }

/* botão enviar e voltar */
.btn-enviar .stButton>button {
    background:linear-gradient(135deg,#1a56db,#3b82f6) !important;
    color:white !important; border-radius:50px !important; font-weight:900 !important;
    font-size:1rem !important; border:none !important; height:3.2em !important;
    width:100% !important; box-shadow:0 4px 15px rgba(26,86,219,.3) !important;
}
.btn-voltar .stButton>button {
    background:#eef2ff !important; color:#1a56db !important;
    border:none !important; border-radius:50px !important; font-weight:900 !important;
    height:2.5em !important;
}

/* seções do form */
.secao { background:white; padding:16px 18px; border-radius:18px; box-shadow:0 2px 14px rgba(30,86,219,.09); border:1px solid #e8eeff; margin-bottom:14px; }
.secao-titulo { font-size:.82rem; font-weight:900; color:#94a3b8; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; }
.cat-card { border-radius:12px; padding:11px 15px; margin-top:10px; border-left:5px solid; }
.cat-foco { font-size:.78rem; font-weight:700; color:#475569; }
.cat-exemplo { font-size:.78rem; font-style:italic; color:#64748b; font-weight:600; }
.grupo-desc { background:#eef2ff; border-radius:10px; padding:7px 12px; font-size:.78rem; color:#1e3a8a !important; font-weight:700 !important; margin:8px 0 6px 0; }

/* cards gerais */
.card { background:white; padding:16px 18px; border-radius:18px; box-shadow:0 2px 12px rgba(30,86,219,.08); border:1px solid #e8eeff; margin-bottom:12px; }
.card-clicavel { cursor:pointer; transition:box-shadow .15s; }
.card-clicavel:hover { box-shadow:0 4px 20px rgba(30,86,219,.18) !important; }
.status-badge { padding:4px 11px; border-radius:20px; font-size:.75rem; font-weight:900; color:white; display:inline-block; }

/* card detalhe */
.detalhe-box { background:#f8faff; border-radius:14px; padding:14px 16px; margin-top:10px; border:1px solid #dbe8ff; }
.resposta-box { background:#ecfdf5; border-radius:12px; padding:14px 16px; margin-top:12px; border-left:4px solid #10b981; }
.resposta-titulo { font-size:.75rem; font-weight:900; color:#059669; letter-spacing:.8px; text-transform:uppercase; margin-bottom:6px; }

/* upload */
div[data-testid="stFileUploadDropzone"] { background-color:#eef2ff !important; border:2px dashed #1a56db !important; border-radius:14px !important; }
div[data-testid="stFileUploadDropzone"] button { background-color:#1a56db !important; color:white !important; }

/* app header */
.app-header { text-align:center; margin-bottom:14px; }
.app-header h1 { font-size:1.4rem !important; font-weight:900 !important; margin:0 !important; color:#1a56db !important; }
.app-header p { font-size:.8rem !important; color:#64748b !important; margin:2px 0 0 0 !important; font-weight:700 !important; }

/* forum cards */
.forum-card { background:white; padding:14px 16px; border-radius:16px; box-shadow:0 2px 8px rgba(30,86,219,.07); border:1px solid #e8eeff; margin-bottom:10px; }
.forum-linha { font-weight:900; font-size:.98rem; color:#1a56db; }
.forum-rota  { font-size:.78rem; color:#64748b; font-weight:700; }
.forum-meta  { font-size:.76rem; color:#94a3b8; margin:3px 0 6px 0; font-weight:700; }
.forum-texto { font-size:.88rem; color:#334155; font-style:italic; font-weight:600; margin-bottom:10px; }
.forum-sep   { border:none; border-top:1px solid #f1f5f9; margin:8px 0; }

/* comentários no forum */
.coment-item { background:#f8faff; border-radius:10px; padding:8px 12px; margin-top:6px; font-size:.82rem; color:#334155; font-weight:600; }
.coment-autor { font-weight:900; color:#1a56db; font-size:.78rem; }

/* nav inferior */
.nav-ativo button { background:#eef2ff !important; color:#1a56db !important; }
div[data-testid="stAlert"] { border-radius:12px !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 1 — RECLAMAÇÃO
# ════════════════════════════════════════════════════════
if aba == "reclamacao":
    st.markdown('<div class="app-header"><h1>🚌 Reclama no Ponto</h1><p>Relate problemas no transporte público</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="secao"><div class="secao-titulo">1 · Tipo do problema</div>', unsafe_allow_html=True)
    escolha_cat = st.selectbox("Categoria:", list(categorias.keys()), key="sel_cat", label_visibility="collapsed")
    ic = categorias[escolha_cat]
    st.markdown(f"""<div class="cat-card" style="background:{ic['cor']}15;border-color:{ic['cor']};">
        <div style="font-size:.95rem;font-weight:900;color:{ic['cor']};">{escolha_cat}</div>
        <div class="cat-foco">🎯 Foco: {ic['foco']}</div>
        <div class="cat-exemplo">💬 Ex: {ic['exemplo']}</div>
    </div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="secao"><div class="secao-titulo">2 · Linha do ônibus</div>', unsafe_allow_html=True)
    escolha_grupo = st.selectbox("Grupo:", list(grupos_linhas.keys()), key="sel_grupo", label_visibility="collapsed")
    gi = grupos_linhas[escolha_grupo]
    st.markdown(f'<div class="grupo-desc">🗺️ {gi["desc"]}</div>', unsafe_allow_html=True)
    linha = st.selectbox("Número:", gi["linhas"], key="sel_linha", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="secao"><div class="secao-titulo">3 · Detalhes</div>', unsafe_allow_html=True)
    placa     = st.text_input("Placa do Ônibus (Opcional):", placeholder="Ex: ABC-1234", key="inp_placa")
    descricao = st.text_area("Descrição:", placeholder="Descreva o problema brevemente...", height=90, key="inp_desc")
    foto      = st.file_uploader("📎 Anexar foto (Opcional):", key="inp_foto")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-enviar">', unsafe_allow_html=True)
    if st.button("🚀  ENVIAR RECLAMAÇÃO", key="btn_enviar"):
        if not descricao:
            st.warning("⚠️ Por favor, descreva o problema.")
        else:
            novo_p = f"#RP-2026-{len(st.session_state.minhas_reclamacoes) + 1:03d}"
            st.session_state.minhas_reclamacoes.append({
                "protocolo": novo_p, "grupo": escolha_grupo, "linha": linha,
                "status": "Recebido", "data": datetime.now().strftime("%d/%m/%Y"),
                "cat": escolha_cat, "placa": placa, "descricao": descricao, "resposta": "",
            })
            st.success(f"✅ Protocolo **{novo_p}** registrado!")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 2 — FÓRUM
# ════════════════════════════════════════════════════════
elif aba == "forum":
    st.markdown("<h3>💬 Fórum da Comunidade</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b;font-size:.85rem;'>Apoie ocorrências ou deixe um comentário</p>", unsafe_allow_html=True)

    for post in FORUM_POSTS:
        pid = post["id"]
        apoios   = st.session_state.forum_apoios.get(pid, 0)
        coments  = st.session_state.forum_coments.get(pid, [])
        expandido = st.session_state.forum_expandido == pid

        # ── cabeçalho do card ──
        st.markdown(f"""
        <div class="forum-card">
            <div class="forum-linha">Linha {post['linha']}</div>
            <div class="forum-rota">{post['rota']}</div>
            <div class="forum-meta">📍 {post['local']} &nbsp;·&nbsp; Há {post['tempo']} &nbsp;·&nbsp; {post['cat']}</div>
            <div class="forum-texto">"{post['texto']}"</div>
        </div>
        """, unsafe_allow_html=True)

        # ── ações: apoiar + comentar ──
        ca, cb, cc = st.columns([2, 2, 3])
        with ca:
            label_apoio = f"👍 Apoiar ({apoios})" if apoios else "👍 Apoiar"
            if st.button(label_apoio, key=f"apoio_{pid}"):
                st.session_state.forum_apoios[pid] = apoios + 1
                st.rerun()
        with cb:
            label_coment = f"💬 ({len(coments)})" if coments else "💬 Comentar"
            if st.button(label_coment, key=f"toggle_{pid}"):
                st.session_state.forum_expandido = None if expandido else pid
                st.rerun()

        # ── área de comentários (expandida) ──
        if expandido:
            for c in coments:
                st.markdown(f'<div class="coment-item"><span class="coment-autor">{c["autor"]}</span><br>{c["texto"]}</div>', unsafe_allow_html=True)

            novo_c = st.text_input("Seu comentário:", key=f"inp_c_{pid}", placeholder="Escreva aqui...", label_visibility="collapsed")
            if st.button("Enviar comentário", key=f"send_c_{pid}"):
                if novo_c.strip():
                    if pid not in st.session_state.forum_coments:
                        st.session_state.forum_coments[pid] = []
                    st.session_state.forum_coments[pid].append({"autor": "Você", "texto": novo_c.strip()})
                    st.session_state.forum_expandido = pid
                    st.rerun()

        st.markdown("<hr style='border:none;border-top:1px solid #e8eeff;margin:4px 0 12px 0;'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ABA 3 — MINHAS RECLAMAÇÕES
# ════════════════════════════════════════════════════════
else:
    # ── DETALHE de uma reclamação ──
    if st.session_state.rec_detalhe is not None:
        idx = st.session_state.rec_detalhe
        rec = st.session_state.minhas_reclamacoes[idx]

        cor = "#f59e0b" if rec['status']=="Em Análise" else "#10b981" if rec['status']=="Concluído" else "#1a56db"
        grupo_curto = rec.get('grupo','').split("(")[0].strip()

        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("← Voltar", key="btn_voltar"):
            st.session_state.rec_detalhe = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:#1a56db;font-weight:900;font-size:1.05rem;">{rec['protocolo']}</span>
                <span class="status-badge" style="background:{cor};">{rec['status']}</span>
            </div>
            <div style="color:#334155;font-size:.9rem;font-weight:700;">🚌 Linha <b>{rec['linha']}</b> &nbsp;·&nbsp; {grupo_curto}</div>
            <div style="color:#64748b;font-size:.82rem;font-weight:700;margin-top:4px;">{rec['cat']} &nbsp;·&nbsp; 📅 {rec['data']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Detalhes da ocorrência
        st.markdown(f"""
        <div class="detalhe-box">
            <div style="font-size:.75rem;font-weight:900;color:#94a3b8;letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px;">📋 Detalhes da Ocorrência</div>
            {'<div style="font-size:.85rem;font-weight:700;color:#64748b;margin-bottom:6px;">🚗 Placa: ' + rec['placa'] + '</div>' if rec.get('placa') else ''}
            <div style="font-size:.9rem;color:#334155;font-weight:600;line-height:1.5;">{rec.get('descricao', '—')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Resposta da empresa
        resposta = rec.get('resposta', '')
        if resposta:
            st.markdown(f"""
            <div class="resposta-box">
                <div class="resposta-titulo">✅ Resposta da Empresa Responsável</div>
                <div style="font-size:.88rem;color:#065f46;font-weight:600;line-height:1.5;">{resposta}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#fafafa;border-radius:12px;padding:14px 16px;margin-top:12px;border:1px dashed #cbd5e1;text-align:center;">
                <div style="font-size:.82rem;color:#94a3b8;font-weight:700;">⏳ Aguardando resposta da empresa responsável</div>
            </div>
            """, unsafe_allow_html=True)

    # ── LISTA de reclamações ──
    else:
        st.markdown("<h3>🔍 Minhas Reclamações</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#64748b;font-size:.85rem;'>Toque em uma reclamação para ver os detalhes</p>", unsafe_allow_html=True)

        if not st.session_state.minhas_reclamacoes:
            st.markdown('<div class="card" style="text-align:center;padding:30px;"><div style="font-size:2.5rem;">📭</div><p style="color:#64748b;margin-top:10px;">Nenhuma reclamação registrada ainda.</p></div>', unsafe_allow_html=True)
        else:
            for i, rec in enumerate(reversed(st.session_state.minhas_reclamacoes)):
                idx_real = len(st.session_state.minhas_reclamacoes) - 1 - i
                cor = "#f59e0b" if rec['status']=="Em Análise" else "#10b981" if rec['status']=="Concluído" else "#1a56db"
                grupo_curto = rec.get('grupo','').split("(")[0].strip()
                tem_resposta = "💬" if rec.get('resposta') else ""

                st.markdown(f"""
                <div class="card card-clicavel">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="color:#1a56db;font-weight:900;font-size:.95rem;">{rec['protocolo']}</span>
                        <span class="status-badge" style="background:{cor};">{rec['status']}</span>
                    </div>
                    <div style="color:#334155;font-size:.88rem;font-weight:700;">🚌 Linha <b>{rec['linha']}</b> {tem_resposta}</div>
                    <div style="color:#64748b;font-size:.78rem;font-weight:700;margin-top:2px;">{grupo_curto}</div>
                    <div style="color:#94a3b8;font-size:.8rem;font-weight:700;margin-top:4px;">{rec['cat']} &nbsp;·&nbsp; 📅 {rec['data']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Ver detalhes →", key=f"det_{idx_real}"):
                    st.session_state.rec_detalhe = idx_real
                    st.rerun()

# ════════════════════════════════════════════════════════
# BARRA DE NAVEGAÇÃO INFERIOR
# ════════════════════════════════════════════════════════
def nav_class(nome):
    return "nav-ativo" if aba == nome else ""

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="{nav_class("reclamacao")}">', unsafe_allow_html=True)
    if st.button("📝\nReclamar", key="nav_rec", use_container_width=True):
        st.session_state.aba_ativa = "reclamacao"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="{nav_class("forum")}">', unsafe_allow_html=True)
    if st.button("💬\nFórum", key="nav_for", use_container_width=True):
        st.session_state.aba_ativa = "forum"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="{nav_class("minhas")}">', unsafe_allow_html=True)
    if st.button("🔍\nMeus Chamados", key="nav_min", use_container_width=True):
        st.session_state.aba_ativa = "minhas"
        st.session_state.rec_detalhe = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
