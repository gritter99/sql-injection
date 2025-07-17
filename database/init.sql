-- Criação da tabela de usuários para demonstração de SQL Injection
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('user1', 'password123', 'user1@example.com', 'user'),
('user2', 'mypassword', 'user2@example.com', 'user'),
('testuser', 'test123', 'test@example.com', 'user');

-- Criar tabela de produtos para demonstração adicional
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir produtos de exemplo
INSERT INTO products (name, description, price, category) VALUES
('Produto A', 'Descrição do produto A', 29.99, 'categoria1'),
('Produto B', 'Descrição do produto B', 49.99, 'categoria2'),
('Produto C', 'Descrição do produto C', 19.99, 'categoria1'),
('Produto D', 'Descrição do produto D', 99.99, 'categoria3'); 