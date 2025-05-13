import requests
import json
import time
import random
import os  # <- Necessário para acessar as variáveis de ambiente

# Lista de chamadas para APIs da Microsoft
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
    response = requests.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data=data,
        headers=headers
    )
    json_data = response.json()
    
    if 'access_token' not in json_data:
        raise Exception(f"Erro ao obter token: {json_data}")
    
    # Se você quiser atualizar o token de refresh, pegue aqui também
    return json_data['access_token']

def main():
    # Pega variáveis do ambiente (fornecidas no GitHub Actions)
    refresh_token = os.environ["REFRESH_TOKEN"]
    client_id = os.environ["CONFIG_ID"]
    client_secret = os.environ["CONFIG_KEY"]

    # Obtém access token
    access_token = get_access_token(refresh_token, client_id, client_secret)

    # Define cabeçalhos e embaralha chamadas
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    })

    random.shuffle(calls)
    endpoints = calls[random.randint(0, 10):]
    num = 0

    for endpoint in endpoints:
        try:
            response = session.get(endpoint)
            if response.status_code == 200:
                num += 1
                print(f'{num}ª chamada bem-sucedida: {endpoint}')
            else:
                print(f'Erro {response.status_code} ao chamar: {endpoint}')
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")

    localtime = time.asctime(time.localtime(time.time()))
    print('Execução concluída em:', localtime)
    print('Total de chamadas realizadas:', str(num))

# Executa 3 vezes
for _ in range(3):
    main()
