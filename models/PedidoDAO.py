class PedidoDAO():
    def __init__(self, con):
        self.con = con

    def Inserir(self, pedido):
        try:
            sql = "INSERT INTO Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, status_compra, Usuario_codigo, Produto_codigo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (pedido.data_pedido, pedido.data_entrega, pedido.quantidade, pedido.situacao, pedido.modo_entrega, pedido.status_compra, pedido.usuario_codigo, pedido.produto_codigo))

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


    def Listar(self, codigo, tipo):
        try:
            cursor = self.con.cursor()
            if tipo == "Checagem_individual":
                sql = "SELECT * FROM Pedido WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                usuario = cursor.fetchone()
                return usuario

            elif tipo == "Listagem_individual":
                sql = "SELECT * FROM Pedido WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                usuario = cursor.fetchall()
                return usuario

            else:
                sql = "SELECT * FROM Pedido"
                cursor.execute(sql)
                usuarios = cursor.fetchall()
                return usuarios
        except:
            return None

    def Atualizar(self, pedido):
        try:
            sql = "UPDATE Pedido " \
                  "SET data_entrega=%s, modo_entrega=%s, " \
                  "quantidade=%s" \
                  "WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (pedido.data_entrega, pedido.modo_entrega, pedido.quantidade, pedido.codigo))
            self.con.commit()
            return cursor.rowcount

        except:
            return 0


    def Excluir(self, codigo):
        try:
            sql = "DELETE FROM Pedido WHERE codigo = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            self.con.commit()
            print(cursor.rowcount)
            return cursor.rowcount
        except:
            return 0

