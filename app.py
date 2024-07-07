import subprocess
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def get_fila_espera():
    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    c.execute('SELECT * FROM alunos WHERE status = "Aguardando"')
    alunos = c.fetchall()
    conn.close()
    return alunos


def get_chamados():
    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    c.execute('SELECT * FROM alunos WHERE status = "Chamado"')
    chamados = c.fetchall()
    conn.close()
    return chamados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chamados')
def chamados():
    chamados = get_chamados()
    return render_template('chamados.html', chamados=chamados)

@socketio.on('connect')
def handle_connect():
    alunos = get_fila_espera()
    emit('fila_espera', {'alunos': alunos})

@app.route('/sistema')
def sistema():
    return render_template('sistema.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    instrumento = request.form['instrumento']
    igreja = request.form['igreja']
    tipo_teste = request.form['tipo_teste']
    nota_prova = float(request.form['nota_prova'])
    status = 'Aguardando'

    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO alunos (nome, instrumento, igreja, tipo_teste, nota_prova, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, instrumento, igreja, tipo_teste, nota_prova, status))
    conn.commit()
    conn.close()

    # Emitir evento para atualizar a fila de espera
    alunos = get_fila_espera()
    socketio.emit('fila_espera', {'alunos': alunos})

    return redirect(url_for('sistema'))

@app.route('/chamar/<int:id>', methods=['POST'])
def chamar(id):
    encarregado = request.json.get('encarregado')
    
    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    c.execute('UPDATE alunos SET status = "Chamado", encarregado = ? WHERE id = ?', (encarregado, id))
    conn.commit()

    # Obter informações do aluno
    c.execute('SELECT nome, instrumento, igreja, tipo_teste, nota_prova FROM alunos WHERE id = ?', (id,))
    aluno = c.fetchone()
    conn.close()

    # Emitir evento para notificação de chamada
    mensagem = f'O candidato para {aluno[1]}, {aluno[0]} da comum {aluno[2]} está sendo chamado para o teste prático pelo {encarregado}.'
    socketio.emit('notificacao_chamada', {
        'id': id,
        'mensagem': mensagem,
        'nome': aluno[0],
        'instrumento': aluno[1],
        'igreja': aluno[2],
        'tipo_teste': aluno[3],
        'nota_prova': aluno[4],
        'encarregado': encarregado
    })
    
    return jsonify(success=True)

@app.route('/limpar_lista', methods=['POST'])
def limpar_lista():
    conn = sqlite3.connect('testes_musicais.db')
    c = conn.cursor()
    c.execute('DELETE FROM alunos WHERE status = "Chamado"')
    conn.commit()
    conn.close()

    # Emitir evento para atualizar a lista de chamados
    socketio.emit('lista_limpa')

    return jsonify(success=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
