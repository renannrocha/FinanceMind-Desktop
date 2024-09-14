import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import search_query
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

def conectar_banco():
    """Função para conectar ao banco de dados SQLite"""
    return sqlite3.connect('finance.db')

import matplotlib.pyplot as plt
from database import search_query

def gerar_grafico_transacoes(frame):
    """Gera um gráfico de transações e o exibe no frame fornecido."""
    # Consulta para obter transações
    transacoes = search_query('SELECT tipo, valor FROM transacoes')

    if not transacoes:
        return

    # Separar os dados
    tipos = [t[0] for t in transacoes]
    valores = [t[1] for t in transacoes]

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(tipos, valores, color='skyblue')
    ax.set_xlabel('Tipo de Transação')
    ax.set_ylabel('Valor')
    ax.set_title('Gráfico de Transações')

    # Adicionar o gráfico ao frame Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def gerar_relatorio(data_inicio, data_fim):
    """Gera um relatório de transações entre as datas especificadas"""
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tipo, SUM(valor) as total
        FROM transacoes
        WHERE data BETWEEN ? AND ?
        GROUP BY tipo
    ''', (data_inicio, data_fim))

    dados = cursor.fetchall()
    conn.close()

    # Criar um relatório simples em texto
    relatorio = "Relatório de Transações\n"
    relatorio += f"Período: {data_inicio} a {data_fim}\n\n"

    for tipo, total in dados:
        relatorio += f"{tipo}: R${total:.2f}\n"

    # Exemplo de como você pode salvar o relatório em um arquivo
    with open('relatorio_transacoes.txt', 'w') as f:
        f.write(relatorio)

    print("Relatório gerado com sucesso e salvo como 'relatorio_transacoes.txt'.")
