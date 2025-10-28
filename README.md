# 🎭 Sistema Dança

Sistema completo de gerenciamento de eventos de dança, com separação de frontend (Vue.js) e backend (Django REST Framework).

## 📋 Funcionalidades

### Para Administradores (Superusers)
- ✅ Gerenciamento completo de eventos, categorias e tipos de eventos
- ✅ Controle de camisas e lotes
- ✅ Gerenciamento de profissionais e inscrições
- ✅ Planejamento financeiro
- ✅ Controle de caixa (entradas e saídas)
- ✅ Gerenciamento de pagamentos
- ✅ Dashboard com resumo de atividades

### Para Usuários Normais
- ✅ Perfil pessoal com foto
- ✅ Inscrição em eventos
- ✅ Compra de camisas
- ✅ Visualização de calendário de eventos
- ✅ Histórico de pedidos e pagamentos
- ✅ Comprovantes de pagamento

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.12+
- Django 5.2.7
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Pillow (para upload de imagens)
- QRCode (para PIX)

### Frontend
- Vue.js 3
- Vue Router
- Axios
- Bootstrap Icons
- Vite

### Integrações de Pagamento
- PagSeguro
- InfinitePay
- PIX (via QR Code)

## 📦 Requisitos

- Python 3.12+
- Node.js 18+
- PostgreSQL
- Git

## 🚀 Instalação

### Backend (Django)

1. **Clone o repositório**
```bash
git clone https://github.com/ThalesLeal/danca-backend.git
cd danca-backend
```

2. **Crie um ambiente virtual**
```bash
python3 -m venv env
source env/bin/activate  # Linux/Mac
# ou
env\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
# Edite o arquivo .env com suas configurações
# ou crie um arquivo .env baseado no .env.example
```

Arquivo `.env` de exemplo:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=danca
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=sua-senha
MEDIA_ROOT=./media
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

O backend estará disponível em: `http://localhost:8000`

### Frontend (Vue.js)

1. **Entre no diretório do frontend**
```bash
cd ../danca-frontend
```

2. **Instale as dependências**
```bash
npm install
```

3. **Configure a URL da API**
Crie um arquivo `.env` na raiz do projeto frontend:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

4. **Execute o servidor de desenvolvimento**
```bash
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

## 📝 Uso

### Acesso ao Sistema

1. Acesse `http://localhost:5173`
2. Faça login com suas credenciais
3. Se você for superuser, terá acesso ao painel administrativo completo
4. Se for usuário normal, será direcionado ao seu perfil

### Criar Usuário Administrador

```bash
python manage.py createsuperuser
```

### Criar Usuário Normal

1. Acesse a página de login
2. Clique em "Cadastre-se"
3. Preencha os dados
4. Faça login com suas credenciais

## 📁 Estrutura do Projeto

```
danca/
├── _conf/               # Configurações Django
│   ├── settings.py      # Configurações do projeto
│   └── urls.py          # URLs do projeto
├── _core/               # Aplicação core
│   ├── models.py        # Modelo de usuário
│   ├── views.py         # Views de autenticação
│   └── serializers.py   # Serializadores
├── danca/               # Aplicação principal
│   ├── models.py        # Modelos de dados
│   ├── serializers.py   # Serializadores DRF
│   ├── views.py         # Viewsets DRF
│   ├── services/        # Serviços de negócio
│   │   └── payment_service.py
│   └── migrations/      # Migrações do banco
├── media/               # Arquivos enviados pelos usuários
├── requirements.txt     # Dependências Python
└── manage.py           # Script de gerenciamento Django

danca-frontend/
├── src/
│   ├── components/      # Componentes Vue
│   │   ├── Navbar.vue
│   │   └── Sidebar.vue
│   ├── views/          # Páginas Vue
│   │   ├── LoginView.vue
│   │   ├── PerfilView.vue
│   │   ├── MeusPedidosView.vue
│   │   ├── MeusEventosView.vue
│   │   └── CalendarioView.vue
│   ├── services/       # Serviços de API
│   │   └── api.js
│   └── router/         # Rotas Vue
│       └── index.js
└── package.json        # Dependências Node
```

## 🔧 Comandos Úteis

### Backend
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Acessar shell Django
python manage.py shell

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic
```

### Frontend
```bash
# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

## 🔐 Autenticação

O sistema utiliza JWT (JSON Web Tokens) para autenticação:

- **Endpoint de login**: `POST /api/auth/token/`
- **Endpoint de registro**: `POST /api/auth/register/`
- **Endpoint de refresh**: `POST /api/auth/token/refresh/`
- **Endpoint de perfil**: `GET /api/auth/user/`

## 📊 API Endpoints

### Autenticação
- `POST /api/auth/token/` - Obter token JWT
- `POST /api/auth/token/refresh/` - Renovar token
- `POST /api/auth/register/` - Registrar novo usuário
- `GET /api/auth/user/` - Obter dados do usuário atual
- `PUT /api/auth/user/profile/` - Atualizar perfil

### Eventos
- `GET /api/eventos/` - Listar eventos
- `POST /api/eventos/` - Criar evento
- `GET /api/eventos/{id}/` - Detalhes do evento
- `PUT /api/eventos/{id}/` - Atualizar evento
- `DELETE /api/eventos/{id}/` - Excluir evento

### Pagamentos
- `GET /api/pagamentos/` - Listar pagamentos
- `POST /api/pagamentos/` - Criar pagamento
- `POST /api/pagamentos/processar/` - Processar pagamento

## 🧪 Testes

### Backend
```bash
python manage.py test
```

### Frontend
```bash
npm test
```

## 🐛 Solução de Problemas

### Erro de CORS
Se você encontrar erros de CORS, verifique se a origem do frontend está incluída em `CORS_ALLOWED_ORIGINS` no arquivo `settings.py`.

### Erro de conexão com banco
Verifique se o PostgreSQL está rodando e se as credenciais no `.env` estão corretas.

### Erro de migrações
Se houver problemas com migrações, execute:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuidores

- **Thales Leal** - Desenvolvimento inicial

## 📞 Suporte

Para suporte, abra uma issue no repositório do GitHub.

---

Desenvolvido com ❤️ usando Django e Vue.js
