import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_consultas():
    r = client.get("/usuarios/1")
    assert r.status_code == 200
    print("buscar_usuario: OK")

    r = client.get("/usuarios/1/posts")
    assert r.status_code == 200
    print("posts_do_usuario: OK")

    r = client.get("/posts/1")
    assert r.status_code == 200
    print("buscar_post: OK")

    r1 = client.get("/usuarios/1/seguidores")
    r2 = client.get("/usuarios/2/seguindo")
    assert r1.status_code == 200 and r2.status_code == 200
    print("seguidores/seguindo: OK")

    r = client.get("/usuarios/2/feed")
    assert r.status_code == 200
    print("feed_do_usuario: OK")

def test_comandos():
    r = client.post("/usuarios", json={"nome": "Diana", "email": "diana@exemplo.com", "bio": "Dev"})
    assert r.status_code == 201
    diana_id = r.json()["id"]
    print("criar_usuario: OK")

    r = client.post("/posts", json={"usuario_id": diana_id, "texto": "Post teste"})
    assert r.status_code == 201
    post_id = r.json()["id"]
    print("criar_post: OK")

    r = client.post(f"/posts/{post_id}/comentarios", json={"usuario_id": 1, "texto": "Legal!"})
    assert r.status_code == 201
    print("comentar: OK")

    r = client.post(f"/posts/{post_id}/curtidas", json={"usuario_id": 1})
    assert r.status_code == 201
    print("curtir: OK")

    r = client.post("/usuarios/1/seguir", json={"alvo_id": diana_id})
    assert r.status_code == 201
    print("seguir: OK")

if __name__ == "__main__":
    print("Executando testes da API REST...")
    test_consultas()
    test_comandos()
    print("Todos os testes REST passaram com sucesso!")
