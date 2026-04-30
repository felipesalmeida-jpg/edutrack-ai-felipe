# Change: hybrid-search

## Why
Os usuários precisam buscar disciplinas por nome ou identificar disciplinas
com tarefas atrasadas, combinando consulta ao banco de dados com lógica Python.

## What Changes
- Criação do endpoint GET /subjects/search no Xano com filtro por nome
- Criação do script scripts/filter_overdue.py para filtrar tarefas atrasadas

## Impact
- Backend: novo endpoint de busca no Xano
- Python: novo script de filtragem por atraso
