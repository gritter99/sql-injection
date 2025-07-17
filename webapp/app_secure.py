from flask import Flask, request, render_template, jsonify, session
import mysql.connector
import os
import logging
import re
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'secure_secret_key_change_in_production'

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'appuser'),
    'password': os.getenv('DB_PASSWORD', 'apppassword'),
    'database': os.getenv('DB_NAME', 'vulnerable_app')
}

# Configurar logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Função para obter conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Erro ao conectar ao banco: {err}")
        return None

def validate_input(input_string, max_length=100):
    """Validar e sanitizar entrada do usuário"""
    if not input_string:
        return None
    
    # Remover caracteres perigosos
    cleaned = re.sub(r'[<>"\';\\]', '', input_string)
    
    # Limitar tamanho
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned.strip()

def detect_sql_injection(input_string):
    """Detectar tentativas de SQL Injection"""
    if not input_string:
        return False
    
    # Padrões suspeitos
    suspicious_patterns = [
        r"(\'|\")[^\'\"]*(\'\s*OR\s*\'\w*\'\s*=\s*\'\w*\'|\"\s*OR\s*\"\w*\"\s*=\s*\"\w*\")",
        r"(\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
        r"(\'\s*OR\s*1\s*=\s*1|\"\s*OR\s*1\s*=\s*1)",
        r"(--|\#|\/\*)",
        r"(\'\s*;\s*|\"\s*;\s*)"
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            logger.warning(f"🚨 SQL Injection detectado: {input_string}")
            return True
    
    return False

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index_secure.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login SEGURA - Usando prepared statements"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validação básica
        if not username or not password:
            return jsonify({'success': False, 'message': 'Usuário e senha são obrigatórios'})
        
        # Detectar tentativas de SQL Injection
        if detect_sql_injection(username) or detect_sql_injection(password):
            logger.warning(f"🚨 Tentativa de SQL Injection bloqueada - User: {username}")
            return jsonify({
                'success': False, 
                'message': 'Tentativa de ataque detectada e bloqueada!'
            })
        
        # Validar entrada
        username = validate_input(username, 50)
        password = validate_input(password, 255)
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Entrada inválida'})
        
        # MITIGAÇÃO: Usar prepared statements (parameterized queries)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        
        # Log da query segura (sem mostrar valores)
        logger.info(f"Executando query segura: {query.replace('%s', '?')}")
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                # SEGURO: Usar parâmetros ao invés de concatenação
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user['id']  # type: ignore
                    session['username'] = user['username']  # type: ignore
                    session['role'] = user['role']  # type: ignore
                    return jsonify({
                        'success': True, 
                        'message': f'Login realizado com sucesso! Bem-vindo, {user["username"]}',  # type: ignore
                        'user': {
                            'id': user['id'],  # type: ignore
                            'username': user['username'],  # type: ignore
                            'role': user['role']  # type: ignore
                        }
                    })
                else:
                    return jsonify({'success': False, 'message': 'Credenciais inválidas'})
                    
            except mysql.connector.Error as err:
                logger.error(f"Erro na query: {err}")
                return jsonify({'success': False, 'message': 'Erro interno do servidor'})
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'success': False, 'message': 'Erro de conexão com o banco'})
    
    return render_template('login_secure.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Página de busca SEGURA - Usando prepared statements"""
    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        
        # Validação básica
        if not search_term:
            return jsonify({'success': False, 'message': 'Termo de busca é obrigatório'})
        
        # Detectar tentativas de SQL Injection
        if detect_sql_injection(search_term):
            logger.warning(f"🚨 Tentativa de SQL Injection bloqueada - Search: {search_term}")
            return jsonify({
                'success': False, 
                'message': 'Tentativa de ataque detectada e bloqueada!'
            })
        
        # Validar entrada
        search_term = validate_input(search_term, 100)
        if not search_term:
            return jsonify({'success': False, 'message': 'Termo de busca inválido'})
        
        # MITIGAÇÃO: Usar prepared statements
        query = "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s"
        search_param = f"%{search_term}%"
        
        # Log da query segura
        logger.info(f"Executando busca segura para: {search_term}")
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                # SEGURO: Usar parâmetros
                cursor.execute(query, (search_param, search_param))
                products = cursor.fetchall()
                
                return jsonify({
                    'success': True,
                    'products': products,
                    'message': f'{len(products)} produto(s) encontrado(s)'
                })
                
            except mysql.connector.Error as err:
                logger.error(f"Erro na query de busca: {err}")
                return jsonify({'success': False, 'message': 'Erro interno do servidor'})
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'success': False, 'message': 'Erro de conexão'})
    
    return render_template('search_secure.html')

@app.route('/users')
def users():
    """Página para listar usuários (apenas para admins) - COM AUTORIZAÇÃO"""
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    if session.get('role') != 'admin':
        logger.warning(f"🚨 Tentativa de acesso não autorizado por: {session.get('username')}")
        return jsonify({'error': 'Acesso negado - Apenas administradores'}), 403
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            # Não expor senhas
            cursor.execute("SELECT id, username, email, role, created_at FROM users")
            users = cursor.fetchall()
            return jsonify({'users': users})
        except mysql.connector.Error as err:
            logger.error(f"Erro: {err}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'error': 'Erro de conexão'}), 500

@app.route('/logout')
def logout():
    """Logout do usuário"""
    username = session.get('username', 'Usuário desconhecido')
    session.clear()
    logger.info(f"Logout realizado: {username}")
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

@app.route('/security-status')
def security_status():
    """Endpoint para mostrar status de segurança"""
    return jsonify({
        'security_measures': [
            'Prepared Statements (SQL Injection Protection)',
            'Input Validation and Sanitization',
            'SQL Injection Pattern Detection',
            'Proper Error Handling',
            'Session Management',
            'Authorization Checks',
            'Security Logging'
        ],
        'status': 'SECURE',
        'message': 'Todas as mitigações estão ativas'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 