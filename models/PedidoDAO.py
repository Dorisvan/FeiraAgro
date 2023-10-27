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


    def Visualizar_pedido(self, tipo, codigo):
        try:
            if tipo == 0:
                sql = "SELECT * FROM Pedido WHERE Pedido.Usuario_codigo = %s"
                cursor = self.con.cursor()
                cursor.execute(sql, (codigo,))
                pedidos = cursor.fetchall()
                print(pedidos)
                return pedidos
            else:
                sql = "SELECT DISTINCT pe.codigo,  pe.data_pedido, pe.data_entrega, pe.quantidade, pe.situacao, pe.modo_entrega, pe.Usuario_codigo, pe.Produto_codigo" \
                      "FROM Pedido as pe, Produto as pr, Usuario as u " \
                      "WHERE pr.Usuario_codigo = %s AND pr.codigo = pe.Produto_codigo"
                cursor = self.con.cursor()
                cursor.execute(sql, (codigo,))
                pedidos = cursor.fetchall()
                return pedidos
        except:
            pass


