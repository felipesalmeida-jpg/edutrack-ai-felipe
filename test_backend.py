#!/usr/bin/env python
"""
Script de teste BACKEND - Cria disciplinas e tarefas via API Xano
"""
import os
import requests
import json
from datetime import datetime, timedelta

BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")
TASKS_BASE_URL = os.getenv("XANO_TASKS_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:Y3YwWHda")
TOKEN = os.getenv("XANO_AUTH_TOKEN", "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.OXHfof6B1aUgy_fblJ7EThNqsF3nTGZJ4sbgbiJUnGnxt9owZPghWaBibYsHUti8DbpP0BseZ_lrDDVR1X7ugUPxgCjPLwZv.TavsPUpe6DWDjz9VN-S14A.g1VGdmHEMtUNoFYD3UsF1NtJYa2w1F3Pu2ekty6hhxUZM1gK2Xo5A10Tfv2rcXIeVRrZQVocCYkWJ6POrfG6Uwek6m-W0JC-e1EOYCrJQutG9RFJuk_4ZjGibKsbfFmt3-4BRGiozP6Twd4p0pEXyUEGcxWJgnnHf-7WuRuRuFztk.FhpkNCyFM07bxo3a5xBBatlZCU_rgOnGxu_AH9H2y2k")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_backend():
    print("\n" + "="*80)
    print("TESTE BACKEND - Gestão de Disciplinas e Tarefas")
    print("="*80)
    
    # 1. CRIAR 3 DISCIPLINAS
    print("\n[1] CRIANDO 3 DISCIPLINAS...")
    disciplinas = []
    
    disciplinas_data = [
        {"name": "Cálculo I", "professor": "Dr. Silva", "day_of_week": "Segunda", "semester": "2024.1"},
        {"name": "Física Aplicada", "professor": "Dra. Costa", "day_of_week": "Quarta", "semester": "2024.1"},
        {"name": "Programação Python", "professor": "Prof. Oliveira", "day_of_week": "Sexta", "semester": "2024.1"},
    ]
    
    for i, disc_data in enumerate(disciplinas_data, 1):
        try:
            resp = requests.post(f"{BASE_URL}/subjects", json=disc_data, headers=HEADERS)
            if resp.status_code == 200:
                disc = resp.json()
                disciplinas.append(disc)
                print(f"   ✅ [{i}] '{disc_data['name']}' criada (ID: {disc.get('id')})")
            else:
                print(f"   ❌ [{i}] ERRO: {resp.status_code} - {resp.json().get('message', resp.text)}")
        except Exception as e:
            print(f"   ❌ [{i}] EXCEÇÃO: {e}")
    
    if not disciplinas:
        print("\n[ERRO] Nenhuma disciplina foi criada! Abortando testes de tarefas.")
        return
    
    # 2. CRIAR 3 TAREFAS (1 por disciplina)
    print("\n[2] CRIANDO 3 TAREFAS...")
    tarefas = []
    
    tarefas_data = [
        {"title": "Prova 1 - Cálculo", "description": "Capítulos 1-3", "subject_id": disciplinas[0].get('id'), "due_date": (datetime.now() + timedelta(days=7)).isoformat(), "priority": "high", "status": "pending"},
        {"title": "Trabalho Prático - Física", "description": "Experiência com pêndulo", "subject_id": disciplinas[1].get('id'), "due_date": (datetime.now() + timedelta(days=5)).isoformat(), "priority": "medium", "status": "pending"},
        {"title": "Projeto Final - Python", "description": "Sistema de gestão", "subject_id": disciplinas[2].get('id'), "due_date": (datetime.now() + timedelta(days=14)).isoformat(), "priority": "medium", "status": "pending"},
    ]
    
    for i, tarefa_data in enumerate(tarefas_data, 1):
        try:
            resp = requests.post(f"{TASKS_BASE_URL}/academic_tasks", json=tarefa_data, headers=HEADERS)
            if resp.status_code == 200:
                tarefa = resp.json()
                tarefas.append(tarefa)
                print(f"   ✅ [{i}] '{tarefa_data['title']}' criada (ID: {tarefa.get('id')})")
            else:
                print(f"   ❌ [{i}] ERRO: {resp.status_code} - {resp.json().get('message', resp.text)}")
        except Exception as e:
            print(f"   ❌ [{i}] EXCEÇÃO: {e}")
    
    # 3. LISTAR DISCIPLINAS
    print("\n[3] LISTANDO TODAS AS DISCIPLINAS...")
    try:
        resp = requests.get(f"{BASE_URL}/subjects", headers=HEADERS)
        if resp.status_code == 200:
            subjects_list = resp.json()
            print(f"   ✅ Total de disciplinas: {len(subjects_list)}")
            for subj in subjects_list:
                print(f"      - {subj.get('name')} (Prof: {subj.get('professor')}, Semestre: {subj.get('semester')})")
        else:
            print(f"   ❌ ERRO: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ EXCEÇÃO: {e}")
    
    # 4. LISTAR TAREFAS
    print("\n[4] LISTANDO TODAS AS TAREFAS...")
    try:
        resp = requests.get(f"{TASKS_BASE_URL}/academic_tasks", headers=HEADERS)
        if resp.status_code == 200:
            tasks_list = resp.json()
            print(f"   ✅ Total de tarefas: {len(tasks_list)}")
            for task in tasks_list:
                print(f"      - {task.get('title')} (Priority: {task.get('priority')}, Status: {task.get('status')})")
        else:
            print(f"   ❌ ERRO: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ EXCEÇÃO: {e}")
    
    # 5. EDITAR UMA DISCIPLINA
    if disciplinas:
        print("\n[5] EDITANDO DISCIPLINA...")
        disc_id = disciplinas[0].get('id')
        try:
            update_data = {"name": "Cálculo I - Revisado", "professor": "Dr. Silva (Atualizado)"}
            resp = requests.patch(f"{BASE_URL}/subjects/{disc_id}", json=update_data, headers=HEADERS)
            if resp.status_code == 200:
                print(f"   ✅ Disciplina ID {disc_id} editada com sucesso")
            else:
                print(f"   ❌ ERRO: {resp.status_code} - {resp.json().get('message', resp.text)}")
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {e}")
    
    # 6. EDITAR UMA TAREFA
    if tarefas:
        print("\n[6] EDITANDO TAREFA...")
        task_id = tarefas[0].get('id')
        try:
            update_data = {"status": "completed"}
            resp = requests.patch(f"{TASKS_BASE_URL}/academic_tasks/{task_id}", json=update_data, headers=HEADERS)
            if resp.status_code == 200:
                print(f"   ✅ Tarefa ID {task_id} marcada como concluída")
            else:
                print(f"   ❌ ERRO: {resp.status_code} - {resp.json().get('message', resp.text)}")
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {e}")
    
    # 7. DELETAR UMA TAREFA
    if len(tarefas) > 1:
        print("\n[7] DELETANDO TAREFA...")
        task_id = tarefas[1].get('id')
        try:
            resp = requests.delete(f"{TASKS_BASE_URL}/academic_tasks/{task_id}", headers=HEADERS)
            if resp.status_code == 200:
                print(f"   ✅ Tarefa ID {task_id} deletada com sucesso")
            else:
                print(f"   ❌ ERRO: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {e}")
    
    # 8. DELETAR UMA DISCIPLINA
    if len(disciplinas) > 1:
        print("\n[8] DELETANDO DISCIPLINA...")
        disc_id = disciplinas[1].get('id')
        try:
            resp = requests.delete(f"{BASE_URL}/subjects/{disc_id}", headers=HEADERS)
            if resp.status_code == 200:
                print(f"   ✅ Disciplina ID {disc_id} deletada com sucesso")
            else:
                print(f"   ❌ ERRO: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ EXCEÇÃO: {e}")
    
    print("\n" + "="*80)
    print("TESTE BACKEND CONCLUÍDO")
    print("="*80)

if __name__ == "__main__":
    test_backend()
