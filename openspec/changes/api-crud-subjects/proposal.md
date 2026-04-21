# Change: api-crud-subjects

## Why
O frontend (Streamlit) precisa consumir dados de disciplinas de forma segura,
garantindo que cada usuário acesse apenas seus próprios dados.

## What Changes
- Criação dos endpoints CRUD para a tabela subjects:
  - POST /subjects - criar disciplina
  - GET /subjects - listar disciplinas do usuário
  - PATCH /subjects/{id} - atualizar disciplina
  - DELETE /subjects/{id} - deletar disciplina

## Impact
- Backend: novos endpoints no Xano com filtro por user_id
- Frontend: poderá consumir as APIs de disciplinas
