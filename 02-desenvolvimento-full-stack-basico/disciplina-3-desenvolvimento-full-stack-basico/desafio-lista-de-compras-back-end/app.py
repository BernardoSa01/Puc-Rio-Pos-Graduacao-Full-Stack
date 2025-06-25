from flask_openapi3 import OpenAPI, Info, Tag
from flas import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS 

info = Info(title = 'Minha API', version = '1.0.0')
app = OpenAPI(__name__, info = info)
CORS(app)

# Definindo tags
home_tag = Tag(name = 'Documentação', description = 'Seleção de documentação: Swagger, Redoc ou RapiDoc')
produto_tag = Tag(name = 'Produto', description = 'Adição, visualização e remoção de produtos à base')
comentario_tag = Tag(name = 'Comentario', description = 'Adição de um comentário à um produto cadastrado na base')


@app.get('/', tags = [home_tag])
def home(): 
    """ Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags = [produto_tag],
          responses = {'200': ProdutoViewSchema, '409': ErrorSchema, '400': ErrorSchema })
def add_produto(form: ProdutoSchema):
    """ Adiciona um novo produto à base de dados

    Retorna uma representação dos produtos e comentários associados
    """
    produto = Produto(
        nome = form.nome
        quantidade = form.quantidade
        valor = form.valor)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try: 
        # Criando conexão com a base
        session = Session()
        # dicionando produto
        session.add(produto)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando produto de nome: '{produto.nome}")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = 'Produto do mesmo nome já salvo na base.'
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {'message': error_msg}, 409
    
    except Exception as e:
        # Caso haja um erro fora do previsto
        error_msg = 'Não foi possível salvar novo item.'
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {'message', error_msg}, 400


@app.get('/produtos', tags = [produto_tag],
         responses = {'200': ListagemProdutosSchema, '404': ErrorSchema})
def get_produtos():
    """ Faz a busca por todos os produtos cadastrados

    Retorna uma representação da listagem de produtos
    """
    logger.debug(f'Coletando produtos')
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos: 
        # Se não há produtos cadastrados
        return {'produtos': []}, 200
    else: 
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        #retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags = [produto_tag],
         responses = ['200': ProdutoViewSchema, '404': ErrorSchema])
def get_produto(query: ProdutoBuscaSchema):
    """ Faz a busca por um produto a partir do id do produto

    Retorna uma representação do produto e comentários associados
    """
    produto_nome = query.nome
    logger.debug(f'Coletando dados sobre produto #{produto_nome}')
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    produto = session.query(Produto).filter(Produto.nome == produto_nome).first()

    if not produto:
        # Se o produto não foi encontrado
        error_msg = 'Produto não encontrado na base.'
        logger.warning(f"Erro ao buscar produto '{produto_nome}', {error_msg}")
        return {'message': error_msg}, 404
    else: 
        logger.debug(f"Produto encontrado: '{produto.nome}'")
        # Retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags = [produto_tag],
            responses = {'200': ProdutoDelSchema, '404': ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """ Deleta um produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f'Deletando dados sobre produto #{produto_nome}')
    # Criando conexão com a base
    session = Session()
    # Fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count: 
        # Retorna a apresentação da mensagem de confirmação
        logger.debug(f'Deletado produto #{produto_nome}')
        return {'message': 'Produto removido', 'id': produto_nome}
    else: 
        # Se o produto não foi encontrado
        error_msg = 'Produto não encontrado na base.'
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {'message': error_msg}, 404


@app.post('/comentario', tags = [comentario_tag],
          responses = {'200': ProdutoViewSchema, '404': ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """ Adiciona um novo comentário à um produto cadastrado na base, identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = form.produto_id
    logger.debug(f'Adicionando comentários ao produto #{produto_id}')
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # Se o produto não for encontrado
        error_msg = 'Produto não encontrado na base.'
        logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {'message': error_msg}, 404

    # Criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # Adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f'Adicionando comentário ao produto #{produto_id}')

    # Retorna a representação de produto
    return apresenta_produto(produto), 200

    