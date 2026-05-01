# Change: api-crud-subjects

## Why
O frontend (Streamlit) precisa consumir dados de disciplinas de forma segura,
garantindo que cada usu�rio acesse apenas seus pr�prios dados.

## What Changes
- Cria��o dos endpoints CRUD para a tabela subjects:
  - POST /subjects - criar disciplina
  - GET /subjects - listar disciplinas do usu�rio
  - PATCH /subjects/{id} - atualizar disciplina
  - DELETE /subjects/{id} - deletar disciplina

## Impact
- Backend: novos endpoints no Xano com filtro por user_id
- Frontend: poder� consumir as APIs de disciplinas
