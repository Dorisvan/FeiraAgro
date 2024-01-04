class MensagemDAO():
    def __init__(self, con):
        self.con = con

    def Inserir(self, Mensagem):
        try:
            sql = "INSERT INTO Mensagem(conteudo, tipo, situacao, Usuario_codigo) " \
                  "VALUES (%s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (
            Mensagem.conteudo, Mensagem.tipo, Mensagem.situacao, Mensagem.Usuario_codigo))

            self.con.commit()

            codigo = cursor.lastrowid

            return codigo

        except:
            return 0


    def Listar(self, codigo, tipo):
        try:
            cursor = self.con.cursor()
            if tipo == "Checagem_individual":
                sql = "SELECT * FROM Mensagem WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                Mensagem = cursor.fetchone()
                return Mensagem

            elif tipo == "Listagem_individual":
                sql = "SELECT * FROM Mensagem WHERE Usuario_codigo=%s"
                cursor.execute(sql, (codigo,))
                Mensagem = cursor.fetchall()
                return Mensagem

            else:
                sql = "SELECT * FROM Mensagem"
                cursor.execute(sql)
                Mensagens = cursor.fetchall()
                return Mensagens
        except:
            return None

    def Alertas(self, codigo):
        try:
            cursor = self.con.cursor()
            sql = "SELECT count(codigo)  FROM Mensagem WHERE Usuario_codigo=%s and situacao=%s"
            cursor.execute(sql, (codigo, "Não_lida"))
            Mensagens = cursor.fetchall()
            return Mensagens

        except:
            return None


    def Atualizar(self, codigo):
        try:
            sql = "UPDATE Mensagem " \
                  "SET situacao=%s" \
                  "WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, ("Lida", codigo,))
            self.con.commit()
            return cursor.rowcount

        except:
            return 0


