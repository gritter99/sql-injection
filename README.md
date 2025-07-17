# Trabalho Prático 02 - SQL Injection Demo

## Descrição

Este projeto implementa um ambiente web vulnerável para demonstração de ataques de SQL Injection, desenvolvido para a disciplina de Tópicos Avançados em Segurança Computacional.

## Estrutura do Projeto

```
sql-injection/
├── docker-compose.yml          # Orquestração dos containers
├── webapp/                     # Aplicação web vulnerável
│   ├── app.py                 # Aplicação Flask
│   ├── Dockerfile             # Container da aplicação
│   ├── requirements.txt       # Dependências Python
│   └── templates/             # Templates HTML
│       ├── index.html         # Página inicial
│       ├── login.html         # Página de login (vulnerável)
│       └── search.html        # Página de busca (vulnerável)
├── database/                  # Configuração do banco de dados
│   └── init.sql              # Script de inicialização
├── ids/                       # Sistema de detecção de intrusão
│   └── rules/                # Regras do Suricata
```

## Como Executar

### Pré-requisitos

- Docker
- Docker Compose

### Instruções

1. Clone o repositório:
```bash
git clone https://github.com/gritter99/sql-injection.git
cd sql-injection
```

2. Execute o ambiente com Docker Compose:
```bash
docker-compose up -d
```

3. Acesse a aplicação em: http://localhost:5000

### Serviços Disponíveis

- **Aplicação Web**: http://localhost:5000
- **Banco de dados MySQL**: localhost:3306

## Vulnerabilidades Implementadas

### 1. Login Vulnerável (SQL Injection)
- **Endpoint**: `/login`
- **Vulnerabilidade**: Query SQL sem sanitização
- **Payload de exemplo**: `' OR '1'='1' --`

### 2. Busca Vulnerável (SQL Injection)
- **Endpoint**: `/search`
- **Vulnerabilidade**: Query SQL sem sanitização
- **Payload de exemplo**: `' UNION SELECT 1,username,password,4,5,6 FROM users --`

## Dados de Teste

### Usuários Disponíveis:
- **admin** / admin123 (administrador)
- **user1** / password123 (usuário comum)
- **user2** / mypassword (usuário comum)
- **testuser** / test123 (usuário de teste)

### Produtos de Exemplo:
- Produto A, B, C, D (para teste de busca)

## Próximas Etapas

1. Configurar ferramentas de segurança (firewall, IDS)
2. Implementar scripts de monitoramento
3. Realizar simulação de ataques
4. Aplicar mitigações
5. Elaborar relatório final

## ⚠️ Aviso de Segurança

Este projeto contém vulnerabilidades intencionais e deve ser usado APENAS para fins educacionais em ambiente controlado. NÃO utilize em produção!

## Autor

Desenvolvido para a disciplina de Tópicos Avançados em Segurança Computacional - UnB 2025/1
