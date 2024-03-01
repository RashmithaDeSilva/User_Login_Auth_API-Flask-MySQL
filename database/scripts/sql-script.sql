USE chatbot;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    email VARCHAR(250) UNIQUE,
    password VARCHAR(250)
);

INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', '$2b$12$NAtSvoCpsLkkdV5Sylp9/uDjsTUj/5CVz1OnxWyRwGESCJGTfA0ue');
