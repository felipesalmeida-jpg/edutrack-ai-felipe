# Tabela: subject

## Visão Geral
Esta tabela armazena as disciplinas acadêmicas cadastradas pelos usuários. Ela servirá como fundação para o gerenciamento acadêmico, controle de acesso e futuras automações dentro do EduTrack AI.

## Relacionamentos
- **user**: Cada `subject` pertence a um único `user`. A relação é definida pelo campo `user_id` (N:1), o que garante a propriedade do registro e viabiliza o controle de acesso autenticado.

## Esquema de Dados (Schema)

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|---|---|---|---|---|
| `id` | integer | Sim | Auto-increment | Identificador único da disciplina (Primary Key). |
| `created_at` | timestamp | Sim | `now` | Data e hora em que a disciplina foi registrada. |
| `user_id` | table reference | Sim | - | Chave estrangeira referenciando a tabela de autenticação `user`. |
| `name` | text | Sim | - | Nome da disciplina (ex: "Engenharia de Software"). |
| `description` | text | Não | `null` | Descrição detalhada ou link para ementa da matéria. |
| `semester` | text | Não | `null` | Período ou semestre letivo (ex: "2024.1"). |
| `credits` | integer | Não | `0` | Carga horária ou número de créditos. |
| `status` | text | Sim | `active` | Estado atual da disciplina (ex: `active`, `completed`, `dropped`). |

## Índices
- **Index em `user_id`**: Essencial para otimizar as buscas (Query), pois a operação mais recorrente do sistema será listar as disciplinas ativas de um usuário logado.