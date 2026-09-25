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