import requests

BASE_URL = "http://localhost:8000/careers/"

# Criar post
print("=== CRIAR POST ===")
response = requests.post(BASE_URL, json={
    "username": "testuser",
    "title": "Meu Primeiro Post",
    "content": "Este é o conteúdo do post"
})
print(f"Status: {response.status_code}")
print(response.json())

# Listar posts
print("\n=== LISTAR POSTS ===")
response = requests.get(BASE_URL)
print(f"Status: {response.status_code}")
print(response.json())

# Obter o ID do primeiro post
if response.json():
    post_id = response.json()[0]['id']
    
    # Atualizar post
    print(f"\n=== ATUALIZAR POST {post_id} ===")
    response = requests.patch(f"{BASE_URL}{post_id}/", json={
        "username": "testuser",
        "title": "Título Atualizado",
        "content": "Conteúdo atualizado"
    })
    print(f"Status: {response.status_code}")
    print(response.json())
    
    # Deletar post
    print(f"\n=== DELETAR POST {post_id} ===")
    response = requests.delete(f"{BASE_URL}{post_id}/?username=testuser")
    print(f"Status: {response.status_code}")