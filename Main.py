from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI(title="API de Gerenciamento de Produtos", version="1.0")

# Modelo de dados do Produto
class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int

# === Banco de dados SQLite ===
def init_db():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# === 🔍 Listar todos os produtos ===
@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    dados = cursor.fetchall()
    conn.close()
    
    produtos = []
    for p in dados:
        produtos.append({
            "id": p[0],
            "nome": p[1],
            "descricao": p[2],
            "preco": p[3],
            "quantidade": p[4]
        })
    return produtos

# === 🔍 Buscar produto por ID ===
@app.get("/produtos/{produto_id}", response_model=Produto)
def buscar_produto(produto_id: int):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    p = cursor.fetchone()
    conn.close()
    
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {
        "id": p[0],
        "nome": p[1],
        "descricao": p[2],
        "preco": p[3],
        "quantidade": p[4]
    }

# === ➕ Cadastrar novo produto ===
@app.post("/produtos", response_model=Produto)
def cadastrar_produto(produto: Produto):
    if produto.preco < 0:
        raise HTTPException(status_code=400, detail="Preço não pode ser negativo")
    if produto.quantidade < 0:
        raise HTTPException(status_code=400, detail="Quantidade não pode ser negativa")
    
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, quantidade)
        VALUES (?, ?, ?, ?)
    ''', (produto.nome, produto.descricao, produto.preco, produto.quantidade))
    conn.commit()
    produto_id = cursor.lastrowid
    conn.close()
    
    return {"id": produto_id, **produto.dict(exclude={"id"})}

# === ✏️ Atualizar produto ===
@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto: Produto):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    cursor.execute('''
        UPDATE produtos 
        SET nome=?, descricao=?, preco=?, quantidade=?
        WHERE id=?
    ''', (produto.nome, produto.descricao, produto.preco, produto.quantidade, produto_id))
    conn.commit()
    conn.close()
    
    return {"id": produto_id, **produto.dict(exclude={"id"})}

# === 🗑️ Excluir produto ===
@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    conn.close()
    
    return {"mensagem": "Produto excluído com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
