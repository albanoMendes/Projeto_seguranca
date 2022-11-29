import mysql.connector

try:
        con = mysql.connector.connect(host='localhost', database='segurança_bd', user='root', password='');

        # D
        criar_tabela_SQL = """ CREATE TABLE if not exists eleitor(
                                idEleitor int(11) NOT NULL,
                                nome VARCHAR(50) NOT NULL,
                                cpf VARCHAR(20) UNIQUE,
                                PRIMARY KEY (idEleitor)) """;
        cursor = con.cursor()
        cursor.execute(criar_tabela_SQL)
        print("Tabela Eleitor criada com sucesso!")
        criar_tabela_SQL = """ CREATE TABLE if not exists candidato(
                                idCandidato int(11) NOT NULL AUTO_INCREMENT,
                                nomePartido VARCHAR(100) NOT NULL,
                                sigla VARCHAR(10) UNIQUE,
                                presidente VARCHAR(50) UNIQUE,
                                PRIMARY KEY (idCandidato)) """;
        cursor = con.cursor()
        cursor.execute(criar_tabela_SQL)
        print("Tabela Candidato criada com sucesso!")
        criar_tabela_SQL = """ CREATE TABLE if not exists voto(
                                idVoto int(11) NOT NULL AUTO_INCREMENT,
                                cpfEleitor VARCHAR(20) NOT NULL,
                                idCandidato int(11),
                                PRIMARY KEY (idVoto)) """;
        cursor = con.cursor()
        cursor.execute(criar_tabela_SQL)
        print("Tabela Voto criada com sucesso!")
except mysql.connector.Error as erro:
        print("Falha ao criar a tabela no MySQL: {}".format(erro));
finally:
        if con.is_connected():
                cursor.close()
                con.close()
                print("Conexão MySql foi encerrada")
