# Contexto do Sistema - EduTrack AI

## Visão Geral
Este projeto é um backend de gestão acadêmica construído usando XanoScript e Desenvolvimento Orientado por Especificações (OpenSpec).

## Propósito
Permitir que os usuários gerenciem seu ciclo de vida acadêmico, incluindo disciplinas, tarefas e cálculos de progresso.

## Core Entities
- **Users**: Gerenciados via autenticação nativa do Xano (JWT)[cite: 14].
- **Subjects**: Disciplinas acadêmicas pertencentes a cada usuário[cite: 10, 12].
- **Academic Tasks**: Tarefas (provas, lições, trabalhos) vinculadas a uma disciplina.

## Relationships
- **Users → Subjects**: Cada disciplina pertence a um único usuário (`subjects.user_id`)[cite: 10, 14].
- **Subjects → Academic Tasks**: Cada tarefa está vinculada a uma disciplina (`academic_tasks.subject_id`).

## Funcionalidades Implementadas
- **CRUD de Subjects**: Endpoints completos (POST, GET, PATCH, DELETE) com filtro obrigatório de `user_id`[cite: 14].
- **CRUD de Academic Tasks**: Gerenciamento de tarefas vinculadas a disciplinas[cite: 13].
- **Cálculo de Progresso**: Lógica híbrida usando Python para calcular a porcentagem de conclusão de disciplinas[cite: 14, 15].
- **Busca Avançada**: Filtro inteligente de disciplinas por nome ou status de tarefas atrasadas.

## Evolução Esperada
O sistema avançará para automações acadêmicas (notificações) e painéis analíticos detalhados na interface Streamlit.