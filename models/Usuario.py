class Usuario():
    def __init__(self, nome, email, senha, endereco, tipo, nivel, contato, estado_login, perfil_produtor_codigo=''):
        self.codigo = 0
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco
        self.tipo = tipo
        self.nivel = nivel
        self.contato = contato
        self.estado_login = estado_login
        self.perfil_produtor_codigo = perfil_produtor_codigo


    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo


    def getEstado_login(self):
        return self.estado_login

    def setEstado_login(self, estado_login):
        self.estado_login = estado_login





