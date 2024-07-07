import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('testes_musicais.db')

# Criar um cursor
c = conn.cursor()

# Criar a tabela alunos
c.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        instrumento TEXT,
        igreja TEXT,
        tipo_teste TEXT,
        nota_prova REAL,
        status TEXT
    )
''')


# Confirmar as mudanças
conn.commit()
conn.close()
