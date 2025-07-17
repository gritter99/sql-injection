#!/usr/bin/env python3
"""
Script de Monitoramento de SQL Injection
Trabalho Prático 02 - Segurança Computacional
"""

import docker
import re
import time
import json
from datetime import datetime
import signal
import sys

class SQLInjectionMonitor:
    def __init__(self):
        self.client = docker.from_env()
        self.container_name = "vulnerable_webapp"
        self.running = True
        
        # Padrões de SQL Injection para detectar
        self.sql_patterns = [
            r"' OR '1'='1'",
            r"' OR 1=1",
            r"' UNION SELECT",
            r"'; DROP TABLE",
            r"' OR 1=1 #",
            r"' OR 1=1 --",
            r"admin' --",
            r"admin' #",
            r"' OR '1'='1' --",
            r"' OR '1'='1' #",
            r"UNION.*SELECT.*FROM",
            r"INSERT.*INTO",
            r"UPDATE.*SET",
            r"DELETE.*FROM"
        ]
        
        # Contador de ataques
        self.attack_count = 0
        self.alerts = []
        
    def setup_signal_handlers(self):
        """Configurar handlers para parar o monitoramento graciosamente"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handler para parar o monitoramento"""
        print(f"\n[{datetime.now()}] Parando monitoramento...")
        self.running = False
        
    def detect_sql_injection(self, log_line):
        """Detectar padrões de SQL Injection nos logs"""
        for pattern in self.sql_patterns:
            if re.search(pattern, log_line, re.IGNORECASE):
                return True, pattern
        return False, None
        
    def create_alert(self, log_line, pattern):
        """Criar alerta de detecção"""
        self.attack_count += 1
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "attack_id": self.attack_count,
            "pattern_detected": pattern,
            "log_line": log_line.strip(),
            "severity": "HIGH",
            "source": "SQL_INJECTION_MONITOR"
        }
        
        self.alerts.append(alert)
        return alert
        
    def log_alert(self, alert):
        """Registrar alerta no arquivo de log"""
        with open("sql_injection_alerts.log", "a") as f:
            f.write(f"{json.dumps(alert)}\n")
            
    def print_alert(self, alert):
        """Exibir alerta no console"""
        print(f"\n🚨 ALERTA DE SQL INJECTION #{alert['attack_id']}")
        print(f"⏰ Timestamp: {alert['timestamp']}")
        print(f"🎯 Padrão detectado: {alert['pattern_detected']}")
        print(f"📝 Log: {alert['log_line']}")
        print(f"⚠️  Severidade: {alert['severity']}")
        print("-" * 80)
        
    def monitor_logs(self):
        """Monitorar logs em tempo real"""
        try:
            container = self.client.containers.get(self.container_name)
            
            print(f"🔍 Iniciando monitoramento de SQL Injection...")
            print(f"📦 Container: {self.container_name}")
            print(f"⏰ Início: {datetime.now()}")
            print("=" * 80)
            
            # Monitorar logs em tempo real
            for log in container.logs(stream=True, follow=True):
                if not self.running:
                    break
                    
                log_line = log.decode('utf-8')
                
                # Detectar SQL Injection
                is_attack, pattern = self.detect_sql_injection(log_line)
                
                if is_attack:
                    alert = self.create_alert(log_line, pattern)
                    self.print_alert(alert)
                    self.log_alert(alert)
                    
                # Mostrar logs normais (opcional)
                if "Executando query" in log_line:
                    print(f"📊 {datetime.now().strftime('%H:%M:%S')} - {log_line.strip()}")
                    
        except Exception as e:
            if "not found" in str(e).lower():
                print(f"❌ Container '{self.container_name}' não encontrado!")
            else:
                print(f"❌ Erro no monitoramento: {e}")
            return
            
    def generate_report(self):
        """Gerar relatório de ataques detectados"""
        if not self.alerts:
            print("\n📊 Nenhum ataque detectado durante o monitoramento.")
            return
            
        print(f"\n📊 RELATÓRIO DE ATAQUES DETECTADOS")
        print("=" * 50)
        print(f"Total de ataques: {self.attack_count}")
        print(f"Período: {self.alerts[0]['timestamp']} até {self.alerts[-1]['timestamp']}")
        print("\nPadrões mais comuns:")
        
        # Contar padrões
        pattern_count = {}
        for alert in self.alerts:
            pattern = alert['pattern_detected']
            pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
            
        for pattern, count in sorted(pattern_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {pattern}: {count} ocorrências")
            
    def run(self):
        """Executar o monitoramento"""
        self.setup_signal_handlers()
        
        try:
            self.monitor_logs()
        except KeyboardInterrupt:
            pass
        finally:
            self.generate_report()
            print(f"\n✅ Monitoramento finalizado. Logs salvos em 'sql_injection_alerts.log'")

if __name__ == "__main__":
    monitor = SQLInjectionMonitor()
    monitor.run() 