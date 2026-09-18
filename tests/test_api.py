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

