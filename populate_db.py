import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('testes_musicais.db')
c = conn.cursor()

# Dados de exemplo
alunos = [
    ("João Silva", "Trompete", "Igreja Central", "Reunião de Jovens", 9.0, "Aguardando"),
    ("Maria Souza", "Violino", "Igreja Sul", "Culto Oficial", 8.5, "Aguardando"),
    ("Carlos Pereira", "sax", "Igreja Norte", "Oficialização", 7.8, "Aguardando"),
    ("Ana Oliveira", "Violino", "Igreja Leste", "Reunião de Jovens", 8.2, "Aguardando"),
    ("Lucas Fernandes", "Flauta", "Igreja Oeste", "Culto Oficial", 9.5, "Aguardando")
]

# Inserir dados na tabela alunos
c.executemany('''
    INSERT INTO alunos (nome, instrumento, igreja, tipo_teste, nota_prova, status)
    VALUES (?, ?, ?, ?, ?, ?)
''', alunos)

# Confirmar as mudanças
conn.commit()
conn.close()

