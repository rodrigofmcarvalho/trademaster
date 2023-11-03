import os
import psycopg2

from faker import Faker
from dataclasses import dataclass

# Configurações do banco de dados
DATABASE = os.environ.get('DB_NAME')
USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')

fake = Faker('pt_BR')

@dataclass
class Cliente:
    nome: str
    email: str
    telefone: str
    cpf: str
    endereco: str
    numero: int
    cidade: str
    estado: str
    cep: str
    cartao_de_credito: str

@dataclass
class Funcionario:
    nome: str
    email: str
    telefone: str
    cpf: str
    endereco: str
    numero: int
    cidade: str
    estado: str
    cep: str
    cargo: str
    expediente: str

@dataclass
class Franquia:
    nome: str
    endereco: str
    cidade: str
    estado: str
    cep: str

@dataclass
class Item:
    tipo: str
    titulo: str
    descricao: str
    preco: float
    disponivel_para_aluguel: bool


def generate_cliente() -> Cliente:
    return Cliente(
        nome=fake.name(),
        email=fake.email(),
        telefone=fake.phone_number(),
        cpf=fake.unique.cpf(),
        endereco=fake.street_address(),
        numero=fake.random_int(min=1, max=9999),
        cidade=fake.city(),
        estado=fake.state(),
        cep=fake.postcode(),
        cartao_de_credito=fake.credit_card_number()
    )

def generate_funcionario() -> Funcionario:
    return Funcionario(
        nome=fake.name(),
        email=fake.email(),
        telefone=fake.phone_number(),
        cpf=fake.unique.cpf(),
        endereco=fake.street_address(),
        numero=fake.random_int(min=1, max=9999),
        cidade=fake.city(),
        estado=fake.state(),
        cep=fake.postcode(),
        cargo=fake.job(),
        expediente=fake.random_element(elements=("Manha", "Tarde", "Noite"))
    )

def generate_franquia() -> Franquia:
    return Franquia(
        nome=fake.company(),
        endereco=fake.street_address(),
        cidade=fake.city(),
        estado=fake.state(),
        cep=fake.postcode()
    )

def generate_item() -> Item:
    return Item(
        tipo=fake.random_element(elements=("Livro", "Filme", "DVD de Serie")),
        titulo=fake.catch_phrase(),
        descricao=fake.text(),
        preco=fake.random_number(digits=5, fix_len=False) / 100,
        disponivel_para_aluguel=fake.boolean()
    )

def main():
    connection = psycopg2.connect(database='postgres', user='postgres', password='admin', host='localhost', port='5432')
    cursor = connection.cursor()

    for _ in range(10000):
        cliente = generate_cliente()
        funcionario = generate_funcionario()
        franquia = generate_franquia()
        item = generate_item()

        cursor.execute("""
            INSERT INTO Clientes (Nome, Email, Telefone, CPF, Endereco, Numero, Cidade, Estado, CEP, CartaoDeCredito) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (cliente.nome, cliente.email, cliente.telefone, cliente.cpf, cliente.endereco, cliente.numero, cliente.cidade, cliente.estado, cliente.cep, cliente.cartao_de_credito))

        cursor.execute("""
            INSERT INTO Funcionarios (Nome, Email, Telefone, CPF, Endereco, Numero, Cidade, Estado, CEP, Cargo, Expediente) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (funcionario.nome, funcionario.email, funcionario.telefone, funcionario.cpf, funcionario.endereco, funcionario.numero, funcionario.cidade, funcionario.estado, funcionario.cep, funcionario.cargo, funcionario.expediente))

        cursor.execute("""
            INSERT INTO Franquias (Nome, Endereco, Cidade, Estado, CEP) 
            VALUES (%s, %s, %s, %s, %s)
        """, (franquia.nome, franquia.endereco, franquia.cidade, franquia.estado, franquia.cep))

        cursor.execute("""
            INSERT INTO Itens (Tipo, Titulo, Descricao, Preco, DisponivelParaAluguel) 
            VALUES (%s, %s, %s, %s, %s)
        """, (item.tipo, item.titulo, item.descricao, item.preco, item.disponivel_para_aluguel))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
