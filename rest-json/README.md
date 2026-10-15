# Protocolo REST (JSON)

Implementação da rede social simplificada utilizando o estilo arquitetural REST sobre HTTP com payloads JSON.

## O que o REST faz melhor que o GraphQL nesse domínio
O REST oferece caching HTTP nativo e transparente em nível de infraestrutura (proxies e navegadores) para recursos identificáveis por URI (`/usuarios/1`, `/posts/1`), além de integração universal e padronizada através dos verbos e códigos de status HTTP sem complexidade adicional no cliente.

---

## Como Executar

### 1. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor
```bash
python app.py
```
O servidor iniciará em `http://localhost:8000`.
A documentação interativa Swagger (OpenAPI) fica acessível em `http://localhost:8000/docs`.

### 3. Rodar Testes
```bash
python test_rest.py
```

---

## Exemplos de Requisição e Resposta

### Comandos (Escrita - POST)

#### 1. criar_usuario
`POST http://localhost:8000/usuarios`

Requisição:
```bash
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Mariana Santos",
    "email": "mariana@exemplo.com",
    "bio": "Desenvolvedora"
  }'
```

Resposta (`201 Created`):
```json
{
  "id": 4,
  "nome": "Mariana Santos",
  "email": "mariana@exemplo.com",
  "criado_em": "2026-10-14T21:30:00.123456",
  "perfil": {
    "id": 4,
    "usuario_id": 4,
    "bio": "Desenvolvedora",
    "avatar_url": "https://imagens.exemplo.com/avatar_4.png",
    "atualizado_em": "2026-10-14T21:30:00.123456"
  }
}
```

#### 2. criar_post
`POST http://localhost:8000/posts`

Requisição:
```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 4,
    "texto": "Publicacao de teste"
  }'
```

Resposta (`201 Created`):
```json
{
  "id": 3,
  "usuario_id": 4,
  "texto": "Publicacao de teste",
  "criado_em": "2026-10-14T21:30:10.654321"
}
```

#### 3. comentar
`POST http://localhost:8000/posts/3/comentarios`

Requisição:
```bash
curl -X POST http://localhost:8000/posts/3/comentarios \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "texto": "Comentario de teste"
  }'
```

Resposta (`201 Created`):
```json
{
  "id": 3,
  "usuario_id": 1,
  "post_id": 3,
  "texto": "Comentario de teste",
  "criado_em": "2026-10-14T21:30:15.987654"
}
```

#### 4. curtir
`POST http://localhost:8000/posts/3/curtidas`

Requisição:
```bash
curl -X POST http://localhost:8000/posts/3/curtidas \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 2
  }'
```

Resposta (`201 Created`):
```json
{
  "id": 4,
  "usuario_id": 2,
  "post_id": 3,
  "criado_em": "2026-10-14T21:30:20.111222"
}
```

#### 5. seguir
`POST http://localhost:8000/usuarios/2/seguir`

Requisição:
```bash
curl -X POST http://localhost:8000/usuarios/2/seguir \
  -H "Content-Type: application/json" \
  -d '{
    "alvo_id": 4
  }'
```

Resposta (`201 Created`):
```json
{
  "id": 4,
  "seguidor_id": 2,
  "seguido_id": 4,
  "criado_em": "2026-10-14T21:30:25.333444"
}
```

---

### Consultas (Leitura - GET)

#### 1. buscar_usuario
`GET http://localhost:8000/usuarios/1`

Requisição:
```bash
curl -X GET http://localhost:8000/usuarios/1
```

Resposta (`200 OK`):
```json
{
  "id": 1,
  "nome": "Ana Silva",
  "email": "ana@exemplo.com",
  "criado_em": "2026-10-14T21:29:39.064837",
  "perfil": {
    "id": 1,
    "usuario_id": 1,
    "bio": "Desenvolvedora de software",
    "avatar_url": "https://imagens.exemplo.com/avatar_1.png",
    "atualizado_em": "2026-10-14T21:29:39.064837"
  }
}
```

#### 2. posts_do_usuario
`GET http://localhost:8000/usuarios/1/posts`

Requisição:
```bash
curl -X GET http://localhost:8000/usuarios/1/posts
```

Resposta (`200 OK`):
```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "texto": "Primeiro post na rede social!",
    "criado_em": "2026-10-14T21:29:39.064837"
  }
]
```

#### 3. buscar_post
`GET http://localhost:8000/posts/1`

Requisição:
```bash
curl -X GET http://localhost:8000/posts/1
```

Resposta (`200 OK`):
```json
{
  "id": 1,
  "usuario_id": 1,
  "texto": "Primeiro post na rede social!",
  "criado_em": "2026-10-14T21:29:39.064837",
  "autor": {
    "id": 1,
    "nome": "Ana Silva",
    "email": "ana@exemplo.com",
    "criado_em": "2026-10-14T21:29:39.064837"
  },
  "comentarios": [
    {
      "id": 1,
      "usuario_id": 2,
      "post_id": 1,
      "texto": "Muito bom, bem-vinda!",
      "criado_em": "2026-10-14T21:29:39.064837"
    },
    {
      "id": 2,
      "usuario_id": 3,
      "post_id": 1,
      "texto": "Show de bola!",
      "criado_em": "2026-10-14T21:29:39.064837"
    }
  ],
  "curtidas": [
    { "id": 1, "usuario_id": 2, "post_id": 1, "criado_em": "2026-10-14T21:29:39.064837" },
    { "id": 2, "usuario_id": 3, "post_id": 1, "criado_em": "2026-10-14T21:29:39.064837" }
  ],
  "total_curtidas": 2
}
```

#### 4. seguidores_de / seguindo_de
`GET http://localhost:8000/usuarios/1/seguidores` e `GET http://localhost:8000/usuarios/2/seguindo`

Requisição (seguidores):
```bash
curl -X GET http://localhost:8000/usuarios/1/seguidores
```

Resposta (`200 OK`):
```json
[
  { "id": 2, "nome": "Bruno Souza", "email": "bruno@exemplo.com", "criado_em": "2026-10-14T21:29:39.064837" },
  { "id": 3, "nome": "Carlos Lima", "email": "carlos@exemplo.com", "criado_em": "2026-10-14T21:29:39.064837" }
]
```

Requisição (seguindo):
```bash
curl -X GET http://localhost:8000/usuarios/2/seguindo
```

Resposta (`200 OK`):
```json
[
  { "id": 1, "nome": "Ana Silva", "email": "ana@exemplo.com", "criado_em": "2026-10-14T21:29:39.064837" }
]
```

#### 5. feed_do_usuario
`GET http://localhost:8000/usuarios/2/feed`

Requisição:
```bash
curl -X GET http://localhost:8000/usuarios/2/feed
```

Resposta (`200 OK`):
```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "texto": "Primeiro post na rede social!",
    "criado_em": "2026-10-14T21:29:39.064837"
  }
]
```
