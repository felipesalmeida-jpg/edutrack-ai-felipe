import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

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
# FUNÇÕES DE API
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def buscar_disciplinas():
    try:
        api_url = f"{XANO_BASE_URL}/subjects"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        return response.json() if response.status_code == 200 else []
    except:
        return []

@st.cache_data(ttl=300)
def buscar_tarefas():
    try:
        api_url = f"{XANO_TASKS_BASE_URL}/academic_tasks"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            tarefas = response.json()
            if isinstance(tarefas, dict) and "items" in tarefas:
                return tarefas["items"]
            return tarefas if isinstance(tarefas, list) else []
        return []
    except:
        return []

# ---------------------------------------------------------
# FUNÇÕES DE EXPORTAÇÃO
# ---------------------------------------------------------
def exportar_csv_disciplinas(disciplinas):
    """Exporta disciplinas para CSV"""
    df = pd.DataFrame([{
        "ID": d.get("id"),
        "Nome": d.get("name"),
        "Professor": d.get("professor", "N/A"),
        "Dia da Semana": d.get("day_of_week", "N/A"),
        "Semestre": d.get("semester", "N/A"),
        "Status": d.get("status", "active"),
        "Criado em": d.get("created_at", "N/A")
    } for d in disciplinas])
    return df.to_csv(index=False).encode('utf-8')

def gerar_pdf_simples(titulo, linhas):
    """Gera um PDF simples em bytes usando apenas Python."""
    from io import BytesIO

    def escape_text(text):
        return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    content = "BT\n/F1 12 Tf\n50 770 Td\n"
    for linha in linhas:
        content += f"({escape_text(linha)}) Tj\n0 -14 Td\n"
    content += "ET\n"
    content_bytes = content.encode("latin-1", "replace")

    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    obj4 = b"4 0 obj\n<< /Length %d >>\nstream\n" % len(content_bytes) + content_bytes + b"\nendstream\nendobj\n"
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    objects = [obj1, obj2, obj3, obj4, obj5]
    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = []
    for obj in objects:
        offsets.append(buffer.tell())
        buffer.write(obj)

    xref_offset = buffer.tell()
    buffer.write(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin-1"))
    for offset in offsets:
        buffer.write(f"{offset:010d} 00000 n \n".encode("latin-1"))

    buffer.write(b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objects) + 1))
    buffer.write(f"startxref\n{xref_offset}\n%%%%EOF".encode("latin-1"))
    return buffer.getvalue()


def exportar_pdf_disciplinas(disciplinas):
    linhas = [
        "EduTrack AI - Disciplinas",
        "",
        "ID | Nome | Professor | Dia | Semestre | Status",
        "-----------------------------------------------------------"
    ]
    for d in disciplinas:
        linhas.append(
            f"{d.get('id')} | {d.get('name')} | {d.get('professor', 'N/A')} | {d.get('day_of_week', 'N/A')} | {d.get('semester', 'N/A')} | {d.get('status', 'active')}"
        )
    return gerar_pdf_simples("Relatório de Disciplinas", linhas)


def exportar_pdf_tarefas(tarefas, disciplinas_map):
    linhas = [
        "EduTrack AI - Tarefas",
        "",
        "ID | Título | Disciplina | Prioridade | Status | Prazo",
        "-----------------------------------------------------------"
    ]
    for t in tarefas:
        linhas.append(
            f"{t.get('id')} | {t.get('title')} | {disciplinas_map.get(t.get('subject_id'), 'N/A')} | {t.get('priority', 'medium')} | {t.get('status')} | {t.get('due_date', 'N/A')}"
        )
    return gerar_pdf_simples("Relatório de Tarefas", linhas)


def exportar_csv_tarefas(tarefas, disciplinas_map):
    """Exporta tarefas para CSV"""
    df = pd.DataFrame([{
        "ID": t.get("id"),
        "Título": t.get("title"),
        "Descrição": t.get("description", ""),
        "Disciplina": disciplinas_map.get(t.get("subject_id"), "N/A"),
        "Status": t.get("status"),
        "Prioridade": t.get("priority", "medium"),
        "Prazo": t.get("due_date"),
        "Criado em": t.get("created_at")
    } for t in tarefas])
    return df.to_csv(index=False).encode('utf-8')

# ---------------------------------------------------------
# ANÁLISES HISTÓRICAS
# ---------------------------------------------------------
def analisar_por_periodo(tarefas, periodo):
    """Analisa tarefas por período"""
    hoje = datetime.now().date()

    if periodo == "Última semana":
        inicio = hoje - timedelta(days=7)
    elif periodo == "Último mês":
        inicio = hoje - timedelta(days=30)
    elif periodo == "Últimos 3 meses":
        inicio = hoje - timedelta(days=90)
    else:
        inicio = hoje - timedelta(days=365)

    tarefas_periodo = []
    for tarefa in tarefas:
        if tarefa.get("created_at"):
            try:
                data_criacao = datetime.fromisoformat(tarefa.get("created_at").replace("Z", "+00:00")).date()
                if data_criacao >= inicio:
                    tarefas_periodo.append(tarefa)
            except:
                continue

    return tarefas_periodo

def evolucao_temporal(tarefas):
    """Cria dados para gráfico de evolução temporal"""
    dados = {}
    for tarefa in tarefas:
        if tarefa.get("created_at"):
            try:
                data = datetime.fromisoformat(tarefa.get("created_at").replace("Z", "+00:00")).date()
                mes_ano = data.strftime("%Y-%m")

                if mes_ano not in dados:
                    dados[mes_ano] = {"total": 0, "concluidas": 0}

                dados[mes_ano]["total"] += 1
                if tarefa.get("status") == "completed":
                    dados[mes_ano]["concluidas"] += 1
            except:
                continue

    return dados

# ---------------------------------------------------------
# PÁGINA PRINCIPAL - RELATÓRIOS
# ---------------------------------------------------------
st.title("📊 Relatórios e Análises")
st.markdown("Análise detalhada do seu progresso acadêmico")

# Buscar dados
disciplinas = buscar_disciplinas()
tarefas = buscar_tarefas()

disciplinas_map = {d.get("id"): d.get("name") for d in disciplinas}

# Abas de navegação
tab1, tab2, tab3 = st.tabs(["📈 Análises", "📅 Histórico", "💾 Exportar Dados"])

# ---------------------------------------------------------
# ABA 1: ANÁLISES
# ---------------------------------------------------------
with tab1:
    st.subheader("Análises de Progresso")

    if tarefas:
        # Distribuição por status
        status_counts = {}
        for tarefa in tarefas:
            status = tarefa.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Gráfico de pizza
        labels = []
        values = []
        colors = []

        status_config = {
            "completed": ("✅ Concluídas", "#28a745"),
            "pending": ("⏳ Pendentes", "#ffc107"),
            "in_progress": ("🚀 Em Progresso", "#17a2b8"),
            "overdue": ("⚠️ Atrasadas", "#dc3545")
        }

        for status, count in status_counts.items():
            config = status_config.get(status, ("❓ Desconhecido", "#6c757d"))
            labels.append(f"{config[0]} ({count})")
            values.append(count)

        df_status = pd.DataFrame({
            "Status": labels,
            "Quantidade": values
        }).set_index("Status")

        st.bar_chart(df_status)
        st.write("**Distribuição de Tarefas por Status**")

        # Estatísticas
        total = len(tarefas)
        concluidas = status_counts.get("completed", 0)
        taxa_conclusao = (concluidas / total * 100) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Tarefas", total)
        with col2:
            st.metric("Tarefas Concluídas", concluidas)
        with col3:
            st.metric("Taxa de Conclusão", f"{taxa_conclusao:.1f}%")
    else:
        st.info("Nenhuma tarefa encontrada para análise.")

# ---------------------------------------------------------
# ABA 2: HISTÓRICO
# ---------------------------------------------------------
with tab2:
    st.subheader("Histórico por Período")

    periodo = st.selectbox(
        "Selecione o período:",
        ["Última semana", "Último mês", "Últimos 3 meses", "Último ano"]
    )

    tarefas_periodo = analisar_por_periodo(tarefas, periodo)

    if tarefas_periodo:
        st.write(f"**{len(tarefas_periodo)} tarefas criadas no período selecionado**")

        # Evolução temporal
        evolucao = evolucao_temporal(tarefas_periodo)

        if evolucao:
            meses = sorted(evolucao.keys())
            totais = [evolucao[m]["total"] for m in meses]
            concluidas = [evolucao[m]["concluidas"] for m in meses]

            df_evolucao = pd.DataFrame({
                "Criadas": totais,
                "Concluídas": concluidas
            }, index=meses)
            st.bar_chart(df_evolucao)
            st.write("**Evolução de Tarefas por Mês**")

        # Lista detalhada
        st.subheader("Tarefas do Período")
        for tarefa in sorted(tarefas_periodo, key=lambda x: x.get("created_at", ""), reverse=True):
            with st.expander(f"📝 {tarefa.get('title')}"):
                st.write(f"**Status:** {tarefa.get('status')}")
                st.write(f"**Disciplina:** {disciplinas_map.get(tarefa.get('subject_id'), 'N/A')}")
                if tarefa.get("description"):
                    st.write(f"**Descrição:** {tarefa.get('description')}")
                if tarefa.get("due_date"):
                    st.write(f"**Prazo:** {tarefa.get('due_date')[:10]}")
    else:
        st.info(f"Nenhuma tarefa encontrada no período '{periodo}'.")

# ---------------------------------------------------------
# ABA 3: EXPORTAR DADOS
# ---------------------------------------------------------
with tab3:
    st.subheader("Exportar Dados")

    st.markdown("Baixe seus dados em formato CSV para backup ou análise externa.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Disciplinas")
        if disciplinas:
            csv_disciplinas = exportar_csv_disciplinas(disciplinas)
            pdf_disciplinas = exportar_pdf_disciplinas(disciplinas)
            st.download_button(
                label="📥 Baixar Disciplinas (CSV)",
                data=csv_disciplinas,
                file_name="disciplinas_edutrack.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.download_button(
                label="📥 Baixar Disciplinas (PDF)",
                data=pdf_disciplinas,
                file_name="disciplinas_edutrack.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.write(f"**{len(disciplinas)} disciplinas** para exportar")
        else:
            st.info("Nenhuma disciplina para exportar.")

    with col2:
        st.subheader("📝 Tarefas")
        if tarefas:
            csv_tarefas = exportar_csv_tarefas(tarefas, disciplinas_map)
            pdf_tarefas = exportar_pdf_tarefas(tarefas, disciplinas_map)
            st.download_button(
                label="📥 Baixar Tarefas (CSV)",
                data=csv_tarefas,
                file_name="tarefas_edutrack.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.download_button(
                label="📥 Baixar Tarefas (PDF)",
                data=pdf_tarefas,
                file_name="tarefas_edutrack.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.write(f"**{len(tarefas)} tarefas** para exportar")
        else:
            st.info("Nenhuma tarefa para exportar.")

    st.divider()
    st.markdown("**💡 Dica:** Os arquivos CSV podem ser abertos no Excel, Google Sheets ou qualquer editor de planilhas para análise adicional.")