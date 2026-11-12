# 📦 API de Gerenciamento de Produtos

API RESTful desenvolvida com **Python + FastAPI** para gerenciamento de estoque de produtos.

## 🛠️ Tecnologias
- **FastAPI** — Framework moderno para APIs
- **SQLite** — Banco de dados relacional
- **Pydantic** — Validação de dados

## ✅ Funcionalidades
- ✅ Listar todos os produtos
- ✅ Buscar produto por ID
- ✅ Cadastrar novo produto
- ✅ Atualizar dados do produto
- ✅ Excluir produto
- ✅ Validação de dados
- ✅ Documentação automática com Swagger

## 📡 Endpoints
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/produtos` | Listar todos os produtos |
| GET | `/produtos/{id}` | Buscar produto por ID |
| POST | `/produtos` | Cadastrar novo produto |
| PUT | `/produtos/{id}` | Atualizar produto |
| DELETE | `/produtos/{id}` | Excluir produto |

## 🚀 Como rodar
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
