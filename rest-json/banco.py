from datetime import datetime
import threading

class BancoDeDados:
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()

    def reset(self):
        with getattr(self, "_lock", threading.Lock()):
            self.usuarios = {}
            self.perfis = {}
            self.posts = {}
            self.comentarios = {}
            self.curtidas = []
            self.seguidores = []

            self._next_usuario_id = 1
            self._next_perfil_id = 1
            self._next_post_id = 1
            self._next_comentario_id = 1
            self._next_curtida_id = 1
            self._next_seguidor_id = 1

            self._popular_dados_iniciais()

    def _agora(self) -> str:
        return datetime.now().isoformat()

    def _popular_dados_iniciais(self):
        u1 = self._criar_usuario_interno("Ana Silva", "ana@exemplo.com", "Desenvolvedora de software")
        u2 = self._criar_usuario_interno("Bruno Souza", "bruno@exemplo.com", "Estudante de computacao")
        u3 = self._criar_usuario_interno("Carlos Lima", "carlos@exemplo.com", "Entusiasta de tecnologia")

        p1 = self._criar_post_interno(u1["id"], "Primeiro post na rede social!")
        p2 = self._criar_post_interno(u2["id"], "Finalizando os testes do projeto.")

        self._seguir_interno(u2["id"], u1["id"])
        self._seguir_interno(u3["id"], u1["id"])
        self._seguir_interno(u3["id"], u2["id"])

        self._comentar_interno(u2["id"], p1["id"], "Muito bom, bem-vinda!")
        self._comentar_interno(u3["id"], p1["id"], "Show de bola!")

        self._curtir_interno(u2["id"], p1["id"])
        self._curtir_interno(u3["id"], p1["id"])
        self._curtir_interno(u1["id"], p2["id"])

    def _criar_usuario_interno(self, nome: str, email: str, bio: str = "") -> dict:
        for u in self.usuarios.values():
            if u["email"].lower() == email.lower():
                raise ValueError(f"Email '{email}' já está em uso.")

        uid = self._next_usuario_id
        self._next_usuario_id += 1

        usuario = {
            "id": uid,
            "nome": nome.strip(),
            "email": email.strip().lower(),
            "criado_em": self._agora()
        }
        self.usuarios[uid] = usuario

        pid = self._next_perfil_id
        self._next_perfil_id += 1
        perfil = {
            "id": pid,
            "usuario_id": uid,
            "bio": bio.strip() if bio else "Perfil de usuario",
            "avatar_url": f"https://imagens.exemplo.com/avatar_{uid}.png",
            "atualizado_em": self._agora()
        }
        self.perfis[uid] = perfil

        res = dict(usuario)
        res["perfil"] = perfil
        return res

    def criar_usuario(self, nome: str, email: str, bio: str = "") -> dict:
        with self._lock:
            if not nome or not email:
                raise ValueError("Nome e email são obrigatórios.")
            return self._criar_usuario_interno(nome, email, bio)

    def _criar_post_interno(self, usuario_id: int, texto: str) -> dict:
        if usuario_id not in self.usuarios:
            raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
        if not texto or not texto.strip():
            raise ValueError("O texto do post não pode ser vazio.")

        pid = self._next_post_id
        self._next_post_id += 1

        post = {
            "id": pid,
            "usuario_id": usuario_id,
            "texto": texto.strip(),
            "criado_em": self._agora()
        }
        self.posts[pid] = post
        return post

    def criar_post(self, usuario_id: int, texto: str) -> dict:
        with self._lock:
            return self._criar_post_interno(usuario_id, texto)

    def _comentar_interno(self, usuario_id: int, post_id: int, texto: str) -> dict:
        if usuario_id not in self.usuarios:
            raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
        if post_id not in self.posts:
            raise ValueError(f"Post com ID {post_id} não encontrado.")
        if not texto or not texto.strip():
            raise ValueError("O comentário não pode ser vazio.")

        cid = self._next_comentario_id
        self._next_comentario_id += 1

        comentario = {
            "id": cid,
            "usuario_id": usuario_id,
            "post_id": post_id,
            "texto": texto.strip(),
            "criado_em": self._agora()
        }
        self.comentarios[cid] = comentario
        return comentario

    def comentar(self, usuario_id: int, post_id: int, texto: str) -> dict:
        with self._lock:
            return self._comentar_interno(usuario_id, post_id, texto)

    def _curtir_interno(self, usuario_id: int, post_id: int) -> dict:
        if usuario_id not in self.usuarios:
            raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
        if post_id not in self.posts:
            raise ValueError(f"Post com ID {post_id} não encontrado.")

        for curtida in self.curtidas:
            if curtida["usuario_id"] == usuario_id and curtida["post_id"] == post_id:
                raise ValueError("Usuário já curtiu esta publicação.")

        lid = self._next_curtida_id
        self._next_curtida_id += 1

        curtida = {
            "id": lid,
            "usuario_id": usuario_id,
            "post_id": post_id,
            "criado_em": self._agora()
        }
        self.curtidas.append(curtida)
        return curtida

    def curtir(self, usuario_id: int, post_id: int) -> dict:
        with self._lock:
            return self._curtir_interno(usuario_id, post_id)

    def _seguir_interno(self, usuario_id: int, alvo_id: int) -> dict:
        if usuario_id not in self.usuarios:
            raise ValueError(f"Usuário de origem ID {usuario_id} não encontrado.")
        if alvo_id not in self.usuarios:
            raise ValueError(f"Usuário alvo ID {alvo_id} não encontrado.")
        if usuario_id == alvo_id:
            raise ValueError("Um usuário não pode seguir a si mesmo.")

        for s in self.seguidores:
            if s["seguidor_id"] == usuario_id and s["seguido_id"] == alvo_id:
                raise ValueError(f"Usuário {usuario_id} já segue o usuário {alvo_id}.")

        sid = self._next_seguidor_id
        self._next_seguidor_id += 1

        relacao = {
            "id": sid,
            "seguidor_id": usuario_id,
            "seguido_id": alvo_id,
            "criado_em": self._agora()
        }
        self.seguidores.append(relacao)
        return relacao

    def seguir(self, usuario_id: int, alvo_id: int) -> dict:
        with self._lock:
            return self._seguir_interno(usuario_id, alvo_id)

    def buscar_usuario(self, id: int) -> dict | None:
        with self._lock:
            usuario = self.usuarios.get(id)
            if not usuario:
                return None
            resultado = dict(usuario)
            resultado["perfil"] = self.perfis.get(id)
            return resultado

    def posts_do_usuario(self, usuario_id: int) -> list[dict]:
        with self._lock:
            if usuario_id not in self.usuarios:
                raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
            user_posts = [p for p in self.posts.values() if p["usuario_id"] == usuario_id]
            return sorted(user_posts, key=lambda x: x["id"], reverse=True)

    def buscar_post(self, id: int) -> dict | None:
        with self._lock:
            post = self.posts.get(id)
            if not post:
                return None
            res = dict(post)
            autor = self.usuarios.get(post["usuario_id"])
            res["autor"] = autor

            coments = [c for c in self.comentarios.values() if c["post_id"] == id]
            res["comentarios"] = coments

            curts = [c for c in self.curtidas if c["post_id"] == id]
            res["curtidas"] = curts
            res["total_curtidas"] = len(curts)
            return res

    def seguidores_de(self, id: int) -> list[dict]:
        with self._lock:
            if id not in self.usuarios:
                raise ValueError(f"Usuário com ID {id} não encontrado.")
            seguidor_ids = [s["seguidor_id"] for s in self.seguidores if s["seguido_id"] == id]
            return [self.usuarios[sid] for sid in seguidor_ids if sid in self.usuarios]

    def seguindo_de(self, id: int) -> list[dict]:
        with self._lock:
            if id not in self.usuarios:
                raise ValueError(f"Usuário com ID {id} não encontrado.")
            seguido_ids = [s["seguido_id"] for s in self.seguidores if s["seguidor_id"] == id]
            return [self.usuarios[sid] for sid in seguido_ids if sid in self.usuarios]

    def feed_do_usuario(self, usuario_id: int) -> list[dict]:
        with self._lock:
            if usuario_id not in self.usuarios:
                raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
            seguidos = {s["seguido_id"] for s in self.seguidores if s["seguidor_id"] == usuario_id}
            posts_feed = [p for p in self.posts.values() if p["usuario_id"] in seguidos]
            return sorted(posts_feed, key=lambda x: x["id"], reverse=True)

banco = BancoDeDados()
