import re
import matplotlib.pyplot as plt
import numpy as np

def ler_polinomio():
    print("Digite o polinômio em x no formato '2x^2 + 3x + 4', com espaços entre os termos e operadores:")
    polinomio_str = input("f(x) = ")
    return polinomio_str

def exibir_polinomio(polinomio):
    if not polinomio:
        return "0"
        
    termos = []
    for grau in sorted(polinomio.keys(), reverse=True):
        coef = polinomio[grau]
        if abs(coef) < 1e-10:  # Handle floating point precision
            continue
            
        # Format term based on degree and coefficient
        if grau == 0:  # constant term
            termo = f"{coef:g}"
        elif grau == 1:  # degree 1 (x term)
            if coef == 1:
                termo = "x"
            elif coef == -1:
                termo = "-x"
            else:
                termo = f"{coef:g}x"
        else:  # degree 2 and higher
            if coef == 1:
                termo = f"x^{grau}"
            elif coef == -1:
                termo = f"-x^{grau}"
            else:
                termo = f"{coef:g}x^{grau}"
        
        # Add plus sign for positive terms (except first term)
        if coef > 0 and termos:
            termos.append(f"+ {termo}")
        else:
            termos.append(termo)
    
    return " ".join(termos) if termos else "0"

def processar_polinomio(polinomio_str):
    # Improved regex to better handle negative numbers and coefficients
    termos = re.findall(r'([+-]?\s*\d*\.?\d*)x(?:\^(\d+))?|([+-]?\s*\d+\.?\d*)', polinomio_str.replace(" ", ""))
    
    polinomio = {}
    
    for coef_str, grau_str, constante in termos:
        if constante:  # Constant term
            grau = 0
            coeficiente = float(constante)
        else:
            # Extract degree and coefficient for terms with 'x'
            grau = int(grau_str) if grau_str else 1
            coef_str = coef_str.strip()
            if coef_str in ('', '+'):
                coeficiente = 1
            elif coef_str == '-':
                coeficiente = -1
            else:
                coeficiente = float(coef_str)
        
        # Store or update coefficient in dictionary
        polinomio[grau] = polinomio.get(grau, 0) + coeficiente
    
    return polinomio

def avaliar_polinomio(polinomio, x):
    return sum(coef * (x ** grau) for grau, coef in polinomio.items())

def calcular_integral_indefinida(polinomio):
    integral = {}
    for grau, coef in polinomio.items():
        novo_grau = grau + 1
        integral[novo_grau] = coef / novo_grau
    return integral

def calcular_integral_definida(polinomio, a, b):
    integral = calcular_integral_indefinida(polinomio)
    integral_b = avaliar_polinomio(integral, b)
    integral_a = avaliar_polinomio(integral, a)
    return integral_b - integral_a

def calcular_integral_definida_modulo(polinomio1, polinomio2, a, b):
    # Calculate difference polynomial f1(x) - f2(x)
    polinomio_diff = {}
    for grau in set(polinomio1.keys()).union(polinomio2.keys()):
        coef1 = polinomio1.get(grau, 0)
        coef2 = polinomio2.get(grau, 0)
        polinomio_diff[grau] = coef1 - coef2
    
    return abs(calcular_integral_definida(polinomio_diff, a, b))

def calcular_soma_riemann_esquerda(polinomio1, polinomio2, a, b, n):
    dx = (b - a) / n
    soma = 0.0
    for i in range(n):
        x = a + i * dx
        altura = abs(avaliar_polinomio(polinomio1, x) - avaliar_polinomio(polinomio2, x))
        soma += altura * dx
    return soma

def plotar_grafico(polinomio1, polinomio2, a, b, n):
    # Create points for plotting
    x = np.linspace(a, b, 200)
    
    # Evaluate polynomials using numpy for vectorization
    def evaluate_poly(x_val, poly):
        return sum(coef * (x_val ** grau) for grau, coef in poly.items())
    
    y1 = np.array([evaluate_poly(xi, polinomio1) for xi in x])
    y2 = np.array([evaluate_poly(xi, polinomio2) for xi in x])

    plt.figure(figsize=(10, 6))
    
    # Plot main functions
    plt.plot(x, y1, label="f1(x)", color="blue", linewidth=2)
    plt.plot(x, y2, label="f2(x)", color="red", linewidth=2)
    
    # Fill between curves
    plt.fill_between(x, y1, y2, color="gray", alpha=0.3)

    # Draw Riemann rectangles
    dx = (b - a) / n
    for i in range(n):
        xi = a + i * dx
        y1_val = evaluate_poly(xi, polinomio1)
        y2_val = evaluate_poly(xi, polinomio2)
        
        # Determine which value is greater
        base = min(y1_val, y2_val)
        altura = abs(y1_val - y2_val)
        
        # Plot rectangle from the lower curve to the upper curve
        plt.bar(xi, altura, bottom=base, width=dx, align="edge", 
               edgecolor="black", color="cyan", alpha=0.3)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.title(f"Região entre f1(x) e f2(x) no intervalo [{a}, {b}]")
    
    # Set y-axis limits with some padding
    y_min = min(min(y1), min(y2))
    y_max = max(max(y1), max(y2))
    padding = (y_max - y_min) * 0.1
    plt.ylim(y_min - padding, y_max + padding)
    
    plt.show()

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

        area_riemann = calcular_soma_riemann_esquerda(polinomio1, polinomio2, a, b, n)
        area_integral = calcular_integral_definida_modulo(polinomio1, polinomio2, a, b)

        print(f"\nResultados:")
        print(f"Área usando soma de Riemann (n={n}): {area_riemann:.6f}")
        print(f"Área usando integral definida: {area_integral:.6f}")
        print(f"Erro absoluto: {abs(area_integral - area_riemann):.6f}")

        plotar_grafico(polinomio1, polinomio2, a, b, n)

    except ValueError as e:
        print(f"\nErro: {str(e)}")
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")

if __name__ == "__main__":
    main()