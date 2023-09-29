class Perfil_ProdutorDAO():
    def __init__(self, con):
        self.con = con

    def Inserir(self, perfil):
        try:
            sql = "INSERT INTO perfil_produtor(descricao_producao, local_venda, img0, img1, img2, img3, Usuario_codigo) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (perfil.descricao_producao, perfil.local_venda, perfil.img0, perfil.img1, perfil.img2, perfil.img3, perfil.Usuario_codigo))

            self.con.commit()

            codigo = cursor.lastrowid

            return codigo

        except:
            return 0

    def Buscar_perfil(self, codigo):
        sql = "SELECT * FROM Perfil_Produtor WHERE Usuario_codigo=%s"

        cursor = self.con.cursor()
        cursor.execute(sql, (codigo,))

        return cursor.fetchone()



    def visualizar_perfil(self, codigo):
        try:
            sql = "SELECT p.codigo, p.descricao_producao, p.local_venda, p.img0, p.img1, p.img2, p.img3, p.Usuario_codigo, u.nome, u.email, u.endereco, u.contato" \
                  "FROM Perfil_Produtor as p, Usuario as u" \
                  "WHERE p.Usuario_codigo = u.codigo AND" \
                  "     p.codigo = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            perfil = cursor.fetchall()
            return perfil
