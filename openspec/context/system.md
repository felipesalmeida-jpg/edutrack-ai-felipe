# Contexto do Sistema

## Visão Geral
Este projeto é um backend de gestão acadêmica construído usando XanoScript e Desenvolvimento Orientado por Especificações.

## Propósito
Permitir que os usuários gerenciem disciplinas acadêmicas e dados relacionados.

## Entidades Principais
Usuários (autenticação nativa do Xano)

## Disciplinas 
(matérias acadêmicas pertencentes aos usuários)

*Status:* Implementadas na base de dados (`subject`), com endpoints CRUD completos via XanoScript, testes integrados e listagem dinâmica operando na interface em Streamlit (autenticada via JWT).

## Relacionamentos
Cada disciplina pertence a um usuário.

## Evolução Esperada
O sistema avançará para o gerenciamento de Tarefas (`tasks`) vinculadas às disciplinas, incluindo posteriormente automações acadêmicas e painéis analíticos.