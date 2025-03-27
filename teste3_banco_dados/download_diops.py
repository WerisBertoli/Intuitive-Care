import requests
import os
import zipfile
import mysql.connector
from mysql.connector import Error

# Criar diretórios
download_dir = "downloads_diops"
os.makedirs(download_dir, exist_ok=True)
operadoras_dir = "downloads_operadoras"
os.makedirs(operadoras_dir, exist_ok=True)

# Definir anos (últimos 2 anos: 2023 e 2024)
years = [2023, 2024]

# URLs base
base_url_diops = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
base_url_operadoras = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

# Função para descompactar arquivos ZIP
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Arquivo {zip_path} descompactado com sucesso.")

# Função para conectar ao MySQL
def conectar_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='9665',
            database='saude_analitica',
            allow_local_infile=True
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao MySQL!")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# 3.1 - Baixar arquivos DIOPS dos últimos 2 anos
for year in years:
    year_url = f"{base_url_diops}{year}/"
    for quarter in range(1, 5):
        file_name = f"{quarter}T{year}.zip"
        url = f"{year_url}{file_name}"
        file_path = os.path.join(download_dir, file_name)
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo {file_name} baixado com sucesso.")
            unzip_file(file_path, download_dir)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {file_name}: {e}")

# 3.2 - Baixar dados cadastrais das operadoras
file_name_operadoras = "Relatorio_cadop.csv"
url_operadoras = f"{base_url_operadoras}{file_name_operadoras}"
file_path_operadoras = os.path.join(operadoras_dir, file_name_operadoras)
try:
    response = requests.get(url_operadoras, timeout=30)
    response.raise_for_status()
    with open(file_path_operadoras, 'wb') as f:
        f.write(response.content)
    print(f"Arquivo {file_name_operadoras} baixado com sucesso.")
except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar {file_name_operadoras}: {e}")

# Conectar ao MySQL e importar os dados
connection = conectar_mysql()
if connection:
    cursor = connection.cursor()
    
    # Importar operadoras
    cursor.execute(f"""
        LOAD DATA LOCAL INFILE '{os.path.abspath(file_path_operadoras)}'
        INTO TABLE operadoras
        FIELDS TERMINATED BY ';' 
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@Registro_ANS, @CNPJ, @Razao_Social, @Nome_Fantasia, @Modalidade, @Logradouro, @Numero, @Complemento, @Bairro, @Cidade, @UF, @CEP, @DDD, @Telefone, @Fax, @Endereco_eletronico, @Representante, @Cargo_Representante, @Regiao_de_Comercializacao, @Data_Registro_ANS)
        SET
            id_operadora = @Registro_ANS,
            nome_operadora = @Razao_Social,
            cnpj = @CNPJ,
            data_registro = STR_TO_DATE(@Data_Registro_ANS, '%Y-%m-%d')
    """)
    connection.commit()
    print(f"Dados de {file_name_operadoras} importados com sucesso.")

    # Importar cada CSV do DIOPS
    for year in years:
        for quarter in range(1, 5):
            csv_file = f"{quarter}T{year}.csv"
            csv_path = os.path.join(download_dir, csv_file)
            if os.path.exists(csv_path):
                cursor.execute(f"""
                    LOAD DATA LOCAL INFILE '{os.path.abspath(csv_path)}'
                    INTO TABLE demonstrativos_diops
                    FIELDS TERMINATED BY ';' 
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\n'
                    IGNORE 1 LINES
                    (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
                    SET
                        data = STR_TO_DATE(data, '%Y-%m-%d'),
                        vl_saldo_inicial = REPLACE(vl_saldo_inicial, ',', '.'),
                        vl_saldo_final = REPLACE(vl_saldo_final, ',', '.')
                """)
                connection.commit()
                print(f"Dados de {csv_file} importados com sucesso.")

    # Verificar quantas linhas em demonstrativos_diops contêm "SINISTRO"
    cursor.execute("""
        SELECT COUNT(*)
        FROM demonstrativos_diops
        WHERE descricao LIKE '%SINISTRO%'
    """)
    sinistro_count = cursor.fetchone()[0]
    print(f"Número de linhas em demonstrativos_diops com 'SINISTRO': {sinistro_count}")

    # Verificar quantas linhas em demonstrativos_diops com "SINISTRO" têm data preenchida
    cursor.execute("""
        SELECT COUNT(*)
        FROM demonstrativos_diops
        WHERE descricao LIKE '%SINISTRO%'
        AND data IS NOT NULL
    """)
    sinistro_with_date_count = cursor.fetchone()[0]
    print(f"Número de linhas em demonstrativos_diops com 'SINISTRO' e data preenchida: {sinistro_with_date_count}")

    # Popular eventos_sinistros com JOIN para evitar erro de chave estrangeira
    cursor.execute("""
        INSERT INTO eventos_sinistros (id_operadora, descricao, valor, data_evento)
        SELECT 
            CAST(d.reg_ans AS UNSIGNED) AS id_operadora,
            d.descricao,
            d.vl_saldo_final AS valor,
            d.data AS data_evento
        FROM demonstrativos_diops d
        JOIN operadoras o ON CAST(d.reg_ans AS UNSIGNED) = o.id_operadora
        WHERE d.descricao LIKE '%SINISTRO%'
        AND d.data IS NOT NULL
    """)
    connection.commit()
    print(f"Tabela eventos_sinistros populada com sucesso.")

    # Verificar quantas linhas foram inseridas em eventos_sinistros
    cursor.execute("""
        SELECT COUNT(*)
        FROM eventos_sinistros
    """)
    eventos_count = cursor.fetchone()[0]
    print(f"Número de linhas em eventos_sinistros: {eventos_count}")

    # Verificar se há correspondência no JOIN
    cursor.execute("""
        SELECT COUNT(*)
        FROM eventos_sinistros e
        JOIN operadoras o ON e.id_operadora = o.id_operadora
    """)
    join_count = cursor.fetchone()[0]
    print(f"Número de linhas com correspondência no JOIN: {join_count}")

    # Verificar as datas em eventos_sinistros
    cursor.execute("""
        SELECT MIN(data_evento), MAX(data_evento)
        FROM eventos_sinistros
    """)
    min_date, max_date = cursor.fetchone()
    print(f"Menor data em eventos_sinistros: {min_date}")
    print(f"Maior data em eventos_sinistros: {max_date}")

    # Query analítica ajustada para o 4T2024 (outubro a dezembro de 2024)
    print("10 operadoras com maiores despesas no último trimestre de 2024 (4T2024):")
    # Verificar se há dados no período
    cursor.execute("""
        SELECT COUNT(*)
        FROM eventos_sinistros
        WHERE data_evento BETWEEN '2024-10-01' AND '2024-12-31'
    """)
    num_registros = cursor.fetchone()[0]

    if num_registros == 0:
        print("Nenhum registro encontrado para o período de 2024-10-01 a 2024-12-31.")
        print("Sugestão: Tente um período anterior, como o 3T2024 (2024-07-01 a 2024-09-30).")
    else:
        cursor.execute("""
            SELECT 
                o.nome_operadora,
                SUM(e.valor) AS total_despesas
            FROM eventos_sinistros e
            JOIN operadoras o ON e.id_operadora = o.id_operadora
            WHERE e.data_evento BETWEEN '2024-10-01' AND '2024-12-31'
            GROUP BY o.nome_operadora
            ORDER BY total_despesas DESC
            LIMIT 10
        """)
        resultados = cursor.fetchall()
        for nome, despesa in resultados:
            print(f"{nome}: R$ {float(despesa):,.2f}")

    # Opcional: Manter a query para o ano de 2023 como referência
    print("\n10 operadoras com maiores despesas no ano de 2023 (para referência):")
    cursor.execute("""
        SELECT 
            o.nome_operadora,
            SUM(e.valor) AS total_despesas
        FROM eventos_sinistros e
        JOIN operadoras o ON e.id_operadora = o.id_operadora
        WHERE e.data_evento BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY o.nome_operadora
        ORDER BY total_despesas DESC
        LIMIT 10
    """)
    resultados = cursor.fetchall()
    for nome, despesa in resultados:
        print(f"{nome}: R$ {float(despesa):,.2f}")

    # Fechar a conexão
    cursor.close()
    connection.close()