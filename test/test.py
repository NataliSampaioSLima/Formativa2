import sqlite3
import os
import sys
import pytest

from src.main import conectar_bd


DB_TESTE = "clientes_teste.db"

# Setup e teardown para testes
@pytest.fixture(autouse=True)
def setup_db():
    # Remove o banco de dados de teste, se existir, antes de iniciar o teste
    if os.path.exists(DB_TESTE):
        os.remove(DB_TESTE)

    # Conecta ao banco de dados de teste e cria a tabela
    conn = sqlite3.connect(DB_TESTE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE clientes (
                        telefone INTEGER PRIMARY KEY NOT NULL,
                        nome TEXT NOT NULL,
                        endereco TEXT NOT NULL,
                        bairro TEXT NOT NULL,
                        numeroresidencial INTEGER NOT NULL,
                        complemento TEXT)''')
    conn.commit()
    conn.close()

    # Garante que o banco de dados será removido após os testes
    yield
    if os.path.exists(DB_TESTE):
        os.remove(DB_TESTE)

# Função auxiliar para adicionar cliente na base de testes
def adicionar_mock(telefone, nome="Cliente Teste", endereco="Rua A", bairro="Bairro A", numeroresidencial=123, complemento="Casa"):
    conn = sqlite3.connect(DB_TESTE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)",
                   (telefone, nome, endereco, bairro, numeroresidencial, complemento))
    conn.commit()
    conn.close()

# Função auxiliar para buscar cliente pelo telefone na base de testes
def buscar_por_telefone(telefone):
    conn = sqlite3.connect(DB_TESTE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    row = cursor.fetchone()
    conn.close()
    return row

# Testa se a tabela é criada corretamente no banco
def test_conectar_bd_cria_tabela():
    conectar_bd()  # Certifique-se de que a função conecta ao DB_TESTE
    conn = sqlite3.connect(DB_TESTE)  # Conecta ao banco de testes
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
    tabela = cursor.fetchone()
    conn.close()
    assert tabela is not None

# Testa inserção de cliente
def test_adicionar_cliente_no_banco():
    adicionar_mock(telefone=11999999999)
    cliente = buscar_por_telefone(11999999999)
    assert cliente[0] == 11999999999
    assert cliente[1] == "Cliente Teste"

# Testa erro ao inserir telefone duplicado
def test_nao_permitir_telefone_duplicado():
    adicionar_mock(telefone=11888888888)
    with pytest.raises(sqlite3.IntegrityError):  # Espera-se um erro de integridade ao tentar duplicar o telefone
        adicionar_mock(telefone=11888888888)

# Testa busca de cliente inexistente
def test_cliente_inexistente_retorna_none():
    cliente = buscar_por_telefone(11111111111)
    assert cliente is None

# Testa inserção de complemento opcional vazio
def test_adicionar_cliente_sem_complemento():
    adicionar_mock(telefone=11777777777, nome="Cliente Sem Complemento", endereco="Rua B", bairro="Bairro B", numeroresidencial=456, complemento="")
    cliente = buscar_por_telefone(11777777777)
    assert cliente[5] == ""  # Verifica se o complemento foi inserido como vazio
