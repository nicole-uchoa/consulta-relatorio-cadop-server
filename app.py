from typing import NamedTuple, Tuple
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

class Resultado:
    def __init__(self, registro_ans, cnpj, nome_fantasia, razao_social, representante):
        self.registro_ans = registro_ans
        self.cnpj = cnpj
        self.nome_fantasia = nome_fantasia
        self.razao_social = razao_social
        self.representante = representante

#configurações psycopg2
class ConexaoPsy:        
    def conexao():
        host = "localhost"
        dbname = "db_cadop"
        user = "nicole"
        password = "123456"
        sslmode = "allow"
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        conn = psycopg2.connect(conn_string)
        print("Connection established")
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        return cursor

class Consulta:
    def busca(nome):
        cursor = ConexaoPsy.conexao()
        nome = str('%') + nome + str('%')
        cursor.execute("SELECT registro_ans, cnpj, nome_fantasia, razao_social, representante \
            FROM \
                relatorio_cadop rc \
            WHERE \
                UPPER(razao_social) LIKE UPPER(%s) \
                OR UPPER(nome_fantasia) LIKE UPPER(%s) \
                OR UPPER(representante) LIKE UPPER(%s) \
            ", [nome, nome, nome])
        consultas = []

        for row in cursor:
            consultas.append(Resultado(row.registro_ans, row.cnpj, row.nome_fantasia, row.razao_social, row.representante).__dict__)
        
        return consultas

    def allResults():
        cursor = ConexaoPsy.conexao()
        cursor.execute('SELECT * FROM relatorio_cadop')
        consultas = []

        for row in cursor:
            consultas.append(Resultado(row.registro_ans, row.cnpj, row.nome_fantasia, row.razao_social, row.representante).__dict__)
        
        return consultas
        
        

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def all_db():
    return jsonify({
        'status': 'success',
        'search': Consulta.allResults()
    })

@app.route('/result', methods=['GET'])
def results():
    return jsonify({
        'status': 'success',
        'search': Consulta.busca(request.args.get('nome'))
    })
        
if __name__ == '__main__':
    app.run()