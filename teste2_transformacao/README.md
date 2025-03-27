# Teste 2: Transformação de Dados do Rol de Procedimentos

## Descrição
Este projeto faz parte do **Teste 2** da Intuitive Care, que consiste em transformar os dados extraídos do PDF "Anexo I - Rol de Procedimentos e Eventos em Saúde" (obtido no Teste 1) em um formato estruturado. O objetivo é substituir as abreviações "OD" e "AMB" por "Seg. Odontológica" e "Seg. Ambulatorial", respectivamente, em todas as células da tabela (incluindo cabeçalho e dados), e salvar o resultado em um arquivo CSV compactado em um ZIP.

## Estrutura do Projeto
- **Pasta**: `teste2_transformacao`
- **Arquivo principal**: `transformacao.py`
- **Dependências**:
  - Python 3.6 ou superior
  - Bibliotecas: `pdfplumber`, `pandas`, `shutil`, `zipfile` (nativas do Python, exceto `pdfplumber` e `pandas`)
- **Entrada**:
  - Arquivo PDF: `../teste1_webscraping/downloads/anexo_i..pdf` (gerado no Teste 1)
- **Saídas**:
  - Arquivo CSV: `output/rol_procedimentos.csv`
  - Arquivo ZIP: `Teste_Werisder.zip` (contendo o CSV)

## Pré-requisitos
Antes de executar o script, certifique-se de que:
1. O Teste 1 foi concluído e o arquivo `anexo_i..pdf` está disponível no caminho `../teste1_webscraping/downloads/anexo_i..pdf`.
2. As seguintes bibliotecas Python estão instaladas:
   - `pdfplumber`: Para extração de tabelas do PDF.
   - `pandas`: Para manipulação de dados.
   - `shutil`: Para manipulação de arquivos e pastas.

### Instalação das Dependências
Execute os seguintes comandos para instalar as bibliotecas necessárias:
```bash
pip install pdfplumber pandas