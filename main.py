import os
import msal
import requests
from decouple import config


# Caminho para salvar o cache
CACHE_PATH = "token_cache.json"


def carregar_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            try:
                cache.deserialize(f.read())
            except Exception:
                pass
    return cache

def salvar_cache(cache):
    if cache and cache.has_state_changed:
        with open(CACHE_PATH, "w") as f:
            f.write(cache.serialize())

client_id = config('CLIENT_ID')
tenant_id = config('TENANT_ID')
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['Mail.Read']

# Inicializa cache e app
token_cache = carregar_cache()
app = msal.PublicClientApplication(client_id, authority=authority, token_cache=token_cache)

# Tenta usar token existente
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(scopes, account=accounts[0])
else:
    flow = app.initiate_device_flow(scopes=scopes)
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)

# Salva cache atualizado
salvar_cache(token_cache)

flow = app.initiate_device_flow(scopes=scopes)

if 'user_code' not in flow:
    raise Exception("Falha ao iniciar o fluxo de autenticação.")

if 'access_token' in result:
    print("✅ Autenticado com sucesso!")

    headers = {'Authorization': f"Bearer {result['access_token']}"}
    url = 'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$top=5&$orderby=receivedDateTime desc'

    response = requests.get(url, headers=headers)
    emails = response.json().get('value', [])

    for i, email in enumerate(emails, 1):
        print(f"\n📧 Email {i}")
        print("Assunto:", email['subject'])
        print("De:", email['from']['emailAddress']['name'])
        print("Recebido em:", email['receivedDateTime'])
        print("Prévia do corpo:", email['bodyPreview'])

else:
    print("❌ Falha na autenticação:", result.get("error_description"))