# Teste de Nivelamento - Intuitive Care

## Descrição

Este repositório contém a entrega do teste de nivelamento da Intuitive Care, realizado por **Werisder de Souza Bertoli**. O projeto está dividido em quatro partes, cada uma abordando diferentes aspectos de desenvolvimento, desde web scraping até a criação de uma interface web com API. As partes são:

- **Parte 1 - Web Scraping**: Extração de documentos da ANS (Agência Nacional de Saúde Suplementar) a partir de uma página web.
- **Parte 2 - Transformação de Dados**: Conversão de PDFs baixados na Parte 1 em arquivos CSV.
- **Parte 3 - Banco de Dados e Análise**: Extração, armazenamento e análise de dados DIOPS, com listagem das 10 operadoras com maiores despesas em sinistros.
- **Parte 4 - Teste de API**: Desenvolvimento de uma interface web com Vue.js e uma API em Python para busca textual de operadoras.

Cada parte está organizada em seu próprio diretório, com um `README.md` específico contendo instruções detalhadas para execução, estrutura do código e observações.

## Estrutura do Repositório

- **`teste1_webscraping/`**: Contém os arquivos da Parte 1 (web scraping).
  - [Leia o README da Parte 1](teste1_webscraping/README.md) para mais detalhes.
- **`teste2_transformacao/`**: Contém os arquivos da Parte 2 (transformação de PDFs em CSVs).
  - [Leia o README da Parte 2](teste2_transformacao/README.md) para mais detalhes.
- **`teste3_banco_dados/`**: Contém os arquivos da Parte 3 (banco de dados e análise de dados DIOPS).
  - [Leia o README da Parte 3](teste3_banco_dados/README.md) para mais detalhes.
- **`teste4_api/`**: Contém os arquivos da Parte 4 (interface web e API).
  - [Leia o README da Parte 4](teste4_api/README.md) para mais detalhes.
- **`.gitignore`**: Arquivo para ignorar arquivos desnecessários (como `node_modules`, ambientes virtuais, etc.).

## Pré-requisitos Gerais

Para executar as diferentes partes do projeto, você precisará das seguintes ferramentas:

- **Python 3.13** ou superior (para as Partes 1, 2, 3 e 4).
- **Node.js** e **npm** (para a Parte 4 - frontend).
- **MySQL** (para a Parte 3 e 4 - banco de dados).
- **Postman** (para testar a API na Parte 4).

Instruções específicas para cada parte, incluindo dependências e passos para execução, estão nos READMEs correspondentes.

## Instruções Gerais

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/intuitivecare-teste.git
cd intuitivecare
