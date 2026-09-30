# RatoeiraLab — Modelo V7

## V7 — Velocidade, posição e distância percorrida

A V7 amplia a simulação temporal criada na V6.

Até a V6, o RatoeiraLab simulava principalmente a fase em que o carrinho ainda estava sendo impulsionado pela ratoeira.

A V7 passa a acompanhar o movimento completo do carrinho, incluindo:

- posição ao longo do tempo;
- distância total percorrida;
- velocidade ao longo do movimento;
- tempo total de movimento;
- distância percorrida durante a fase impulsionada;
- distância percorrida após o fim da impulsão;
- movimento por inércia até a parada.

A V7 ainda não faz a análise formal de cumprimento da meta de 10 metros. Essa verificação pertence à V8.

---

## 1. Ideia principal da V7

A V7 divide o movimento em duas fases.

```text
FASE 1 — movimento impulsionado pela ratoeira

mola/corda fornecendo tração
↓
velocidade sendo atualizada
↓
posição aumentando
↓
mola ou corda termina

FASE 2 — movimento livre

força de tração = 0
↓
resistência ao rolamento continua atuando
↓
carrinho desacelera
↓
posição continua aumentando
↓
velocidade chega a zero
```

Essa separação é importante porque o fim da ação da mola não significa que o carrinho para instantaneamente.

Se ainda existir velocidade, o carrinho continua avançando por inércia.

---

## 2. Posição inicial

A V7 adiciona uma nova variável de estado:

```python
posicao_atual_m = 0.0
```

Ela representa a posição do carrinho em metros.

A simulação começa em:

```text
x = 0 m
```

---

## 3. Diferença entre deslocamento e posição

Na V6 já existia o deslocamento calculado em cada passo:

```text
Δx = v × Δt
```

Esse valor representa apenas quanto o carrinho andou durante um único intervalo de tempo.

A posição representa a soma acumulada de todos esses deslocamentos.

A relação utilizada na V7 é:

```text
x_novo = x_atual + Δx
```

onde:

- `x_novo` = nova posição do carrinho, em m;
- `x_atual` = posição anterior, em m;
- `Δx` = deslocamento calculado naquele passo, em m.

No código:

```python
posicao_atual_m += deslocamento_passo_m
```

---

## 4. Atualização da posição durante a fase impulsionada

Durante a fase em que a ratoeira ainda fornece tração, a V7 mantém o fluxo físico criado na V6:

```text
aceleração
↓
velocidade
↓
deslocamento
↓
posição
↓
corda desenrolada
↓
ângulo da mola
↓
força
↓
nova aceleração
```

Depois de calcular o deslocamento do passo:

```python
deslocamento_passo_m = calcular_deslocamento(
    nova_velocidade,
    passo_tempo
)
```

a posição é atualizada:

```python
posicao_atual_m += deslocamento_passo_m
```

---

## 5. Histórico da posição

A V7 adiciona:

```python
historico_posicao
```

A lista começa com a posição inicial:

```python
historico_posicao = [posicao_atual_m]
```

Depois, a cada passo de tempo:

```python
historico_posicao.append(posicao_atual_m)
```

Com isso, o RatoeiraLab passa a guardar a posição do carrinho ao longo do tempo.

Esse histórico será especialmente útil na V10, quando serão criados gráficos.

---

## 6. Históricos sincronizados

Ao final da V7, o simulador mantém:

```python
historico_tempo
historico_velocidade
historico_aceleracao
historico_angulo
historico_posicao
```

Cada passo registrado adiciona um valor a todas essas listas.

Assim, um mesmo índice representa o mesmo instante da simulação.

Exemplo:

```text
historico_tempo[100]
historico_velocidade[100]
historico_aceleracao[100]
historico_angulo[100]
historico_posicao[100]
```

representam o estado do carrinho no mesmo passo temporal.

---

## 7. Fim da fase impulsionada

A fase impulsionada continua utilizando as condições de encerramento definidas na V6.

Ela pode terminar por:

```text
carrinho_parou
mola_finalizada
corda_finalizada
tempo_maximo_atingido
```

Porém, na V7, terminar a fase impulsionada não significa necessariamente terminar toda a simulação.

Se:

```text
velocidade_atual > 0
```

o carrinho ainda possui movimento.

Por isso, a V7 adiciona uma segunda fase.

---

## 8. Registro do estado no fim da impulsão

Antes de iniciar a fase livre, a V7 guarda o estado final da fase impulsionada:

```python
posicao_fim_impulsionada_m = posicao_atual_m
tempo_fim_impulsao = tempo_atual
velocidade_fim_impulsao = velocidade_atual
```

Essas variáveis preservam os resultados da V6.

Isso é necessário porque `tempo_atual`, `velocidade_atual` e `posicao_atual_m` continuam sendo atualizados durante a fase livre.

---

## 9. Força resultante na fase livre

Quando a mola ou a corda deixam de fornecer tração:

```text
Ftração = 0
```

A resistência ao rolamento continua atuando contra o movimento.

Portanto:

```text
Fresultante = -Frr
```

onde:

- `Fresultante` = força resultante durante a fase livre, em N;
- `Frr` = resistência ao rolamento, em N;
- o sinal negativo indica que a força atua contra o sentido do movimento.

---

## 10. Aceleração da fase livre

Pela Segunda Lei de Newton:

```text
a = F / m
```

Durante a fase livre:

```text
a = -Frr / m
```

No código:

```python
aceleracao_fase_livre = (
    -forca_resistencia_rolamento
    / resultado_aceleracao["massa_total_carrinho_kg"]
)
```

Como o modelo atual considera a resistência ao rolamento constante, essa desaceleração também permanece constante durante a fase livre.

---

## 11. Relação simplificada da desaceleração

Como:

```text
Frr = Crr × N
```

e, no plano horizontal:

```text
N = m × g
```

então:

```text
Frr = Crr × m × g
```

Substituindo na aceleração:

```text
a = -(Crr × m × g) / m
```

a massa cancela:

```text
a = -Crr × g
```

Com os valores padrão atuais:

```text
Crr = 0,02
g = 9,81 m/s²
```

temos aproximadamente:

```text
a = -0,1962 m/s²
```

Essa relação é consequência das simplificações adotadas no modelo atual.

---

## 12. Loop da fase livre

A segunda fase utiliza:

```python
while (
    velocidade_atual > 0
    and tempo_atual < tempo_maximo_simulacao
):
```

Isso significa que a fase livre continua enquanto:

- o carrinho ainda estiver se movendo;
- o limite máximo de tempo não tiver sido atingido.

A cada passo:

```text
velocidade diminui
↓
deslocamento é calculado
↓
posição aumenta
↓
tempo aumenta
↓
históricos são atualizados
```

---

## 13. Atualização da velocidade na fase livre

A V7 reutiliza a função criada na V6:

```python
nova_velocidade = atualizar_velocidade(
    velocidade_atual,
    aceleracao_fase_livre,
    passo_tempo
)
```

Como `aceleracao_fase_livre` é negativa, a velocidade diminui gradualmente.

A função `atualizar_velocidade()` já utiliza:

```python
max(0, ...)
```

Portanto, a velocidade nunca fica negativa.

Quando chega a zero, o carrinho é considerado parado.

---

## 14. Atualização da posição na fase livre

Mesmo sem tração da mola, o carrinho continua se deslocando enquanto sua velocidade for positiva.

O deslocamento continua sendo calculado por:

```text
Δx = v × Δt
```

Depois:

```python
posicao_atual_m += deslocamento_passo_m
```

Assim, a posição continua aumentando até a parada.

---

## 15. O que não é mais atualizado na fase livre

Depois que a impulsão termina, a V7 não continua atualizando:

- corda desenrolada;
- ângulo da mola;
- torque da mola;
- força de tração produzida pela mola.

Isso ocorre porque essa fase representa o movimento do carrinho depois que o mecanismo de impulsão já terminou sua atuação.

---

## 16. Históricos durante a fase livre

A fase livre continua registrando:

```python
historico_tempo.append(tempo_atual)
historico_velocidade.append(velocidade_atual)
historico_aceleracao.append(aceleracao_fase_livre)
historico_angulo.append(angulo_atual_rad)
historico_posicao.append(posicao_atual_m)
```

O ângulo da mola permanece armazenado com seu valor final, já que ele não é mais atualizado nessa fase.

---

## 17. Distância durante a fase impulsionada

Como o carrinho começa em:

```text
x = 0
```

a posição no fim da fase impulsionada também representa a distância percorrida durante essa fase.

No código:

```python
distancia_fase_impulsionada_m = (
    posicao_fim_impulsionada_m
)
```

---

## 18. Distância durante a fase livre

A distância percorrida depois do fim da impulsão é calculada por:

```text
distância livre =
posição final - posição no fim da impulsão
```

No código:

```python
distancia_fase_livre_m = (
    posicao_atual_m
    - posicao_fim_impulsionada_m
)
```

---

## 19. Distância total percorrida

Como:

- a posição inicial é `0 m`;
- o carrinho não anda para trás no modelo atual;

a posição final é numericamente igual à distância total percorrida.

Portanto:

```text
distância total = posição final
```

No código, ambas são apresentadas utilizando:

```python
posicao_atual_m
```

Mesmo possuindo o mesmo valor, os dois conceitos são mantidos separados porque representam grandezas conceitualmente diferentes.

---

## 20. Motivo de encerramento da V7

A V7 registra separadamente o motivo de encerramento da simulação completa.

Se a velocidade chegar a zero:

```python
motivo_encerramento_v7 = "carrinho_parou"
```

Se o limite máximo de tempo for atingido:

```python
motivo_encerramento_v7 = "tempo_maximo_atingido"
```

Isso diferencia:

```text
motivo_encerramento
```

que representa o encerramento da fase impulsionada,

de:

```text
motivo_encerramento_v7
```

que representa o encerramento da simulação completa.

---

## 21. Proteção contra simulação excessivamente longa

O limite continua sendo:

```python
tempo_maximo_simulacao = 60.0
```

A fase livre também respeita esse limite.

Isso evita loops excessivamente longos em casos extremos, por exemplo quando a resistência ao rolamento for muito pequena ou igual a zero.

Esse limite é uma proteção computacional e não uma propriedade física do carrinho.

---

## 22. Resultados exibidos pela V7

Ao final, a V7 apresenta:

```text
Tempo total de movimento
Velocidade final
Posição final
Distância total percorrida
Distância durante a fase impulsionada
Distância durante a fase livre
Motivo do encerramento da simulação
```

Exemplo:

```text
---------------- RESULTADOS DA V7 ----------------

Tempo total de movimento: ...
Velocidade final: ...
Posição final: ...
Distância total percorrida: ...
Distância durante a fase impulsionada: ...
Distância durante a fase livre: ...
Motivo do encerramento da simulação: ...
```

---

## 23. Relação entre V6 e V7

A V6 continua representando principalmente:

```text
fase impulsionada
```

Por isso a V7 salva:

```python
tempo_fim_impulsao
velocidade_fim_impulsao
posicao_fim_impulsionada_m
```

antes de começar a fase livre.

Assim, os resultados da V6 continuam mostrando corretamente o instante em que a impulsão terminou, enquanto a V7 mostra o movimento completo até a parada.

---

## 24. Testes realizados

A lógica da V7 foi verificada com diferentes situações.

Foram considerados:

- carrinho em funcionamento normal;
- carrinho que não consegue sair do lugar;
- movimento impulsionado seguido de movimento livre;
- mola muito fraca;
- mola forte;
- corda curta;
- aderência baixa;
- aderência extremamente baixa;
- mola terminando antes da corda;
- corda terminando antes da mola;
- velocidade chegando a zero;
- caso extremo atingindo o limite máximo de tempo.

Também foram verificadas condições internas:

- velocidade nunca fica negativa;
- posição nunca fica negativa;
- posição não diminui;
- distância não fica negativa;
- distância impulsionada + distância livre é consistente com a distância total;
- listas de histórico permanecem com o mesmo tamanho;
- existe continuidade entre o final da fase impulsionada e o início da fase livre;
- o limite de tempo impede loops excessivamente longos.

---

## 25. Aproximação numérica

A V7 continua utilizando o passo temporal definido na V6:

```text
Δt = 0,005 s
```

Por isso, os eventos físicos são detectados dentro dessa resolução temporal.

Por exemplo, uma corda pode terminar entre dois passos da simulação.

O programa limita a quantidade de corda desenrolada, mas o deslocamento daquele passo já foi calculado.

Isso pode produzir pequenas diferenças de alguns milímetros em determinados casos.

Essa diferença é uma consequência esperada da aproximação numérica atual.

---

## 26. Limitações da fase livre

A fase livre considera principalmente a resistência ao rolamento.

O modelo ainda não inclui:

- resistência do ar;
- inércia rotacional das rodas;
- perdas detalhadas nos mancais;
- perdas detalhadas na transmissão;
- deformação das rodas;
- irregularidades da pista;
- distribuição dinâmica de peso;
- transferência de peso;
- velocidade de escorregamento;
- atrito cinético detalhado.

Por isso, em casos extremos, especialmente com velocidades elevadas, a distância prevista durante a fase livre pode ser maior do que ocorreria em um carrinho real.

---

## 27. Limitações gerais da V7

A V7 continua sendo uma aproximação física.

O simulador não deve ser tratado como uma previsão exata do comportamento de um carrinho real.

Além das simplificações já existentes nas versões anteriores, continuam válidas aproximações como:

```text
Ntracao ≈ Ntotal
```

e a relação simplificada entre:

```text
corda desenrolada
↓
variação do ângulo da mola
```

A V7 também não adiciona novas correções avançadas de dinâmica.

---

## 28. Resultado acumulado até a V7

O fluxo físico do RatoeiraLab agora é:

```text
V1 — Geometria
↓
Qual é o alcance geométrico teórico?

V2 — Mola
↓
Quanta força a ratoeira tenta transmitir?

V3 — Massa
↓
Qual seria a aceleração ideal?

V4 — Resistência ao rolamento
↓
Quanto da força é reduzido pelas resistências?

V5 — Aderência
↓
Quanto da força pode realmente ser transmitido ao chão?

V6 — Movimento ao longo do tempo
↓
Como o carrinho se comporta durante a fase impulsionada?

V7 — Velocidade, posição e distância percorrida
↓
Como o carrinho se move até parar completamente?
```

A cadeia principal da V7 pode ser representada por:

```text
FASE 1

força da mola
↓
aceleração
↓
velocidade
↓
deslocamento
↓
posição
↓
atualização da mola
↓
repetição

=============================

fim da impulsão
↓
velocidade ainda > 0?

SIM
↓
FASE 2

Ftração = 0
↓
Fresultante = -Frr
↓
a = -Frr / m
↓
velocidade diminui
↓
deslocamento
↓
posição aumenta
↓
repetição até v = 0
```

---

## 29. O que a V7 ainda não faz

A V7 calcula a distância real simulada do movimento, mas ainda não transforma esse valor em uma avaliação formal da meta do projeto.

Ela não deve responder definitivamente:

```text
"O carrinho atingiu os 10 metros?"
```

Essa responsabilidade pertence à próxima versão.

Também não entram ainda:

- gráficos;
- interface gráfica;
- recomendações automáticas de projeto;
- otimização automática;
- resistência do ar;
- inércia rotacional;
- dinâmica avançada de derrapagem;
- modelo detalhado do centro de massa.

---

## 30. Próxima versão

A próxima etapa do RatoeiraLab será:

```text
V8 — Verificação da meta de 10 metros
```

A V7 agora fornece a informação necessária para isso:

```python
posicao_atual_m
```

que representa a distância final simulada no modelo atual.

Na V8 será possível comparar a distância simulada com a meta definida pelo usuário e interpretar o resultado.

---

## V7 — Velocidade, posição e distância percorrida ✅ CONCLUÍDA

A V7 completa a simulação do movimento do carrinho dentro do modelo físico atual.

Agora o RatoeiraLab consegue acompanhar:

- velocidade ao longo do tempo;
- posição ao longo do tempo;
- distância durante a impulsão;
- movimento por inércia;
- desaceleração após o fim da impulsão;
- distância percorrida na fase livre;
- distância total;
- tempo total de movimento;
- motivo de encerramento da simulação.

Com isso, o simulador deixa de analisar apenas a atuação da ratoeira e passa a representar o movimento do carrinho até sua parada ou até o limite de segurança da simulação.
