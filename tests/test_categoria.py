from app.models.categoria import Categoria

# Teste criar categoria com sucesso
def test_criar_categoria_com_sucesso(cliente, db_session_test):

    resposta = cliente.post(
        "/categorias/nova",
        data={"nome": "Eletrônicos"},
        follow_redirects=False
    )

    assert resposta.status_code == 302
    assert resposta.headers["location"] == "/categorias?criado=ok"

    categoria = db_session_test.query(Categoria).filter(
        Categoria.nome == "Eletrônicos"
    ).first()

    assert categoria is not None
    assert categoria.nome == "Eletrônicos"


# Teste não permitir categoria duplicada
def test_criar_categoria_duplicada(cliente, db_session_test):

    categoria = Categoria(nome="Eletrônicos")

    db_session_test.add(categoria)
    db_session_test.commit()

    resposta = cliente.post(
        "/categorias/nova",
        data={"nome": "Eletrônicos"},
        follow_redirects=False
    )

    assert resposta.status_code == 400
    assert "Já existe uma categoria com este nome." in resposta.text

#Teste editar categoria nova
def test_editar_produto_atualiza_campos(cliente, db_session_test):
    #Criar um produto novo no banco
    categoria = Categoria(nome="Nome antigo")
    db_session_test.add(categoria)
    db_session_test.commit()

    resposta = cliente.post(
        f"/categorias/{categoria.id}/editar",
        data={"nome": "Nome novo", "preco": "30.0", "estoque_atual": "6"},
        follow_redirects=False
    )

    assert resposta.status_code == 302

    buscar_produto = db_session_test.query(Categoria).filter(Categoria.id == categoria.id).first()
    assert buscar_produto.nome == "Nome novo"

# Testar listagem de categorias
def test_listar_categorias(cliente, db_session_test):

    categoria = Categoria(nome="Boné")
    categoria1 = Categoria(nome="Camisa")

    db_session_test.add(categoria)
    db_session_test.add(categoria1)
    db_session_test.commit()

    resposta = cliente.get("/categorias")

    assert resposta.status_code == 200
    assert "Boné" in resposta.text
    assert "Camisa" in resposta.text