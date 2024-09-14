# FinanceMind app

## Descrição

FinanceMind é um aplicativo que permite aos usuários gerenciar suas finanças pessoais, controlando receitas, despesas e orçamentos. O aplicativo fornece funcionalidades para cadastrar transações financeiras, categorizar despesas, visualizar relatórios e acompanhar o progresso financeiro.

## Objetivos

- Permitir o cadastro e gerenciamento de receitas e despesas.
- Categorizar transações financeiras para melhor organização.
- Fornecer relatórios e visualizações gráficas para análise financeira.
- Definir e acompanhar orçamentos por categoria.
- Armazenar dados de forma eficiente usando SQLite.

## Escopo 

- Cadastro de transações financeiras (receitas e despesas).
- Categorias personalizáveis para transações.
- Relatórios mensais com gráficos.
- Definição e acompanhamento de orçamentos.
- Interface de usuário amigável e intuitiva.

## Requisitos do Sistema

### Requisitos Funcionais

1. Cadastro de Transações:

- Adicionar, editar e excluir receitas e despesas.
- Informar data, valor, categoria e descrição.

2. Gerenciamento de Categorias:

- Adicionar, editar e excluir categorias de receitas e despesas.
- Categorias pré-definidas (ex.: Alimentação, Transporte, Lazer) e personalizadas pelo usuário.

3. Relatórios e Análises:

- Visualização de receitas e despesas por período (diário, semanal, mensal).
- Gráficos de pizza para distribuição de despesas por categoria.
- Gráficos de barras para comparativo de receitas vs. despesas.

4. Orçamentos:

- Definir orçamentos mensais por categoria.
- Alertas quando o gasto em uma categoria se aproxima ou excede o orçamento.

5. Autenticação de Usuário:

- Cadastro e login de usuários.

6. Exportação de Dados:

- Exportar relatórios em formatos como CSV e PDF.

### Requisitos Não Funcionais

- **Usabilidade**: Interface intuitiva e fácil de usar.

- **Desempenho**: Respostas rápidas às ações do usuário.

- ***Segurança***: Proteção dos dados financeiros do usuário.

- **Portabilidade**: Funcionamento em diferentes sistemas operacionais (Windows, macOS, Linux).