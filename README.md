# Projeto: Leitura de E-mails do Office 365 com Microsoft Graph API

Este projeto em Python permite acessar os últimos e-mails recebidos em uma conta corporativa do Office 365 usando a Microsoft Graph API com autenticação via Device Code Flow.

## ✅ Requisitos
- Conta corporativa com acesso ao Outlook/Exchange Online
- Acesso ao portal Azure para registrar o aplicativo
- Python 3.8 ou superior
- Bibliotecas: msal, requests, python-decouple

## 🔧 Configuração do Aplicativo no Portal Azure
1. Acesse https://portal.azure.com
2. Vá para Azure Active Directory > App registrations
3. Clique em "New registration"
4. Defina um nome para o app e selecione "Accounts in this organizational directory only"
5. Após criar, copie o Client ID e Tenant ID
6. Vá em "Authentication"
   - Clique em "Add a platform > Mobile and desktop applications"
   - Marque: https://login.microsoftonline.com/common/oauth2/nativeclient
   - Salve
   - Ative a opção "Allow public client flows"
7. Vá em "API permissions"
   - Adicione a permissão delegada Mail.Read
   - Clique em "Grant admin consent"

## ⚙️ Configuração do Ambiente
1. Clone o repositório:
   git clone https://github.com/dgesgi/ler-email-microsoft.git
2. Crie o ambiente virtual:
   python -m venv .venv
3. Ative o ambiente virtual:
   - Windows: .venv\Scripts\activate
   - Linux/macOS: source .venv/bin/activate
4. Instale os requisitos:
   pip install -r requirements.txt

## 📁 Arquivo .env
1. Copie o arquivo `.env-sample` para `.env`
2. Preencha os valores:
   CLIENT_ID=seu_client_id
   TENANT_ID=seu_tenant_id

## ▶️ Execução do Projeto
1. Execute o script principal:
   python main.py
2. Siga as instruções para autenticação via Device Code Flow
3. Os últimos e-mails serão exibidos no terminal
