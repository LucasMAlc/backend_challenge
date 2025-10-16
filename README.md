# Backend Challenge

Backend API construído com Django e Django REST Framework para gerenciar posts.

## Funcionalidades

A API implementa operações CRUD:

### Posts

- **POST** `/careers/` - Criar um novo post
- **GET** `/careers/` - Listar todos os posts
- **GET** `/careers/{id}/` - Obter um post específico
- **PATCH** `/careers/{id}/` - Atualizar título e/ou conteúdo
- **DELETE** `/careers/{id}/` - Deletar um post

### Comments

- **GET** `/comments/` - Listar todos os comentários
- **POST** `/comments/` - Criar um comentário
- **GET** `/comments/{id}/` - Obter um comentário específico
- **PATCH** `/comments/{id}/` - Atualizar um comentário (apenas autor)
- **DELETE** `/comments/{id}/` - Deletar um comentário (apenas autor)

## Bonus Points

- Filtros: Buscar posts por username, título ou data
- Ordenação: Ordenar posts por data, título ou username
- Comentários: Sistema de comentários em posts

## Estrutura de Dados

### Post

#### Criar Post (POST)
```json
{
  "username": "string",
  "title": "string",
  "content": "string"
}
```

#### Resposta (GET/POST/PATCH)
```json
{
  "id": 1,
  "username": "string",
  "created_datetime": "2025-10-15T10:30:00Z",
  "title": "string",
  "content": "string"
}
```

#### Atualizar Post (PATCH)
```json
{
  "title": "string",
  "content": "string"
}
```

### Comment

#### Criar Comentário (POST /comments/)
```json
{
  "post": 1,
  "username": "string",
  "content": "string"
}
```

#### Resposta
```json
{
  "id": 1,
  "post": 1,
  "username": "string",
  "content": "string",
  "created_datetime": "2025-10-15T10:30:00Z"
}
```

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. Clone o repositório
```bash
git clone https://github.com/LucasMAlc/backend_challenge.git
cd backend_challenge
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

5. (Opcional) Crie um superusuário para o admin
```bash
python manage.py createsuperuser
```

6. Inicie o servidor
```bash
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/careers/`

### Estrutura de Arquivos
```
backend_challenge/
├── backend_challenge/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── careers/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── migrations/
├── manage.py
├── requirements.txt
└── README.md
```

## Testando a API

### Usando Python (requests)

```bash
pip install requests
python tests.py
```

### Usando Postman ou Insomnia

1. **POST** `http://localhost:8000/careers/`
   - Body (JSON): `{"username": "user", "title": "título", "content": "conteúdo"}`

2. **GET** `http://localhost:8000/careers/`

3. **PATCH** `http://localhost:8000/careers/1/`
   - Body (JSON): `{"username": "user", "title": "novo título"}`

4. **DELETE** `http://localhost:8000/careers/1/?username=user`

## Tecnologias Utilizadas

- Django 5.2.7
- Django REST Framework 3.16.1
- django-cors-headers 4.3.1
- WhiteNoise 6.6.0 (para servir arquivos estáticos)
- Gunicorn 23.0.0 (servidor WSGI para produção)
- python-dotenv 1.1.1 (gerenciamento de variáveis de ambiente)

## Notas Importantes

- CORS está configurado
- Os campos `id`, `username` e `created_datetime` são read-only e não podem ser modificados após a criação
- A API retorna status 204 (No Content) ao deletar um post

### Regras de Autorização

- **Editar (PATCH)**: Apenas o autor (username) pode editar seu próprio post ou comentário
  - O `username` deve ser enviado no body da requisição
  - Retorna `403 Forbidden` se o username não corresponder ao autor
  
- **Deletar (DELETE)**: Apenas o autor (username) pode deletar seu próprio post ou comentário
  - O `username` deve ser enviado como query parameter: `?username=autor`
  - Retorna `403 Forbidden` se o username não corresponder ao autor

### Recursos de Filtros e Busca

#### Filtros de Posts

- `?username=john` - Filtra por username (busca parcial, case-insensitive)
- `?title=python` - Filtra por título (busca parcial, case-insensitive)
- `?created_after=2025-01-01` - Posts criados após esta data
- `?created_before=2025-12-31` - Posts criados antes desta data

#### Ordenação de Posts

- `?ordering=created_datetime` - Ordem crescente por data
- `?ordering=-created_datetime` - Ordem decrescente por data (padrão)
- `?ordering=title` - Ordem alfabética por título
- `?ordering=username` - Ordem alfabética por username

## Admin Panel

Acesse o painel admin em `http://localhost:8000/admin/` após criar um superusuário.
