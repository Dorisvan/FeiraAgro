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