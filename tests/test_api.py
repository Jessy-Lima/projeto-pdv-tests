from app.models.produto import Produto 
from app.models.categoria import Categoria
from app.models.cliente import Cliente

# Teste para verificar se a tela funciona!
def test_listar_produtos_retorna_200(cliente):

    resposta = cliente.get("/produtos/")

    # 200 = ok, a página carregou sem erro.
    assert resposta.status_code == 200

# Teste a tela de produtos sem o login
def test_listagem_produtos_sem_login():
    from fastapi.testclient import TestClient
    from app.main import app

    cliente_sem_login = TestClient(app)

    resposta = cliente_sem_login.get("/produtos/")

    assert resposta.status_code == 401

# Teste página de lista de produtos criada com sucesso
def test_verificar_produto_criando_com_sucesso(cliente, db_session_test):

    categoria = Categoria(nome="Bonés")
    db_session_test.add(categoria)
    db_session_test.commit()

    # Criando um produto para teste
    produto = Produto(
        nome="Boné Aba Reta",
        preco=129.90,
        estoque_atual=50,
        categoria_id=categoria.id
    )

    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.get("/produtos/")

    # Teste se existe o Boné na listagem de produtos
    assert "Boné Aba Reta" in resposta.text

# Testar se a busca retorna somente os produtos filtrados
def test_listar_produtos_filtrado_por_busca(cliente, db_session_test):

    produto = Produto(
        nome="Camisa Nike",
        preco=99.90,
        estoque_atual=500
    )

    produto1 = Produto(
        nome="Caneca Harry Potter",
        preco=139.90,
        estoque_atual=60
    )

    db_session_test.add(produto)
    db_session_test.add(produto1)
    db_session_test.commit()

    resposta = cliente.get("/produtos", params={"busca": "Harry"})

    assert "Caneca Harry Potter" in resposta.text
    assert "Camisa Nike" not in resposta.text

# Exercício = verificar se a busca da rota cliente funciona
def test_verificar_busca_rota_cliente_funciona(cliente, db_session_test):

    cliente1 = Cliente(
        nome="Helen",
        matricula=325,
        telefone=11934565364
    )

    cliente2 = Cliente(
        nome="Jose",
        matricula=765,
        telefone=11963452364
    )

    db_session_test.add(cliente1)
    db_session_test.add(cliente2)
    db_session_test.commit()

    resposta = cliente.get("/clientes", params={"busca": "Jose"})

    assert "Jose" in resposta.text
    assert "Helen" not in resposta.text