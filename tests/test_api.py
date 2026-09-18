from app.models.produto import Produto 
from app.models.categoria import Categoria

#Teste para verificar se a tela funciona!
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

    #Criando um produto para teste
    produto = Produto(nome="Boné Aba Reta", preco=129.90, estoque_atual=50, categoria_id=categoria.id)
    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.get("/produtos/")

    #Teste se existe o Boné  na listagem de produtos
    assert "Boné Aba Reta" in resposta.text