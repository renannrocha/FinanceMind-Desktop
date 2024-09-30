import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime
from io import BytesIO

def conectar_banco():
    """Função para conectar ao banco de dados SQLite"""
    try:
        return sqlite3.connect('finance.db')
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def gerar_grafico_despesas():
    """Gera um gráfico de despesas."""
    try:
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6], label='Despesas')  # Exemplo de dados
        ax.set_title('Gráfico de Despesas')
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.legend()
        return fig
    except Exception as e:
        print(f"Erro ao gerar gráfico de despesas: {e}")
        return None

def gerar_grafico_receitas():
    """Gera um gráfico de receitas."""
    try:
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [6, 5, 4], label='Receitas')  # Exemplo de dados
        ax.set_title('Gráfico de Receitas')
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.legend()
        return fig
    except Exception as e:
        print(f"Erro ao gerar gráfico de receitas: {e}")
        return None

def gerar_grafico_transacoes():
    """Gera um gráfico de transações."""
    try:
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [2, 3, 5], label='Transações')  # Exemplo de dados
        ax.set_title('Gráfico de Transações')
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.legend()
        return fig
    except Exception as e:
        print(f"Erro ao gerar gráfico de transações: {e}")
        return None

def gerar_relatorio(data_inicio, data_fim):
    """Gera um relatório de transações entre as datas especificadas."""
    conn = conectar_banco()
    if conn is None:
        print("Conexão não estabelecida. Relatório não gerado.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT tipo, SUM(valor) as total
                          FROM transacoes
                          WHERE data BETWEEN ? AND ?
                          GROUP BY tipo''', (data_inicio, data_fim))

        dados = cursor.fetchall()

        # Criar um relatório simples em texto
        relatorio = ""
        for tipo, total in dados:
            relatorio += f"{tipo}: R$ {total:.2f}\n"

        with open("relatorio.txt", "w") as f:
            f.write(relatorio)
        
        print("Relatório gerado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta no banco de dados: {e}")
    except IOError as e:
        print(f"Erro ao escrever o relatório em arquivo: {e}")
    finally:
        conn.close()

# Exemplo de uso das funções
if __name__ == "__main__":
    gerar_grafico_despesas()
    gerar_grafico_receitas()
    gerar_grafico_transacoes()
    gerar_relatorio('2024-01-01', '2024-12-31')

