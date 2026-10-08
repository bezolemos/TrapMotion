"""TrapMotion — motor físico do Projeto 15 (V1 até V10).

Não depende de Tkinter/Matplotlib: recebe números e devolve dicionários.
As equações são um modelo educacional simplificado para carrinhos de ratoeira.
"""

import math

GRAVIDADE = 9.81  # m/s²
PASSO_TEMPO = 0.005  # s
TEMPO_MAXIMO = 60.0  # s


def calcular_constante_torsional(forca_n, comprimento_haste_cm, angulo_graus):
    """Estima k = (F * L) / θ com força perpendicular à haste.

    θ deve ser medido a partir da posição relaxada da mola.
    """
    if not (math.isfinite(forca_n) and math.isfinite(comprimento_haste_cm)
            and math.isfinite(angulo_graus)):
        raise ValueError("As medidas da mola devem ser números finitos.")
    if forca_n <= 0 or comprimento_haste_cm <= 0 or angulo_graus <= 0:
        raise ValueError("Força, haste e ângulo medidos devem ser maiores que zero.")
    comprimento_haste_m = comprimento_haste_cm / 100
    angulo_rad = math.radians(angulo_graus)
    return forca_n * comprimento_haste_m / angulo_rad


def calcular_geometria(diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm):
    """V1: converte medidas, calcula rotações e alcance geométrico ideal."""
    raio_roda_m = diametro_roda_cm / 200
    raio_eixo_m = diametro_eixo_cm / 200
    circunferencia_eixo_m = 2 * math.pi * raio_eixo_m
    circunferencia_roda_m = 2 * math.pi * raio_roda_m
    rotacoes = (comprimento_corda_cm / 100) / circunferencia_eixo_m
    return {
        "raio_roda_m": raio_roda_m,
        "raio_eixo_m": raio_eixo_m,
        "circunferencia_eixo_m": circunferencia_eixo_m,
        "circunferencia_roda_m": circunferencia_roda_m,
        "rotacoes": rotacoes,
        "distancia_teorica_m": rotacoes * circunferencia_roda_m,
    }


def calcular_mola(constante_torsional_mola, angulo_inicial_graus,
                  angulo_atual_graus, comprimento_haste_cm,
                  raio_eixo_m, raio_roda_m):
    """V2: mola torsional ideal; direção da corda perpendicular à haste.

    Torque τ = kθ e energia E = (1/2)kθ².
    """
    angulo_inicial_rad = math.radians(angulo_inicial_graus)
    angulo_atual_rad = math.radians(angulo_atual_graus)
    comprimento_haste_m = comprimento_haste_cm / 100
    torque_inicial = constante_torsional_mola * angulo_inicial_rad
    torque_atual = constante_torsional_mola * angulo_atual_rad
    energia_inicial = 0.5 * constante_torsional_mola * angulo_inicial_rad ** 2
    energia_atual = 0.5 * constante_torsional_mola * angulo_atual_rad ** 2
    tensao_inicial = torque_inicial / comprimento_haste_m
    tensao_atual = torque_atual / comprimento_haste_m
    torque_eixo_inicial = tensao_inicial * raio_eixo_m
    torque_eixo_atual = tensao_atual * raio_eixo_m
    return {
        "angulo_inicial_rad": angulo_inicial_rad,
        "angulo_atual_rad": angulo_atual_rad,
        "torque_inicial": torque_inicial,
        "torque_atual": torque_atual,
        "energia_inicial": energia_inicial,
        "energia_atual": energia_atual,
        "energia_liberada": energia_inicial - energia_atual,
        "porcentagem_energia_restante": 100 * energia_atual / energia_inicial,
        "tensao_inicial_corda": tensao_inicial,
        "tensao_atual_corda": tensao_atual,
        "torque_inicial_eixo": torque_eixo_inicial,
        "torque_atual_eixo": torque_eixo_atual,
        "forca_tracao_inicial": torque_eixo_inicial / raio_roda_m,
        "forca_tracao_atual": torque_eixo_atual / raio_roda_m,
    }


def calcular_aceleracao_ideal(massa_total_carrinho_g, forca_tracao_inicial,
                               forca_tracao_atual):
    """V3: segunda lei de Newton, antes das resistências."""
    massa_kg = massa_total_carrinho_g / 1000
    return {
        "massa_total_carrinho_g": massa_total_carrinho_g,
        "massa_total_carrinho_kg": massa_kg,
        "aceleracao_inicial": forca_tracao_inicial / massa_kg,
        "aceleracao_atual": forca_tracao_atual / massa_kg,
    }


def calcular_resistencia_movimento(massa_total_carrinho_g,
                                   coeficiente_resistencia_rolamento,
                                   forca_tracao_inicial, forca_tracao_atual):
    """V4: superfície horizontal, normal = peso e Frr = Crr * N."""
    massa_kg = massa_total_carrinho_g / 1000
    forca_peso = massa_kg * GRAVIDADE
    forca_normal = forca_peso
    forca_resistencia = coeficiente_resistencia_rolamento * forca_normal
    forca_resultante_inicial = forca_tracao_inicial - forca_resistencia
    forca_resultante_atual = forca_tracao_atual - forca_resistencia
    return {
        "forca_peso": forca_peso,
        "forca_normal": forca_normal,
        "forca_resistencia_rolamento": forca_resistencia,
        "forca_resultante_inicial": forca_resultante_inicial,
        "forca_resultante_atual": forca_resultante_atual,
        "aceleracao_resistencia_inicial": forca_resultante_inicial / massa_kg,
        "aceleracao_resistencia_atual": forca_resultante_atual / massa_kg,
    }


def calcular_aderencia(coeficiente_atrito_estatico, forca_normal):
    """V5: limite da força de tração transmitida: μ * N."""
    return coeficiente_atrito_estatico * forca_normal


def calcular_corda_desenrolada_passo(deslocamento_passo_m, raio_eixo_m, raio_roda_m):
    """V6: sem escorregamento; relaciona roda, eixo e corda."""
    return deslocamento_passo_m * raio_eixo_m / raio_roda_m


def calcular_angulo_mola_variacao(corda_desenrolada_passo_m, comprimento_haste_m):
    """Aproximação geométrica: Δθ ≈ Δcorda / L (radianos)."""
    return corda_desenrolada_passo_m / comprimento_haste_m


def atualizar_angulo_mola(angulo_atual_rad, variacao_angulo_rad):
    return max(0.0, angulo_atual_rad - variacao_angulo_rad)


def atualizar_velocidade(velocidade_atual, aceleracao_atual, passo_tempo):
    return max(0.0, velocidade_atual + aceleracao_atual * passo_tempo)


def calcular_deslocamento(velocidade_atual, passo_tempo):
    return velocidade_atual * passo_tempo


def calcular_ajustes_para_meta(diametro_roda_cm, diametro_eixo_cm,
                               comprimento_corda_cm, distancia_meta_m):
    """V1/V9: três alternativas geométricas isoladas para a meta."""
    diametro_roda_m = diametro_roda_cm / 100
    diametro_eixo_m = diametro_eixo_cm / 100
    comprimento_corda_m = comprimento_corda_cm / 100
    diametro_roda_necessario_cm = (distancia_meta_m * diametro_eixo_m
                                  / comprimento_corda_m) * 100
    comprimento_corda_necessario_cm = (distancia_meta_m * diametro_eixo_m
                                      / diametro_roda_m) * 100
    diametro_eixo_maximo_cm = (comprimento_corda_m * diametro_roda_m
                              / distancia_meta_m) * 100
    return {
        "diametro_roda_necessario_cm": diametro_roda_necessario_cm,
        "aumento_roda_cm": max(0.0, diametro_roda_necessario_cm - diametro_roda_cm),
        "comprimento_corda_necessario_cm": comprimento_corda_necessario_cm,
        "aumento_corda_cm": max(0.0, comprimento_corda_necessario_cm - comprimento_corda_cm),
        "diametro_eixo_maximo_cm": diametro_eixo_maximo_cm,
        "reducao_eixo_cm": max(0.0, diametro_eixo_cm - diametro_eixo_maximo_cm),
    }


def _validar_entradas(roda, eixo, corda, haste, massa, meta,
                      k, angulo_inicial, angulo_atual, mu, crr):
    """Valida os números antes de qualquer divisão ou loop."""
    valores = (roda, eixo, corda, haste, massa, meta,
               k, angulo_inicial, angulo_atual, mu, crr)
    if any(not isinstance(valor, (float, int)) or not math.isfinite(valor)
           for valor in valores):
        raise ValueError("Todos os campos precisam conter números válidos e finitos.")
    if any(valor <= 0 for valor in (roda, eixo, corda, haste, massa, meta, k)):
        raise ValueError("Roda, eixo, corda, haste, massa, meta e constante devem ser maiores que zero.")
    if angulo_inicial <= 0 or angulo_atual < 0 or angulo_atual > angulo_inicial:
        raise ValueError("O ângulo inicial deve ser positivo e o atual entre zero e o inicial.")
    if mu < 0 or crr < 0:
        raise ValueError("Os coeficientes de atrito e rolamento não podem ser negativos.")


def executar_simulacao(
    diametro_roda_cm,
    diametro_eixo_cm,
    comprimento_corda_cm,
    comprimento_haste_cm,
    massa_total_carrinho_g,
    distancia_meta_m,
    constante_torsional_mola,
    angulo_inicial_da_mola_em_graus,
    angulo_atual_da_mola_em_graus,
    coeficiente_atrito_estatico=0.6,
    coeficiente_resistencia_rolamento=0.02,
    passo_tempo=PASSO_TEMPO,
    tempo_maximo_simulacao=TEMPO_MAXIMO,
):
    """Executa a física V1–V9 e devolve históricos para os gráficos da V10.

    Duas fases: (1) impulsionada pela mola; (2) livre, com resistência.
    O modelo desconsidera arrasto, inércia rotacional e patinagem detalhada.
    """
    _validar_entradas(
        diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm,
        comprimento_haste_cm, massa_total_carrinho_g, distancia_meta_m,
        constante_torsional_mola, angulo_inicial_da_mola_em_graus,
        angulo_atual_da_mola_em_graus, coeficiente_atrito_estatico,
        coeficiente_resistencia_rolamento,
    )
    if not math.isfinite(passo_tempo) or not math.isfinite(tempo_maximo_simulacao):
        raise ValueError("Intervalo e duração devem ser finitos.")
    if passo_tempo <= 0 or tempo_maximo_simulacao <= 0:
        raise ValueError("Intervalo e duração devem ser positivos.")

    # V1–V5: a sequência das funções auxiliares preserva o modelo original.
    geometria = calcular_geometria(
        diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm)
    mola = calcular_mola(
        constante_torsional_mola, angulo_inicial_da_mola_em_graus,
        angulo_atual_da_mola_em_graus, comprimento_haste_cm,
        geometria["raio_eixo_m"], geometria["raio_roda_m"])
    aceleracao_ideal = calcular_aceleracao_ideal(
        massa_total_carrinho_g, mola["forca_tracao_inicial"],
        mola["forca_tracao_atual"])
    resistencia = calcular_resistencia_movimento(
        massa_total_carrinho_g, coeficiente_resistencia_rolamento,
        mola["forca_tracao_inicial"], mola["forca_tracao_atual"])
    aderencia_maxima = calcular_aderencia(
        coeficiente_atrito_estatico, resistencia["forca_normal"])
    resistencia_rolamento = resistencia["forca_resistencia_rolamento"]
    massa_kg = aceleracao_ideal["massa_total_carrinho_kg"]
    forca_tracao_util_inicial = min(mola["forca_tracao_inicial"], aderencia_maxima)
    forca_tracao_util_atual = min(mola["forca_tracao_atual"], aderencia_maxima)
    forca_resultante_aderencia_inicial = forca_tracao_util_inicial - resistencia_rolamento
    forca_resultante_aderencia_atual = forca_tracao_util_atual - resistencia_rolamento
    aceleracao_aderencia_inicial = forca_resultante_aderencia_inicial / massa_kg
    aceleracao_aderencia_atual = forca_resultante_aderencia_atual / massa_kg

    # V6/V7: variáveis de estado e registros de cada passo de tempo.
    tempo = 0.0
    velocidade = 0.0
    posicao = 0.0
    corda_usada_m = 0.0
    comprimento_corda_m = comprimento_corda_cm / 100
    comprimento_haste_m = comprimento_haste_cm / 100
    # A simulação parte do ângulo ATUAL informado, e não o ignora.
    angulo_rad = math.radians(angulo_atual_da_mola_em_graus)
    aceleracao = aceleracao_aderencia_atual
    aceleracao_livre = -resistencia_rolamento / massa_kg
    motivo_impulsao = ""

    historico_tempo = [tempo]
    historico_velocidade = [velocidade]
    historico_aceleracao = [aceleracao]
    historico_angulo = [angulo_rad]
    historico_posicao = [posicao]

    # FASE 1 — fio puxando o eixo, enquanto houver ângulo e corda.
    while (angulo_rad > 0 and corda_usada_m < comprimento_corda_m
           and tempo < tempo_maximo_simulacao):
        dt = min(passo_tempo, tempo_maximo_simulacao - tempo)
        nova_velocidade = atualizar_velocidade(velocidade, aceleracao, dt)
        carrinho_parou = nova_velocidade == 0 and aceleracao <= 0
        if carrinho_parou and velocidade == 0:
            motivo_impulsao = "carrinho_parou"
            break

        deslocamento = calcular_deslocamento(nova_velocidade, dt)
        posicao += deslocamento

        corda_passo = calcular_corda_desenrolada_passo(
            deslocamento, geometria["raio_eixo_m"], geometria["raio_roda_m"])
        # Nunca consumir mais corda do que a fisicamente disponível.
        corda_passo = min(corda_passo, max(0.0, comprimento_corda_m - corda_usada_m))
        variacao_angulo = calcular_angulo_mola_variacao(
            corda_passo, comprimento_haste_m)
        angulo_rad = atualizar_angulo_mola(angulo_rad, variacao_angulo)
        angulo_graus = math.degrees(angulo_rad)

        mola_passo = calcular_mola(
            constante_torsional_mola, angulo_inicial_da_mola_em_graus,
            angulo_graus, comprimento_haste_cm,
            geometria["raio_eixo_m"], geometria["raio_roda_m"])
        forca_util_passo = min(mola_passo["forca_tracao_atual"], aderencia_maxima)
        aceleracao = (forca_util_passo - resistencia_rolamento) / massa_kg
        velocidade = nova_velocidade
        corda_usada_m += corda_passo
        tempo += dt

        historico_tempo.append(tempo)
        historico_velocidade.append(velocidade)
        historico_aceleracao.append(aceleracao)
        historico_angulo.append(angulo_rad)
        historico_posicao.append(posicao)

        if carrinho_parou:
            motivo_impulsao = "carrinho_parou"
            break

    if not motivo_impulsao:
        if angulo_rad <= 0:
            motivo_impulsao = "mola_finalizada"
        elif corda_usada_m >= comprimento_corda_m:
            motivo_impulsao = "corda_finalizada"
        else:
            motivo_impulsao = "tempo_maximo_atingido"

    posicao_fim_impulsao = posicao
    tempo_fim_impulsao = tempo
    velocidade_fim_impulsao = velocidade

    # FASE 2 — o carrinho continua por inércia até parar ou chegar a 60 s.
    while velocidade > 0 and tempo < tempo_maximo_simulacao:
        dt = min(passo_tempo, tempo_maximo_simulacao - tempo)
        nova_velocidade = atualizar_velocidade(velocidade, aceleracao_livre, dt)
        posicao += calcular_deslocamento(nova_velocidade, dt)
        velocidade = nova_velocidade
        tempo += dt
        historico_tempo.append(tempo)
        historico_velocidade.append(velocidade)
        historico_aceleracao.append(aceleracao_livre)
        historico_angulo.append(angulo_rad)
        historico_posicao.append(posicao)

    motivo_final = "carrinho_parou" if velocidade == 0 else "tempo_maximo_atingido"

    # V8 — meta simulada e o primeiro instante de sua passagem.
    meta_atingida = posicao >= distancia_meta_m
    if meta_atingida:
        resultado_meta = "meta_atingida"
    elif motivo_final == "tempo_maximo_atingido":
        resultado_meta = "resultado_inconclusivo"
    else:
        resultado_meta = "meta_nao_atingida"

    tempo_meta_atingida = next(
        (t for t, s in zip(historico_tempo, historico_posicao)
         if s >= distancia_meta_m), None)

    # V9 — diagnósticos de design, conforme a lógica da versão original.
    alcance_geometrico_suficiente = geometria["distancia_teorica_m"] >= distancia_meta_m
    forca_inicial_suficiente = forca_tracao_util_inicial > resistencia_rolamento
    aderencia_limitando = mola["forca_tracao_inicial"] > aderencia_maxima
    mola_finalizada = angulo_rad <= 0 or math.isclose(angulo_rad, 0, abs_tol=1e-9)
    corda_finalizada = corda_usada_m >= comprimento_corda_m

    diagnosticos = []
    if not alcance_geometrico_suficiente:
        diagnosticos.append("O alcance geométrico ideal é menor que a meta.")
    if not forca_inicial_suficiente:
        diagnosticos.append("A força de tração inicial não supera a resistência ao rolamento.")
    if aderencia_limitando:
        diagnosticos.append("A tração solicitada supera o limite de aderência adotado.")
    if corda_finalizada and not mola_finalizada:
        diagnosticos.append("A corda terminou antes de a mola relaxar completamente.")
    elif mola_finalizada and not corda_finalizada:
        diagnosticos.append("A mola relaxou antes de a corda terminar.")
    if motivo_final == "tempo_maximo_atingido":
        diagnosticos.append("O limite de 60 segundos interrompeu a simulação.")

    recomendacoes = []
    if resultado_meta == "meta_nao_atingida":
        if not alcance_geometrico_suficiente:
            recomendacoes.append("Ajuste a relação roda/eixo ou o comprimento da corda.")
        if not forca_inicial_suficiente:
            if aderencia_limitando:
                recomendacoes.append("Melhore a aderência ou reduza a resistência ao rolamento.")
            else:
                recomendacoes.append("Revise a força da mola ou reduza a massa/resistências.")
        if corda_finalizada and not mola_finalizada:
            recomendacoes.append("Reavalie o comprimento da corda.")
        if mola_finalizada and not corda_finalizada:
            recomendacoes.append("Revise a relação entre a mola, a corda e o eixo.")
        if not recomendacoes:
            recomendacoes.append("Revise os parâmetros gerais do design.")

    ajustes = None
    if not alcance_geometrico_suficiente:
        ajustes = calcular_ajustes_para_meta(
            diametro_roda_cm, diametro_eixo_cm, comprimento_corda_cm,
            distancia_meta_m)

    # O dicionário devolve todos os resultados para a interface e os gráficos.
    return {
        "geometria": geometria,
        "mola": mola,
        "aceleracao": aceleracao_ideal,
        "resistencia": resistencia,
        "aderencia": {
            "coeficiente": coeficiente_atrito_estatico,
            "forca_maxima": aderencia_maxima,
            "forca_tracao_util_inicial": forca_tracao_util_inicial,
            "forca_tracao_util_atual": forca_tracao_util_atual,
            "forca_resultante_inicial": forca_resultante_aderencia_inicial,
            "forca_resultante_atual": forca_resultante_aderencia_atual,
            "aceleracao_inicial": aceleracao_aderencia_inicial,
            "aceleracao_atual": aceleracao_aderencia_atual,
        },
        "movimento": {
            "tempo_fim_impulsao": tempo_fim_impulsao,
            "velocidade_fim_impulsao": velocidade_fim_impulsao,
            "posicao_fim_impulsao_m": posicao_fim_impulsao,
            "motivo_fim_impulsao": motivo_impulsao,
            "tempo_total_s": tempo,
            "velocidade_final_m_s": velocidade,
            "velocidade_maxima_m_s": max(historico_velocidade),
            "distancia_total_m": posicao,
            "distancia_fase_impulsionada_m": posicao_fim_impulsao,
            "distancia_fase_livre_m": posicao - posicao_fim_impulsao,
            "angulo_final_graus": math.degrees(angulo_rad),
            "corda_desenrolada_m": corda_usada_m,
            "motivo_encerramento": motivo_final,
        },
        "meta": {
            "distancia_meta_m": distancia_meta_m,
            "resultado": resultado_meta,
            "atingida": meta_atingida,
            "tempo_meta_atingida_s": tempo_meta_atingida,
            "porcentagem": 100 * posicao / distancia_meta_m,
            "diferenca_m": posicao - distancia_meta_m,
        },
        "diagnosticos": diagnosticos,
        "recomendacoes": recomendacoes,
        "ajustes_geometricos": ajustes,
        "historicos": {
            "tempo": historico_tempo,
            "velocidade": historico_velocidade,
            "aceleracao": historico_aceleracao,
            "angulo_rad": historico_angulo,
            "posicao": historico_posicao,
        },
        "parametros": {
            "diametro_roda_cm": diametro_roda_cm,
            "diametro_eixo_cm": diametro_eixo_cm,
            "comprimento_corda_cm": comprimento_corda_cm,
            "comprimento_haste_cm": comprimento_haste_cm,
            "massa_total_carrinho_g": massa_total_carrinho_g,
            "constante_torsional_mola": constante_torsional_mola,
            "angulo_inicial_da_mola_em_graus": angulo_inicial_da_mola_em_graus,
            "angulo_atual_da_mola_em_graus": angulo_atual_da_mola_em_graus,
            "coeficiente_atrito_estatico": coeficiente_atrito_estatico,
            "coeficiente_resistencia_rolamento": coeficiente_resistencia_rolamento,
            "passo_tempo": passo_tempo,
            "tempo_maximo_simulacao": tempo_maximo_simulacao,
        },
        "limitacoes": (
            "Modelo educacional simplificado: não inclui arrasto aerodinâmico, "
            "inércia de rotação, patinagem detalhada, distribuição do peso "
            "ou perdas mecânicas adicionais. O valor de μ=0,6 é uma hipótese "
            "de simulação, não uma medição dos materiais reais."
        ),
    }
