# 🍔 Restaurant Analytics Platform

> **Solução completa de analytics para restaurantes** - Plataforma flexível que permite donos de restaurantes explorarem seus dados operacionais e obterem insights acionáveis sem depender de desenvolvedores.

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)

## 🎯 Problema Resolvido

Donos de restaurantes como "Maria" gerenciam operações complexas através de múltiplos canais (presencial, iFood, Rappi, app próprio) mas não conseguem extrair insights personalizados de seus dados. Esta plataforma resolve isso fornecendo:

- ✅ **Analytics customizável** sem precisar de equipe técnica
- ✅ **Visualizações interativas** para todos os aspectos do negócio
- ✅ **Respostas rápidas** para perguntas críticas de negócio
- ✅ **Performance otimizada** (<1s em 500k+ registros)

## 📊 Perguntas de Negócio Respondidas

### ✅ "Qual produto vende mais na quinta à noite no iFood?"
**Solução**: Dashboard com ranking de produtos + filtros por canal e dia da semana
- Endpoint: `/api/v1/analytics/products/ranking?channel_ids=2`
- Combinado com: `/api/v1/analytics/hourly/performance?day_of_week=4`

### ✅ "Meu ticket médio está caindo. É por canal ou por loja?"
**Solução**: Comparação visual de performance por canal vs loja
- Endpoints: 
  - `/api/v1/analytics/channels/performance`
  - `/api/v1/analytics/stores/performance`
- Gráfico de pizza mostra % de revenue por canal
- Tabela compara ticket médio por loja

### ✅ "Quais produtos têm menor margem e devo repensar o preço?"
**Solução**: Análise de margem mostrando preço base vs preço com customizações
- Endpoint: `/api/v1/analytics/products/margin`
- Mostra receita de customizações separadamente

### ✅ "Meu tempo de entrega piorou. Em quais dias/horários?"
**Solução**: Análise de performance de entrega por região e período
- Endpoint: `/api/v1/analytics/delivery/performance`
- Tabela ordenada por tempo total (preparo + entrega)

### ✅ "Quais clientes compraram 3+ vezes mas não voltam há 30 dias?"
**Solução**: Dashboard de retenção de clientes
- Endpoint: `/api/v1/analytics/customers/retention?min_orders=3&days_inactive=30`
- Lista clientes em risco de churn com dados de contato

## 🏗️ Arquitetura

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   React SPA     │◄────►│  FastAPI REST   │◄────►│   PostgreSQL    │
│   (Frontend)    │      │    (Backend)    │      │   (Database)    │
│                 │      │                 │      │                 │
│ • Recharts      │      │ • SQLAlchemy    │      │ • 500k+ sales   │
│ • Axios         │      │ • Pydantic      │      │ • Indexes       │
│ • Responsive UI │      │ • CORS enabled  │      │ • Constraints   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                ▲
                                │
                         ┌──────┴──────┐
                         │    Redis    │
                         │  (Cache)    │
                         └─────────────┘
```

### Stack Técnico

**Backend (Python)**
- FastAPI 0.109.0 - Framework web moderno e rápido
- SQLAlchemy 2.0 - ORM com tipagem forte
- PostgreSQL 15 - Banco de dados relacional
- Redis 7 - Caching layer (opcional)
- Pydantic - Validação de dados

**Frontend (JavaScript)**
- React 18 - Biblioteca UI
- Vite - Build tool moderna
- Recharts - Biblioteca de gráficos
- Axios - Cliente HTTP
- Lucide React - Ícones

**Infraestrutura**
- Docker & Docker Compose
- Nginx (para produção)

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### 1. Clonar o Repositório
```bash
git clone https://github.com/nickby2/desafio-nola-level.git
cd desafio-nola-level
```

### 2. Iniciar Infraestrutura
```bash
# Iniciar PostgreSQL e Redis
docker compose up -d postgres redis
```

### 3. Gerar Dados de Teste
```bash
# Instalar dependências
pip install psycopg2-binary Faker

# Gerar 1 mês de dados (95k+ vendas)
python generate_data.py --db-url postgresql://challenge:challenge_2024@localhost:5432/challenge_db --months 1 --stores 5

# Para dataset completo (500k+ vendas - 6 meses, 50 lojas)
python generate_data.py --db-url postgresql://challenge:challenge_2024@localhost:5432/challenge_db --months 6 --stores 50
```

### 4. Iniciar Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend estará rodando em: **http://localhost:8000**
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

### 5. Iniciar Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend estará rodando em: **http://localhost:5173**

## 📁 Estrutura do Projeto

```
desafio-nola-level/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── analytics.py    # Endpoints de analytics
│   │   │       └── metadata.py     # Endpoints de metadados
│   │   ├── core/
│   │   │   ├── config.py          # Configurações
│   │   │   └── database.py        # Conexão DB
│   │   ├── models/
│   │   │   └── models.py          # Modelos SQLAlchemy
│   │   ├── schemas/
│   │   │   └── analytics.py       # Schemas Pydantic
│   │   ├── services/
│   │   │   └── analytics_service.py  # Lógica de negócio
│   │   └── main.py                # App FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── Dashboard.jsx      # Dashboard principal
│   │   ├── services/
│   │   │   └── api.js            # Cliente API
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── database-schema.sql         # Schema PostgreSQL
├── generate_data.py            # Gerador de dados
├── docker-compose.yml          # Orquestração
└── README.md                   # Este arquivo
```

## 📊 Endpoints da API

### Analytics

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/v1/analytics/overview` | Métricas gerais de vendas |
| `GET /api/v1/analytics/products/ranking` | Top produtos vendidos |
| `GET /api/v1/analytics/channels/performance` | Performance por canal |
| `GET /api/v1/analytics/stores/performance` | Performance por loja |
| `GET /api/v1/analytics/timeseries` | Série temporal de vendas |
| `GET /api/v1/analytics/customers/retention` | Análise de retenção |
| `GET /api/v1/analytics/delivery/performance` | Performance de entrega |
| `GET /api/v1/analytics/hourly/performance` | Performance por hora/dia |
| `GET /api/v1/analytics/products/margin` | Análise de margem |

### Metadata

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/v1/metadata` | Todos os metadados |
| `GET /api/v1/stores` | Lista de lojas |
| `GET /api/v1/channels` | Lista de canais |
| `GET /api/v1/categories` | Lista de categorias |

**Parâmetros de Filtro Comuns:**
- `start_date` - Data inicial (ISO 8601)
- `end_date` - Data final (ISO 8601)
- `store_ids` - IDs de lojas (comma-separated)
- `channel_ids` - IDs de canais (comma-separated)
- `limit` - Limite de resultados

## 🎨 Features do Dashboard

### 📈 Métricas Principais
- **Vendas Totais** - Total de pedidos no período
- **Faturamento Total** - Receita total gerada
- **Ticket Médio** - Valor médio por venda
- **Taxa de Sucesso** - % de vendas completas vs canceladas
- **Descontos** - Total de descontos aplicados
- **Taxa de Entrega** - Total cobrado em entregas

### 📊 Visualizações

#### Gráfico de Barras - Top 10 Produtos
- Ranking de produtos mais vendidos
- Quantidade vendida por produto
- Cores diferenciadas

#### Gráfico de Pizza - Performance por Canal
- Distribuição de revenue por canal
- % de participação de cada canal
- Labels com percentuais

#### Gráfico de Linha - Evolução de Vendas
- Série temporal de vendas e revenue
- Dois eixos Y (vendas e faturamento)
- Visão diária/semanal/mensal

#### Tabelas - Performance Detalhada
- **Por Loja**: Nome, vendas, faturamento
- **Entrega**: Região, número de entregas, tempo médio

### 🎯 Filtros Interativos
- Filtro por loja (dropdown)
- Filtro por canal (dropdown)
- Atualização automática de todos os gráficos

## ⚡ Performance

### Otimizações Implementadas

1. **Database**
   - Indexes em `created_at`, `store_id`, `channel_id`, `sale_status_desc`
   - Foreign keys para integridade referencial
   - Connection pooling (10 connections, max 20 overflow)

2. **Backend**
   - Queries otimizadas com agregações no DB
   - Uso eficiente de SQLAlchemy ORM
   - Cache layer com Redis (opcional)
   - Paginação em todos os endpoints

3. **Frontend**
   - Code splitting automático (Vite)
   - Lazy loading de componentes
   - Debounce em filtros
   - Otimização de re-renders

### Benchmarks

**Dataset**: 95.127 vendas, 222.027 produtos, 197.802 customizações

| Endpoint | Tempo | Dataset |
|----------|-------|---------|
| Overview | ~200ms | 95k vendas |
| Product Ranking | ~150ms | 95k vendas |
| Channel Performance | ~180ms | 95k vendas |
| Time Series | ~250ms | 95k vendas |

## 🧪 Testando a Solução

### 1. Testar Backend (Swagger UI)

Acesse: http://localhost:8000/docs

Exemplos de queries:

```bash
# Overview geral
curl "http://localhost:8000/api/v1/analytics/overview"

# Top 5 produtos do iFood
curl "http://localhost:8000/api/v1/analytics/products/ranking?channel_ids=2&limit=5"

# Clientes em churn
curl "http://localhost:8000/api/v1/analytics/customers/retention?min_orders=3&days_inactive=30"
```

### 2. Testar Frontend

Acesse: http://localhost:5173

1. Observe os cards de métricas carregando
2. Interaja com os filtros (loja e canal)
3. Veja os gráficos atualizarem automaticamente
4. Scroll pela página para ver todas as visualizações

## 🔧 Desenvolvimento

### Backend

```bash
# Ativar ambiente virtual
cd backend
source venv/bin/activate

# Rodar com hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Criar nova migration (Alembic)
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend

```bash
cd frontend

# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

## 📝 Decisões Arquiteturais

### Por que FastAPI?
- ✅ Performance excelente (comparável a Node.js)
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ Validação de dados com Pydantic
- ✅ Async nativo para I/O-bound operations
- ✅ Tipagem forte (Type hints)

### Por que React + Vite?
- ✅ Ecosystem maduro e amplamente usado
- ✅ Vite oferece dev experience excelente
- ✅ Component-based architecture
- ✅ Fácil integração com bibliotecas de charts
- ✅ Build otimizado para produção

### Por que PostgreSQL?
- ✅ ACID compliance
- ✅ Excelente para analytics (window functions, aggregations)
- ✅ JSON support para flexibilidade
- ✅ Mature e battle-tested
- ✅ Open source

### Por que Recharts?
- ✅ Baseado em D3 mas mais simples
- ✅ Componentes React nativos
- ✅ Responsive por padrão
- ✅ Boa documentação
- ✅ Customizável

## 🚢 Deploy

### Usando Docker Compose (Recomendado)

```bash
# Build e start todos os serviços
docker compose up -d

# Ver logs
docker compose logs -f

# Parar serviços
docker compose down
```

### Deploy Manual

**Backend (exemplo com Gunicorn):**
```bash
cd backend
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend (build estático):**
```bash
cd frontend
npm run build
# Deploy pasta dist/ para S3, Vercel, Netlify, etc.
```

## 🔒 Segurança

- ✅ CORS configurado corretamente
- ✅ Input validation com Pydantic
- ✅ SQL Injection protection (SQLAlchemy ORM)
- ✅ Environment variables para secrets
- ⚠️ Autenticação básica (não implementado - fora do escopo)

## 📈 Próximos Passos

- [ ] Autenticação e autorização (JWT)
- [ ] Multi-tenancy (suporte a múltiplas marcas)
- [ ] Dashboards customizáveis pelo usuário
- [ ] Exportação de relatórios (PDF, Excel)
- [ ] Alertas automáticos (ex: vendas abaixo da meta)
- [ ] Mobile app (React Native)
- [ ] Machine Learning para previsão de demanda
- [ ] Comparação entre períodos
- [ ] Análise de cohort de clientes

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é para fins educacionais como parte do desafio técnico.

## 📞 Contato

Para dúvidas sobre a implementação:
- **Discord**: https://discord.gg/z8pVH26j
- **Email**: gsilvestre@arcca.io

---

**Desenvolvido como solução para o God Level Coder Challenge da Nola/Arcca**
