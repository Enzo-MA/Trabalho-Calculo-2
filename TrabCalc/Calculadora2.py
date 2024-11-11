import re
import matplotlib.pyplot as plt
import numpy as np

# Função para ler o polinômio em uma string, no formato esperado pelo usuário
def ler_polinomio():
    print("Digite o polinômio em x no formato '2x^2 + 3x + 4', com espaços entre os termos e operadores:")
    polinomio_str = input("f(x) = ")
    return polinomio_str

# Função para formatar e exibir o polinômio de forma amigável
def exibir_polinomio(polinomio):
    if not polinomio:
        return "0"
        
    termos = []
    for grau in sorted(polinomio.keys(), reverse=True):
        coef = polinomio[grau]
        if abs(coef) < 1e-10:  # Ignora coeficientes muito pequenos (precisão de ponto flutuante)
            continue
            
        # Formata o termo de acordo com o grau e o coeficiente
        if grau == 0:  # Termo constante
            termo = f"{coef:g}"
        elif grau == 1:  # Termo de grau 1 (termo com x)
            if coef == 1:
                termo = "x"
            elif coef == -1:
                termo = "-x"
            else:
                termo = f"{coef:g}x"
        else:  # Termos de grau 2 ou maior
            if coef == 1:
                termo = f"x^{grau}"
            elif coef == -1:
                termo = f"-x^{grau}"
            else:
                termo = f"{coef:g}x^{grau}"
        
        # Adiciona o sinal de mais para termos positivos (exceto o primeiro)
        if coef > 0 and termos:
            termos.append(f"+ {termo}")
        else:
            termos.append(termo)
    
    return " ".join(termos) if termos else "0"

# Função para processar uma string representando um polinômio e transformá-la em um dicionário
def processar_polinomio(polinomio_str):
    # Utiliza uma expressão regular para extrair os termos do polinômio
    # A regex encontra termos com coeficientes, variáveis e constantes
    termos = re.findall(r'([+-]?\s*\d*\.?\d*)x(?:\^(\d+))?|([+-]?\s*\d+\.?\d*)', polinomio_str.replace(" ", ""))
    # 1) Primeira parte: `([+-]?\s*\d*\.?\d*)x(?:\^(\d+))?`
#      - `([+-]?)`: Captura opcionalmente um sinal "+" ou "-".
#      - `\s*`: Captura zero ou mais espaços em branco.
#      - `\d*`: Captura zero ou mais dígitos para o coeficiente, permitindo coeficientes como "2", "-2" ou valores decimais.
#      - `\.?`: Captura opcionalmente um ponto decimal.
#      - `\d*`: Captura a parte fracionária do coeficiente, se houver.
#      - `x`: Indica a presença de "x" (obrigatório, mas não é capturado).
#      - `(?:\^(\d+))?`: Grupo não capturador que verifica a presença opcional do símbolo "^" seguido de um expoente.
#         - `(\d+)`: Captura o expoente após "^" como um número inteiro.
#   
#   2) Segunda parte: `([+-]?\s*\d+\.?\d*)`
#      - Esta parte captura termos constantes, que não possuem "x".
#      - `([+-]?)`: Captura opcionalmente um sinal "+" ou "-".
#      - `\s*`: Captura zero ou mais espaços em branco.
#      - `\d+`: Captura um ou mais dígitos.
#      - `\.?`: Captura opcionalmente um ponto decimal.
#      - `\d*`: Captura a parte fracionária do número, se houver.
    # Dicionário para armazenar os coeficientes e seus graus
    polinomio = {}
    
    # Processa cada termo encontrado na expressão regular
    for coef_str, grau_str, constante in termos:
        if constante:  # Caso o termo seja constante
            grau = 0
            coeficiente = float(constante)
        else:
            # Extrai o grau e o coeficiente para termos com 'x'
            grau = int(grau_str) if grau_str else 1
            coef_str = coef_str.strip()
            if coef_str in ('', '+'):
                coeficiente = 1
            elif coef_str == '-':
                coeficiente = -1
            else:
                coeficiente = float(coef_str)
        
        # Armazena ou atualiza o coeficiente no dicionário
        polinomio[grau] = polinomio.get(grau, 0) + coeficiente
    
    return polinomio

# Avalia o valor do polinômio para um valor x dado
def avaliar_polinomio(polinomio, x):
    return sum(coef * (x ** grau) for grau, coef in polinomio.items())

# Calcula a integral indefinida do polinômio
def calcular_integral_indefinida(polinomio):
    integral = {}
    for grau, coef in polinomio.items():
        novo_grau = grau + 1
        integral[novo_grau] = coef / novo_grau
    return integral

# Calcula a integral definida do polinômio entre os limites a e b
def calcular_integral_definida(polinomio, a, b):
    integral = calcular_integral_indefinida(polinomio)
    integral_b = avaliar_polinomio(integral, b)
    integral_a = avaliar_polinomio(integral, a)
    return integral_b - integral_a

# Calcula a integral definida do módulo da diferença entre dois polinômios
def calcular_integral_definida_modulo(polinomio1, polinomio2, a, b):
    # Calcula o polinômio da diferença f1(x) - f2(x)
    polinomio_diff = {}
    for grau in set(polinomio1.keys()).union(polinomio2.keys()):
        coef1 = polinomio1.get(grau, 0)
        coef2 = polinomio2.get(grau, 0)
        polinomio_diff[grau] = coef1 - coef2
    
    # Calcula o valor absoluto da integral definida da diferença
    return abs(calcular_integral_definida(polinomio_diff, a, b))

# Calcula a área aproximada entre dois polinômios usando a soma de Riemann pela esquerda
def calcular_soma_riemann_esquerda(polinomio1, polinomio2, a, b, n):
    dx = (b - a) / n  # Calcula a largura de cada retângulo
    soma = 0.0
    for i in range(n):
        x = a + i * dx  # Ponto de avaliação
        altura = abs(avaliar_polinomio(polinomio1, x) - avaliar_polinomio(polinomio2, x))
        soma += altura * dx  # Área do retângulo adicionada à soma total
    return soma

# Função para plotar o gráfico das funções e a região entre elas
def plotar_grafico(polinomio1, polinomio2, a, b, n):
    # Cria pontos para plotagem
    x = np.linspace(a, b, 200)
    
    # Avalia os polinômios usando numpy para vetorização
    def evaluate_poly(x_val, poly):
        return sum(coef * (x_val ** grau) for grau, coef in poly.items())
    
    y1 = np.array([evaluate_poly(xi, polinomio1) for xi in x])
    y2 = np.array([evaluate_poly(xi, polinomio2) for xi in x])

    plt.figure(figsize=(10, 6))
    
    # Plota as funções principais
    plt.plot(x, y1, label="f1(x)", color="blue", linewidth=2)
    plt.plot(x, y2, label="f2(x)", color="red", linewidth=2)
    
    # Preenche a área entre as curvas
    plt.fill_between(x, y1, y2, color="gray", alpha=0.3)

    # Desenha retângulos da soma de Riemann
    dx = (b - a) / n
    for i in range(n):
        xi = a + i * dx
        y1_val = evaluate_poly(xi, polinomio1)
        y2_val = evaluate_poly(xi, polinomio2)
        
        # Determina o valor base e altura
        base = min(y1_val, y2_val)
        altura = abs(y1_val - y2_val)
        
        # Plota o retângulo entre as curvas
        plt.bar(xi, altura, bottom=base, width=dx, align="edge", 
                edgecolor="black", color="cyan", alpha=0.3)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.title(f"Região entre f1(x) e f2(x) no intervalo [{a}, {b}]")
    
    # Define os limites do eixo y com algum espaçamento
    y_min = min(min(y1), min(y2))
    y_max = max(max(y1), max(y2))
    padding = (y_max - y_min) * 0.1
    plt.ylim(y_min - padding, y_max + padding)
    
    plt.show()

# Função principal que coordena a entrada do usuário e chama as demais funções
def main():
    try:
        polinomio_str1 = ler_polinomio()
        polinomio_str2 = ler_polinomio()
        a = float(input("Digite o valor de a: "))
        b = float(input("Digite o valor de b: "))
        n = int(input("Digite o número de retângulos para a soma de Riemann: "))

        if n <= 0:
            raise ValueError("O número de retângulos deve ser positivo")
        if b <= a:
            raise ValueError("O valor de b deve ser maior que a")

        polinomio1 = processar_polinomio(polinomio_str1)
        polinomio2 = processar_polinomio(polinomio_str2)

        print("\nPolinômios processados:")
        print(f"f1(x) = {exibir_polinomio(polinomio1)}")
        print(f"f2(x) = {exibir_polinomio(polinomio2)}")

        area_integral = calcular_integral_definida_modulo(polinomio1, polinomio2, a, b)
        area_riemann = calcular_soma_riemann_esquerda(polinomio1, polinomio2, a, b, n)

        print(f"\nÁrea entre f1(x) e f2(x) usando Integral Definida: {area_integral}")
        print(f"Área entre f1(x) e f2(x) usando Soma de Riemann à esquerda: {area_riemann}")
        print(f"Erro absoluto: {abs(area_integral - area_riemann):.6f}")

        plotar_grafico(polinomio1, polinomio2, a, b, n)
    except Exception as e:
        print(f"Erro: {e}")

# Executa a função principal
if __name__ == "__main__":
    main()
