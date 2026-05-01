# EduTrack AI - Gestão Acadêmica Inteligente

O **EduTrack AI** é um sistema de backend e frontend integrado para gestão de disciplinas e tarefas acadêmicas. O projeto utiliza uma arquitetura moderna e segura, focada na experiência do usuário e na integridade dos dados.

## 🛠️ Tecnologias Utilizadas

- **Frontend:** [Streamlit](https://streamlit.io/) (Python)
- **Backend:** [Xano](https://www.xano.com/) (XanoScript)
- **Documentação Técnica:** [OpenSpec](https://openspec.ai/)
- **Lógica de Dados:** Python 3.12+ (Processamento Híbrido)
- **Ambiente de Desenvolvimento:** VS Code com PowerShell em Windows

## 🛡️ Arquitetura de Segurança

O sistema implementa a **Regra de Ouro de Segurança**:
- Todos os endpoints (GET, POST, PATCH, DELETE) são protegidos por autenticação JWT.
- Filtro obrigatório de `user_id = auth.id` em todas as consultas ao banco de dados, garantindo que usuários nunca acessem dados de terceiros.

## 🚀 Como Rodar o Projeto

1. **Clone o repositório:** `git clone https://github.com/felipesalmeida-jpg/edutrack-ai-felipe`
2. **Configure o ambiente Python:**
   - Crie o venv: `python -m venv .venv`
   - Ative o venv: `.\.venv\Scripts\Activate.ps1` (PowerShell)
   - Instale dependências: `pip install -r requirements.txt`
3. **Execute o App:** `streamlit run app.py`

## 📚 Metodologia

Este projeto foi desenvolvido utilizando a metodologia **Spec-Driven Development**, onde cada funcionalidade é planejada em arquivos de especificação (`spec.md`) antes da implementação do código.