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

# ---------------------------------------------------------
# FUNÇÕES DE API - CRUD COMPLETO PARA TAREFAS
# ---------------------------------------------------------
@st.cache_data(ttl=300)  # Cache por 5 minutos
def buscar_tarefas():
    """Busca todas as tarefas do Xano"""
    try:
        api_url = f"{XANO_BASE_URL}/academic_tasks"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            tarefas = response.json()
            return tarefas if isinstance(tarefas, list) else []
    except Exception as e:
        st.error(f"Erro ao buscar tarefas: {e}")
    return []

@st.cache_data(ttl=300)  # Cache por 5 minutos
def buscar_disciplinas():
    """Busca todas as disciplinas do Xano"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            disciplinas = response.json()
            return disciplinas if isinstance(disciplinas, list) else []
    except Exception as e:
        st.error(f"Erro ao buscar disciplinas: {e}")
    return []

def criar_tarefa(titulo, descricao, subject_id, due_date, status, prioridade="medium"):
    """Cria uma nova tarefa"""
    try:
        api_url = f"{XANO_BASE_URL}/academic_tasks"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {
            "title": titulo,
            "description": descricao,
            "subject_id": subject_id,
            "due_date": due_date.isoformat() if due_date else None,
            "status": status,
            "priority": prioridade
        }
        response = requests.post(api_url, json=payload, headers=headers)
        return response.status_code == 200, response.json() if response.text else None
    except Exception as e:
        return False, str(e)

def atualizar_tarefa(tarefa_id, titulo, descricao, subject_id, due_date, status, prioridade="medium"):
    """Atualiza uma tarefa existente"""
    try:
        api_url = f"{XANO_BASE_URL}/academic_tasks/{tarefa_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {
            "title": titulo,
            "description": descricao,
            "subject_id": subject_id,
            "due_date": due_date.isoformat() if due_date else None,
            "status": status,
            "priority": prioridade
        }
        response = requests.patch(api_url, json=payload, headers=headers)
        return response.status_code == 200, response.json() if response.text else None
    except Exception as e:
        return False, str(e)

def deletar_tarefa(tarefa_id):
    """Deleta uma tarefa"""
    try:
        api_url = f"{XANO_BASE_URL}/academic_tasks/{tarefa_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.delete(api_url, headers=headers)
        return response.status_code == 200, None
    except Exception as e:
        return False, str(e)

def obter_nome_disciplina(subject_id, disciplinas):
    """Obtém o nome de uma disciplina pelo ID"""
    for disc in disciplinas:
        if disc.get("id") == subject_id:
            return disc.get("name", "N/A")
    return "Sem disciplina"

def mapear_status_cor(status):
    """Retorna emoji/cor para status"""
    status_map = {
        "pending": ("⏳ Pendente", "blue"),
        "in_progress": ("🚀 Em Progresso", "orange"),
        "completed": ("✅ Concluída", "green"),
        "overdue": ("⚠️ Atrasada", "red")
    }
    return status_map.get(status, ("❓ Desconhecido", "gray"))


def status_label(status):
    return mapear_status_cor(status)[0]


def is_overdue(due_date):
    if not due_date:
        return False
    try:
        if isinstance(due_date, str):
            due_date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00")).date()
        elif isinstance(due_date, datetime):
            due_date_obj = due_date.date()
        else:
            due_date_obj = due_date
        return due_date_obj < datetime.now().date()
    except Exception:
        return False

# ---------------------------------------------------------
# PÁGINA PRINCIPAL
# ---------------------------------------------------------
st.title("📝 Gerenciar Tarefas Acadêmicas")
st.markdown("Sistema completo de CRUD para suas tarefas integrado com Xano")

# Abas de navegação
tab1, tab2, tab3 = st.tabs(["📋 Listar & Editar", "➕ Criar Nova", "🔍 Filtros"])

# ---------------------------------------------------------
# ABA 1: LISTAR E EDITAR TAREFAS
# ---------------------------------------------------------
with tab1:
    st.subheader("Suas Tarefas")
    
    # Buscar dados
    tarefas = buscar_tarefas()
    disciplinas = buscar_disciplinas()
    
    if not tarefas:
        st.info("Nenhuma tarefa encontrada. Crie uma nova usando a aba 'Criar Nova'.")
    else:
        st.write(f"**Total de tarefas:** {len(tarefas)}")
        st.divider()
        
        # Exibir em cards interativas
        for tarefa in tarefas:
            tarefa_id = tarefa.get("id")
            titulo = tarefa.get("title", "N/A")
            descricao = tarefa.get("description", "")
            status = tarefa.get("status", "pending")
            due_date = tarefa.get("due_date")
            subject_id = tarefa.get("subject_id")
            prioridade = tarefa.get("priority", "medium")
            
            status_emoji, status_cor = mapear_status_cor(status)
            nome_disc = obter_nome_disciplina(subject_id, disciplinas)
            prioridade_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(prioridade, "🟡")
            
            # Converter due_date se necessário
            if due_date:
                try:
                    if isinstance(due_date, str):
                        due_date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                    else:
                        due_date_obj = due_date
                    due_date_str = due_date_obj.strftime("%d/%m/%Y")
                except:
                    due_date_str = str(due_date)
            else:
                due_date_str = "Sem prazo"
            
            # Container para cada tarefa
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**📌 {titulo}**")
                    st.caption(f"📚 {nome_disc} • {due_date_str} • {prioridade_emoji} {prioridade.title()}")
                    if descricao:
                        st.caption(f"📄 {descricao[:100]}..." if len(descricao) > 100 else f"📄 {descricao}")
                    st.write(f"{status_emoji}")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_btn_{tarefa_id}", use_container_width=True):
                        st.session_state[f"edit_mode_{tarefa_id}"] = True
                    
                    if st.button("🗑️ Deletar", key=f"delete_btn_{tarefa_id}", use_container_width=True, type="secondary"):
                        st.session_state[f"confirm_delete_{tarefa_id}"] = True
                
                # Modal de edição
                if st.session_state.get(f"edit_mode_{tarefa_id}", False):
                    st.divider()
                    st.write(f"### ✏️ Editando: {titulo}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        novo_titulo = st.text_input("Título", value=titulo, key=f"edit_titulo_{tarefa_id}")
                        novo_descricao = st.text_area("Descrição", value=descricao or "", key=f"edit_desc_{tarefa_id}")
                    
                    with col2:
                        disciplinas_nomes = {d.get("id"): d.get("name") for d in disciplinas}
                        disciplinas_lista = list(disciplinas_nomes.values())
                        idx_disc = disciplinas_lista.index(nome_disc) if nome_disc in disciplinas_lista else 0
                        nova_disc_nome = st.selectbox("Disciplina", disciplinas_lista, index=idx_disc, key=f"edit_disc_{tarefa_id}")
                        nova_subject_id = [k for k, v in disciplinas_nomes.items() if v == nova_disc_nome][0]
                        
                        # Converter due_date para date object
                        if due_date:
                            try:
                                if isinstance(due_date, str):
                                    due_date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00")).date()
                                else:
                                    due_date_obj = due_date.date() if isinstance(due_date, datetime) else due_date
                            except:
                                due_date_obj = None
                        else:
                            due_date_obj = None
                        
                        nova_due_date = st.date_input("Prazo", value=due_date_obj, key=f"edit_due_{tarefa_id}")
                        novo_status = st.selectbox("Status", ["pending", "in_progress", "completed", "overdue"], index=["pending", "in_progress", "completed", "overdue"].index(status), key=f"edit_status_{tarefa_id}")
                        nova_prioridade = st.selectbox("Prioridade", ["low", "medium", "high"], index=["low", "medium", "high"].index(prioridade), key=f"edit_prior_{tarefa_id}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("💾 Salvar", key=f"save_{tarefa_id}", use_container_width=True, type="primary"):
                        if novo_titulo and nova_disc_nome:
                            sucesso, msg = atualizar_tarefa(tarefa_id, novo_titulo, novo_descricao, nova_subject_id, nova_due_date, novo_status, nova_prioridade)
                            if sucesso:
                                st.success(f"✅ Tarefa '{novo_titulo}' atualizada!")
                                st.session_state[f"edit_mode_{tarefa_id}"] = False
                                st.rerun()
                            else:
                                st.error(f"❌ Erro: {msg}")
                        else:
                            st.warning("⚠️ Preencha título e disciplina!")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_{tarefa_id}", use_container_width=True):
                        st.session_state[f"edit_mode_{tarefa_id}"] = False
                        st.rerun()
                
                # Modal de confirmação de deleção
                if st.session_state.get(f"confirm_delete_{tarefa_id}", False):
                    st.warning(f"⚠️ Tem certeza que deseja deletar a tarefa '{titulo}'? Esta ação é irreversível.")
                    col1, col2 = st.columns(2)
                    
                    if col1.button("🗑️ Confirmar Deleção", key=f"confirm_del_{tarefa_id}", use_container_width=True, type="primary"):
                        sucesso, msg = deletar_tarefa(tarefa_id)
                        if sucesso:
                            st.success(f"✅ Tarefa '{titulo}' deletada!")
                            st.session_state[f"confirm_delete_{tarefa_id}"] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Erro: {msg}")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_del_{tarefa_id}", use_container_width=True):
                        st.session_state[f"confirm_delete_{tarefa_id}"] = False
                        st.rerun()

# ---------------------------------------------------------
# ABA 2: CRIAR NOVA TAREFA
# ---------------------------------------------------------
with tab2:
    st.subheader("Criar Nova Tarefa")
    st.markdown("Preencha os campos abaixo para adicionar uma nova tarefa ao seu cronograma.")
    
    disciplinas = buscar_disciplinas()
    disciplinas_nomes = {d.get("id"): d.get("name") for d in disciplinas}
    disciplinas_lista = list(disciplinas_nomes.values())
    
    col1, col2 = st.columns(2)
    
    with col1:
        novo_titulo = st.text_input("📌 Título da Tarefa", placeholder="Ex: Entregar Relatório SQL")
        novo_descricao = st.text_area("📄 Descrição (opcional)", placeholder="Adicione detalhes sobre a tarefa...")
    
    with col2:
        if disciplinas_lista:
            nova_disc_nome = st.selectbox("📚 Disciplina", disciplinas_lista)
            nova_subject_id = [k for k, v in disciplinas_nomes.items() if v == nova_disc_nome][0]
        else:
            st.warning("⚠️ Nenhuma disciplina encontrada. Crie uma primeiro na aba 'Disciplinas'.")
            nova_subject_id = None
        
        nova_due_date = st.date_input("📅 Prazo", value=datetime.now() + timedelta(days=7))
        novo_status = st.selectbox("🏷️ Status Inicial", ["pending", "in_progress", "completed", "overdue"])
        nova_prioridade = st.selectbox("🚨 Prioridade", ["low", "medium", "high"], index=1)
    
    if st.button("✅ Criar Tarefa", type="primary", use_container_width=True):
        if novo_titulo and nova_subject_id:
            sucesso, msg = criar_tarefa(novo_titulo, novo_descricao, nova_subject_id, nova_due_date, novo_status, nova_prioridade)
            if sucesso:
                st.success(f"✅ Tarefa '{novo_titulo}' criada com sucesso!")
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ Erro ao criar: {msg}")
        else:
            st.warning("⚠️ Preencha título e selecione uma disciplina!")

# ---------------------------------------------------------
# ABA 3: FILTROS E BUSCA
# ---------------------------------------------------------
with tab3:
    st.subheader("Filtros e Busca Avançada")
    st.markdown("Filtre suas tarefas por diferentes critérios")
    
    tarefas_all = buscar_tarefas()
    disciplinas = buscar_disciplinas()
    disciplinas_nomes = {d.get("id"): d.get("name") for d in disciplinas}
    
    if tarefas_all:
        # Busca por título
        busca_titulo = st.text_input("🔍 Buscar por título de tarefa:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filtro por disciplina
            disciplinas_lista = ["Todas"] + sorted(list(set([d.get("name") for d in disciplinas if d.get("name")])))
            filtro_disc = st.selectbox("Filtrar por disciplina:", disciplinas_lista)
        
        with col2:
            # Filtro por status
            status_labels = {
                "pending": "⏳ Pendente",
                "in_progress": "🚀 Em Progresso",
                "completed": "✅ Concluída",
                "overdue": "⚠️ Atrasada"
            }
            status_options = ["Todos"] + list(status_labels.values())
            filtro_status_label = st.selectbox("Filtrar por status:", status_options)
            filtro_status = [k for k, v in status_labels.items() if v == filtro_status_label][0] if filtro_status_label != "Todos" else "Todos"
        
        with col3:
            # Filtro por prioridade
            prioridade_options = ["Todas", "low", "medium", "high"]
            prioridade_labels = {"Todas": "Todas", "low": "Baixa", "medium": "Média", "high": "Alta"}
            filtro_prioridade_label = st.selectbox("Filtrar por prioridade:", [prioridade_labels[p] for p in prioridade_options])
            filtro_prioridade = [p for p in prioridade_options if prioridade_labels[p] == filtro_prioridade_label][0]
        
        filtro_prazo = st.selectbox("Filtrar por prazo:", ["Todos", "Próximos 7 dias", "Este mês", "Atrasadas"])
        
        # Aplicar filtros
        tarefas_filtradas = tarefas_all
        
        if busca_titulo:
            tarefas_filtradas = [t for t in tarefas_filtradas if busca_titulo.lower() in t.get("title", "").lower()]
        
        if filtro_disc != "Todas":
            disc_id = [k for k, v in disciplinas_nomes.items() if v == filtro_disc]
            if disc_id:
                tarefas_filtradas = [t for t in tarefas_filtradas if t.get("subject_id") == disc_id[0]]
        
        if filtro_status != "Todos":
            tarefas_filtradas = [t for t in tarefas_filtradas if t.get("status") == filtro_status]
        
        if filtro_prioridade != "Todas":
            tarefas_filtradas = [t for t in tarefas_filtradas if t.get("priority", "medium") == filtro_prioridade]
        
        if filtro_prazo != "Todos":
            hoje = datetime.now().date()
            if filtro_prazo == "Próximos 7 dias":
                tarefas_filtradas = [t for t in tarefas_filtradas if t.get("due_date") and datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00")).date() <= hoje + timedelta(days=7) and datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00")).date() >= hoje]
            elif filtro_prazo == "Este mês":
                tarefas_filtradas = [t for t in tarefas_filtradas if t.get("due_date") and datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00")).date().month == hoje.month]
            elif filtro_prazo == "Atrasadas":
                tarefas_filtradas = [t for t in tarefas_filtradas if t.get("due_date") and datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00")).date() < hoje]
        
        # Exibir resultados
        st.write(f"**Total de resultados:** {len(tarefas_filtradas)} / {len(tarefas_all)}")
        st.divider()
        
        if tarefas_filtradas:
            # Converter para DataFrame para exibição em tabela
            df_data = []
            for t in tarefas_filtradas:
                try:
                    if t.get("due_date"):
                        due_date_obj = datetime.fromisoformat(t.get("due_date").replace("Z", "+00:00"))
                        due_date_str = due_date_obj.strftime("%d/%m/%Y")
                    else:
                        due_date_str = "Sem prazo"
                except:
                    due_date_str = str(t.get("due_date", "Sem prazo"))
                
                status_emoji, _ = mapear_status_cor(t.get("status", "pending"))
                
                df_data.append({
                    "ID": t.get("id"),
                    "Título": t.get("title"),
                    "Disciplina": disciplinas_nomes.get(t.get("subject_id"), "N/A"),
                    "Status": status_emoji,
                    "Prazo": due_date_str,
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
    else:
        st.info("Nenhuma tarefa disponível. Crie uma na aba 'Criar Nova'.")