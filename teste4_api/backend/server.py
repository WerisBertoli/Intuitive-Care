from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from typing import List, Dict
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar o FastAPI
app = FastAPI()

# Configurar CORS para permitir requisições do frontend (Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do frontend Vue.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para conectar ao MySQL
def conectar_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "9665"),
            database=os.getenv("MYSQL_DATABASE", "saude_analitica")
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao MySQL!")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Rota para buscar operadoras por nome
@app.get("/operadoras/busca", response_model=List[Dict])
async def buscar_operadoras(termo: str):
    connection = conectar_mysql()
    if not connection:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")

    try:
        cursor = connection.cursor(dictionary=True)
        # Query para buscar operadoras cujo nome contém o termo (case-insensitive)
        query = """
            SELECT id_operadora, nome_operadora, cnpj, data_registro
            FROM operadoras
            WHERE nome_operadora LIKE %s
            ORDER BY nome_operadora
            LIMIT 10
        """
        # Adicionar wildcards ao termo de busca (ex.: "bradesco" vira "%bradesco%")
        termo_busca = f"%{termo}%"
        cursor.execute(query, (termo_busca,))
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar operadoras: {e}")
    finally:
        cursor.close()
        connection.close()

# Iniciar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)