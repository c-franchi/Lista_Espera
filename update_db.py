import sqlite3

def add_encarregado_column():
    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE alunos ADD COLUMN encarregado TEXT')
        conn.commit()
        print("Coluna 'encarregado' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao adicionar a coluna: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_encarregado_column()

