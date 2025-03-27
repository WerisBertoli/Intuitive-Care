import requests
from bs4 import BeautifulSoup
import os
import zipfile

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Faz a requisição ao site
response = requests.get(url)
if response.status_code != 200:
    print(f"Erro ao acessar o site: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Pasta para salvar os PDFs
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)

# Encontra links para os anexos
pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    text = link.text.lower()
    if ('anexo i' in text or 'anexo ii' in text) and href.endswith('.pdf'):
        if not href.startswith('http'):
            href = f"https://www.gov.br{href}"
        pdf_links.append((text, href))

if not pdf_links:
    print("Nenhum PDF 'Anexo I' ou 'Anexo II' encontrado.")
    exit()

# Baixa os PDFs
for name, pdf_url in pdf_links:
    pdf_name = os.path.join(output_dir, f"{name.strip()}.pdf".replace('/', '_').replace(' ', '_'))
    print(f"Baixando: {pdf_name}")
    try:
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()
        with open(pdf_name, 'wb') as f:
            f.write(pdf_response.content)
    except requests.RequestException as e:
        print(f"Erro ao baixar {pdf_name}: {e}")

# Compacta os PDFs em um ZIP
zip_name = "anexos.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for pdf in os.listdir(output_dir):
        if pdf.endswith('.pdf'):
            zipf.write(os.path.join(output_dir, pdf))

print(f"Arquivos compactados em {zip_name}")