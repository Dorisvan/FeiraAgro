# Bibliotecas e classes
import hashlib
import json
import smtplib

from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from email.message import EmailMessage
from datetime import date
from werkzeug.utils import secure_filename
import datetime


import mysql.connector
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import os
import ssl

from models.Usuario import Usuario
from models.UsuarioDAO import UsuarioDAO
from models.Produto import Produto
from models.ProdutoDAO import ProdutoDAO
from models.Perfil_Produtor import Perfil_Produtor
from models.Perfil_ProdutorDAO import Perfil_ProdutorDAO
from models.Pedido import Pedido
from models.PedidoDAO import PedidoDAO
from models.Mensagem import Mensagem
from models.MensagemDAO import MensagemDAO


# Variáveis gerais

app = Flask(__name__)
app.secret_key = "senha123"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "feiraagro"

# Autorizações

app.auth = {
    # acao: { perfil:permissao }
    'painel': {0:1, 1:1},
    'logout': {0:1, 1:1},
    'perfil_produtor': {0:1, 1:1},
    'visualizar_perfil': {0:1, 1:1},
    'area_do_usuario': {0:1, 1:1},
    'cadastrar_produto': {0:1, 1:1},
    'listar_perfis': {0:1, 1:1}

}


@app.before_request
def autorizacao():
    acao = request.path[1:]
    acao = acao.split('/')
    if len(acao)>=1:
        acao = acao[0]

    acoes = app.auth.keys()
    if acao in list(acoes):
        if session.get('logado') is None:
            return redirect(url_for('login'))
        else:
            estado_login = session['logado']['estado_login']
            if app.auth[acao][estado_login]==0:
                return redirect(url_for('painel'))

@app.route('/verificar_login')
def verificar_login():
    try:
        informacoes_usuario = session.get('logado')
        estado_login = informacoes_usuario['estado_login']
    except:
        estado_login = "Logout"

    return estado_login


@app.route('/verificar_tipo_usuario')
def verificar_tipo_usuario():
    try:
        informacoes_usuario = session.get('logado')
        tipo = informacoes_usuario['tipo']
    except:
        tipo = "Sem_identificação"

    return tipo


# Conexão com o banco de dados

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Páginas simples

@app.route('/')
def index():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    if resultado_login != "Logout":
        resultado_perfil = verificar_perfil("ambos")

    return render_template("index.html", estado_login = resultado_login, tipo_usuario=tipo_usuario)


@app.route('/portfolio')
def portfolio():
    return render_template("#portfolio", titulo="Painel")


@app.route('/painel')
def painel():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    return render_template("painel.html", titulo="Painel", estado_login=resultado_login, tipo_usuario=tipo_usuario)


# Funções de Cadastro/Login/Logout


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        endereco = request.form['endereco']
        tipo = request.form['tipo']
        contato = request.form['contato']
        estado_login = 0
        nivel = 0
        imagem_perfil = ""

        usuario = Usuario(nome, email, senha, endereco, tipo, nivel, contato, estado_login, imagem_perfil)

        dao = UsuarioDAO(get_db())
        codigo = dao.Inserir(usuario)
        print(codigo)

        if codigo >= 0:
            flash("Usuário cadastrado com sucesso!", "success")
        else:
            flash("Erro ao cadastrar!", "danger")

    vartitulo = "Cadastro"
    return render_template("cadastro.html", titulo=vartitulo, estado_login=resultado_login, tipo_usuario=tipo_usuario)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar dados
        dao = UsuarioDAO(get_db())
        usuario = dao.autenticar(email, senha)

        if usuario is not None:
            session['logado'] = {
                'codigo': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'tipo': usuario[5],
                'nivel': usuario[6],
                'estado_login': usuario[8],
            }
            return redirect(url_for('painel'))
        else:
            flash("Erro ao efetuar login! Verifique seus dados novamente.", "danger")

    return render_template("login.html", titulo="Login")


# Função de login com Google
@app.route('/login_google')
def login_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid'])

    flow.redirect_uri = 'http://localhost/retorno'

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

    #return flask.redirect(authorization_url)
    return redirect(authorization_url)

@app.route('/retorno')
def retorno():
    state = request.args.get('state')
    code = request.args.get('code')

    if code is None or code =='':
        flash("Erro ao logar com conta do google.", "danger")
        return redirect(url_for('login'))


    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid'],
        state=state)
    flow.redirect_uri = url_for('retorno', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    resposta_api = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + credentials.token)
    info_usuario = resposta_api.json()

    email_busc = str(info_usuario['email'])
    print((info_usuario['email']))

    dao = UsuarioDAO(get_db())

    user = dao.Buscar_email(email_busc)
    print(user)

    if user is None:
        hash = hashlib.sha512()
        senha = os.urandom(50)
        secret = app.config['SECRET_KEY']
        hash.update(f'{secret}{senha}'.encode('utf-8'))
        senha_criptografada = hash.hexdigest()

        usuario = Usuario(info_usuario['name'], info_usuario['email'], senha_criptografada, "", "", 0,"", "", "")

        id = None

        if usuario.nome and usuario.email and usuario.senha:
            id = dao.Inserir(usuario)

        if id is None or id <= 0:
            flash("Erro ao cadastrar usuário.", "danger")
            return redirect(url_for("login"))
        else:
            user = dao.autenticar(usuario.email, usuario.senha)
            print(user)

    session['logado'] = {
        'codigo': user[0],
        'nome': user[1],
        'email': user[2],
        'tipo': user[5],
        'nivel': user[6],
        'estado_login': user[8],
    }


    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                               params={'token': credentials.token},
                               headers={'content-type': 'application/x-www-form-urlencoded'})
    return redirect('painel')



@app.route('/logout')
def logout():
    session['logado'] = None
    session.clear()
    return redirect(url_for('index'))


@app.route('/verificar_perfil, <tipo>')
def verificar_perfil(tipo):
    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    dao_pf = Perfil_ProdutorDAO(get_db())
    dao_u = UsuarioDAO(get_db())

    teste1 = dao_u.Verificacao_perfil(usuario_codigo)
    teste2 = dao_pf.Verificacao_perfil(usuario_codigo)

    print(teste1)
    print(teste2)

    if tipo == "Ambos":
        if teste1 == "Ok" and teste2 == "Ok":
            return "Ok"

        elif teste1 == "Pendente":
            return redirect(url_for('area_do_usuario'))

        elif teste2 == "Pendente":
            return redirect(url_for("perfil_produtor"))

        else:
            pass

    elif tipo == "teste1":
        if teste1 == "Ok":
            return "Ok"
        else:
            return "Pendente"

    else:
        if teste2 == "Ok":
            return "Ok"
        else:
            return "Pendente"




# Função de upload arquivos

@app.route('/baixar_arquivo, <codigo>, <arquivo>, <nome>, <tipo>, <classificacao>')
def baixar_arquivo(codigo, imagem, tipo, classificacao, nome):
    try:
        os.mkdir("perfis/"+str(codigo))
        os.mkdir("perfis/" + str(codigo) +"/produtos")
        os.mkdir("perfis/" + str(codigo) + "/perfil_usuario")
        os.mkdir("perfis/" + str(codigo) + "/perfil_produtor")
    except:
        pass

    pasta_upload_produtos = os.path.join(os.getcwd(), "perfis/" + str(codigo) + "/produtos")
    pasta_upload_perfil_usuario = os.path.join(os.getcwd(), "perfis/" + str(codigo) + "/perfil_usuario")
    pasta_upload_perfil_produtor = os.path.join(os.getcwd(), "perfis/" + str(codigo) + "/perfil_produtor")

    if classificacao == "criacao":
        if tipo == "produtos":
            arquivo = os.path.join(pasta_upload_produtos, secure_filename(imagem.filename))
            imagem.save(arquivo)
        elif tipo == "perfil_usuario":
            arquivo = os.path.join(pasta_upload_perfil_usuario, secure_filename(imagem.filename))
            imagem.save(arquivo)
        elif tipo == "perfil_produtor":
            arquivo = os.path.join(pasta_upload_perfil_produtor, secure_filename(imagem.filename))
            imagem.save(arquivo)
        else:
            print("Erro ao executar função de baixar arquivos")
    else:
        if tipo == "produtos":
            os.remove(pasta_upload_produtos + "/" + nome)
            arquivo = os.path.join(pasta_upload_produtos, secure_filename(imagem.filename))
            imagem.save(arquivo)
        elif tipo == "perfil_usuario":
            os.remove(pasta_upload_perfil_usuario + "/" + nome)
            arquivo = os.path.join(pasta_upload_perfil_usuario, secure_filename(imagem.filename))
            imagem.save(arquivo)
        elif tipo == "perfil_produtor":
            os.remove(pasta_upload_perfil_produtor + "/" + nome)
            arquivo = os.path.join(pasta_upload_perfil_produtor, secure_filename(imagem.filename))
            imagem.save(arquivo)
        else:
            print("Erro ao executar função de baixar arquivos")


# Funções de CREATE

@app.route('/cadastrar_produto',  methods=['GET', 'POST'])
def cadastrar_produto():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    daoUsuario = UsuarioDAO(get_db())
    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel']
    usuario_codigo = informacoes_usuario['codigo']

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form['valor']
        classificacao = request.form['classificacao']
        procedencia = request.form['procedencia']
        descricao = request.form['descricao']
        imagem_produto = request.files['img_produto']
        nome_imagem = imagem_produto.filename

        baixar_arquivo(usuario_codigo, imagem_produto, "produtos", "criacao", nome_imagem)

        produto = Produto(nome, quantidade, valor, classificacao, procedencia, nome_imagem, descricao, usuario_codigo)

        dao = ProdutoDAO(get_db())
        codigo = dao.Inserir(produto)

        if codigo > 0:
            flash("Solicitação cadastrada com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar solicitação! Verifique seus dados novamente.", "danger")

    #produtos_db = daoProduto.Listar(produto_codigo, "Checagem_individual")

    if resultado_login != "Logout":
        resultado_perfil = verificar_perfil("Ambos")

    if resultado_perfil == "Ok":
        return render_template("cadastrar_produto.html", titulo="Cadastrar_Produto", estado_login=resultado_login, tipo_usuario=tipo_usuario)
    else:
        return redirect(url_for("verificar_perfil", tipo="Ambos"))


@app.route('/cadastrar_pedido'
           ', <codigo_produto>', methods=['GET','POST'])
def cadastrar_pedido(codigo_produto):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    dao1 = PedidoDAO(get_db())
    dao2 = ProdutoDAO(get_db())

    produtos_db = dao2.Listar(codigo_produto, "Checagem_individual")

    if request.method == "POST":
        situacao = "Não entregue"
        data_pedido = date.today()
        data_entrega = request.form['data_entrega']
        modo_entrega = request.form['modo_entrega']
        quantidade = request.form['quantidade']
        status_compra = "Não finalizada"

        pedido = Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, status_compra, usuario_codigo, codigo_produto)
        dao1.Inserir(pedido)

        valor_atualizado = produtos_db[2] - int(quantidade)
        dao2.Atualizar_quantidade(codigo_produto, valor_atualizado)
        # produto = Produto(produtos_db)
        # produto.setcodigo(codigo_produto)

    else:
        pass

    if resultado_login != "Logout":
        resultado_perfil = verificar_perfil("ambos")

    if resultado_perfil == "Ok":
        return render_template("cadastrar_pedido.html", produto = produtos_db, estado_login=resultado_login, tipo_usuario=tipo_usuario)
    else:
        return redirect(url_for("verificar_perfil", tipo="ambos"))


@app.route('/visualizar_produtos, <codigo_produtor>',  methods=['GET', 'POST'])
def visualizar_produtos(codigo_produtor):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    dao = ProdutoDAO(get_db())

    if codigo_produtor == "None":
        produtos = dao.Visualizar(None)
        print('a')
        produtos = list(produtos)
        produtos_db = produtos
        tipo = "todos"
    else:
        produtos = dao.Visualizar(codigo_produtor)
        print(produtos)
        produtos = list(produtos)
        print(produtos)
        produtos_db = list(produtos)
        tipo = "individual"


    return render_template("visualizar_produtos.html", produtos=produtos_db, tipo=tipo, usuario_codigo=usuario_codigo, estado_login=resultado_login, tipo_usuario=tipo_usuario)



@app.route('/editar_produto, <codigo_produto>', methods=['GET', 'POST'])
def editar_produto(codigo_produto):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    informacoes_usuario = session.get('logado')
    dao = ProdutoDAO(get_db())
    usuario_codigo = informacoes_usuario['codigo']

    produto_db = dao.Listar(codigo_produto, "Checagem_individual")
    produto_db = list(produto_db)
    nome_antigo = produto_db[6]
    print(nome_antigo)

    if request.method == "POST":
        nome = request.form['nome']
        classificacao = request.form['classificacao']
        valor = request.form['valor']
        quantidade = request.form['quantidade']
        procedencia = request.form['procedencia']
        descricao = request.form['descricao']
        imagem_produto = request.files['img_produto']

        print(imagem_produto)

        if str(imagem_produto) == "<FileStorage: '' ('application/octet-stream')>":
            nome_imagem = produto_db[6]
        else:
            nome_imagem = imagem_produto.filename
            baixar_arquivo(usuario_codigo, imagem_produto, "produtos", "edicao", nome_antigo)


        produto = Produto(nome, quantidade, valor, classificacao, procedencia, nome_imagem, descricao)
        produto.setCodigo(codigo_produto)
        ret = dao.Editar_produto(produto)

        if ret > 0:
            flash("Atualizado com sucesso! Código %s" % codigo_produto, "success")
        else:
            flash("Erro ao atualizar!", "danger")

    produto_db = dao.Listar(codigo_produto, "Checagem_individual")
    produto_db = list(produto_db)

    return render_template("editar_produto.html", produto=produto_db, estado_login=resultado_login, tipo_usuario=tipo_usuario)


@app.route('/editar_pedido, <codigo_pedido>', methods=['GET', 'POST'])
def editar_pedido(codigo_pedido):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao1 = PedidoDAO(get_db())
    dao2 = ProdutoDAO(get_db())

    pedido_db = dao1.Listar(codigo_pedido, "Checagem_individual")
    data_pedido = pedido_db[1]
    situacao = pedido_db[4]
    status_compra = pedido_db[6]
    usuario_codigo = pedido_db[7]
    codigo_produto = pedido_db[8]


    if pedido_db[4] == "Não entregue" and pedido_db[6] != "Finalizado":
        if request.method == "POST":
            data_entrega = request.form['data_entrega']
            modo_entrega = request.form['modo_entrega']
            quantidade = request.form['quantidade']

            pedido = Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, status_compra, usuario_codigo, codigo_produto)
            pedido.setCodigo(codigo_pedido)
            ret = dao1.Atualizar(pedido)

            #valor_atualizado = produtos_db[2] - int(quantidade)

            if ret > 0:
                flash("Atualizado com sucesso! Código %s" % codigo_pedido, "success")
            else:
                flash("Erro ao atualizar!", "danger")

        pedido_db = dao1.Listar(codigo_pedido, "Checagem_individual")
        return render_template("editar_pedido.html", pedido=pedido_db, estado_login=resultado_login, tipo_usuario=tipo_usuario,)
    else:
        flash("Aparentemente o pedido em questão já encontra-se finalizado ou entregue.", "danger")
        return redirect(url_for('visualizar_pedido', tipo="Meus"))



@app.route('/visualizar_mensagens, <tipo>',  methods=['GET', 'POST'])
def visualizar_mensagens(tipo):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao = MensagemDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    mensagens = dao.Listar(usuario_codigo, tipo)
    mensagens = list(mensagens)

    return render_template("visualizar_mensagens.html", mensagens=mensagens, estado_login=resultado_login, tipo_usuario=tipo_usuario)



@app.route('/area_do_usuario', methods=['GET','POST'])
def area_do_usuario():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()
    resultado = verificar_perfil("teste1")
    print(resultado)

    if resultado != "Ok":
        flash("Foi notado que algumas informações do seu perfil não encontram-se preenchidas. É importante preenchê-las para poder ter acesso a todas as funcionalidades do FeiraAgro.", "danger")
    else:
        pass

    dao = UsuarioDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel']
    usuario_codigo = informacoes_usuario['codigo']


    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        endereco = request.form['endereco']
        tipo = request.form['tipo']
        contato = request.form['contato']
        nivel = 0

        usuario = Usuario(nome, email, senha, endereco, tipo, nivel, contato)
        usuario.setCodigo(usuario_codigo)
        ret = dao.Atualizar(usuario)

        if ret > 0:
            flash("Atualização concluída com sucesso!" , "success")
            usuario = dao.autenticar(email, senha)

            if usuario is not None:
                session['logado'] = {
                    'codigo': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'tipo': usuario[5],
                    'nivel': usuario[6],
                    'estado_login': usuario[8],
                }
        else:
            flash("Erro ao atualizar!", "danger")


    usuario_db = dao.Listar(usuario_codigo, "Checagem_individual")
    vartitulo = "Atualizar_usuario"
    return render_template("area_do_usuario.html", titulo=vartitulo, usuario = usuario_db, estado_login=resultado_login, tipo_usuario=tipo_usuario)

@app.route('/perfil_produtor', methods=['GET','POST'])
def perfil_produtor():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()
    resultado = verificar_perfil("teste2")
    print(resultado)

    if resultado != "Ok":
        flash(
            "Foi notado que algumas informações do seu perfil de produtor não encontram-se preenchidas. É importante preenchê-las para poder ter acesso a todas as funcionalidades do FeiraAgro.",
            "danger")
    else:
        pass

    dao = Perfil_ProdutorDAO(get_db())
    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']
    usuario_tipo = informacoes_usuario['tipo']

    print(usuario_codigo)

    resultado_busca = dao.Buscar_perfil(usuario_codigo)
    print(resultado_busca)

    variavel_condicional = resultado_busca

    if usuario_tipo == "Produtor":
        if resultado_busca == "Criado":
            return redirect(url_for('visualizar_perfil'))

        else:
            vartitulo = "Cadastrar-Perfil"
            if request.method == "POST":
                descricao_producao = request.form["descricao_producao"]
                local_venda = request.form["local_venda"]
                img0 = request.form["img0"]
                img1 = request.form["img1"]
                img2 = request.form["img2"]
                img3 = request.form["img3"]

                perfil_produtor = Perfil_Produtor(descricao_producao, local_venda, img0, img1, img2, img3, usuario_codigo)

                print(perfil_produtor)

                perfil = dao.Inserir(perfil_produtor)

                if perfil >= 0:
                    flash("Usuário cadastrado com sucesso!", "success")
                else:
                    flash("Erro ao cadastrar!", "danger")
    else:
        pass


    return render_template("perfil_produtor.html", variavel_condicional=variavel_condicional, estado_login=resultado_login, tipo_usuario=tipo_usuario)


@app.route('/listar_perfis', methods=['GET','POST'])
def listar_perfis():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao = Perfil_ProdutorDAO(get_db())
    perfil_produtor_db = dao.listar()
    return render_template("listar_item.html", perfil_produtor=perfil_produtor_db, estado_login=resultado_login, tipo_usuario=tipo_usuario)


@app.route('/visualizar_perfil', methods=['GET', 'POST'])
def visualizar_perfil():
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao = Perfil_ProdutorDAO(get_db())
    informacoes_usuario = session.get('logado')
    codigo = informacoes_usuario['codigo']
    tipo = informacoes_usuario['tipo']

    if tipo == "Produtor":
        perfil_produtor_db = dao.visualizar_perfil(codigo)
        perfil = perfil_produtor_db
        print(perfil_produtor)
    else:
        perfil_produtor_db = dao.visualizar_perfil(None)
        perfil = perfil_produtor_db[0]
        perfil = list(perfil)
        print(perfil)
    return render_template("visualizar_perfil.html", perfil_produtor=perfil, tipo=tipo, estado_login=resultado_login, tipo_usuario=tipo_usuario)





@app.route('/visualizar_pedido, <tipo>')
def visualizar_pedido(tipo):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao = PedidoDAO(get_db())
    informacoes_usuario = session.get('logado')
    codigo = informacoes_usuario['codigo']

    if tipo == "Meus":
        pedidos_db = dao.Visualizar_pedido(0, codigo)

    else:
        pedidos_db = dao.Visualizar_pedido(1, codigo)

    return render_template('visualizar_pedido.html', tipo=tipo, pedidos = pedidos_db, estado_login=resultado_login, tipo_usuario=tipo_usuario)


@app.route('/excluir_pedido, <codigo>', methods=['GET', ])
def excluir_pedido(codigo):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    dao1 = PedidoDAO(get_db())
    dao2 = ProdutoDAO(get_db())

    resultado_pedido = dao1.Listar(codigo, "Checagem_individual")
    resultado_produto = dao2.Listar(resultado_pedido[8], "Checagem_individual")

    if resultado_pedido[4] == "Não entregue":
        quantidade_final = resultado_produto[2] + resultado_pedido[3]

        dao2.Atualizar_quantidade(resultado_produto[0], quantidade_final)

        ret = dao1.Excluir(codigo)
        print(ret)
        if ret == 1:
            flash(f"Pedido {codigo} excluído com sucesso!", "success")
        else:
            flash(f"Erro ao excluir pedido {codigo}", "danger")
    else:
        flash(f"O pedido em questão encontra-se já entregue, impossibilitando sua exclusão.", "danger")

    return redirect(url_for('visualizar_pedido', tipo="Meus"))



# Buscas avançadas

@app.route('/busca_avancada, <categoria>' , methods=['GET','POST'])
def busca_avancada(categoria):
    resultado_login = verificar_login()
    tipo_usuario = verificar_tipo_usuario()

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    dao_produto = ProdutoDAO(get_db())

    if request.method == 'POST':
        termo = request.form['termo']
        if categoria == "produtos":
            produtos = dao_produto.Busca_avancada(termo)
            tipo = "todos"

    return render_template("visualizar_produtos.html", produtos = produtos, tipo=tipo, usuario_codigo=usuario_codigo, estado_login=resultado_login, tipo_usuario=tipo_usuario)

# Função de Notificação

# @app.route('/notificar',  methods=['GET', 'POST'])
# def notificar(usuario_email, titulo, mensagem):
#     email_inicial = 'maissanguetestes@gmail.com'
#     senha_email = 'xmfxugkbdnekwxkq'
#     email_destinatario = usuario_email
#
#     titulo = titulo
#     mensagem = mensagem
#
#     em = EmailMessage()
#     em['From'] = email_inicial
#     em['To'] = email_destinatario
#     em['Subject'] = titulo
#     em.set_content(mensagem)
#
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(email_inicial, senha_email)
#         smtp.sendmail(email_inicial, email_destinatario, em.as_string())


# Função de busca avançada por usuários

# @app.route('/usuarios_busca' , methods=['GET','POST'])
# def usuarios_busca():
#     dao = UsuarioDAO(get_db())
#     if request.method == 'POST':
#         termo = request.form['termo']
#
#     usuarios_db = dao.Busca_avancada(termo)
#     return render_template("listar_usuario.html", usuarios=usuarios_db)
#
#
# @app.route('/excluir_usuario/<codigo>', methods=['GET',])
# def excluir_usuario(codigo):
#     dao = UsuarioDAO(get_db())
#     ret = dao.Excluir(codigo)
#     if ret == 1:
#         flash(f"Conta excluída com sucesso!", "success")
#     else:
#         flash(f"Erro ao excluir Conta.", "danger")
#     return redirect(url_for('logout'))


# HOST


if __name__=='__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
