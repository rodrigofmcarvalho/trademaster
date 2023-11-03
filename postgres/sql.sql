CREATE TABLE Clients (
    id_client SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    cep VARCHAR(10) NOT NULL,
    credit_card_number VARCHAR(20) NOT NULL
);

CREATE TABLE Employees (
    id_employee SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    cep VARCHAR(10) NOT NULL,
    role VARCHAR(100) NOT NULL,
    shift VARCHAR(10) CHECK (shift IN ('Morning', 'Afternoon', 'Night'))
);

CREATE TABLE Franchises (
    id_franchise SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    cep VARCHAR(10) NOT NULL
);

CREATE TABLE Items (
    id_item SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    available_for_rental BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE Transactions (
    id_transaction SERIAL PRIMARY KEY,
    item_id INT REFERENCES Items(id_item),
    client_id INT REFERENCES Clients(id_client),
    employee_id INT REFERENCES Employees(id_employee),
    franchise_id INT REFERENCES Franchises(id_franchise),
    transaction_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    transaction_total_amount DECIMAL(10, 2) NOT NULL,
    transaction_status VARCHAR(10) NOT NULL
);

CREATE TABLE Inventory (
    id_inventory SERIAL PRIMARY KEY,
    item_id INT REFERENCES Items(id_item),
    franchise_id INT REFERENCES Franchises(id_franchise),
    quantity INT NOT NULL CHECK (quantity >= 0)
);