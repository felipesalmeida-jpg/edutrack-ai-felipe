import streamlit as st

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# ---------------------------------------------------------
# INTERFACE DA PÁGINA
# ---------------------------------------------------------
st.title("📝 Minhas Tarefas")

# Lista de disciplinas SEM a opção "Todas"
lista_disciplinas = [
    "Selecione",
    "Database Design",
    "Innovation Lab: Advanced No/Low Code",
    "Programming & Algorithms",
    "Software Engineering",
    "SQL Fundamentals"
]
# Status mantém a opção "Todas" para mostrar o progresso geral da matéria escolhida
lista_status = ["Selecione", "Todas", "Concluídas", "Pendentes"]

# Filtros Superiores
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    busca = st.text_input("Buscar tarefa...", placeholder="Ex: Streamlit")
with col2:
    filtro_disciplina = st.selectbox("Filtrar por Disciplina", lista_disciplinas, index=0)
with col3:
    status_filtro = st.selectbox("Status", lista_status, index=0)

st.markdown("---")

# ---------------------------------------------------------
# DADOS DAS TAREFAS
# ---------------------------------------------------------
disc_inno = "Innovation Lab: Advanced No/Low Code"

tarefas = [
    {"id": 1, "titulo": "Configuração do Ambiente", "disciplina": disc_inno, "prazo": "20/02/2026"},
    {"id": 2, "titulo": "Modelagem de Banco de Dados (DER)", "disciplina": disc_inno, "prazo": "25/02/2026"},
    {"id": 3, "titulo": "Criação de Tabelas SQL (DDL)", "disciplina": disc_inno, "prazo": "02/03/2026"},
    {"id": 4, "titulo": "Inserção de Dados (Sistema Restaurante)", "disciplina": disc_inno, "prazo": "05/03/2026"},
    {"id": 5, "titulo": "Consultas SQL Otimizadas", "disciplina": disc_inno, "prazo": "08/03/2026"},
    {"id": 6, "titulo": "Clone de Repositório e Branches (Git)", "disciplina": disc_inno, "prazo": "10/03/2026"},
    {"id": 7, "titulo": "Configuração Streamlit e GitHub Workflows", "disciplina": disc_inno, "prazo": "11/03/2026"},
    {"id": 8, "titulo": "Instalação de Dependências (npm/pip)", "disciplina": disc_inno, "prazo": "15/03/2026"},
    {"id": 9, "titulo": "Estruturação da Interface no Streamlit", "disciplina": disc_inno, "prazo": "20/03/2026"},
    {"id": 10, "titulo": "Conexão com API do Xano via Requests", "disciplina": disc_inno, "prazo": "25/03/2026"},
    {"id": 11, "titulo": "Sistema de Autenticação e Login", "disciplina": disc_inno, "prazo": "05/04/2026"},
    {"id": 12, "titulo": "Ocultar Menu Lateral com CSS/Navigation", "disciplina": disc_inno, "prazo": "15/04/2026"},
    {"id": 13, "titulo": "Bloqueio de Rotas", "disciplina": disc_inno, "prazo": "25/04/2026"},
    {"id": 14, "titulo": "Refatoração e Entrega Final", "disciplina": disc_inno, "prazo": "01/05/2026"},
]

# ---------------------------------------------------------
# MEMÓRIA PERMANENTE
# ---------------------------------------------------------
if "status_tarefas" not in st.session_state:
    st.session_state.status_tarefas = {t['id']: True for t in tarefas}

def atualizar_status(id_tarefa):
    st.session_state.status_tarefas[id_tarefa] = st.session_state[f"ui_check_{id_tarefa}"]

# ---------------------------------------------------------
# LÓGICA DE EXIBIÇÃO
# ---------------------------------------------------------

# REGRA: Se Disciplina ou Status forem "Selecione", a tela fica limpa.
if filtro_disciplina == "Selecione" or status_filtro == "Selecione":
    st.info("👆 **Selecione a disciplina e o status no filtro acima para ver suas tarefas.**")

else:
    tarefas_filtradas = []

    for t in tarefas:
        ta_concluida = st.session_state.status_tarefas[t['id']]

        # Aplica Filtro de Status
        if status_filtro == "Concluídas" and not ta_concluida:
            continue
        if status_filtro == "Pendentes" and ta_concluida:
            continue
            
        # Aplica Filtro de Busca
        if busca.lower() not in t["titulo"].lower() and busca != "":
            continue
            
        # Aplica Filtro de Disciplina (Agora apenas a comparação direta, sem 'Todas')
        if t["disciplina"] != filtro_disciplina:
            continue
            
        tarefas_filtradas.append(t)

    # Renderização
    if len(tarefas_filtradas) == 0:
        if status_filtro == "Pendentes":
            st.success(f"🎉 Nenhuma tarefa pendente para **{filtro_disciplina}**!")
        else:
            st.info("Nenhuma tarefa encontrada para esta seleção.")
    else:
        for t in tarefas_filtradas:
            ta_concluida = st.session_state.status_tarefas[t['id']]
            with st.expander(f"📌 Tarefa {t['id']:02d}: {t['titulo']}"):
                st.write(f"**Prazo:** {t['prazo']}")
                st.checkbox(
                    "✅ Concluída" if ta_concluida else "⏳ Marcar como Concluída",
                    value=ta_concluida,
                    key=f"ui_check_{t['id']}",
                    on_change=atualizar_status,
                    args=(t['id'],)
                )