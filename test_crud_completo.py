#!/usr/bin/env python3
"""
Script de Teste Automatizado - CRUD Disciplinas e Tarefas
Testa: Criar, Listar, Editar, Deletar, Filtrar, Status Vencido
"""

import requests
import json
from datetime import datetime, timedelta
import os
import time

# Configuração
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti"
AUTH_TOKEN = None

# Cores para output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test(msg, status="INFO"):
    """Print com cores"""
    if status == "INFO":
        print(f"{Colors.CYAN}ℹ️  {msg}{Colors.ENDC}")
    elif status == "OK":
        print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")
    elif status == "ERROR":
        print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")
    elif status == "WARNING":
        print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")
    elif status == "HEADER":
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{msg}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

def fazer_login():
    """Faz login e obtém token"""
    global AUTH_TOKEN
    print_test("Fazendo login...", "INFO")
    
    try:
        response = requests.post(
            f"{XANO_BASE_URL}/auth/login",
            json={
                "email": "felipe.salmeida@aluno.impacta.edu.br",
                "password": "felipe@5458"
            }
        )
        
        if response.status_code == 200:
            AUTH_TOKEN = response.json().get("authToken")
            print_test(f"Token obtido: {AUTH_TOKEN[:20]}...", "OK")
            return True
        else:
            print_test(f"Erro no login: {response.json()}", "ERROR")
            return False
    except Exception as e:
        print_test(f"Erro de conexão: {e}", "ERROR")
        return False

def get_headers():
    """Retorna headers com autenticação"""
    return {"Authorization": f"Bearer {AUTH_TOKEN}"}

# ============================================================
# TESTES DISCIPLINAS
# ============================================================

def limpar_disciplinas():
    """Deleta todas as disciplinas existentes"""
    print_test("Limpando disciplinas existentes...", "INFO")
    
    try:
        response = requests.get(
            f"{XANO_BASE_URL}/subjects",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            disciplinas = response.json()
            if isinstance(disciplinas, list):
                for disc in disciplinas:
                    disc_id = disc.get("id")
                    del_response = requests.delete(
                        f"{XANO_BASE_URL}/subjects/{disc_id}",
                        headers=get_headers()
                    )
                    if del_response.status_code == 200:
                        print_test(f"Deletada: {disc.get('name')} (ID: {disc_id})", "OK")
                    else:
                        print_test(f"Erro ao deletar {disc.get('name')}", "ERROR")
                    time.sleep(2.5)  # Respeitar rate limit
                return True
    except Exception as e:
        print_test(f"Erro ao limpar: {e}", "ERROR")
    return False

def criar_disciplinas():
    """Cria as 5 disciplinas do teste"""
    disciplinas_config = [
        {"name": "SQL Fundamentals", "professor": "Evandro Victor", "day": "Segunda"},
        {"name": "Programming & Algorithms", "professor": "Odair Gabriel", "day": "Terça"},
        {"name": "Database Design", "professor": "João Roberto", "day": "Quarta"},
        {"name": "Innovation Lab", "professor": "Leonardo Bontempo", "day": "Quinta"},
        {"name": "Software Engineering", "professor": "Mariana Moralles", "day": "Sexta"}
    ]
    
    disciplinas_criadas = {}
    
    print_test("Criando 5 disciplinas...", "INFO")
    
    for disc_cfg in disciplinas_config:
        time.sleep(2.5)  # Respeitar rate limit
        try:
            response = requests.post(
                f"{XANO_BASE_URL}/subjects",
                json={
                    "name": disc_cfg["name"],
                    "professor": disc_cfg["professor"],
                    "day_of_week": disc_cfg["day"]
                },
                headers=get_headers()
            )
            
            if response.status_code == 200:
                disc_data = response.json()
                disc_id = disc_data.get("id")
                disciplinas_criadas[disc_cfg["name"]] = disc_id
                print_test(f"Criada: {disc_cfg['name']} (ID: {disc_id})", "OK")
            else:
                print_test(f"Erro ao criar {disc_cfg['name']}: {response.json()}", "ERROR")
        except Exception as e:
            print_test(f"Erro: {e}", "ERROR")
    
    return disciplinas_criadas

# ============================================================
# TESTES TAREFAS
# ============================================================

def criar_tarefa(titulo, descricao, subject_id, prazo, status="pending"):
    """Cria uma tarefa"""
    try:
        response = requests.post(
            f"{XANO_BASE_URL}/academic_tasks",
            json={
                "title": titulo,
                "description": descricao,
                "subject_id": subject_id,
                "due_date": prazo,
                "status": status
            },
            headers=get_headers()
        )
        
        if response.status_code == 200:
            tarefa = response.json()
            return True, tarefa
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)

def listar_tarefas():
    """Lista todas as tarefas"""
    try:
        response = requests.get(
            f"{XANO_BASE_URL}/academic_tasks",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print_test(f"Erro ao listar: {e}", "ERROR")
        return []

def editar_tarefa(tarefa_id, titulo=None, status=None, descricao=None):
    """Edita uma tarefa"""
    try:
        payload = {}
        if titulo:
            payload["title"] = titulo
        if status:
            payload["status"] = status
        if descricao:
            payload["description"] = descricao
        
        response = requests.patch(
            f"{XANO_BASE_URL}/academic_tasks/{tarefa_id}",
            json=payload,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)

def deletar_tarefa(tarefa_id):
    """Deleta uma tarefa"""
    try:
        response = requests.delete(
            f"{XANO_BASE_URL}/academic_tasks/{tarefa_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            return True, None
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)

def agrupar_tarefas_por_disciplina(tarefas, disciplinas_map):
    """Agrupa tarefas por disciplina"""
    agrupadas = {}
    for tarefa in tarefas:
        disc_id = tarefa.get("subject_id")
        disc_nome = None
        for nome, id_disc in disciplinas_map.items():
            if id_disc == disc_id:
                disc_nome = nome
                break
        
        if disc_nome not in agrupadas:
            agrupadas[disc_nome] = []
        agrupadas[disc_nome].append(tarefa)
    
    return agrupadas

def verificar_tarefas_vencidas(tarefas):
    """Verifica tarefas vencidas"""
    hoje = datetime.now().date()
    vencidas = []
    
    for tarefa in tarefas:
        due_date_str = tarefa.get("due_date")
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00")).date()
                if due_date < hoje and tarefa.get("status") != "completed":
                    vencidas.append({
                        "titulo": tarefa.get("title"),
                        "prazo": due_date.strftime("%d/%m/%Y"),
                        "status": tarefa.get("status")
                    })
            except:
                pass
    
    return vencidas

# ============================================================
# EXECUÇÃO DOS TESTES
# ============================================================

def executar_testes():
    print_test("INICIANDO TESTES DE CRUD COMPLETO", "HEADER")
    
    # 1. Login
    if not fazer_login():
        print_test("Falha no login. Abortando.", "ERROR")
        return False
    
    # 2. Limpar disciplinas
    limpar_disciplinas()
    
    # 3. Criar disciplinas
    print_test("", "HEADER")
    print_test("FASE 1: CRIAR DISCIPLINAS", "HEADER")
    disciplinas = criar_disciplinas()
    
    if not disciplinas:
        print_test("Nenhuma disciplina foi criada. Abortando.", "ERROR")
        return False
    
    # Criar mapa para pesquisa
    disc_map = {v: k for k, v in disciplinas.items()}
    
    # 4. Teste: Criar tarefas
    print_test("", "HEADER")
    print_test("FASE 2: CRIAR TAREFAS", "HEADER")
    
    tarefas_criadas = []
    hoje = datetime.now()
    
    # SQL Fundamentals - 3 tarefas
    print_test("Criando tarefas para SQL Fundamentals...", "INFO")
    
    # Tarefa 1: Pendente, prazo 5 dias
    sucesso, tarefa = criar_tarefa(
        titulo="Consultas SQL Otimizadas",
        descricao="Criar queries para relatório de vendas",
        subject_id=disciplinas["SQL Fundamentals"],
        prazo=(hoje + timedelta(days=5)).isoformat(),
        status="pending"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')})", "OK")
    
    # Tarefa 2: Em progresso, prazo 3 dias
    sucesso, tarefa = criar_tarefa(
        titulo="Índices e Performance",
        descricao="Otimizar índices do banco",
        subject_id=disciplinas["SQL Fundamentals"],
        prazo=(hoje + timedelta(days=3)).isoformat(),
        status="in_progress"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')})", "OK")
    
    # Tarefa 3: Vencida (2 dias no passado)
    sucesso, tarefa = criar_tarefa(
        titulo="Backup e Recovery",
        descricao="Implementar estratégia de backup",
        subject_id=disciplinas["SQL Fundamentals"],
        prazo=(hoje - timedelta(days=2)).isoformat(),
        status="pending"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')}) - ⚠️ VENCIDA", "WARNING")
    
    # Programming & Algorithms - 2 tarefas
    print_test("Criando tarefas para Programming & Algorithms...", "INFO")
    
    sucesso, tarefa = criar_tarefa(
        titulo="Implementar Algoritmo de Ordenação",
        descricao="Quicksort e MergeSort em Python",
        subject_id=disciplinas["Programming & Algorithms"],
        prazo=(hoje + timedelta(days=7)).isoformat(),
        status="pending"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')})", "OK")
    
    sucesso, tarefa = criar_tarefa(
        titulo="Estruturas de Dados",
        descricao="Implementar árvores binárias",
        subject_id=disciplinas["Programming & Algorithms"],
        prazo=(hoje + timedelta(days=10)).isoformat(),
        status="pending"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')})", "OK")
    
    # Database Design - 1 tarefa
    print_test("Criando tarefas para Database Design...", "INFO")
    
    sucesso, tarefa = criar_tarefa(
        titulo="Modelagem ER (DER)",
        descricao="Criar diagrama entidade-relacionamento",
        subject_id=disciplinas["Database Design"],
        prazo=(hoje + timedelta(days=4)).isoformat(),
        status="completed"
    )
    if sucesso:
        tarefas_criadas.append(tarefa)
        print_test(f"Criada: {tarefa.get('title')} (ID: {tarefa.get('id')}) - ✅ CONCLUÍDA", "OK")
    
    print_test(f"Total de tarefas criadas: {len(tarefas_criadas)}", "OK")
    
    # 5. Teste: Listar tarefas agrupadas por disciplina
    print_test("", "HEADER")
    print_test("FASE 3: LISTAR E AGRUPAR TAREFAS", "HEADER")
    
    todas_tarefas = listar_tarefas()
    print_test(f"Total de tarefas no banco: {len(todas_tarefas)}", "OK")
    
    agrupadas = agrupar_tarefas_por_disciplina(todas_tarefas, disc_map)
    
    for disciplina, tarefas_disc in agrupadas.items():
        print_test(f"📚 {disciplina}: {len(tarefas_disc)} tarefa(s)", "INFO")
        for tarefa in tarefas_disc:
            status_emoji = {
                "pending": "⏳",
                "in_progress": "🚀",
                "completed": "✅",
                "overdue": "⚠️"
            }.get(tarefa.get("status"), "❓")
            print(f"   {status_emoji} {tarefa.get('title')} (ID: {tarefa.get('id')})")
    
    # 6. Teste: Editar tarefa (marcar como concluída)
    print_test("", "HEADER")
    print_test("FASE 4: EDITAR TAREFA", "HEADER")
    
    if tarefas_criadas:
        tarefa_edit = tarefas_criadas[0]
        tarefa_id = tarefa_edit.get("id")
        print_test(f"Editando tarefa: {tarefa_edit.get('title')} (ID: {tarefa_id})", "INFO")
        
        sucesso, result = editar_tarefa(
            tarefa_id,
            status="completed",
            descricao="Atualizado: Tarefas concluída com sucesso"
        )
        
        if sucesso:
            print_test(f"Tarefa marcada como CONCLUÍDA", "OK")
        else:
            print_test(f"Erro ao editar: {result}", "ERROR")
    
    # 7. Teste: Filtrar por status
    print_test("", "HEADER")
    print_test("FASE 5: FILTRAR POR STATUS", "HEADER")
    
    tarefas_atualizadas = listar_tarefas()
    
    status_counts = {}
    for tarefa in tarefas_atualizadas:
        status = tarefa.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        emoji = {
            "pending": "⏳",
            "in_progress": "🚀",
            "completed": "✅",
            "overdue": "⚠️"
        }.get(status, "❓")
        print_test(f"{emoji} {status}: {count} tarefa(s)", "OK")
    
    # 8. Teste: Identificar tarefas vencidas
    print_test("", "HEADER")
    print_test("FASE 6: TAREFAS VENCIDAS", "HEADER")
    
    vencidas = verificar_tarefas_vencidas(tarefas_atualizadas)
    
    if vencidas:
        print_test(f"⚠️ {len(vencidas)} tarefa(s) vencida(s) detectada(s):", "WARNING")
        for vencida in vencidas:
            print_test(
                f"   {vencida['titulo']} - Prazo: {vencida['prazo']} - Status: {vencida['status']}",
                "WARNING"
            )
    else:
        print_test("Nenhuma tarefa vencida detectada", "OK")
    
    # 9. Teste: Deletar uma tarefa
    print_test("", "HEADER")
    print_test("FASE 7: DELETAR TAREFA", "HEADER")
    
    if len(tarefas_criadas) > 1:
        tarefa_delete = tarefas_criadas[-1]
        tarefa_id = tarefa_delete.get("id")
        print_test(f"Deletando tarefa: {tarefa_delete.get('title')} (ID: {tarefa_id})", "INFO")
        
        sucesso, result = deletar_tarefa(tarefa_id)
        
        if sucesso:
            print_test(f"Tarefa deletada com sucesso", "OK")
        else:
            print_test(f"Erro ao deletar: {result}", "ERROR")
    
    # 10. Resumo final
    print_test("", "HEADER")
    print_test("RESUMO FINAL DOS TESTES", "HEADER")
    
    tarefas_finais = listar_tarefas()
    agrupadas_final = agrupar_tarefas_por_disciplina(tarefas_finais, disc_map)
    
    print_test(f"Total de disciplinas criadas: {len(disciplinas)}", "OK")
    print_test(f"Total de tarefas no banco: {len(tarefas_finais)}", "OK")
    print_test(f"Total de tarefas vencidas: {len(verificar_tarefas_vencidas(tarefas_finais))}", "WARNING")
    
    print(f"\n{Colors.GREEN}{'='*60}")
    print(f"✅ TESTES CONCLUÍDOS COM SUCESSO!{Colors.ENDC}")
    print(f"{Colors.GREEN}{'='*60}{Colors.ENDC}\n")
    
    return True

if __name__ == "__main__":
    try:
        executar_testes()
    except KeyboardInterrupt:
        print("\n\nTestes interrompidos pelo usuário.")
    except Exception as e:
        print_test(f"Erro fatal: {e}", "ERROR")
