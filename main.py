import requests
import json
import time
import random
import os

# Leitura das variáveis de ambiente passadas pelo GitHub Actions
client_id = os.environ.get("CONFIG_ID")
client_secret = os.environ.get("CONFIG_KEY")
refresh_token = os.environ.get("REFRESH_TOKEN")

# Lista de chamadas à API para manter a conta ativa
calls = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/beta/me/outlook/masterCategories',
    'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]

def get_access_token(refresh_token, client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    
    if response.status_code != 200:
        print("Erro ao obter access_token:", response.text)
        return None

    result = response.json()
    return result.get('access_token')

def main():
    access_token = get_access_token(refresh_token, client_id, client_secret)
    if not access_token:
        print("Access token inválido. Abortando execução.")
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    session = requests.Session()
    session.headers.update(headers)

    random.shuffle(calls)
    endpoints = calls[random.randint(0, 10):]

    success_count = 0
    for endpoint in endpoints:
        try:
            response = session.get(endpoint)
            if response.status_code == 200:
                success_count += 1
                print(f"{success_count}ª chamada bem-sucedida: {endpoint}")
            else:
                print(f"Falha na chamada: {endpoint} | Código: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {endpoint}: {e}")

    print('Execução finalizada em:', time.asctime(time.localtime()))
    print('Total de chamadas realizadas:', success_count)

# Repetir 3 vezes
for _ in range(3):
    main()
