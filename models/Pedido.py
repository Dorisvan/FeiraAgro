class Pedido():
    def __init__(self, data_pedido, data_entrega, quantidade, situacao, modo_entrega, status_compra, usuario_codigo, produto_codigo):
        self.codigo = 0
        self.data_pedido = data_pedido
        self.data_entrega = data_entrega
        self.quantidade = quantidade
        self.situacao = situacao
        self.modo_entrega = modo_entrega
        self.status_compra = status_compra
        self.usuario_codigo = usuario_codigo
        self.produto_codigo = produto_codigo

    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo