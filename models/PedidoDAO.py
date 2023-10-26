class PedidoDAO():
    def __init__(self, con):
        self.con = con

    def Inserir(self, pedido):
        try:
            sql = "INSERT INTO Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, Usuario_codigo, Produto_codigo) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (pedido.data_pedido, pedido.data_entrega, pedido.quantidade, pedido.situacao, pedido.modo_entrega, pedido.usuario_codigo, pedido.produto_codigo))

            self.con.commit()

            codigo = cursor.lastrowid
            return codigo

        except:
            return 0

