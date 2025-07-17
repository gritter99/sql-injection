from flask import Flask, request, render_template, jsonify, session
import mysql.connector
import os
import logging

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key'

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'appuser'),
    'password': os.getenv('DB_PASSWORD', 'apppassword'),
    'database': os.getenv('DB_NAME', 'vulnerable_app')
}

# Configurar logging para debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Função para obter conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Erro ao conectar ao banco: {err}")
        return None

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login VULNERÁVEL a SQL Injection"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABILIDADE: Query SQL sem sanitização
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        # Log da query para debug (útil para demonstração)
        logger.info(f"Executando query: {query}")
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query)
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user['id']  # type: ignore
                    session['username'] = user['username']  # type: ignore
                    session['role'] = user['role']  # type: ignore
                    return jsonify({
                        'success': True, 
                        'message': f'Login realizado com sucesso! Bem-vindo, {user["username"]}',  # type: ignore
                        'user': user
                    })
                else:
                    return jsonify({'success': False, 'message': 'Credenciais inválidas'})
                    
            except mysql.connector.Error as err:
                logger.error(f"Erro na query: {err}")
                return jsonify({'success': False, 'message': f'Erro no banco de dados: {err}'})
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'success': False, 'message': 'Erro de conexão com o banco'})
    
    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Página de busca VULNERÁVEL a SQL Injection"""
    if request.method == 'POST':
        search_term = request.form['search_term']
        
        # VULNERABILIDADE: Query SQL sem sanitização
        query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        
        # Log da query para debug
        logger.info(f"Executando query de busca: {query}")
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query)
                products = cursor.fetchall()
                
                return jsonify({
                    'success': True,
                    'products': products,
                    'query': query  # Mostrar query para fins educacionais
                })
                
            except mysql.connector.Error as err:
                logger.error(f"Erro na query de busca: {err}")
                return jsonify({'success': False, 'message': f'Erro no banco: {err}'})
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'success': False, 'message': 'Erro de conexão'})
    
    return render_template('search.html')

@app.route('/users')
def users():
    """Página para listar usuários (apenas para admins)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    if session.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, username, email, role, created_at FROM users")
            users = cursor.fetchall()
            return jsonify({'users': users})
        except mysql.connector.Error as err:
            return jsonify({'error': f'Erro: {err}'}), 500
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'error': 'Erro de conexão'}), 500

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 