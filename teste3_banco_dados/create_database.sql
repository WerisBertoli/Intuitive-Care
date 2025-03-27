-- Arquivo: create_database.sql
-- Descrição: Script para criar o banco de dados e as tabelas necessárias para a Parte 3 do projeto.

-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS saude_analitica;
USE saude_analitica;

-- Criar a tabela operadoras
CREATE TABLE operadoras (
    id_operadora INT PRIMARY KEY,           -- Registro_ANS
    nome_operadora VARCHAR(255) NOT NULL,  -- Razao_Social
    cnpj VARCHAR(14) NOT NULL,             -- CNPJ
    data_registro DATE                     -- Data_Registro_ANS
);

-- Criar a tabela demonstrativos_diops
CREATE TABLE demonstrativos_diops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,                  -- DATA
    reg_ans VARCHAR(20),        -- REG_ANS
    cd_conta_contabil VARCHAR(50), -- CD_CONTA_CONTABIL
    descricao TEXT,             -- DESCRICAO
    vl_saldo_inicial DECIMAL(15,2), -- VL_SALDO_INICIAL
    vl_saldo_final DECIMAL(15,2)    -- VL_SALDO_FINAL
);

-- Criar a tabela eventos_sinistros
CREATE TABLE eventos_sinistros (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_operadora INT,           -- Ligação com operadoras (REG_ANS)
    descricao VARCHAR(255),     -- Descrição do evento/sinistro
    valor DECIMAL(15,2),        -- Valor do sinistro (pode vir de VL_SALDO_FINAL)
    data_evento DATE,           -- Data do evento (pode vir de DATA)
    FOREIGN KEY (id_operadora) REFERENCES operadoras(id_operadora)
);