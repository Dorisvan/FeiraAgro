class Produto():
    def __init__(self, nome, quantidade, valor, classificacao, procedencia, usuario_codigo, pedido_codigo, img_produto="", descricao=""):
        self.codigo = 0
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.classificacao = classificacao
        self.procedencia = procedencia
        self.img_produto = img_produto
        self.descricao = descricao
        self.usuario_codigo = usuario_codigo
        self.pedido_codigo = pedido_codigo

    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo





