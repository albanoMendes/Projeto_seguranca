import mysql.connector
from mysql.connector import Error
#Buscar candidatos na Banco de Dados MySQL

def candidatos():
    try:
        con = mysql.connector.connect(host='localhost',
                                      database='segurança_bd',
                                      user='root',
                                      password='');
        consulta_sql = "SELECT * FROM candidato";
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

        print("CONCORRENTES AS ELEIÇÕES")

        print("CODIGO   PARTIDOS   CANDIDATO")
        for linha in linhas:
            print("  ",linha[0],"     ", linha[2],"   ",linha[3])

    except Error as e:
        print("Erro ao acessar tabela MySQL", e)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão MySql foi encerrada")

candidatos();
