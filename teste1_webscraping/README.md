# Teste 1 - Web Scraping
Este script acessa o site da ANS, baixa os PDFs "Anexo I" e "Anexo II" e os compacta em "anexos.zip".

## Como Executar
1. Ative o ambiente virtual: `source ../venv/bin/activate`
2. Instale dependências: `pip install requests beautifulsoup4`
3. Rode o script: `python webscraping.py`

## Resultados
- PDFs salvos em `downloads/`
- Arquivo compactado: `anexos.zip`