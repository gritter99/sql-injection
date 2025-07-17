#!/usr/bin/env python3
"""
Script de Comparação: Vulnerável vs Seguro
Demonstra a eficácia das mitigações implementadas
"""

import requests
import time
import json
from datetime import datetime

class SecurityComparison:
    def __init__(self):
        self.vulnerable_url = "http://localhost:5000"
        self.secure_url = "http://localhost:5001"
        
        # Payloads de teste
        self.attack_payloads = [
            {"username": "admin' # ", "password": "qualquer"},
            {"username": "' OR 1=1 # ", "password": "qualquer"},
            {"username": "' UNION SELECT 1,2,3,4,5,6 # ", "password": "qualquer"},
        ]
        
        self.search_payloads = [
            "' OR 1=1 # ",
            "' UNION SELECT id,username,password,email,role,created_at FROM users # ",
        ]
        
    def test_endpoint(self, url, endpoint, data):
        """Testar um endpoint específico"""
        try:
            response = requests.post(f"{url}/{endpoint}", data=data, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def run_comparison(self):
        """Executar comparação completa"""
        print("🔍 COMPARAÇÃO DE SEGURANÇA")
        print("=" * 50)
        print(f"🎯 Vulnerável: {self.vulnerable_url}")
        print(f"🛡️  Seguro: {self.secure_url}")
        print()
        
        # Teste de conectividade
        print("📡 Testando conectividade...")
        try:
            vuln_status = requests.get(self.vulnerable_url, timeout=5).status_code
            secure_status = requests.get(self.secure_url, timeout=5).status_code
            print(f"  Vulnerável: {'✅' if vuln_status == 200 else '❌'}")
            print(f"  Seguro: {'✅' if secure_status == 200 else '❌'}")
        except:
            print("  ❌ Erro de conectividade")
            return
        
        print("\n" + "=" * 50)
        print("🔐 TESTE DE LOGIN")
        print("=" * 50)
        
        for i, payload in enumerate(self.attack_payloads, 1):
            print(f"\n[{i}] Testando: {payload['username']}")
            
            # Teste na versão vulnerável
            vuln_result = self.test_endpoint(self.vulnerable_url, "login", payload)
            
            # Teste na versão segura
            secure_result = self.test_endpoint(self.secure_url, "login", payload)
            
            print(f"  🎯 Vulnerável: {'✅ SUCESSO' if vuln_result.get('success') else '❌ FALHOU'}")
            print(f"  🛡️  Seguro: {'✅ BLOQUEADO' if not secure_result.get('success') else '❌ PASSOU'}")
            
            if secure_result.get('message'):
                print(f"     Mensagem: {secure_result['message']}")
        
        print("\n" + "=" * 50)
        print("🔍 TESTE DE BUSCA")
        print("=" * 50)
        
        for i, payload in enumerate(self.search_payloads, 1):
            print(f"\n[{i}] Testando: {payload}")
            
            # Teste na versão vulnerável
            vuln_result = self.test_endpoint(self.vulnerable_url, "search", {"search_term": payload})
            
            # Teste na versão segura
            secure_result = self.test_endpoint(self.secure_url, "search", {"search_term": payload})
            
            print(f"  🎯 Vulnerável: {'✅ SUCESSO' if vuln_result.get('success') else '❌ FALHOU'}")
            print(f"  🛡️  Seguro: {'✅ BLOQUEADO' if not secure_result.get('success') else '❌ PASSOU'}")
            
            if secure_result.get('message'):
                print(f"     Mensagem: {secure_result['message']}")
        
        print("\n" + "=" * 50)
        print("📊 RESUMO DA COMPARAÇÃO")
        print("=" * 50)
        
        print("🎯 VERSÃO VULNERÁVEL:")
        print("  ❌ Concatenação de strings SQL")
        print("  ❌ Sem validação de entrada")
        print("  ❌ Sem detecção de ataques")
        print("  ❌ Logs mostram queries completas")
        
        print("\n🛡️ VERSÃO SEGURA:")
        print("  ✅ Prepared Statements")
        print("  ✅ Validação e sanitização de entrada")
        print("  ✅ Detecção de padrões de SQL Injection")
        print("  ✅ Logs de segurança adequados")
        print("  ✅ Mensagens de erro apropriadas")
        
        print("\n✅ MITIGAÇÕES IMPLEMENTADAS:")
        print("  1. Parameterized Queries (Prepared Statements)")
        print("  2. Input Validation and Sanitization")
        print("  3. SQL Injection Pattern Detection")
        print("  4. Proper Error Handling")
        print("  5. Security Logging")

if __name__ == "__main__":
    comparison = SecurityComparison()
    comparison.run_comparison() 