class Mensagem():
    def __init__(self, conteudo, Usuario_codigo, tipo='',situacao=''):
        self.codigo = 0
        self.conteudo = conteudo
        self.Usuario_codigo = Usuario_codigo
        self.tipo = tipo
        self.situacao = situacao

    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo




