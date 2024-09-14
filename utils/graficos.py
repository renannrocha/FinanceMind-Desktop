import matplotlib.pyplot as plt

def gerar_grafico_receitas_despesas(receitas, despesas):
    labels = ['Receitas', 'Despesas']
    valores = [receitas, despesas]

    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()
