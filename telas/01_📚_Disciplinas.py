import streamlit as st
import requests
import os
import pandas as pd

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")

# ---------------------------------------------------------
# FUNÇÕES DE API - CRUD COMPLETO
# ---------------------------------------------------------
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

def criar_disciplina(nome, professor, dia, semestre="", sala="", horario=""):
    """Cria uma nova disciplina"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {"name": nome, "professor": professor, "day_of_week": dia, "semester": semestre, "room": sala, "schedule": horario}
        response = requests.post(api_url, json=payload, headers=headers)
        return response.status_code == 200, response.json() if response.text else None
    except Exception as e:
        return False, str(e)

def atualizar_disciplina(disciplina_id, nome, professor, dia, semestre="", sala="", horario=""):
    """Atualiza uma disciplina existente"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects/{disciplina_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {"name": nome, "professor": professor, "day_of_week": dia, "semester": semestre, "room": sala, "schedule": horario}
        response = requests.patch(api_url, json=payload, headers=headers)
        return response.status_code == 200, response.json() if response.text else None
    except Exception as e:
        return False, str(e)

def arquivar_disciplina(disciplina_id, arquivar=True):
    """Arquiva ou reativa uma disciplina"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects/{disciplina_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {"status": "archived" if arquivar else "active"}
        response = requests.patch(api_url, json=payload, headers=headers)
        return response.status_code == 200, response.json() if response.text else None
    except Exception as e:
        return False, str(e)

def deletar_disciplina(disciplina_id):
    """Deleta uma disciplina"""
    try:
        api_url = f"{XANO_BASE_URL}/subjects/{disciplina_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.delete(api_url, headers=headers)
        return response.status_code == 200, None
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------
# PÁGINA PRINCIPAL
# ---------------------------------------------------------
st.title("📚 Gerenciar Disciplinas")
st.markdown("Sistema completo de CRUD para suas disciplinas integrado com Xano")

# Abas de navegação
tab1, tab2, tab3 = st.tabs(["📋 Listar & Editar", "➕ Criar Nova", "🔍 Filtros"])

# ---------------------------------------------------------
# ABA 1: LISTAR E EDITAR DISCIPLINAS
# ---------------------------------------------------------
with tab1:
    st.subheader("Suas Disciplinas")
    
    # Buscar disciplinas
    disciplinas = buscar_disciplinas()
    
    if not disciplinas:
        st.info("Nenhuma disciplina encontrada. Crie uma nova usando a aba 'Criar Nova'.")
    else:
        st.write(f"**Total de disciplinas:** {len(disciplinas)}")
        st.divider()
        
        # Exibir em formato de tabela com controles
        for disc in disciplinas:
            disc_id = disc.get("id")
            nome = disc.get("name", "N/A")
            prof = disc.get("professor", "N/A")
            dia = disc.get("day_of_week", "N/A")
            semestre = disc.get("semester", "N/A")
            sala = disc.get("room", "N/A")
            horario = disc.get("schedule", "N/A")
            status = disc.get("status", "active")
            
            # Container para cada disciplina
            with st.container(border=True):
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1.5, 1.5, 1.5, 1.5])
                
                col1.write(f"**📖 {nome}**")
                col2.write(f"👨‍🏫 {prof}")
                col3.write(f"📅 {dia}")
                col4.write(f"📚 {semestre}")
                col5.write(f"🏫 {sala}")
                col6.write(f"🕒 {horario}")
                
                # Status badge and metadata
                if status == "archived":
                    st.caption("📦 ARQUIVADA")
                else:
                    st.caption("✅ ATIVA")
                
                col_meta1, col_meta2 = st.columns([2, 1])
                col_meta1.write(f"ID: `{disc_id}`")
                col_meta2.write("")
                
                # Botões de ação
                btn1, btn2, btn3 = st.columns(3)
                if btn1.button("✏️ Editar", key=f"edit_btn_{disc_id}", use_container_width=True):
                    st.session_state[f"edit_mode_{disc_id}"] = True
                
                if status == "active":
                    if btn2.button("📦 Arquivar", key=f"archive_btn_{disc_id}", use_container_width=True):
                        st.session_state[f"confirm_archive_{disc_id}"] = True
                else:
                    if btn2.button("🔄 Reativar", key=f"reactivate_btn_{disc_id}", use_container_width=True):
                        st.session_state[f"confirm_reactivate_{disc_id}"] = True
                
                if btn3.button("🗑️ Deletar", key=f"delete_btn_{disc_id}", use_container_width=True, type="secondary"):
                    st.session_state[f"confirm_delete_{disc_id}"] = True
                
                # Modal de edição
                if st.session_state.get(f"edit_mode_{disc_id}", False):
                    st.divider()
                    st.write(f"### ✏️ Editando: {nome}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        novo_nome = st.text_input("Nome", value=nome, key=f"edit_nome_{disc_id}")
                    with col2:
                        novo_prof = st.text_input("Professor", value=prof, key=f"edit_prof_{disc_id}")
                    with col3:
                        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                        novo_dia = st.selectbox("Dia", dias, index=dias.index(dia) if dia in dias else 0, key=f"edit_dia_{disc_id}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        novo_semestre = st.text_input("Semestre", value=semestre if semestre != "N/A" else "", placeholder="Ex: 2024.1", key=f"edit_semestre_{disc_id}")
                    with col2:
                        novo_sala = st.text_input("Sala", value=sala if sala != "N/A" else "", placeholder="Ex: Sala 101", key=f"edit_sala_{disc_id}")
                    with col3:
                        novo_horario = st.text_input("Horário", value=horario if horario != "N/A" else "", placeholder="Ex: 08:00-10:00", key=f"edit_horario_{disc_id}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("💾 Salvar", key=f"save_{disc_id}", use_container_width=True, type="primary"):
                        if novo_nome and novo_prof and novo_dia:
                            sucesso, msg = atualizar_disciplina(disc_id, novo_nome, novo_prof, novo_dia, novo_semestre, novo_sala, novo_horario)
                            if sucesso:
                                st.success(f"✅ Disciplina '{novo_nome}' atualizada!")
                                st.session_state[f"edit_mode_{disc_id}"] = False
                                st.rerun()
                            else:
                                st.error(f"❌ Erro: {msg}")
                        else:
                            st.warning("⚠️ Preencha nome, professor e dia!")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_{disc_id}", use_container_width=True):
                        st.session_state[f"edit_mode_{disc_id}"] = False
                        st.rerun()
                
                # Modal de confirmação de arquivar
                if st.session_state.get(f"confirm_archive_{disc_id}", False):
                    st.warning(f"⚠️ Tem certeza que deseja arquivar '{nome}'? Ela ficará oculta mas poderá ser reativada depois.")
                    col1, col2 = st.columns(2)
                    
                    if col1.button("📦 Confirmar Arquivar", key=f"confirm_arc_{disc_id}", use_container_width=True, type="primary"):
                        sucesso, msg = arquivar_disciplina(disc_id, arquivar=True)
                        if sucesso:
                            st.success(f"✅ Disciplina '{nome}' arquivada!")
                            st.session_state[f"confirm_archive_{disc_id}"] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Erro: {msg}")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_arc_{disc_id}", use_container_width=True):
                        st.session_state[f"confirm_archive_{disc_id}"] = False
                        st.rerun()
                
                # Modal de confirmação de reativar
                if st.session_state.get(f"confirm_reactivate_{disc_id}", False):
                    st.info(f"🔄 Tem certeza que deseja reativar '{nome}'? Ela voltará a aparecer na lista ativa.")
                    col1, col2 = st.columns(2)
                    
                    if col1.button("🔄 Confirmar Reativar", key=f"confirm_reac_{disc_id}", use_container_width=True, type="primary"):
                        sucesso, msg = arquivar_disciplina(disc_id, arquivar=False)
                        if sucesso:
                            st.success(f"✅ Disciplina '{nome}' reativada!")
                            st.session_state[f"confirm_reactivate_{disc_id}"] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Erro: {msg}")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_reac_{disc_id}", use_container_width=True):
                        st.session_state[f"confirm_reactivate_{disc_id}"] = False
                        st.rerun()
                
                # Modal de confirmação de deleção
                if st.session_state.get(f"confirm_delete_{disc_id}", False):
                    st.warning(f"⚠️ Tem certeza que deseja deletar '{nome}'? Esta ação é irreversível.")
                    col1, col2 = st.columns(2)
                    
                    if col1.button("🗑️ Confirmar Deleção", key=f"confirm_del_{disc_id}", use_container_width=True, type="primary"):
                        sucesso, msg = deletar_disciplina(disc_id)
                        if sucesso:
                            st.success(f"✅ Disciplina '{nome}' deletada!")
                            st.session_state[f"confirm_delete_{disc_id}"] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Erro: {msg}")
                    
                    if col2.button("❌ Cancelar", key=f"cancel_del_{disc_id}", use_container_width=True):
                        st.session_state[f"confirm_delete_{disc_id}"] = False
                        st.rerun()

# ---------------------------------------------------------
# ABA 2: CRIAR NOVA DISCIPLINA
# ---------------------------------------------------------
with tab2:
    st.subheader("Criar Nova Disciplina")
    st.markdown("Preencha os campos abaixo para adicionar uma nova disciplina ao seu cronograma.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        novo_nome = st.text_input("📖 Nome da Disciplina", placeholder="Ex: Python Avançado")
        novo_prof = st.text_input("👨‍🏫 Professor(a)", placeholder="Ex: João Silva")
    
    with col2:
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        novo_dia = st.selectbox("📅 Dia da Semana", dias)
        novo_semestre = st.text_input("📚 Semestre", placeholder="Ex: 2024.1")
    
    with col3:
        novo_sala = st.text_input("🏫 Sala", placeholder="Ex: Sala 101")
        novo_horario = st.text_input("🕒 Horário", placeholder="Ex: 08:00-10:00")
    
    if st.button("✅ Criar Disciplina", type="primary", use_container_width=True):
        if novo_nome and novo_prof and novo_dia:
            sucesso, msg = criar_disciplina(novo_nome, novo_prof, novo_dia, novo_semestre, novo_sala, novo_horario)
            if sucesso:
                st.success(f"✅ Disciplina '{novo_nome}' criada com sucesso!")
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ Erro ao criar: {msg}")
        else:
            st.warning("⚠️ Preencha nome, professor e dia!")

# ---------------------------------------------------------
# ABA 3: FILTROS E BUSCA
# ---------------------------------------------------------
with tab3:
    st.subheader("Filtros e Busca Avançada")
    st.markdown("Filtre suas disciplinas por diferentes critérios")
    
    disciplinas_all = buscar_disciplinas()
    
    if disciplinas_all:
        # Busca por nome
        busca_nome = st.text_input("🔍 Buscar por nome de disciplina:")
        
        # Filtros por dia, professor e status
        col1, col2, col3 = st.columns(3)
        with col1:
            dias_unicos = ["Todos"] + sorted(list(set([d.get("day_of_week") for d in disciplinas_all if d.get("day_of_week")])))
            filtro_dia = st.selectbox("Filtrar por dia:", dias_unicos)
        
        with col2:
            profs_unicos = ["Todos"] + sorted(list(set([d.get("professor") for d in disciplinas_all if d.get("professor")])))
            filtro_prof = st.selectbox("Filtrar por professor:", profs_unicos)
        
        with col3:
            status_options = ["Todos", "active", "archived"]
            status_labels = {"Todos": "Todos", "active": "Ativas", "archived": "Arquivadas"}
            filtro_status = st.selectbox("Filtrar por status:", [status_labels[s] for s in status_options])
            filtro_status = [s for s in status_options if status_labels[s] == filtro_status][0]
        
        filtro_semestre = st.text_input("Filtrar por semestre:")
        
        # Aplicar filtros
        disciplinas_filtradas = disciplinas_all
        
        if busca_nome:
            disciplinas_filtradas = [d for d in disciplinas_filtradas if busca_nome.lower() in d.get("name", "").lower()]
        
        if filtro_dia != "Todos":
            disciplinas_filtradas = [d for d in disciplinas_filtradas if d.get("day_of_week") == filtro_dia]
        
        if filtro_prof != "Todos":
            disciplinas_filtradas = [d for d in disciplinas_filtradas if d.get("professor") == filtro_prof]
        
        if filtro_status != "Todos":
            disciplinas_filtradas = [d for d in disciplinas_filtradas if d.get("status", "active") == filtro_status]
        
        if filtro_semestre:
            disciplinas_filtradas = [d for d in disciplinas_filtradas if filtro_semestre.lower() in (d.get("semester", "")).lower()]
        
        # Exibir resultados
        st.write(f"**Total de resultados:** {len(disciplinas_filtradas)} / {len(disciplinas_all)}")
        st.divider()
        
        if disciplinas_filtradas:
            # Converter para DataFrame para exibição em tabela
            df_data = []
            for d in disciplinas_filtradas:
                df_data.append({
                    "ID": d.get("id"),
                    "Nome": d.get("name"),
                    "Professor": d.get("professor"),
                    "Dia": d.get("day_of_week"),
                    "Semestre": d.get("semester", "N/A"),
                    "Sala": d.get("room", "N/A"),
                    "Horário": d.get("schedule", "N/A"),
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma disciplina encontrada com os filtros selecionados.")
    else:
        st.info("Nenhuma disciplina disponível. Crie uma na aba 'Criar Nova'.")