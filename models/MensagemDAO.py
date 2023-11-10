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

