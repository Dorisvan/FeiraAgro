class Perfil_Produtor():
    def __init__(self, descricao_producao="", local_venda="", img0="", img1="", img2="", img3=""):
        self.codigo = 0
        self.descricao_producao = descricao_producao
        self.local_venda = local_venda
        self.img0 = img0
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3


    def getCodigo(self):
        return self.codigo

    def setCodigo(self, codigo):
        self.codigo = codigo