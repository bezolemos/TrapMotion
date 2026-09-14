import math


def calcular_geometria(diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm):

    # Cálculos feitos dentro da função
    raio_roda_m = (diametro_roda_cm / 100) / 2
    raio_eixo_m = (diametro_eixo_cm / 100) / 2

    circunferencia_eixo_m = 2 * math.pi * raio_eixo_m
    circunferencia_roda_m = 2 * math.pi * raio_roda_m

    rotacoes = (comprimento_corda_cm / 100) / circunferencia_eixo_m

    distancia_teorica_m = (rotacoes * circunferencia_roda_m)
    resultados = {
        "raio_roda_m": raio_roda_m,
        "raio_eixo_m": raio_eixo_m,
        "circunferencia_eixo_m": circunferencia_eixo_m,
        "circunferencia_roda_m": circunferencia_roda_m,
        "rotacoes": rotacoes,
        "distancia_teorica_m": distancia_teorica_m
}
    return resultados

def calcular_ajustes_para_meta(diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm, distancia_meta_m):
    # Conversão das medidas para metros, variável temporária para facilitar os cálculos
    diametro_roda_m = diametro_roda_cm / 100
    diametro_eixo_m = diametro_eixo_cm / 100
    comprimento_corda_m = comprimento_corda_cm / 100

    # Alternativa 1: aumentar o diâmetro da roda
    diametro_roda_necessario_m = (distancia_meta_m * diametro_eixo_m / comprimento_corda_m)

    # Alternativa 2: aumentar o comprimento da corda
    comprimento_corda_necessario_m = (distancia_meta_m * diametro_eixo_m / diametro_roda_m)

    # Alternativa 3: reduzir o diâmetro do eixo
    diametro_eixo_maximo_m = (comprimento_corda_m * diametro_roda_m / distancia_meta_m)

    # Conversão dos resultados para centímetros
    diametro_roda_necessario_cm = (diametro_roda_necessario_m * 100)

    comprimento_corda_necessario_cm = (comprimento_corda_necessario_m * 100)

    diametro_eixo_maximo_cm = (diametro_eixo_maximo_m * 100)

    # Calcula quanto cada medida precisaria mudar
    aumento_roda_cm = max(0.0,diametro_roda_necessario_cm - diametro_roda_cm)

    aumento_corda_cm = max(0.0,comprimento_corda_necessario_cm - comprimento_corda_cm)

    reducao_eixo_cm = max(0.0,diametro_eixo_cm - diametro_eixo_maximo_cm)

    ajustes = {
        "diametro_roda_necessario_cm":
            diametro_roda_necessario_cm,

        "aumento_roda_cm":
            aumento_roda_cm,

        "comprimento_corda_necessario_cm":
            comprimento_corda_necessario_cm,

        "aumento_corda_cm":
            aumento_corda_cm,

        "diametro_eixo_maximo_cm":
            diametro_eixo_maximo_cm,

        "reducao_eixo_cm":
            reducao_eixo_cm
    }
    return ajustes

diametro_roda_cm = float(input("Digite o diâmetro da roda em cm: "))
diametro_eixo_cm = float(input("Digite o diâmetro do eixo em cm: "))
comprimento_corda_cm = float(input("Digite o comprimento da corda em cm: "))
comprimento_haste_cm = float(input("Digite o comprimento da haste em cm: "))
distancia_meta_m = float(input("Digite a distância da meta em metros: "))

#Variáveis da parte da mola
constante_torsional_mola = float(input("Digite a constante torsional da mola em N·m/rad: ")) # Kθ​
angulo_inicial_da_mola_em_graus = float(input("Digite o ângulo inicial da mola em graus: "))
angulo_atual_da_mola_em_graus = float(input("Digite o ângulo atual da mola em graus: "))

if constante_torsional_mola <= 0 or angulo_inicial_da_mola_em_graus <= 0 or angulo_atual_da_mola_em_graus < 0 or angulo_atual_da_mola_em_graus > angulo_inicial_da_mola_em_graus:
    print("A constante torsional da mola deve ser positiva e maior que zero, o ângulo inicial da mola deve ser maior ou igual a zero"
    "e o ângulo atual da mola deve ser maior ou igual a zero e menor ou igual ao ângulo inicial.")
    exit()

if diametro_roda_cm <= 0 or diametro_eixo_cm <= 0 or comprimento_corda_cm <= 0 or comprimento_haste_cm <= 0 or distancia_meta_m <= 0:
    print("Todos os valores devem ser positivos e maiores que zero.")
    exit()

angulo_inicial_em_rad = math.radians(angulo_inicial_da_mola_em_graus)
angulo_atual_em_rad = math.radians(angulo_atual_da_mola_em_graus)
torque_inicial = constante_torsional_mola * angulo_inicial_em_rad
torque_atual = constante_torsional_mola * angulo_atual_em_rad
energia_inicial = 0.5 * constante_torsional_mola * (angulo_inicial_em_rad ** 2) #fórmula de energia armazenada na mola: E = 1/2 * k * θ²
energia_atual = 0.5 * constante_torsional_mola * (angulo_atual_em_rad ** 2)
energia_liberada = energia_inicial - energia_atual #quanto da energia inicial já saiu da mola.
porcentagem_energia_restante = (energia_atual / energia_inicial) * 100 

print(f"Torque inicial: {torque_inicial:.4f} N·m")
print(f"Torque atual: {torque_atual:.4f} N·m") #    τ=kθ​θ -> torque naquele instante 





 


resultado_geometria = calcular_geometria(diametro_roda_cm,diametro_eixo_cm,comprimento_corda_cm)

# Retira a distância de dentro do dicionário
distancia_calculada_m = resultado_geometria["distancia_teorica_m"]
margem_calculada_m  = distancia_calculada_m - distancia_meta_m
porcentagem_meta = (distancia_calculada_m / distancia_meta_m) * 100

if distancia_calculada_m >= distancia_meta_m:
    print("O carrinho alcançou a meta!")
    print(f"sobraram {margem_calculada_m:.2f} metros da meta")
    print(f"A distância teórica corresponde {porcentagem_meta:.2f}% da meta")
else:
    print("O carrinho não alcançou a meta.")
    print(f"faltaram {abs(margem_calculada_m):.2f} metros para a meta")
    print(f"A distância teórica corresponde {porcentagem_meta:.2f}% da meta")

    ajustes = calcular_ajustes_para_meta(diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm, distancia_meta_m)

    print("\nPossíveis ajustes geométricos:")
    print("Escolha uma das alternativas abaixo:")
    print("\n1. Aumentar o diâmetro da roda para "f'{ajustes["diametro_roda_necessario_cm"]:.2f} cm 'f'(+{ajustes["aumento_roda_cm"]:.2f} cm).')
    print("2. Aumentar o comprimento da corda para " f'{ajustes["comprimento_corda_necessario_cm"]:.2f} cm 'f'(+{ajustes["aumento_corda_cm"]:.2f} cm).')
    print("3. Reduzir o diâmetro do eixo para no máximo "f'{ajustes["diametro_eixo_maximo_cm"]:.3f} cm 'f'(-{ajustes["reducao_eixo_cm"]:.3f} cm).')
    print("\n⚠ Cada alternativa foi calculada separadamente, ""mantendo as outras medidas iguais.")
    print("⚠ A influência dessas mudanças no torque ""será analisada na V2.")

print(
    "⚠ Este resultado é apenas teórico e ainda não considera "
    "massa, atrito, derrapagem ou perdas de energia."
)