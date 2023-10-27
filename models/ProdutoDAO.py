class ProdutoDAO():
    def __init__(self, con):
        self.con = con

    def Inserir(self, produto):
        try:
            sql = "INSERT INTO Produto(nome, quantidade, valor, classificacao, procedencia, usuario_codigo, img_produto, descricao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (produto.nome, produto.quantidade, produto.valor, produto.classificacao, produto.procedencia, produto.usuario_codigo, produto.img_produto, produto.descricao,))

            self.con.commit()

            codigo = cursor.lastrowid
            return codigo

        except:
            return 0


    def Visualizar(self, codigo):
        cursor = self.con.cursor()
        print(codigo)
        try:
            if codigo == None:
                sql = "SELECT DISTINCT p.codigo, p.nome, p.quantidade, p.valor, p.classificacao, p.procedencia, p.img_produto, p.descricao, p.Usuario_codigo as codigo_dono, u.nome as nome_do_produtor, u.contato, u.endereco, pf.local_venda " \
                      "FROM Produto as p, Usuario as u, Perfil_produtor as pf " \
                      "WHERE u.codigo = p.Usuario_codigo AND u.codigo = pf.Usuario_codigo " \
                      "ORDER BY p.Usuario_codigo, p.nome"

                cursor.execute(sql)
                produtos = cursor.fetchall()
                return produtos

            else:
                sql = "SELECT DISTINCT p.codigo, p.nome, p.quantidade, p.valor, p.classificacao, p.procedencia, p.img_produto, p.descricao, p.Usuario_codigo as codigo_dono, u.nome as nome_do_produtor, u.contato, u.endereco, pf.local_venda " \
                      "FROM Produto as p, Usuario as u, Perfil_produtor as pf " \
                      "WHERE u.codigo = p.Usuario_codigo AND u.codigo = pf.Usuario_codigo AND pf.Usuario_codigo = %s " \
                      "ORDER BY p.Usuario_codigo, p.nome"

                cursor.execute(sql, (codigo,))
                produtos = cursor.fetchall()
                return produtos
        except:
            return 0

    def Listar(self, codigo, tipo):
        try:
            cursor = self.con.cursor()
            if tipo == "Checagem_individual":
                # pegar somente uma planta
                sql = "SELECT * FROM Produto WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                produto = cursor.fetchone()
                return produto

            elif tipo == "Listagem_individual":
                sql = "SELECT * FROM Produto WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                produto = cursor.fetchall()
                return produto

            else:
                # pegar todas as plantas
                sql = "SELECT * FROM Produto"
                cursor.execute(sql)
                produtos = cursor.fetchall()
                return produtos
        except:
            return None


    def Atualizar_quantidade(self, codigo, valor_atualizado):
        try:
            sql = "UPDATE Produto " \
                  "SET quantidade=%s WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (valor_atualizado, codigo))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0




