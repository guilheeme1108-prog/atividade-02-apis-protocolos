# Protocolo GraphQL

Implementação da rede social simplificada utilizando o protocolo GraphQL com schema fortemente tipado (SDL) através da biblioteca Strawberry.

## O que o GraphQL faz melhor que o REST nesse domínio
O GraphQL elimina o under-fetching ao permitir carregar em uma única requisição declarativa a árvore completa de relações (post, autor, comentários, curtidas e contadores) sem over-fetching de campos indesejados.

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
O servidor iniciará em `http://localhost:8001`.
O playground interativo GraphiQL fica acessível no navegador em `http://localhost:8001/graphql`.

### 3. Rodar Testes
```bash
python test_graphql.py
```

---

## Exemplos de Requisição e Resposta

O endpoint único para todas as requisições é `POST http://localhost:8001/graphql`.

### Comandos (Mutations)

#### 1. criarUsuario
Mutation:
```graphql
mutation {
  criarUsuario(
    nome: "Fernanda Costa"
    email: "fernanda@exemplo.com"
    bio: "Engenheira de Sistemas"
  ) {
    id
    nome
    email
    perfil {
      bio
      avatarUrl
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { criarUsuario(nome: \"Fernanda Costa\", email: \"fernanda@exemplo.com\", bio: \"Engenheira de Sistemas\") { id nome email perfil { bio avatarUrl } } }"
  }'
```

Resposta:
```json
{
  "data": {
    "criarUsuario": {
      "id": 5,
      "nome": "Fernanda Costa",
      "email": "fernanda@exemplo.com",
      "perfil": {
        "bio": "Engenheira de Sistemas",
        "avatarUrl": "https://imagens.exemplo.com/avatar_5.png"
      }
    }
  }
}
```

#### 2. criarPost
Mutation:
```graphql
mutation {
  criarPost(usuarioId: 5, texto: "Publicação criada via GraphQL mutation.") {
    id
    texto
    criadoEm
    autor {
      nome
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { criarPost(usuarioId: 5, texto: \"Publicação criada via GraphQL mutation.\") { id texto criadoEm autor { nome } } }"
  }'
```

Resposta:
```json
{
  "data": {
    "criarPost": {
      "id": 4,
      "texto": "Publicação criada via GraphQL mutation.",
      "criadoEm": "2026-10-14T21:35:00.000000",
      "autor": {
        "nome": "Fernanda Costa"
      }
    }
  }
}
```

#### 3. comentar
Mutation:
```graphql
mutation {
  comentar(usuarioId: 1, postId: 4, texto: "Excelente iniciativa.") {
    id
    texto
    autor {
      nome
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { comentar(usuarioId: 1, postId: 4, texto: \"Excelente iniciativa.\") { id texto autor { nome } } }"
  }'
```

Resposta:
```json
{
  "data": {
    "comentar": {
      "id": 4,
      "texto": "Excelente iniciativa.",
      "autor": {
        "nome": "Ana Silva"
      }
    }
  }
}
```

#### 4. curtir
Mutation:
```graphql
mutation {
  curtir(usuarioId: 2, postId: 4) {
    id
    usuario {
      nome
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { curtir(usuarioId: 2, postId: 4) { id usuario { nome } } }"
  }'
```

Resposta:
```json
{
  "data": {
    "curtir": {
      "id": 5,
      "usuario": {
        "nome": "Bruno Souza"
      }
    }
  }
}
```

#### 5. seguir
Mutation:
```graphql
mutation {
  seguir(usuarioId: 1, alvoId: 5) {
    id
    seguidor {
      nome
    }
    seguido {
      nome
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { seguir(usuarioId: 1, alvoId: 5) { id seguidor { nome } seguido { nome } } }"
  }'
```

Resposta:
```json
{
  "data": {
    "seguir": {
      "id": 5,
      "seguidor": {
        "nome": "Ana Silva"
      },
      "seguido": {
        "nome": "Fernanda Costa"
      }
    }
  }
}
```

---

### Consultas (Queries)

#### 1. buscarUsuario
Query:
```graphql
query {
  buscarUsuario(id: 1) {
    id
    nome
    email
    perfil {
      bio
      avatarUrl
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { buscarUsuario(id: 1) { id nome email perfil { bio avatarUrl } } }"}'
```

Resposta:
```json
{
  "data": {
    "buscarUsuario": {
      "id": 1,
      "nome": "Ana Silva",
      "email": "ana@exemplo.com",
      "perfil": {
        "bio": "Desenvolvedora de software",
        "avatarUrl": "https://imagens.exemplo.com/avatar_1.png"
      }
    }
  }
}
```

#### 2. postsDoUsuario
Query:
```graphql
query {
  postsDoUsuario(usuarioId: 1) {
    id
    texto
    criadoEm
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { postsDoUsuario(usuarioId: 1) { id texto criadoEm } }"}'
```

Resposta:
```json
{
  "data": {
    "postsDoUsuario": [
      {
        "id": 1,
        "texto": "Primeiro post na rede social!",
        "criadoEm": "2026-10-14T21:29:39.064837"
      }
    ]
  }
}
```

#### 3. buscarPost
Query:
```graphql
query {
  buscarPost(id: 1) {
    id
    texto
    totalCurtidas
    autor {
      nome
    }
    comentarios {
      id
      texto
      autor {
        nome
      }
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { buscarPost(id: 1) { id texto totalCurtidas autor { nome } comentarios { id texto autor { nome } } } }"}'
```

Resposta:
```json
{
  "data": {
    "buscarPost": {
      "id": 1,
      "texto": "Primeiro post na rede social!",
      "totalCurtidas": 2,
      "autor": {
        "nome": "Ana Silva"
      },
      "comentarios": [
        {
          "id": 1,
          "texto": "Muito bom, bem-vinda!",
          "autor": {
            "nome": "Bruno Souza"
          }
        },
        {
          "id": 2,
          "texto": "Show de bola!",
          "autor": {
            "nome": "Carlos Lima"
          }
        }
      ]
    }
  }
}
```

#### 4. seguidoresDe / seguindoDe
Query:
```graphql
query {
  seguidoresDe(id: 1) {
    id
    nome
  }
  seguindoDe(id: 2) {
    id
    nome
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { seguidoresDe(id: 1) { id nome } seguindoDe(id: 2) { id nome } }"}'
```

Resposta:
```json
{
  "data": {
    "seguidoresDe": [
      { "id": 2, "nome": "Bruno Souza" },
      { "id": 3, "nome": "Carlos Lima" }
    ],
    "seguindoDe": [
      { "id": 1, "nome": "Ana Silva" }
    ]
  }
}
```

#### 5. feedDoUsuario
Query:
```graphql
query {
  feedDoUsuario(usuarioId: 2) {
    id
    texto
    autor {
      nome
      email
    }
  }
}
```

Requisição (cURL):
```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { feedDoUsuario(usuarioId: 2) { id texto autor { nome email } } }"}'
```

Resposta:
```json
{
  "data": {
    "feedDoUsuario": [
      {
        "id": 1,
        "texto": "Primeiro post na rede social!",
        "autor": {
          "nome": "Ana Silva",
          "email": "ana@exemplo.com"
        }
      }
    ]
  }
}
```
