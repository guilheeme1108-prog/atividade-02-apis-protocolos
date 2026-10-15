import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def gql(query):
    res = client.post("/graphql", json={"query": query})
    assert res.status_code == 200
    body = res.json()
    assert "errors" not in body
    return body["data"]

def test_consultas():
    q1 = "query { buscarUsuario(id: 1) { id nome email perfil { bio } } }"
    d = gql(q1)
    assert d["buscarUsuario"]["nome"] == "Ana Silva"
    print("buscarUsuario: OK")

    q2 = "query { postsDoUsuario(usuarioId: 1) { id texto } }"
    d = gql(q2)
    assert len(d["postsDoUsuario"]) >= 1
    print("postsDoUsuario: OK")

    q3 = "query { buscarPost(id: 1) { id texto autor { nome } totalCurtidas comentarios { texto } } }"
    d = gql(q3)
    assert d["buscarPost"]["id"] == 1
    print("buscarPost: OK")

    q4 = "query { seguidoresDe(id: 1) { id } seguindoDe(id: 2) { id } }"
    d = gql(q4)
    print("seguidoresDe/seguindoDe: OK")

    q5 = "query { feedDoUsuario(usuarioId: 2) { id texto autor { nome } } }"
    d = gql(q5)
    print("feedDoUsuario: OK")

def test_comandos():
    m1 = 'mutation { criarUsuario(nome: "Eduardo", email: "edu@exemplo.com", bio: "Gamer") { id nome } }'
    d = gql(m1)
    edu_id = d["criarUsuario"]["id"]
    print("criarUsuario: OK")

    m2 = f'mutation {{ criarPost(usuarioId: {edu_id}, texto: "Post do Edu") {{ id texto }} }}'
    d = gql(m2)
    edu_post_id = d["criarPost"]["id"]
    print("criarPost: OK")

    m3 = f'mutation {{ comentar(usuarioId: 1, postId: {edu_post_id}, texto: "Comentario") {{ id }} }}'
    d = gql(m3)
    print("comentar: OK")

    m4 = f'mutation {{ curtir(usuarioId: 1, postId: {edu_post_id}) {{ id }} }}'
    d = gql(m4)
    print("curtir: OK")

    m5 = f'mutation {{ seguir(usuarioId: 2, alvoId: {edu_id}) {{ id }} }}'
    d = gql(m5)
    print("seguir: OK")

if __name__ == "__main__":
    print("Executando testes da API GraphQL...")
    test_consultas()
    test_comandos()
    print("Todos os testes GraphQL passaram com sucesso!")
