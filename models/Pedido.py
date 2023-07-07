class Pedido():
    def __init__(self, data, situacao, modo_entrega, usuario_codigo):
        self.codigo = 0
        self.data = data
        self.situacao = situacao
        self.modo_entrega = modo_entrega
        self.usuario_codigo = usuario_codigo

    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo