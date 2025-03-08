import os
import base64
import requests
from dotenv import load_dotenv

# Carregando ENV´s
load_dotenv()

# Configurações
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
FILE_PATH = "README.md"

# URL da API para acessar o README
url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

# Cabeçalhos com autenticação
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Obter o SHA do README atual
response = requests.get(url, headers=headers)

if response.status_code == 200:
    sha = response.json()["sha"]
    print(f"SHA do arquivo: {sha}")
else:
    print("Erro ao obter o SHA:", response.json())
    exit()

# Novo conteúdo para o README (em Base64)
novo_conteudo = "### Novo README 🚀\n\nEste arquivo foi atualizado via API do GitHub!"
base64_content = base64.b64encode(novo_conteudo.encode()).decode()

# Criar payload para atualização
payload = {
    "message": "Atualizando README via API",
    "content": base64_content,
    "sha": sha  # Necessário para modificar o arquivo existente
}

# Enviar requisição PUT para atualizar o arquivo
response = requests.put(url, headers=headers, json=payload)

if response.status_code == 200:
    print("✅ README atualizado com sucesso!")
else:
    print("❌ Erro ao atualizar:", response.json())
