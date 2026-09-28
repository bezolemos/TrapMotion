# RatoeiraLab — Modelo V6

## V6 — Movimento ao longo do tempo

A V6 transforma os cálculos das versões anteriores em uma simulação temporal.

Até a V5, o RatoeiraLab calculava principalmente estados físicos específicos:

- força produzida pela mola;
- força de tração;
- resistência ao rolamento;
- limite de aderência;
- força resultante;
- aceleração.

A V6 passa a atualizar essas grandezas ao longo do tempo, em pequenos intervalos.

Isso permite observar como a mola perde força enquanto o carrinho se movimenta.

A V6 simula apenas a **fase impulsionada pela mola**.

---

## 1. Ideia principal da V6

A simulação é dividida em pequenos passos de tempo.

No código:

```python
passo_tempo = 0.005
```

Portanto:

```text
Δt = 0,005 s
```

A cada passo, o programa atualiza o estado do carrinho.

O fluxo principal é:

```text
aceleração
↓
velocidade
↓
deslocamento
↓
corda desenrolada
↓
variação do ângulo da mola
↓
novo ângulo da mola
↓
nova força de tração
↓
nova força resultante
↓
nova aceleração
```

Depois o processo se repete.

---

## 2. Estado inicial da simulação

A V6 começa com:

```python
tempo_atual = 0.0
velocidade_atual = 0.0
corda_desenrolada_total_m = 0.0
```

O ângulo da mola começa no ângulo inicial definido pelo usuário:

```python
angulo_atual_rad = math.radians(
    angulo_inicial_da_mola_em_graus
)
```

A aceleração inicial utilizada pela simulação vem da V5:

```python
aceleracao_atual_simulacao = aceleracao_aderencia_inicial
```

Assim, o instante:

```text
t = 0
```

da V6 é consistente com o resultado inicial da V5.

---

## 3. Atualização da velocidade

A velocidade é atualizada por:

```text
v_nova = v_atual + a × Δt
```

onde:

- `v_nova` = nova velocidade, em m/s;
- `v_atual` = velocidade antes do passo, em m/s;
- `a` = aceleração atual, em m/s²;
- `Δt` = passo de tempo, em s.

No código:

```python
nova_velocidade = max(
    0,
    velocidade_atual
    + aceleracao_atual * passo_tempo
)
```

O `max(0, ...)` impede velocidades negativas.

Neste modelo, quando a velocidade chega a zero durante uma desaceleração, o carrinho é considerado parado.

---

## 4. Deslocamento durante um passo

Depois de atualizar a velocidade, a V6 calcula o deslocamento daquele pequeno intervalo:

```text
Δx = v × Δt
```

onde:

- `Δx` = deslocamento no passo, em m;
- `v` = velocidade utilizada no passo, em m/s;
- `Δt` = intervalo de tempo, em s.

No código, a velocidade recém-atualizada é usada:

```python
deslocamento_passo_m = (
    nova_velocidade * passo_tempo
)
```

Essa forma de integração é uma aproximação numérica simples, adequada ao nível atual do RatoeiraLab.

---

## 5. Relação entre deslocamento e corda desenrolada

O deslocamento do carrinho faz a roda girar.

Como o eixo gira junto com a roda, a corda também é desenrolada.

A relação usada é:

```text
ΔL = Δx × (r_eixo / r_roda)
```

onde:

- `ΔL` = quantidade de corda desenrolada no passo, em m;
- `Δx` = deslocamento do carrinho no passo, em m;
- `r_eixo` = raio do eixo, em m;
- `r_roda` = raio da roda, em m.

No código:

```python
corda_desenrolada_passo_m = (
    deslocamento_passo_m
    * (raio_eixo_m / raio_roda_m)
)
```

Essa relação conecta o movimento linear do carrinho à rotação do sistema roda/eixo.

---

## 6. Limite da corda disponível

A simulação não pode desenrolar mais corda do que realmente existe.

Por isso é calculada:

```python
corda_restante_m = (
    comprimento_corda_m
    - corda_desenrolada_total_m
)
```

Depois:

```python
corda_desenrolada_passo_m = min(
    corda_desenrolada_passo_m,
    corda_restante_m
)
```

Assim, se restarem apenas `0,002 m` de corda, o programa não poderá desenrolar `0,003 m`.

---

## 7. Relação entre corda e ângulo da mola

Na simplificação física usada desde a V2, a corda exerce força perpendicular à haste.

A variação angular da mola é relacionada ao comprimento de corda liberado por:

```text
Δθ = ΔL / L
```

onde:

- `Δθ` = variação do ângulo da mola, em rad;
- `ΔL` = corda desenrolada no passo, em m;
- `L` = comprimento da haste, em m.

No código:

```python
angulo_mola_variacao_rad = (
    corda_desenrolada_passo_m
    / comprimento_haste_m
)
```

---

## 8. Atualização do ângulo da mola

O novo ângulo é:

```text
θ_novo = θ_atual - Δθ
```

No código:

```python
novo_angulo_rad = max(
    0,
    angulo_atual_rad
    - variacao_angulo_rad
)
```

Novamente, `max()` impede que o ângulo fique negativo.

Quando o ângulo chega a zero, a mola terminou sua ação dentro do modelo.

---

## 9. Recalcular a mola durante a simulação

Depois de obter o novo ângulo, a V6 reaproveita os cálculos da V2.

O novo ângulo produz:

```text
novo ângulo
↓
novo torque da mola
↓
nova tensão na corda
↓
novo torque no eixo
↓
nova força de tração
```

Assim, a força da mola não permanece constante durante a simulação.

Conforme o ângulo diminui, a força de tração também tende a diminuir.

---

## 10. Limite de aderência em cada passo

A V6 mantém a regra criada na V5:

```text
Ftracao_util = min(
    Ftracao,
    Faderencia_max
)
```

No código:

```python
forca_tracao_util_passo = min(
    resultado_mola_passo["forca_tracao_atual"],
    forca_aderencia_maxima
)
```

Portanto, mesmo durante a simulação temporal, a força transmitida ao chão não ultrapassa o limite de aderência adotado pelo modelo.

---

## 11. Nova força resultante

Depois de aplicar o limite de aderência:

```text
Fresultante =
Ftracao_util - Frr
```

onde:

- `Fresultante` = força resultante no passo, em N;
- `Ftracao_util` = força de tração utilizável, em N;
- `Frr` = resistência ao rolamento, em N.

No código:

```python
forca_resultante_passo = (
    forca_tracao_util_passo
    - forca_resistencia_rolamento
)
```

---

## 12. Nova aceleração

A aceleração de cada passo é recalculada pela Segunda Lei de Newton:

```text
a = F / m
```

No código:

```python
aceleracao_passo = (
    forca_resultante_passo
    / massa_total_carrinho_kg
)
```

Essa nova aceleração será utilizada no próximo passo da simulação.

Portanto:

```text
a(t)
↓
v(t + Δt)
↓
x(t + Δt)
↓
θ(t + Δt)
↓
F(t + Δt)
↓
a(t + Δt)
```

---

## 13. Loop temporal

A simulação utiliza um `while`.

Ela continua enquanto:

```text
ângulo da mola > 0
E
ainda existir corda disponível
E
tempo < tempo máximo
```

No código:

```python
while (
    angulo_atual_rad > 0
    and corda_desenrolada_total_m < comprimento_corda_m
    and tempo_atual < tempo_maximo_simulacao
):
```

A cada repetição:

```python
tempo_atual += passo_tempo
```

Assim, o tempo avança gradualmente.

---

## 14. Condições de encerramento

A V6 pode terminar por quatro motivos.

### Carrinho parado

```text
carrinho_parou
```

Acontece quando a velocidade chega a zero e a aceleração não consegue manter o movimento.

Se o carrinho não consegue nem iniciar o movimento, a simulação termina em:

```text
t = 0 s
```

### Mola finalizada

```text
mola_finalizada
```

Acontece quando:

```text
θ <= 0
```

### Corda finalizada

```text
corda_finalizada
```

Acontece quando toda a corda disponível foi desenrolada.

### Tempo máximo atingido

```text
tempo_maximo_atingido
```

A V6 utiliza:

```python
tempo_maximo_simulacao = 60.0
```

Esse limite não representa uma propriedade física do carrinho.

Ele funciona como uma proteção para evitar uma simulação excessivamente longa ou um possível loop sem encerramento.

---

## 15. Histórico da simulação

A V6 começa a armazenar a evolução das grandezas físicas.

São utilizadas as listas:

```python
historico_tempo
historico_velocidade
historico_aceleracao
historico_angulo
```

Elas registram os valores desde:

```text
t = 0
```

até o encerramento da fase impulsionada.

Esses dados serão especialmente importantes nas próximas versões para análise do movimento e geração de gráficos.

---

## 16. Resultados mostrados pela V6

Ao terminar a simulação, a V6 apresenta:

- tempo da fase impulsionada;
- velocidade ao final da fase;
- ângulo final da mola;
- quantidade total de corda desenrolada;
- motivo do encerramento da simulação.

Exemplo de saída:

```text
---------------- RESULTADOS DA V6 ----------------

Tempo da fase impulsionada: ...
Velocidade ao final da fase: ...
Ângulo final da mola: ...
Corda desenrolada: ...
Motivo do encerramento: ...
```

---

## 17. Testes realizados

A lógica da V6 foi verificada com diferentes situações.

Foram considerados casos como:

- funcionamento normal;
- mola forte;
- mola muito fraca;
- aderência muito baixa ou igual a zero;
- corda curta;
- resistência superior à tração;
- carrinho que não consegue iniciar o movimento;
- carrinho que começa andando e depois para;
- finalização completa da mola;
- finalização da corda;
- limite máximo de tempo.

Também foram verificadas condições internas:

- velocidade não fica negativa;
- ângulo da mola não fica negativo;
- a corda não ultrapassa o comprimento disponível;
- as listas de histórico permanecem com tamanhos consistentes;
- existe proteção contra uma simulação excessivamente longa;
- o estado inicial da V6 é consistente com a aceleração inicial calculada na V5.

---

## 18. Aproximação numérica

A V6 não calcula o movimento de forma contínua.

Ela divide o tempo em intervalos:

```text
Δt = 0,005 s
```

Por isso existe uma pequena aproximação numérica.

Por exemplo, uma condição física pode ser atingida entre dois passos de tempo.

O programa registra o encerramento dentro da resolução temporal adotada.

Para o objetivo atual do RatoeiraLab, essa aproximação é considerada adequada.

---

## 19. Limitações da V6

A V6 ainda utiliza um modelo físico simplificado.

Ela não simula detalhadamente:

- patinagem;
- atrito cinético;
- velocidade de escorregamento;
- distribuição real de peso entre os eixos;
- transferência dinâmica de peso;
- resistência do ar;
- inércia rotacional das rodas;
- perdas detalhadas nos mancais;
- flexibilidade da estrutura;
- perdas detalhadas na transmissão;
- irregularidades da pista.

Além disso, a aproximação da V5:

```text
Ntracao ≈ Ntotal
```

continua sendo utilizada.

Isso pode superestimar o limite de aderência quando apenas parte do peso do carrinho está apoiada sobre o eixo tracionado.

A relação entre movimento da corda e movimento angular da mola também continua baseada na simplificação geométrica definida na V2.

---

## 20. Resultado acumulado até a V6

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
Como essas grandezas mudam enquanto o carrinho
é impulsionado pela mola?
```

A cadeia principal da V6 é:

```text
a
↓
v_nova = v + aΔt
↓
Δx = v_nova Δt
↓
ΔL = Δx × (r_eixo / r_roda)
↓
Δθ = ΔL / L
↓
θ_novo = θ - Δθ
↓
novo torque da mola
↓
nova força de tração
↓
limite de aderência
↓
força resultante
↓
nova aceleração
↓
próximo passo de tempo
```

---

## 21. Próxima versão

A próxima etapa do RatoeiraLab será:

```text
V7 — Velocidade, posição e distância percorrida
```

A V6 construiu a base temporal necessária.

A V7 poderá utilizar essa base para analisar de forma mais completa:

- velocidade ao longo do movimento;
- posição do carrinho;
- distância percorrida;
- comportamento após o fim da fase impulsionada;
- evolução completa do movimento até a parada.

---

## V6 — Movimento ao longo do tempo ✅ CONCLUÍDA

A V6 transforma o RatoeiraLab de um conjunto de cálculos em estados específicos em uma simulação que evolui no tempo.

Agora o simulador atualiza continuamente, dentro de pequenos passos discretos:

- velocidade;
- deslocamento;
- quantidade de corda desenrolada;
- ângulo da mola;
- força de tração;
- força resultante;
- aceleração.

Essa estrutura será a base das próximas versões do projeto.
