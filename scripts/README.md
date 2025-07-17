# Scripts de Segurança - SQL Injection Demo

Este diretório contém scripts desenvolvidos para detectar, monitorar e simular ataques de SQL Injection.

## 📁 Arquivos Disponíveis

### 1. `monitor_sql_injection.py`
**Descrição**: Script de monitoramento em tempo real que detecta tentativas de SQL Injection nos logs da aplicação.

**Funcionalidades**:
- Monitoramento em tempo real dos logs do container
- Detecção de padrões de SQL Injection
- Geração de alertas com timestamp
- Relatório final com estatísticas
- Salvamento de logs em arquivo JSON

**Como usar**:
```bash
# Instalar dependências
pip install docker

# Executar monitoramento
python scripts/monitor_sql_injection.py

# Parar com Ctrl+C
```

**Padrões detectados**:
- `' OR '1'='1'`
- `' OR 1=1`
- `' UNION SELECT`
- `admin' --`
- `admin' #`
- E muitos outros...

### 2. `firewall_setup.sh`
**Descrição**: Script para configurar firewall básico com iptables e regras de detecção.

**Funcionalidades**:
- Configuração de política restritiva
- Regras específicas para detectar SQL Injection
- Logging de tentativas suspeitas
- Proteção contra DDoS básica
- Persistência de regras

**Como usar**:
```bash
# Executar com privilégios de administrador
sudo bash scripts/firewall_setup.sh

# Monitorar logs do firewall
sudo tail -f /var/log/kern.log | grep 'SQL_INJECTION'
```

**Portas configuradas**:
- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)
- 5000 (Aplicação vulnerável)
- 3306 (MySQL - apenas local)

### 3. `attack_simulator.py`
**Descrição**: Simulador de ataques automatizado para testar as defesas implementadas.

**Funcionalidades**:
- Ataques automatizados no login e busca
- Múltiplos payloads de SQL Injection
- Relatório detalhado dos resultados
- Salvamento de resultados em JSON
- Taxa de sucesso dos ataques

**Como usar**:
```bash
# Instalar dependências
pip install requests

# Executar simulação
python scripts/attack_simulator.py

# Especificar alvo customizado
python scripts/attack_simulator.py http://localhost:5000
```

**Payloads testados**:
- Bypass de autenticação
- Extração de dados com UNION
- Enumeração de tabelas
- Tentativas de DROP TABLE

## 🔧 Pré-requisitos

### Python
```bash
pip install docker requests
```

### Sistema
- Docker (para monitoramento)
- iptables (para firewall)
- Privilégios sudo (para firewall)

## 🚀 Fluxo de Uso Recomendado

1. **Configurar firewall**:
   ```bash
   sudo bash scripts/firewall_setup.sh
   ```

2. **Iniciar monitoramento** (em terminal separado):
   ```bash
   python scripts/monitor_sql_injection.py
   ```

3. **Executar simulação de ataques**:
   ```bash
   python scripts/attack_simulator.py
   ```

4. **Analisar resultados**:
   - Verificar alertas do monitor
   - Consultar logs do firewall
   - Revisar relatórios gerados

## 📊 Arquivos de Saída

### Monitoramento
- `sql_injection_alerts.log` - Alertas em formato JSON
- Console com alertas em tempo real

### Simulação
- `attack_report_YYYYMMDD_HHMMSS.json` - Relatório detalhado
- Console com resultado de cada ataque

### Firewall
- `/var/log/kern.log` - Logs do sistema com alertas
- `/etc/iptables/rules.v4` - Regras persistentes

## ⚠️ Avisos de Segurança

1. **Uso apenas educacional**: Estes scripts são para fins acadêmicos
2. **Ambiente controlado**: Execute apenas em ambiente de teste
3. **Firewall**: As regras são básicas, não use em produção
4. **Monitoramento**: Pode gerar muitos logs em ambiente real

## 🔍 Troubleshooting

### Erro "Container não encontrado"
```bash
# Verificar se o container está rodando
docker ps

# Iniciar ambiente se necessário
docker-compose up -d
```

### Erro de permissão no firewall
```bash
# Executar com sudo
sudo bash scripts/firewall_setup.sh
```

### Erro de conexão no simulador
```bash
# Verificar se a aplicação está acessível
curl http://localhost:5000
```

## 📝 Logs Importantes

Para análise detalhada, consulte:
- Logs da aplicação: `docker logs vulnerable_webapp`
- Logs do firewall: `sudo tail -f /var/log/kern.log`
- Alertas do monitor: `cat sql_injection_alerts.log`
- Relatórios de ataque: `cat attack_report_*.json` 