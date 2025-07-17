#!/bin/bash
# Script de Configuração de Firewall Básico
# Trabalho Prático 02 - Segurança Computacional

echo "🔥 Configurando Firewall Básico para SQL Injection Demo"
echo "======================================================="

# Função para verificar se o comando foi executado com sucesso
check_command() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Erro: $1"
        exit 1
    fi
}

# Limpar regras existentes
echo "🧹 Limpando regras existentes..."
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
check_command "Regras limpas"

# Política padrão - DROP (mais restritiva)
echo "🔒 Configurando política padrão..."
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
check_command "Política padrão configurada"

# Permitir loopback
echo "🔄 Permitindo tráfego loopback..."
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
check_command "Loopback permitido"

# Permitir conexões estabelecidas
echo "🔗 Permitindo conexões estabelecidas..."
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
check_command "Conexões estabelecidas permitidas"

# Permitir SSH (porta 22) - para administração
echo "🔑 Permitindo SSH (porta 22)..."
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
check_command "SSH permitido"

# Permitir HTTP (porta 80) - para aplicação web
echo "🌐 Permitindo HTTP (porta 80)..."
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
check_command "HTTP permitido"

# Permitir HTTPS (porta 443) - para aplicação web segura
echo "🔒 Permitindo HTTPS (porta 443)..."
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
check_command "HTTPS permitido"

# Permitir aplicação vulnerável (porta 5000) - para testes
echo "🎯 Permitindo aplicação vulnerável (porta 5000)..."
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
check_command "Aplicação vulnerável permitida"

# Permitir MySQL (porta 3306) apenas para localhost
echo "🗄️ Permitindo MySQL (porta 3306) apenas local..."
sudo iptables -A INPUT -p tcp -s 127.0.0.1 --dport 3306 -j ACCEPT
sudo iptables -A INPUT -p tcp -s 172.16.0.0/12 --dport 3306 -j ACCEPT
check_command "MySQL permitido localmente"

# Regras específicas para detectar SQL Injection
echo "🚨 Configurando regras de detecção de SQL Injection..."

# Detectar tentativas de SQL Injection comuns
sudo iptables -A INPUT -p tcp --dport 5000 -m string --string "' OR '1'='1'" --algo bm -j LOG --log-prefix "SQL_INJECTION_ATTEMPT: "
sudo iptables -A INPUT -p tcp --dport 5000 -m string --string "UNION SELECT" --algo bm -j LOG --log-prefix "SQL_INJECTION_UNION: "
sudo iptables -A INPUT -p tcp --dport 5000 -m string --string "'; DROP TABLE" --algo bm -j LOG --log-prefix "SQL_INJECTION_DROP: "
sudo iptables -A INPUT -p tcp --dport 5000 -m string --string "admin' --" --algo bm -j LOG --log-prefix "SQL_INJECTION_COMMENT: "

check_command "Regras de detecção configuradas"

# Limitar conexões por IP (proteção contra DDoS)
echo "🛡️ Configurando proteção contra DDoS..."
sudo iptables -A INPUT -p tcp --dport 5000 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
check_command "Proteção DDoS configurada"

# Log de tentativas de conexão suspeitas
echo "📝 Configurando logging de tentativas suspeitas..."
sudo iptables -A INPUT -j LOG --log-prefix "FIREWALL_DROP: " --log-level 4
check_command "Logging configurado"

# Salvar regras (Ubuntu/Debian)
echo "💾 Salvando regras do firewall..."
if command -v iptables-save > /dev/null; then
    sudo iptables-save > /etc/iptables/rules.v4
    check_command "Regras salvas"
else
    echo "⚠️ iptables-save não encontrado, regras não serão persistentes"
fi

# Exibir regras configuradas
echo ""
echo "📋 Regras configuradas:"
echo "======================="
sudo iptables -L -n --line-numbers

echo ""
echo "🔍 Para monitorar logs do firewall:"
echo "tail -f /var/log/kern.log | grep 'SQL_INJECTION'"
echo ""
echo "✅ Firewall configurado com sucesso!"
echo "⚠️  ATENÇÃO: Este é um ambiente de teste. Não use em produção!" 