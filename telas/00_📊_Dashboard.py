import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")
XANO_TASKS_BASE_URL = os.getenv("XANO_TASKS_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:Y3YwWHda")

# ---------------------------------------------------------
# FUNÇÕES DE API - REUTILIZANDO LÓGICA EXISTENTE
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def buscar_disciplinas():
    """Busca todas as disciplinas do usuário"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar disciplinas: {e}")
    return []

@st.cache_data(ttl=300)
def buscar_tarefas():
    """Busca todas as tarefas do usuário"""
    try:
        api_url = f"{XANO_TASKS_BASE_URL}/academic_tasks"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            tarefas = response.json()
            if isinstance(tarefas, dict) and "items" in tarefas:
                return tarefas["items"]
            return tarefas if isinstance(tarefas, list) else []
    except Exception as e:
        st.error(f"Erro ao buscar tarefas: {e}")
    return []

# ---------------------------------------------------------
# FUNÇÕES DE ANÁLISE DE DADOS
# ---------------------------------------------------------
def calcular_metricas(disciplinas, tarefas):
    """Calcula métricas principais do dashboard"""
    disciplinas_ativas = [d for d in disciplinas if d.get("status") != "archived"]
    total_disciplinas = len(disciplinas_ativas)
    disciplinas_arquivadas = len([d for d in disciplinas if d.get("status") == "archived"])

    tarefas_pendentes = [t for t in tarefas if t.get("status") == "pending"]
    tarefas_atrasadas = [t for t in tarefas if t.get("status") == "overdue" or
                        (t.get("due_date") and
                         datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00")).date() < datetime.now().date() and
                         t.get("status") != "completed")]

    tarefas_concluidas = [t for t in tarefas if t.get("status") == "completed"]
    total_tarefas = len(tarefas)

    progresso_geral = (len(tarefas_concluidas) / total_tarefas * 100) if total_tarefas > 0 else 0

    return {
        "total_disciplinas": total_disciplinas,
        "disciplinas_arquivadas": disciplinas_arquivadas,
        "tarefas_pendentes": len(tarefas_pendentes),
        "tarefas_atrasadas": len(tarefas_atrasadas),
        "progresso_geral": progresso_geral,
        "total_tarefas": total_tarefas
    }

def proximas_tarefas(tarefas, limite=5):
    """Retorna as próximas tarefas por prazo"""
    hoje = datetime.now().date()
    tarefas_com_prazo = []

    for tarefa in tarefas:
        if tarefa.get("due_date") and tarefa.get("status") != "completed":
            try:
                prazo = datetime.fromisoformat(tarefa.get("due_date").replace("Z", "+00:00")).date()
                if prazo >= hoje:
                    tarefas_com_prazo.append({
                        "titulo": tarefa.get("title"),
                        "prazo": prazo,
                        "dias_restantes": (prazo - hoje).days,
                        "status": tarefa.get("status")
                    })
            except:
                continue

    return sorted(tarefas_com_prazo, key=lambda x: x["prazo"])[:limite]

def progresso_por_disciplina(disciplinas, tarefas):
    """Calcula progresso por disciplina"""
    progresso = {}

    for disc in disciplinas:
        if disc.get("status") == "archived":
            continue

        disc_id = disc.get("id")
        disc_nome = disc.get("name", "N/A")

        tarefas_disc = [t for t in tarefas if t.get("subject_id") == disc_id]
        if tarefas_disc:
            concluidas = len([t for t in tarefas_disc if t.get("status") == "completed"])
            total = len(tarefas_disc)
            percentual = (concluidas / total * 100) if total > 0 else 0
            progresso[disc_nome] = {
                "concluidas": concluidas,
                "total": total,
                "percentual": percentual
            }

    return progresso

# ---------------------------------------------------------
# PÁGINA PRINCIPAL - DASHBOARD
# ---------------------------------------------------------
st.title("📊 Dashboard - EduTrack AI")
st.markdown("Bem-vindo! Aqui está uma visão geral do seu progresso acadêmico.")

# Buscar dados
disciplinas = buscar_disciplinas()
tarefas = buscar_tarefas()

# Calcular métricas
metricas = calcular_metricas(disciplinas, tarefas)

# ---------------------------------------------------------
# MÉTRICAS PRINCIPAIS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📚 Disciplinas Ativas",
        value=metricas["total_disciplinas"],
        help="Total de disciplinas cadastradas"
    )

with col2:
    st.metric(
        label="⏳ Tarefas Pendentes",
        value=metricas["tarefas_pendentes"],
        help="Tarefas ainda não concluídas"
    )

with col3:
    st.metric(
        label="⚠️ Tarefas em Atraso",
        value=metricas["tarefas_atrasadas"],
        delta=f"{metricas['tarefas_atrasadas']} atrasadas" if metricas["tarefas_atrasadas"] > 0 else None,
        delta_color="inverse" if metricas["tarefas_atrasadas"] > 0 else "normal",
        help="Tarefas com prazo vencido"
    )

with col4:
    st.metric(
        label="✅ Progresso Geral",
        value=f"{metricas['progresso_geral']:.1f}%",
        help=f"{len([t for t in tarefas if t.get('status') == 'completed'])} de {metricas['total_tarefas']} tarefas concluídas"
    )

if metricas.get("disciplinas_arquivadas", 0) > 0:
    st.info(f"📦 {metricas['disciplinas_arquivadas']} disciplinas arquivadas estão fora das contagens ativas.")
st.divider()

# ---------------------------------------------------------
# PRÓXIMAS TAREFAS
# ---------------------------------------------------------
st.subheader("📅 Próximas Tarefas")

proximas = proximas_tarefas(tarefas)

if proximas:
    for tarefa in proximas:
        dias = tarefa["dias_restantes"]
        cor = "🟢" if dias > 7 else "🟡" if dias > 0 else "🔴"

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{tarefa['titulo']}**")
                st.caption(f"{cor} Prazo: {tarefa['prazo'].strftime('%d/%m/%Y')} ({dias} dias)")
            with col2:
                status_emoji = {"pending": "⏳", "in_progress": "🚀", "overdue": "⚠️"}.get(tarefa["status"], "❓")
                st.write(f"{status_emoji} {tarefa['status'].replace('_', ' ').title()}")
else:
    st.info("🎉 Nenhuma tarefa pendente com prazo definido!")

st.divider()

# ---------------------------------------------------------
# PROGRESSO POR DISCIPLINA
# ---------------------------------------------------------
st.subheader("📈 Progresso por Disciplina")

progresso_disc = progresso_por_disciplina(disciplinas, tarefas)

if progresso_disc:
    disciplinas_nomes = list(progresso_disc.keys())
    percentuais = [progresso_disc[d]["percentual"] for d in disciplinas_nomes]

    df_prog = pd.DataFrame({
        "Disciplina": disciplinas_nomes,
        "Progresso": percentuais
    }).set_index("Disciplina")

    st.bar_chart(df_prog)
    st.write("**Percentual de Conclusão por Disciplina**")

    # Tabela detalhada
    st.subheader("Detalhes por Disciplina")
    dados_tabela = []
    for disc_nome, dados in progresso_disc.items():
        dados_tabela.append({
            "Disciplina": disc_nome,
            "Concluídas": dados["concluidas"],
            "Total": dados["total"],
            "Progresso": f"{dados['percentual']:.1f}%"
        })

    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma disciplina com tarefas cadastradas ainda.")

# ---------------------------------------------------------
# ATALHOS RÁPIDOS
# ---------------------------------------------------------
st.divider()
st.subheader("🚀 Ações Rápidas")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Nova Tarefa", use_container_width=True, type="primary"):
        st.switch_page("telas/02_📝_Tarefas.py")

with col2:
    if st.button("📚 Gerenciar Disciplinas", use_container_width=True):
        st.switch_page("telas/01_📚_Disciplinas.py")

with col3:
    if st.button("📊 Ver Relatórios", use_container_width=True):
        st.switch_page("telas/03_📊_Relatórios.py")