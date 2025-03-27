# Parte 3: Extração, Armazenamento e Análise de Dados DIOPS

## Descrição

Este projeto faz parte da **Parte 3** do exercício da Intuitive Care, que consiste em extrair, armazenar e analisar os dados do DIOPS (Demonstrativos Contábeis das Operadoras de Planos de Saúde) disponibilizados pela ANS (Agência Nacional de Saúde Suplementar). O objetivo principal é listar as 10 operadoras com maiores despesas em sinistros no último trimestre disponível (4T2024, outubro a dezembro de 2024), com base nos dados dos últimos 2 anos (2023 e 2024).

### Funcionalidades

1. **Download de Arquivos**:
   - Baixa os arquivos ZIP do DIOPS dos últimos 2 anos (2023 e 2024), contendo os demonstrativos contábeis trimestrais (1T2023 a 4T2024).
   - Baixa o arquivo `Relatorio_cadop.csv`, que contém os dados cadastrais das operadoras de planos de saúde ativas.

2. **Descompactação**:
   - Descompacta os arquivos ZIP baixados, extraindo os CSVs correspondentes (ex.: `1T2023.csv`, `2T2023.csv`, etc.).

3. **Armazenamento em Banco de Dados**:
   - Usa o banco de dados MySQL `saude_analitica`.
   - Importa os dados do `Relatorio_cadop.csv` para a tabela `operadoras`.
   - Importa os dados dos CSVs do DIOPS para a tabela `demonstrativos_diops`.
   - Popula a tabela `eventos_sinistros` com registros que contêm "SINISTRO" na descrição e têm data preenchida, associando-os às operadoras via `id_operadora`.

4. **Análise**:
   - Lista as 10 operadoras com maiores despesas em sinistros no último trimestre disponível (4T2024, outubro a dezembro de 2024).
   - Como referência, também lista as 10 operadoras com maiores despesas em sinistros no ano de 2023.

### Estrutura do Banco de Dados

O banco de dados `saude_analitica` contém as seguintes tabelas:

- **`operadoras`**:
  - `id_operadora` (UNSIGNED INTEGER, PRIMARY KEY): Identificador único da operadora (Registro ANS).
  - `nome_operadora` (VARCHAR): Nome da operadora (Razão Social).
  - `cnpj` (VARCHAR): CNPJ da operadora.
  - `data_registro` (DATE): Data de registro da operadora na ANS.

- **`demonstrativos_diops`**:
  - `id` (AUTO_INCREMENT, PRIMARY KEY): Identificador único do registro.
  - `data` (DATE): Data do demonstrativo.
  - `reg_ans` (VARCHAR): Registro ANS da operadora.
  - `cd_conta_contabil` (VARCHAR): Código da conta contábil.
  - `descricao` (VARCHAR): Descrição do evento financeiro.
  - `vl_saldo_inicial` (DECIMAL): Valor do saldo inicial.
  - `vl_saldo_final` (DECIMAL): Valor do saldo final.

- **`eventos_sinistros`**:
  - `id` (AUTO_INCREMENT, PRIMARY KEY): Identificador único do registro.
  - `id_operadora` (UNSIGNED INTEGER, FOREIGN KEY): Referência à operadora.
  - `descricao` (VARCHAR): Descrição do evento (contém "SINISTRO").
  - `valor` (DECIMAL): Valor do sinistro (vl_saldo_final).
  - `data_evento` (DATE): Data do evento.

### Pré-requisitos

- **Python 3.13** ou superior.
- Bibliotecas Python:
  - `requests`
  - `mysql-connector-python`
  - `zipfile` (nativo no Python)
- **MySQL** instalado e configurado.
- Banco de dados `saude_analitica` criado no MySQL com as tabelas necessárias.

#### Criar o Banco de Dados e as Tabelas

O arquivo `create_database.sql` contém os comandos para criar o banco de dados e as tabelas. Para configurar o ambiente:

1. Execute o script SQL no MySQL:

```bash
mysql -u root -p < create_database.sql