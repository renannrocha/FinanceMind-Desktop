import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime
from io import BytesIO

def conectar_banco():
    """Função para conectar ao banco de dados SQLite"""
    return sqlite3.connect('finance.db')

def gerar_grafico_despesas():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6], label='Despesas')  # Exemplo de dados
    ax.set_title('Gráfico de Despesas')
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.legend()
    return fig

def gerar_grafico_receitas():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [6, 5, 4], label='Receitas')  # Exemplo de dados
    ax.set_title('Gráfico de Receitas')
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.legend()
    return fig

def gerar_grafico_transacoes():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 3, 5], label='Transações')  # Exemplo de dados
    ax.set_title('Gráfico de Transações')
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.legend()
    return fig

def gerar_relatorio(data_inicio, data_fim):
    """Gera um relatório de transações entre as datas especificadas"""
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''SELECT tipo, SUM(valor) as total
                      FROM transacoes
                      WHERE data BETWEEN ? AND ?
                      GROUP BY tipo''', (data_inicio, data_fim))

    dados = cursor.fetchall()
    conn.close()

    # Criar um relatório simples em texto
    relatorio = ""
    for tipo, total in dados:
        relatorio += f"{tipo}: R$ {total:.2f}\n"

    with open("relatorio.txt", "w") as f:
        f.write(relatorio)
