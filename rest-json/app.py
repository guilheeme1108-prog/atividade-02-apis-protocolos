from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from banco import banco

app = FastAPI(title="Rede Social - REST")

class CriarUsuarioRequest(BaseModel):
    nome: str = Field(..., example="Mariana Santos")
    email: str = Field(..., example="mariana@exemplo.com")
    bio: Optional[str] = Field("", example="Desenvolvedora")

class CriarPostRequest(BaseModel):
    usuario_id: int = Field(..., example=1)
    texto: str = Field(..., example="Publicacao de teste")

class CriarComentarioRequest(BaseModel):
    usuario_id: int = Field(..., example=2)
    texto: str = Field(..., example="Comentario de teste")

class CurtirPostRequest(BaseModel):
    usuario_id: int = Field(..., example=2)

class SeguirUsuarioRequest(BaseModel):
    alvo_id: int = Field(..., example=1)

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def criar_usuario(payload: CriarUsuarioRequest):
    try:
        return banco.criar_usuario(payload.nome, payload.email, payload.bio or "")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def criar_post(payload: CriarPostRequest):
    try:
        return banco.criar_post(payload.usuario_id, payload.texto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/posts/{post_id}/comentarios", status_code=status.HTTP_201_CREATED)
def comentar(post_id: int, payload: CriarComentarioRequest):
    try:
        return banco.comentar(payload.usuario_id, post_id, payload.texto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/posts/{post_id}/curtidas", status_code=status.HTTP_201_CREATED)
def curtir(post_id: int, payload: CurtirPostRequest):
    try:
        return banco.curtir(payload.usuario_id, post_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/usuarios/{usuario_id}/seguir", status_code=status.HTTP_201_CREATED)
def seguir(usuario_id: int, payload: SeguirUsuarioRequest):
    try:
        return banco.seguir(usuario_id, payload.alvo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/usuarios/{id}", status_code=status.HTTP_200_OK)
def buscar_usuario(id: int):
    usuario = banco.buscar_usuario(id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário {id} não encontrado.")
    return usuario

@app.get("/usuarios/{usuario_id}/posts", status_code=status.HTTP_200_OK)
def posts_do_usuario(usuario_id: int):
    try:
        return banco.posts_do_usuario(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def buscar_post(id: int):
    post = banco.buscar_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} não encontrado.")
    return post

@app.get("/usuarios/{id}/seguidores", status_code=status.HTTP_200_OK)
def seguidores_de(id: int):
    try:
        return banco.seguidores_de(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/usuarios/{id}/seguindo", status_code=status.HTTP_200_OK)
def seguindo_de(id: int):
    try:
        return banco.seguindo_de(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/usuarios/{usuario_id}/feed", status_code=status.HTTP_200_OK)
def feed_do_usuario(usuario_id: int):
    try:
        return banco.feed_do_usuario(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
