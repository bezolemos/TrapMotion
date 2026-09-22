import math


def calcular_geometria(
    diametro_roda_cm,
    diametro_eixo_cm,
    comprimento_corda_cm
):
    # Cálculos feitos dentro da função
    raio_roda_m = (diametro_roda_cm / 100) / 2
    raio_eixo_m = (diametro_eixo_cm / 100) / 2

    circunferencia_eixo_m = 2 * math.pi * raio_eixo_m
    circunferencia_roda_m = 2 * math.pi * raio_roda_m

    rotacoes = (
        comprimento_corda_cm / 100
    ) / circunferencia_eixo_m

    distancia_teorica_m = (
        rotacoes * circunferencia_roda_m
    )

    resultados = {
        "raio_roda_m": raio_roda_m,
        "raio_eixo_m": raio_eixo_m,
        "circunferencia_eixo_m": circunferencia_eixo_m,
        "circunferencia_roda_m": circunferencia_roda_m,
        "rotacoes": rotacoes,
        "distancia_teorica_m": distancia_teorica_m
    }

    return resultados


def calcular_mola(
    constante_torsional_mola,
    angulo_inicial_graus,
    angulo_atual_graus,
    comprimento_haste_cm,
    raio_eixo_m,
    raio_roda_m
):
    # ---------------- Conversões ----------------

    comprimento_haste_m = comprimento_haste_cm / 100

    angulo_inicial_rad = math.radians(
        angulo_inicial_graus
    )

    angulo_atual_rad = math.radians(
        angulo_atual_graus
    )

    # ---------------- Torque produzido pela mola ----------------

    torque_inicial = (
        constante_torsional_mola * angulo_inicial_rad
    )

    torque_atual = (
        constante_torsional_mola * angulo_atual_rad
    )

    # ---------------- Energia armazenada na mola ----------------

    energia_inicial = (
        0.5
        * constante_torsional_mola
        * (angulo_inicial_rad ** 2)
    )

    energia_atual = (
        0.5
        * constante_torsional_mola
        * (angulo_atual_rad ** 2)
    )

    energia_liberada = (
        energia_inicial - energia_atual
    )

    porcentagem_energia_restante = (
        energia_atual / energia_inicial
    ) * 100

    # ---------------- Tensão da corda ----------------
    # Simplificação da V2:
    # O ângulo entre a haste e a corda é considerado
    # sempre igual a 90 graus.

    tensao_inicial_corda = (
        torque_inicial / comprimento_haste_m
    )

    tensao_atual_corda = (
        torque_atual / comprimento_haste_m
    )

    # ---------------- Torque transmitido ao eixo ----------------

    torque_inicial_eixo = (
        tensao_inicial_corda * raio_eixo_m
    )

    torque_atual_eixo = (
        tensao_atual_corda * raio_eixo_m
    )

    # ---------------- Força de tração ideal ----------------

    forca_tracao_inicial = (
        torque_inicial_eixo / raio_roda_m
    )

    forca_tracao_atual = (
        torque_atual_eixo / raio_roda_m
    )

    resultados_mola = {
        "angulo_inicial_rad": angulo_inicial_rad,
        "angulo_atual_rad": angulo_atual_rad,

        "torque_inicial": torque_inicial,
        "torque_atual": torque_atual,

        "energia_inicial": energia_inicial,
        "energia_atual": energia_atual,
        "energia_liberada": energia_liberada,

        "porcentagem_energia_restante":
            porcentagem_energia_restante,

        "tensao_inicial_corda": tensao_inicial_corda,
        "tensao_atual_corda": tensao_atual_corda,

        "torque_inicial_eixo": torque_inicial_eixo,
        "torque_atual_eixo": torque_atual_eixo,

        "forca_tracao_inicial": forca_tracao_inicial,
        "forca_tracao_atual": forca_tracao_atual
    }

    return resultados_mola


def calcular_aceleracao_ideal(
    massa_total_carrinho_g,
    forca_tracao_inicial,
    forca_tracao_atual
):
    # Conversão de gramas para quilogramas
    massa_total_carrinho_kg = (
        massa_total_carrinho_g / 1000
    )

    # Segunda Lei de Newton: a = F / m
    aceleracao_inicial = (
        forca_tracao_inicial / massa_total_carrinho_kg
    )

    aceleracao_atual = (
        forca_tracao_atual / massa_total_carrinho_kg
    )

    resultados_aceleracao = {
        "massa_total_carrinho_g":
            massa_total_carrinho_g,

        "massa_total_carrinho_kg":
            massa_total_carrinho_kg,

        "aceleracao_inicial":
            aceleracao_inicial,

        "aceleracao_atual":
            aceleracao_atual
    }

    return resultados_aceleracao


def calcular_resistencia_movimento(
    massa_total_carrinho_g,
    coeficiente_resistencia_rolamento,
    forca_tracao_inicial,
    forca_tracao_atual
):
    # Conversão de gramas para quilogramas
    massa_total_carrinho_kg = (
        massa_total_carrinho_g / 1000
    )

    # Peso: P = m * g
    forca_peso = (
        massa_total_carrinho_kg * gravidade
    )

    # Em um plano horizontal,
    # a força normal é igual ao peso
    forca_normal = forca_peso

    # Resistência ao rolamento: Frr = Crr * N
    forca_resistencia_rolamento = (
        coeficiente_resistencia_rolamento
        * forca_normal
    )

    # Força resultante: Fres = Ftracao - Frr
    forca_resultante_inicial = (
        forca_tracao_inicial
        - forca_resistencia_rolamento
    )

    forca_resultante_atual = (
        forca_tracao_atual
        - forca_resistencia_rolamento
    )

    # Aceleração considerando resistência
    aceleracao_resistencia_inicial = (
        forca_resultante_inicial
        / massa_total_carrinho_kg
    )

    aceleracao_resistencia_atual = (
        forca_resultante_atual
        / massa_total_carrinho_kg
    )

    return (
        forca_peso,
        forca_normal,
        forca_resistencia_rolamento,
        forca_resultante_inicial,
        forca_resultante_atual,
        aceleracao_resistencia_inicial,
        aceleracao_resistencia_atual
    )

def calcular_aderencia(coeficiente_atrito_estatico, forca_normal):
    # Força de aderência máxima: Faderencia = μ * N
    forca_aderencia_maxima = (
        coeficiente_atrito_estatico * forca_normal
    )
    return forca_aderencia_maxima




def calcular_ajustes_para_meta(
    diametro_roda_cm,
    diametro_eixo_cm,
    comprimento_corda_cm,
    distancia_meta_m
):
    # Conversão das medidas para metros
    diametro_roda_m = diametro_roda_cm / 100
    diametro_eixo_m = diametro_eixo_cm / 100
    comprimento_corda_m = comprimento_corda_cm / 100

    # Alternativa 1: aumentar o diâmetro da roda
    diametro_roda_necessario_m = (
        distancia_meta_m
        * diametro_eixo_m
        / comprimento_corda_m
    )

    # Alternativa 2: aumentar o comprimento da corda
    comprimento_corda_necessario_m = (
        distancia_meta_m
        * diametro_eixo_m
        / diametro_roda_m
    )

    # Alternativa 3: reduzir o diâmetro do eixo
    diametro_eixo_maximo_m = (
        comprimento_corda_m
        * diametro_roda_m
        / distancia_meta_m
    )

    # Conversão dos resultados para centímetros
    diametro_roda_necessario_cm = (
        diametro_roda_necessario_m * 100
    )

    comprimento_corda_necessario_cm = (
        comprimento_corda_necessario_m * 100
    )

    diametro_eixo_maximo_cm = (
        diametro_eixo_maximo_m * 100
    )

    # Calcula quanto cada medida precisaria mudar
    aumento_roda_cm = max(
        0.0,
        diametro_roda_necessario_cm - diametro_roda_cm
    )

    aumento_corda_cm = max(
        0.0,
        comprimento_corda_necessario_cm
        - comprimento_corda_cm
    )

    reducao_eixo_cm = max(
        0.0,
        diametro_eixo_cm - diametro_eixo_maximo_cm
    )

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


# ---------------- Variáveis de geometria ----------------

diametro_roda_cm = float(
    input("Digite o diâmetro da roda em cm: ")
)

diametro_eixo_cm = float(
    input("Digite o diâmetro do eixo em cm: ")
)

comprimento_corda_cm = float(
    input("Digite o comprimento da corda em cm: ")
)

comprimento_haste_cm = float(
    input("Digite o comprimento da haste em cm: ")
)

distancia_meta_m = float(
    input("Digite a distância da meta em metros: ")
)


# ---------------- Variáveis da mola ----------------

constante_torsional_mola = float(
    input(
        "Digite a constante torsional da mola "
        "em N·m/rad: "
    )
)

angulo_inicial_da_mola_em_graus = float(
    input(
        "Digite o ângulo inicial da mola em graus: "
    )
)

angulo_atual_da_mola_em_graus = float(
    input(
        "Digite o ângulo atual da mola em graus: "
    )
)


# ---------------- Variável da V3 ----------------

massa_total_carrinho_g = float(
    input(
        "Digite a massa total do carrinho em g: "
    )
)


# ---------------- Variáveis da V4 ----------------

gravidade = 9.81  # m/s²

coeficiente_resistencia_rolamento = 0.02

# ---------------- Variáveis da V5 ----------------
coeficiente_atrito_estatico = float(input("Digite o coeficiente de atrito estático (μ): "))





# ---------------- Validação das entradas ----------------

if (
    constante_torsional_mola <= 0
    or angulo_inicial_da_mola_em_graus <= 0
    or angulo_atual_da_mola_em_graus < 0
    or angulo_atual_da_mola_em_graus
    > angulo_inicial_da_mola_em_graus
):
    print(
        "A constante torsional da mola deve ser maior que zero. "
        "O ângulo inicial também deve ser maior que zero. "
        "O ângulo atual deve estar entre zero e o ângulo inicial."
    )
    exit()


if (
    diametro_roda_cm <= 0
    or diametro_eixo_cm <= 0
    or comprimento_corda_cm <= 0
    or comprimento_haste_cm <= 0
    or distancia_meta_m <= 0
):
    print(
        "Todos os valores geométricos devem ser "
        "positivos e maiores que zero."
    )
    exit()


if massa_total_carrinho_g <= 0:
    print(
        "A massa total do carrinho deve ser "
        "positiva e maior que zero."
    )
    exit()


if coeficiente_resistencia_rolamento < 0:
    print(
        "O coeficiente de resistência ao rolamento "
        "não pode ser negativo."
    )
    exit()

if coeficiente_atrito_estatico < 0:
    print(
        "O coeficiente de atrito estático (μ) "
        "não pode ser negativo."
    )
    exit()
# ---------------- Execução dos cálculos ----------------

resultado_geometria = calcular_geometria(
    diametro_roda_cm,
    diametro_eixo_cm,
    comprimento_corda_cm
)


resultado_mola = calcular_mola(
    constante_torsional_mola,
    angulo_inicial_da_mola_em_graus,
    angulo_atual_da_mola_em_graus,
    comprimento_haste_cm,
    resultado_geometria["raio_eixo_m"],
    resultado_geometria["raio_roda_m"]
)


resultado_aceleracao = calcular_aceleracao_ideal(
    massa_total_carrinho_g,
    resultado_mola["forca_tracao_inicial"],
    resultado_mola["forca_tracao_atual"]
)


(
    forca_peso,
    forca_normal,
    forca_resistencia_rolamento,
    forca_resultante_inicial,
    forca_resultante_atual,
    aceleracao_resistencia_inicial,
    aceleracao_resistencia_atual
) = calcular_resistencia_movimento(
    massa_total_carrinho_g,
    coeficiente_resistencia_rolamento,
    resultado_mola["forca_tracao_inicial"],
    resultado_mola["forca_tracao_atual"]
)

forca_aderencia_maxima = calcular_aderencia(
    coeficiente_atrito_estatico,
    forca_normal
)

if math.isclose(resultado_mola["forca_tracao_inicial"],forca_aderencia_maxima):
    print(
        "\n⚠ A força de tração inicial está no limite "
        "de aderência."
    )

elif (resultado_mola["forca_tracao_inicial"] < forca_aderencia_maxima):
    print(
        "\n✅ A força de tração inicial está dentro "
        "do limite de aderência."
    )

else:
    print(
        "\n⚠ A força de tração inicial excede "
        "o limite de aderência. "
        "O carrinho pode derrapar."
    )
#----- agora vamos verificar a força de tração atual em relação à aderência máxima
if math.isclose(resultado_mola["forca_tracao_atual"],forca_aderencia_maxima):
    print(
        "\n⚠ A força de tração atual está no limite "
        "de aderência."
    )

elif (resultado_mola["forca_tracao_atual"] < forca_aderencia_maxima):
    print(
        "\n✅ A força de tração atual está dentro "
        "do limite de aderência."
    )

else:
    print(
        "\n⚠ A força de tração atual excede "
        "o limite de aderência. "
        "O carrinho pode derrapar."
    )

forca_tracao_util_inicial = min(resultado_mola["forca_tracao_inicial"], forca_aderencia_maxima)
forca_tracao_util_atual = min(resultado_mola["forca_tracao_atual"], forca_aderencia_maxima)

forca_resultante_aderencia_inicial = forca_tracao_util_inicial - forca_resistencia_rolamento
forca_resultante_aderencia_atual = forca_tracao_util_atual - forca_resistencia_rolamento

aceleracao_aderencia_inicial = (
    forca_resultante_aderencia_inicial
    / resultado_aceleracao["massa_total_carrinho_kg"]
)

aceleracao_aderencia_atual = (
    forca_resultante_aderencia_atual
    / resultado_aceleracao["massa_total_carrinho_kg"]
)

reducao_aceleracao_inicial = (resultado_aceleracao["aceleracao_inicial"] - aceleracao_resistencia_inicial)

reducao_aceleracao_atual = (resultado_aceleracao["aceleracao_atual"] - aceleracao_resistencia_atual)

# ---------------- Resultados da V2 ----------------

print("\n---------------- RESULTADOS DA V2 ----------------")

print(
    f"Torque inicial: "
    f"{resultado_mola['torque_inicial']:.4f} N·m"
)

print(
    f"Torque atual: "
    f"{resultado_mola['torque_atual']:.4f} N·m"
)

print(
    f"Energia inicial: "
    f"{resultado_mola['energia_inicial']:.4f} J"
)

print(
    f"Energia atual: "
    f"{resultado_mola['energia_atual']:.4f} J"
)

print(
    f"Energia liberada: "
    f"{resultado_mola['energia_liberada']:.4f} J"
)

print(
    f"Porcentagem de energia restante: "
    f"{resultado_mola['porcentagem_energia_restante']:.2f}%"
)

print(
    f"Tensão inicial da corda: "
    f"{resultado_mola['tensao_inicial_corda']:.4f} N"
)

print(
    f"Tensão atual da corda: "
    f"{resultado_mola['tensao_atual_corda']:.4f} N"
)

print(
    f"Torque inicial no eixo: "
    f"{resultado_mola['torque_inicial_eixo']:.4f} N·m"
)

print(
    f"Torque atual no eixo: "
    f"{resultado_mola['torque_atual_eixo']:.4f} N·m"
)

print(
    f"Força de tração inicial nas rodas: "
    f"{resultado_mola['forca_tracao_inicial']:.4f} N"
)

print(
    f"Força de tração atual nas rodas: "
    f"{resultado_mola['forca_tracao_atual']:.4f} N"
)


# ---------------- Resultados da V3 ----------------

print("\n---------------- RESULTADOS DA V3 ----------------")

print(
    f"Massa total do carrinho: "
    f"{resultado_aceleracao['massa_total_carrinho_kg']:.3f} kg"
)

print(
    f"Aceleração ideal inicial: "
    f"{resultado_aceleracao['aceleracao_inicial']:.4f} m/s²"
)

print(
    f"Aceleração ideal atual: "
    f"{resultado_aceleracao['aceleracao_atual']:.4f} m/s²"
)

# ---------------- Resultados da V4 -------------------
print("\n---------------- RESULTADOS DA V4 ----------------")

print(f"coeficiente de resistência ao rolamento: {coeficiente_resistencia_rolamento:.4f}")

print(f"força peso: {forca_peso:.4f} N")
print(f"força normal: {forca_normal:.4f} N")

print(f"resistência ao rolamento: {forca_resistencia_rolamento:.4f} N")

print(f"força resultante inicial: {forca_resultante_inicial:.4f} N")
print(f"força resultante atual: {forca_resultante_atual:.4f} N")

print(f"aceleração inicial com resistência: {aceleracao_resistencia_inicial:.4f} m/s²")
print(f"aceleração atual com resistência: {aceleracao_resistencia_atual:.4f} m/s²")

# ------------------- Resultados da V5 ----------------------

print(
    f"Coeficiente de atrito estático: "
    f"{coeficiente_atrito_estatico:.4f}"
)

print(
    f"Força máxima de aderência: "
    f"{forca_aderencia_maxima:.4f} N"
)

print(
    f"Força de tração utilizável inicial: "
    f"{forca_tracao_util_inicial:.4f} N"
)

print(
    f"Força de tração utilizável atual: "
    f"{forca_tracao_util_atual:.4f} N"
)

print(
    f"Força resultante inicial considerando aderência: "
    f"{forca_resultante_aderencia_inicial:.4f} N"
)

print(
    f"Força resultante atual considerando aderência: "
    f"{forca_resultante_aderencia_atual:.4f} N"
)

print(
    f"Aceleração inicial considerando aderência: "
    f"{aceleracao_aderencia_inicial:.4f} m/s²"
)

print(
    f"Aceleração atual considerando aderência: "
    f"{aceleracao_aderencia_atual:.4f} m/s²"
)
# ---------------- Interpretação da V3 ----------------

aceleracao_inicial = (
    resultado_aceleracao["aceleracao_inicial"]
)

aceleracao_atual = (
    resultado_aceleracao["aceleracao_atual"]
)

print("\nInterpretação da aceleração:")


if aceleracao_atual == 0:
    print(
        "A aceleração atual é zero porque a mola não produz "
        "mais força de tração neste estado."
    )

    print(
        "No modelo ideal, o carrinho ainda pode continuar em "
        "movimento com velocidade constante. No mundo real, "
        "as resistências começariam a reduzir sua velocidade."
    )


elif aceleracao_atual < aceleracao_inicial:
    print(
        "A aceleração atual é menor que a inicial porque "
        "a força produzida pela mola diminuiu."
    )

    print(
        "Isso não significa necessariamente que o carrinho está "
        "perdendo velocidade. Ele ainda pode estar acelerando, "
        "mas com menor intensidade."
    )


elif aceleracao_atual == aceleracao_inicial:
    print(
        "A aceleração atual é igual à inicial porque "
        "a força de tração permaneceu igual."
    )


else:
    print(
        "A aceleração atual é maior que a inicial. Esse resultado "
        "não é esperado pelas simplificações atuais do modelo."
    )


print(
    "Para a mesma força de tração, aumentar a massa reduz "
    "a aceleração, enquanto diminuir a massa aumenta "
    "a aceleração."
)


# ---------------- Interpretação da V4 ----------------

if forca_resultante_inicial > 0:
    print(
        "A força de tração supera a resistência ao rolamento. "
        "Há aceleração no sentido do movimento."
    )

elif forca_resultante_inicial == 0:
    print(
        "A força de tração e a resistência ao rolamento "
        "estão equilibradas. A aceleração resultante é zero."
    )

else:
    print(
        "A resistência ao rolamento supera a força de tração."
    )

    print(
        "Se o carrinho já estiver em movimento para frente, "
        "isso indica tendência à desaceleração."
    )


if forca_resultante_atual > 0:
    print(
        "A força de tração ainda supera a resistência ao rolamento "
        "na situação atual."
    )

elif forca_resultante_atual == 0:
    print(
        "A força de tração e a resistência ao rolamento "
        "estão equilibradas na situação atual."
    )

else:
    print(
        "A resistência ao rolamento agora supera a tração "
        "na situação atual."
    )

    print(
        "Se o carrinho estiver em movimento para frente, "
        "isso indica tendência à desaceleração."
    )


# ---------------- Verificação da distância ----------------

distancia_calculada_m = (
    resultado_geometria["distancia_teorica_m"]
)

margem_calculada_m = (
    distancia_calculada_m - distancia_meta_m
)

porcentagem_meta = (
    distancia_calculada_m / distancia_meta_m
) * 100


if distancia_calculada_m >= distancia_meta_m:
    print("\nA geometria do projeto possui alcance teórico "
    "suficiente para a meta.")

    print(
        f"Sobraram {margem_calculada_m:.2f} "
        "metros da meta."
    )

    print(
        f"A distância teórica corresponde a "
        f"{porcentagem_meta:.2f}% da meta."
    )


else:
    print("\nA geometria do projeto não possui alcance teórico "
    "suficiente para a meta.")

    print(
        f"Faltaram {abs(margem_calculada_m):.2f} "
        "metros para a meta."
    )

    print(
        f"A distância teórica corresponde a "
        f"{porcentagem_meta:.2f}% da meta."
    )

    ajustes = calcular_ajustes_para_meta(
        diametro_roda_cm,
        diametro_eixo_cm,
        comprimento_corda_cm,
        distancia_meta_m
    )

    print("\nPossíveis ajustes geométricos:")
    print("Escolha uma das alternativas abaixo:")

    print(
        "\n1. Aumentar o diâmetro da roda para "
        f"{ajustes['diametro_roda_necessario_cm']:.2f} cm "
        f"(+{ajustes['aumento_roda_cm']:.2f} cm)."
    )

    print(
        "2. Aumentar o comprimento da corda para "
        f"{ajustes['comprimento_corda_necessario_cm']:.2f} cm "
        f"(+{ajustes['aumento_corda_cm']:.2f} cm)."
    )

    print(
        "3. Reduzir o diâmetro do eixo para no máximo "
        f"{ajustes['diametro_eixo_maximo_cm']:.3f} cm "
        f"(-{ajustes['reducao_eixo_cm']:.3f} cm)."
    )

    print(
        "\n⚠ Cada alternativa foi calculada separadamente, "
        "mantendo as outras medidas iguais."
    )


# ---------------- Limitações do modelo ----------------

print(
    "\n⚠ Este resultado ainda é simplificado. "
    "A V5 considera a resistência ao rolamento e o limite "
    "de aderência das rodas, mas não simula detalhadamente "
    "a patinagem, o atrito cinético, a distribuição de peso "
    "entre os eixos, a resistência do ar, a inércia rotacional "
    "ou outras perdas mecânicas."
)