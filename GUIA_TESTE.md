# 🧪 Guia de Teste - CRUD Disciplinas e Tarefas

## ✅ Pré-requisitos

1. **Streamlit rodando** - `streamlit run app.py`
2. **Autenticado** - Login com suas credenciais
3. **Navegador** - http://localhost:8501

---

## 🧬 Teste 1: DISCIPLINAS (Criar, Editar, Deletar, Listar)

### 1.1 - Criar Disciplina
```
1. Barra lateral: Clique em "Disciplinas" (01_📚_Disciplinas)
2. Aba "Criar Nova"
3. Preencha:
   - Nome: "Análise de Dados"
   - Professor: "Carlos Santos"
   - Dia: "Terça"
4. Clique "✅ Criar Disciplina"
5. Aguarde sucesso ✅
6. Veja confete (balloons)
```

### 1.2 - Listar Disciplinas
```
1. Aba "Listar & Editar"
2. Deve ver a disciplina criada como card
3. Informações visíveis:
   - Nome: "Análise de Dados"
   - Professor: "Carlos Santos"
   - Dia: "Terça"
   - ID: número
4. Botões: ✏️ (Editar) e 🗑️ (Deletar)
```

### 1.3 - Editar Disciplina
```
1. Card da disciplina criada
2. Clique no botão ✏️
3. Modal aparece com campos preenchidos
4. Altere Professor para "Maria Silva"
5. Clique "💾 Salvar"
6. Sucesso: Modal fecha e lista atualiza
7. Veja o novo professor na listagem
```

### 1.4 - Deletar Disciplina
```
1. Card da disciplina editada
2. Clique no botão 🗑️
3. Modal de confirmação aparece
4. Clique "🗑️ Confirmar Deleção"
5. Sucesso: Disciplina desaparece da lista
6. Total de disciplinas diminui em 1
```

### 1.5 - Filtros
```
1. Aba "Filtros"
2. Teste cada filtro:
   a) Busca por Nome:
      - Digite "Python" → vê só disciplinas com "Python"
      - Digite "Análise" → vê só "Análise de Dados"
   b) Filtro por Dia:
      - Selecione "Terça" → vê só tarefas de terça
      - Selecione "Todos" → vê todas
   c) Filtro por Professor:
      - Selecione professor → vê só dele
      - Selecione "Todos" → vê todos
3. Verificar contadores de resultados
```

---

## 🧬 Teste 2: TAREFAS (Criar, Editar, Deletar, Listar)

### 2.1 - Criar Tarefa
```
1. Barra lateral: Clique em "Tarefas" (02_📝_Tarefas)
2. Aba "Criar Nova"
3. Preencha:
   - Título: "Análise de Vendas Q1"
   - Descrição: "Gerar relatório de análise de vendas"
   - Disciplina: "Análise de Dados" (ou outra existente)
   - Prazo: 20/03/2025 (ex.)
   - Status: "pending"
4. Clique "✅ Criar Tarefa"
5. Aguarde sucesso ✅
6. Veja confete (balloons)
```

### 2.2 - Listar Tarefas
```
1. Aba "Listar & Editar"
2. Deve ver a tarefa criada como card
3. Informações visíveis:
   - Título: "Análise de Vendas Q1"
   - Disciplina: "Análise de Dados"
   - Descrição resumida (primeiros 100 chars)
   - Status: "⏳ Pendente"
   - Prazo: "20/03/2025"
4. Botões: ✏️ (Editar) e 🗑️ (Deletar)
```

### 2.3 - Editar Tarefa
```
1. Card da tarefa criada
2. Clique no botão ✏️
3. Modal aparece com campos preenchidos
4. Altere Status para "in_progress"
5. Altere Prazo para 22/03/2025
6. Clique "💾 Salvar"
7. Sucesso: Modal fecha e lista atualiza
8. Veja o novo status "🚀 Em Progresso" no card
```

### 2.4 - Deletar Tarefa
```
1. Card da tarefa editada
2. Clique no botão 🗑️
3. Modal de confirmação aparece
4. Clique "🗑️ Confirmar Deleção"
5. Sucesso: Tarefa desaparece da lista
6. Total de tarefas diminui em 1
```

### 2.5 - Filtros
```
1. Aba "Filtros"
2. Teste cada filtro:
   a) Busca por Título:
      - Digite "Análise" → vê só tarefas com "Análise"
   b) Filtro por Disciplina:
      - Selecione "Análise de Dados" → vê só dessa
      - Selecione "Todas" → vê todas
   c) Filtro por Status:
      - Selecione "🚀 Em Progresso" → vê só em progresso
      - Selecione "Todos" → vê todos
   d) Filtro por Prazo:
      - "Próximos 7 dias" → vê próximas 1 semana
      - "Este mês" → vê este mês
      - "Atrasadas" → vê vencidas
3. Verificar contadores de resultados
```

---

## 🔗 Teste 3: Integração Disciplinas ↔ Tarefas

### 3.1 - Vincular Tarefa a Disciplina
```
1. Criar nova tarefa
2. Selecionar disciplina "Análise de Dados"
3. Criar a tarefa
4. Ir para Filtros de Tarefas
5. Filtrar por "Análise de Dados"
6. Deve aparecer a tarefa criada
7. Outras disciplinas não devem aparecer
```

### 3.2 - Vincular Múltiplas Tarefas
```
1. Criar 3 tarefas diferentes vinculadas a "Análise de Dados"
2. Criar 2 tarefas vinculadas a outra disciplina
3. Ir para Filtros
4. Selecionar "Análise de Dados"
5. Deve aparecer exatamente 3 tarefas
```

---

## 🔒 Teste 4: Segurança e Validação

### 4.1 - Campos Obrigatórios (Disciplinas)
```
1. Aba "Criar Nova"
2. Deixar Nome vazio
3. Deixar Professor vazio
4. Clicar "✅ Criar Disciplina"
5. Deve aparecer warning: "⚠️ Preencha todos os campos!"
```

### 4.2 - Campos Obrigatórios (Tarefas)
```
1. Aba "Criar Nova"
2. Deixar Título vazio
3. Clicar "✅ Criar Tarefa"
4. Deve aparecer warning: "⚠️ Preencha título e selecione uma disciplina!"
```

### 4.3 - Modal de Confirmação
```
1. Tentar deletar uma disciplina
2. Modal deve aparecer com aviso
3. Se clicar "❌ Cancelar" → modal fecha, nada é deletado
4. Se clicar "🗑️ Confirmar" → disciplina é deletada
```

---

## 📱 Teste 5: UX/Interface

### 5.1 - Abas Funcionam
```
1. Disciplinas: Clique entre abas sem problemas
2. Tarefas: Clique entre abas sem problemas
3. Dados persistem quando volta para aba
```

### 5.2 - Cards com Border
```
1. Cada disciplina/tarefa aparece em card com border
2. Botões alinhados corretamente
3. Texto formatado (emojis, negrito)
```

### 5.3 - Responsividade
```
1. Redimensionar navegador
2. Cards devem se adaptar (responsive)
3. Botões devem permanecer acessíveis
```

---

## 🔴 Teste 6: Tratamento de Erros

### 6.1 - API Offline
```
1. Desligar Xano ou servidor
2. Tentar criar disciplina
3. Deve aparecer erro: "❌ Erro ao criar: ..."
```

### 6.2 - Token Expirado
```
1. Logout
2. Ir para Disciplinas
3. Deve aparecer: "⚠️ Acesso negado. Por favor, faça login..."
```

---

## ✅ Checklist Final

- [ ] Disciplinas: Create ✅
- [ ] Disciplinas: Read ✅
- [ ] Disciplinas: Update ✅
- [ ] Disciplinas: Delete ✅
- [ ] Disciplinas: Filtros funcionam ✅
- [ ] Tarefas: Create ✅
- [ ] Tarefas: Read ✅
- [ ] Tarefas: Update ✅
- [ ] Tarefas: Delete ✅
- [ ] Tarefas: Filtros funcionam ✅
- [ ] Vinculação disciplina-tarefa ✅
- [ ] Validação de campos ✅
- [ ] Modais de confirmação ✅
- [ ] Mensagens de sucesso/erro ✅
- [ ] Interface responsiva ✅

---

## 📊 Dados de Teste Sugeridos

### Disciplinas
```
1. "Python Avançado" | "João Silva" | "Quarta"
2. "Análise de Dados" | "Carlos Santos" | "Terça"
3. "Web Development" | "Marina Costa" | "Quinta"
4. "Cloud Computing" | "Pedro Oliveira" | "Segunda"
5. "Machine Learning" | "Ana Paula" | "Sexta"
```

### Tarefas
```
Para cada disciplina:
- Tarefa 1: Status "pending", Prazo próximos 7 dias
- Tarefa 2: Status "in_progress", Prazo este mês
- Tarefa 3: Status "completed", Prazo no passado
- Tarefa 4: Status "overdue", Prazo bem no passado
```

---

## 🎯 Sucesso

Se todos os testes passarem, o sistema está **100% funcional**! 🚀

Qualquer dúvida ou erro, revise:
- `CRUD_COMPLETO_RESUMO.md` - Documentação técnica
- `telas/01_📚_Disciplinas.py` - Código disciplinas
- `telas/02_📝_Tarefas.py` - Código tarefas
