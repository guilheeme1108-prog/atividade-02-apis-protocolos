from typing import List, Optional
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from banco import banco

@strawberry.type
class PerfilType:
    id: int
    usuario_id: int
    bio: str
    avatar_url: str
    atualizado_em: str

@strawberry.type
class UsuarioType:
    id: int
    nome: str
    email: str
    criado_em: str

    @strawberry.field
    def perfil(self) -> Optional[PerfilType]:
        p = banco.perfis.get(self.id)
        if not p:
            return None
        return PerfilType(**p)

    @strawberry.field
    def posts(self) -> List["PostType"]:
        posts = banco.posts_do_usuario(self.id)
        return [PostType(**p) for p in posts]

    @strawberry.field
    def seguidores(self) -> List["UsuarioType"]:
        segs = banco.seguidores_de(self.id)
        return [UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"]) for u in segs]

    @strawberry.field
    def seguindo(self) -> List["UsuarioType"]:
        segs = banco.seguindo_de(self.id)
        return [UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"]) for u in segs]

@strawberry.type
class PostType:
    id: int
    usuario_id: int
    texto: str
    criado_em: str

    @strawberry.field
    def autor(self) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(self.usuario_id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.field
    def comentarios(self) -> List["ComentarioType"]:
        coments = [c for c in banco.comentarios.values() if c["post_id"] == self.id]
        return [ComentarioType(**c) for c in coments]

    @strawberry.field
    def curtidas(self) -> List["CurtidaType"]:
        curts = [c for c in banco.curtidas if c["post_id"] == self.id]
        return [CurtidaType(**c) for c in curts]

    @strawberry.field
    def total_curtidas(self) -> int:
        return len([c for c in banco.curtidas if c["post_id"] == self.id])

@strawberry.type
class ComentarioType:
    id: int
    usuario_id: int
    post_id: int
    texto: str
    criado_em: str

    @strawberry.field
    def autor(self) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(self.usuario_id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.field
    def post(self) -> Optional[PostType]:
        p = banco.posts.get(self.post_id)
        if not p:
            return None
        return PostType(**p)

@strawberry.type
class CurtidaType:
    id: int
    usuario_id: int
    post_id: int
    criado_em: str

    @strawberry.field
    def usuario(self) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(self.usuario_id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.field
    def post(self) -> Optional[PostType]:
        p = banco.posts.get(self.post_id)
        if not p:
            return None
        return PostType(**p)

@strawberry.type
class SeguidorType:
    id: int
    seguidor_id: int
    seguido_id: int
    criado_em: str

    @strawberry.field
    def seguidor(self) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(self.seguidor_id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.field
    def seguido(self) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(self.seguido_id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

@strawberry.type
class Query:
    @strawberry.field
    def buscar_usuario(self, id: int) -> Optional[UsuarioType]:
        u = banco.buscar_usuario(id)
        if not u:
            return None
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.field
    def posts_do_usuario(self, usuario_id: int) -> List[PostType]:
        posts = banco.posts_do_usuario(usuario_id)
        return [PostType(**p) for p in posts]

    @strawberry.field
    def buscar_post(self, id: int) -> Optional[PostType]:
        p = banco.buscar_post(id)
        if not p:
            return None
        return PostType(id=p["id"], usuario_id=p["usuario_id"], texto=p["texto"], criado_em=p["criado_em"])

    @strawberry.field
    def seguidores_de(self, id: int) -> List[UsuarioType]:
        segs = banco.seguidores_de(id)
        return [UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"]) for u in segs]

    @strawberry.field
    def seguindo_de(self, id: int) -> List[UsuarioType]:
        segs = banco.seguindo_de(id)
        return [UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"]) for u in segs]

    @strawberry.field
    def feed_do_usuario(self, usuario_id: int) -> List[PostType]:
        feed = banco.feed_do_usuario(usuario_id)
        return [PostType(**p) for p in feed]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def criar_usuario(self, nome: str, email: str, bio: Optional[str] = "") -> UsuarioType:
        u = banco.criar_usuario(nome, email, bio or "")
        return UsuarioType(id=u["id"], nome=u["nome"], email=u["email"], criado_em=u["criado_em"])

    @strawberry.mutation
    def criar_post(self, usuario_id: int, texto: str) -> PostType:
        p = banco.criar_post(usuario_id, texto)
        return PostType(**p)

    @strawberry.mutation
    def comentar(self, usuario_id: int, post_id: int, texto: str) -> ComentarioType:
        c = banco.comentar(usuario_id, post_id, texto)
        return ComentarioType(**c)

    @strawberry.mutation
    def curtir(self, usuario_id: int, post_id: int) -> CurtidaType:
        c = banco.curtir(usuario_id, post_id)
        return CurtidaType(**c)

    @strawberry.mutation
    def seguir(self, usuario_id: int, alvo_id: int) -> SeguidorType:
        s = banco.seguir(usuario_id, alvo_id)
        return SeguidorType(**s)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Rede Social - GraphQL")
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
