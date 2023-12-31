class UsuarioDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, usuario):
        try:
            sql = "INSERT INTO Usuario(nome, email, senha, endereco, tipo, nivel, contato, estado_login, imagem_perfil) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.endereco, usuario.tipo, usuario.nivel, usuario.contato, usuario.estado_login, usuario.imagem_perfil))

            self.con.commit()

            codigo = cursor.lastrowid

            return codigo

        except:
            return 0


    def Listar(self, codigo, tipo):
        try:
            cursor = self.con.cursor()
            if tipo == "Checagem_individual":
                sql = "SELECT * FROM Usuario WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                usuario = cursor.fetchone()
                return usuario

            elif tipo == "Listagem_individual":
                sql = "SELECT * FROM Usuario WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                usuario = cursor.fetchall()
                return usuario

            else:
                sql = "SELECT * FROM Usuario"
                cursor.execute(sql)
                usuarios = cursor.fetchall()
                return usuarios
        except:
            return None


    def Buscar_email(self, email):
        sql = "SELECT * FROM Usuario WHERE email=%s"

        cursor = self.con.cursor()
        cursor.execute(sql, (email,))

        return cursor.fetchone()


    def Busca_avancada(self, termo):
        try:
            sql = "SELECT * FROM Solicitacao WHERE codigo LIKE %s OR data LIKE %s OR urgencia LIKE %s OR local_internacao LIKE %s OR situacao LIKE %s"
            sql2 = "SELECT DISTINCT * FROM Usuario as u WHERE u.codigo LIKE %s OR u.cpf LIKE %s OR u.nome LIKE %s OR u.dt_nasc LIKE %s OR u.peso LIKE %s OR u.tipo_sanguineo LIKE %s OR u.cep LIKE %s OR u.cidade LIKE %s OR u.email LIKE %s OR u.senha LIKE %s OR u.telefone LIKE %s OR u.opcao_doacao LIKE %s OR u.estado_doacao LIKE %s OR u.nivel_usuario LIKE %s"
            cursor = self.con.cursor()
            cursor.execute(sql2, (termo, termo, termo, termo, termo, termo, termo, termo, termo, termo, termo, termo, termo, termo))
            resultado = cursor.fetchall()

            return resultado
        except:
            return("Não há nenhum usuário com esse dado informado no sistema.")


    def Atualizar(self, usuario):
        try:
            sql = "UPDATE Usuario " \
                  "SET nome=%s, email=%s, " \
                  "senha=%s, endereco=%s, tipo=%s, contato=%s " \
                  "WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.endereco, usuario.tipo, usuario.contato, usuario.codigo))
            self.con.commit()
            return cursor.rowcount

        except:
            return 0


    def Excluir(self, codigo):
        try:
            sql = "DELETE FROM Usuario WHERE codigo = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def autenticar(self, email, senha):
        try:
            sql = "SELECT * FROM Usuario WHERE email=%s AND senha=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (email, senha))

            usuario = cursor.fetchone()  # lastrowid, fetchone, fetchall
            return usuario

        except:
            return None


    def Verificacao_perfil(self, codigo):
        cursor = self.con.cursor()

        try:
            sql = "SELECT * FROM Usuario WHERE codigo = %s"

            cursor.execute(sql, (codigo,))
            resultado = cursor.fetchone()
            resultado = list(resultado)

            if resultado != None and resultado[4] != "" and resultado[5] != "" and resultado[5] !="Não sei":
                Situacao = "Ok"
                return Situacao
            else:
                Situacao = "Pendente"
                return Situacao

        except:
            pass