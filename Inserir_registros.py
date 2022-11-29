import mysql.connector
from mysql.connector import Error
# Inserir registros em banco de dados MySQL [TESTES]

try:
    con = mysql.connector.connect(host='localhost', database='segurança_bd', user='root', password='');

    inserir_eleitor = """ INSERT INTO eleitor
                            (nome, cpf)
                          VALUES
                              ('Marcos Paulo', '022.423.009-04'),
                              ('Douglas Silva', '052.623.109-14'),
                              ('André Miranda', '152.024.119-18')
                      """
    cursor = con.cursor()
    cursor.execute(inserir_eleitor)
    con.commit()
    print(cursor.rowcount, "Registros inseridos na tabela Eleitor!")
    
    inserir_candidato = """ INSERT INTO candidato
                            (nomePartido, sigla, presidente)
                          VALUES
                              ('MOVIMENTO DEMOCRÁTICO BRASILEIRO','MDB','LUIZ FELIPE BALEIA TENUTO ROSSI'),
                              ('PARTIDO TRABALHISTA BRASILEIRO', 'PTB', 'KASSYO SANTOS RAMO'),
                              ('PARTIDO DOS TRABALHADORES', 'PT', 'GLEISI HELENA HOFFMANN'),
                              ('PARTIDO DA SOCIAL DEMOCRACIA BRASILEIRA', 'PSDB', 'BRUNO CAVALCANTI DE ARAÚJO')
                      """
    cursor = con.cursor()
    cursor.execute(inserir_candidato)
    con.commit()
    print(cursor.rowcount, "Registros inseridos na tabela Candidatos!")
    
except Error as erro:
        print("Falha ao inserir dados na tabela MySQL: {}".format(erro));
finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão MySql foi encerrada")

