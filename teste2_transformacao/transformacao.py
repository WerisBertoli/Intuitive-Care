import pdfplumber
import pandas as pd
import os
import zipfile

# Caminho para o PDF do Anexo I
pdf_path = "../teste1_webscraping/downloads/anexo_i..pdf"

# Verifica se o PDF existe
if not os.path.exists(pdf_path):
    print(f"Erro: Arquivo {pdf_path} não encontrado. Verifique o caminho e se o arquivo foi baixado corretamente.")
    exit(1)

# Remove arquivos antigos para evitar confusão
zip_name = "Teste_Werisder.zip"
output_dir = "output"
csv_path = os.path.join(output_dir, "rol_procedimentos.csv")

# Remove o ZIP antigo, se existir
if os.path.exists(zip_name):
    try:
        os.remove(zip_name)
        print(f"Arquivo ZIP antigo {zip_name} removido.")
    except Exception as e:
        print(f"Aviso: Não foi possível remover o arquivo ZIP antigo {zip_name}: {str(e)}")

# Remove a pasta output e seu conteúdo, se existir
if os.path.exists(output_dir):
    try:
        import shutil
        shutil.rmtree(output_dir)
        print(f"Pasta {output_dir} e seu conteúdo removidos.")
    except Exception as e:
        print(f"Aviso: Não foi possível remover a pasta {output_dir}: {str(e)}")

# Cria a pasta para salvar o CSV
os.makedirs(output_dir, exist_ok=True)

# Extrai tabelas do PDF
all_tables = []
try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Processando PDF com {len(pdf.pages)} páginas...")
        for i, page in enumerate(pdf.pages, 1):
            table = page.extract_table()
            if table:
                print(f"Tabela encontrada na página {i}. Adicionando {len(table)} linhas.")
                all_tables.extend(table)
            else:
                print(f"Nenhuma tabela encontrada na página {i}.")
except Exception as e:
    print(f"Erro ao processar o PDF: {str(e)}")
    exit(1)

# Verifica se alguma tabela foi extraída
if not all_tables:
    print("Erro: Nenhuma tabela encontrada no PDF. Verifique se o PDF contém tabelas legíveis.")
    exit(1)

# Converte para DataFrame
try:
    df = pd.DataFrame(all_tables[1:], columns=all_tables[0])
    print(f"DataFrame criado com {len(df)} linhas e {len(df.columns)} colunas.")
except Exception as e:
    print(f"Erro ao converter a tabela para DataFrame: {str(e)}")
    exit(1)

# Substitui abreviações (OD e AMB) no cabeçalho
df.columns = df.columns.str.replace('OD', 'Seg. Odontológica', case=False)
df.columns = df.columns.str.replace('AMB', 'Seg. Ambulatorial', case=False)

# Substitui abreviações (OD e AMB) em todas as células do DataFrame
df = df.astype(str)  # Converte todas as células para string
df = df.replace('OD', 'Seg. Odontológica')
df = df.replace('AMB', 'Seg. Ambulatorial')

# Substitui 'nan' (resultante de valores nulos convertidos para string) por vazio
df = df.replace('nan', '')

# Salva em CSV
try:
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Arquivo CSV salvo em {csv_path}")
except Exception as e:
    print(f"Erro ao salvar o CSV: {str(e)}")
    exit(1)

# Compacta em ZIP
try:
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path)
    print(f"Arquivo CSV compactado em {zip_name}")
except Exception as e:
    print(f"Erro ao criar o arquivo ZIP: {str(e)}")
    exit(1)

# Não removemos o CSV, para que ele permaneça na pasta output
print("Processo concluído com sucesso! O arquivo CSV foi mantido em output/rol_procedimentos.csv.")