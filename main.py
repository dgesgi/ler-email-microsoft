import msal
import requests
from decouple import config

client_id = config('CLIENT_ID')
tenant_id = config('TENANT_ID')
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['Mail.Read']

app = msal.PublicClientApplication(client_id=client_id, authority=authority)

flow = app.initiate_device_flow(scopes=scopes)

if 'user_code' not in flow:
    raise Exception("Falha ao iniciar o fluxo de autenticação.")

print(flow['message'])  # Instruções para login

result = app.acquire_token_by_device_flow(flow)

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