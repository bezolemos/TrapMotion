# RatoeiraLab — Modelo V5

## V5 — Aderência das rodas e limite de tração

A V5 adiciona ao simulador o limite de aderência entre as rodas e o chão.

Nas versões anteriores, o programa calculava a força que a mola tenta transmitir às rodas e descontava a resistência ao rolamento.

Porém, ainda existia uma simplificação importante:

o modelo assumia que qualquer força produzida pela mola poderia ser transmitida integralmente ao chão.

Na prática, existe um limite de aderência.

Se a força solicitada pelas rodas ultrapassar esse limite, pode ocorrer patinagem ou derrapagem.

A V5 passa a calcular:

- força máxima de aderência;
- comparação entre força de tração e limite de aderência;
- força de tração realmente utilizável pelo modelo;
- força resultante considerando aderência;
- aceleração considerando aderência.

---

## 1. Entrada adicionada na V5

A V5 adiciona:

- coeficiente de atrito estático.

No código:

```python
coeficiente_atrito_estatico
```

Símbolo:

```text
μs
```

O coeficiente de atrito estático é adimensional, ou seja, não possui unidade.

Ele representa de forma simplificada a capacidade de aderência entre as rodas e a superfície.

O valor depende das duas superfícies em contato.

Por exemplo:

- borracha sobre madeira;
- plástico sobre madeira;
- borracha sobre piso liso.

Por isso, não existe necessariamente um único coeficiente válido para um material isoladamente.

---

## 2. Atrito estático e aderência

Uma roda tracionada precisa de atrito com o chão para conseguir transmitir força.

Quando o eixo aplica torque à roda, a roda tenta empurrar o chão para trás.

O chão exerce uma força sobre a roda no sentido oposto.

Essa interação permite que o carrinho seja acelerado para frente.

Enquanto o ponto da roda em contato com o chão não estiver deslizando, o contato pode ser aproximado por atrito estático.

Portanto, o atrito estático não deve ser interpretado simplesmente como uma força que freia o carrinho.

Ele é necessário para que exista transmissão de força entre roda e chão.

---

## 3. Diferença entre aderência e resistência ao rolamento

Na V4 foi utilizada a resistência ao rolamento:

```text
Frr = Crr × N
```

onde:

- `Frr` = resistência ao rolamento, em N;
- `Crr` = coeficiente de resistência ao rolamento;
- `N` = força normal, em N.

A resistência ao rolamento representa uma força contrária ao movimento.

Por isso, ela é subtraída da força de tração.

Na V5 é introduzido:

```text
Faderencia_max = μs × N
```

A força máxima de aderência não é uma força que deve ser simplesmente subtraída.

Ela representa um limite para a quantidade de força que pode ser transmitida ao chão sem ultrapassar a aderência do modelo.

Portanto:

```text
resistência ao rolamento = perda de força
```

enquanto:

```text
aderência = limite de transmissão de força
```

---

## 4. Força máxima de aderência

A principal nova fórmula da V5 é:

```text
Faderencia_max = μs × N
```

onde:

- `Faderencia_max` = força máxima de aderência, em N;
- `μs` = coeficiente de atrito estático;
- `N` = força normal, em N.

No código:

```python
forca_aderencia_maxima = (
    coeficiente_atrito_estatico * forca_normal
)
```

A função criada foi:

```python
calcular_aderencia()
```

Ela recebe:

```python
coeficiente_atrito_estatico
forca_normal
```

e retorna:

```python
forca_aderencia_maxima
```

---

## 5. Força normal utilizada

Fisicamente, o limite de aderência das rodas tracionadas deveria utilizar apenas a força normal suportada pelo eixo que recebe torque.

A relação mais completa seria:

```text
Faderencia_max = μs × Ntracao
```

Porém, isso exigiria conhecer a distribuição de peso do carrinho entre os eixos.

A V5 utiliza a aproximação:

```text
Ntracao ≈ Ntotal
```

Portanto:

```text
Faderencia_max = μs × N
```

onde `N` é a força normal total já calculada na V4.

Em superfície horizontal:

```text
N = P
```

e:

```text
P = m × g
```

Essa aproximação tende a ser otimista, pois assume que toda a força normal está disponível para gerar aderência nas rodas tracionadas.

A distribuição real de peso entre os eixos não é modelada na V5.

---

## 6. Comparação entre tração e aderência

A força de tração calculada na V2 representa quanto a mola tenta transmitir às rodas.

A V5 compara essa força com o limite de aderência.

São analisadas:

```python
resultado_mola["forca_tracao_inicial"]
```

e:

```python
resultado_mola["forca_tracao_atual"]
```

em relação a:

```python
forca_aderencia_maxima
```

As interpretações são:

### Tração menor que a aderência máxima

```text
Ftracao < Faderencia_max
```

A força solicitada está dentro do limite de aderência.

O modelo considera que toda a força de tração pode ser transmitida.

### Tração aproximadamente igual à aderência máxima

```text
Ftracao ≈ Faderencia_max
```

A força solicitada está aproximadamente no limite de aderência.

No código, a comparação utiliza:

```python
math.isclose()
```

Isso evita depender de igualdade exata entre números do tipo `float`.

### Tração maior que a aderência máxima

```text
Ftracao > Faderencia_max
```

A força solicitada ultrapassa o limite de aderência do modelo.

Nesse caso, existe possibilidade de patinagem.

A V5 não simula detalhadamente a derrapagem.

Ela apenas limita a força que pode ser considerada utilizável.

---

## 7. Força de tração utilizável

A V5 introduz:

```python
forca_tracao_util_inicial
forca_tracao_util_atual
```

A fórmula utilizada é:

```text
Ftracao_util = min(Ftracao, Faderencia_max)
```

No código:

```python
forca_tracao_util_inicial = min(
    resultado_mola["forca_tracao_inicial"],
    forca_aderencia_maxima
)
```

e:

```python
forca_tracao_util_atual = min(
    resultado_mola["forca_tracao_atual"],
    forca_aderencia_maxima
)
```

A função `min()` retorna o menor dos valores fornecidos.

Isso produz dois casos principais.

### Caso 1 — aderência suficiente

Se:

```text
Ftracao = 0,40 N
Faderencia_max = 0,60 N
```

então:

```text
Ftracao_util = 0,40 N
```

Toda a força solicitada pode ser utilizada.

### Caso 2 — aderência limitada

Se:

```text
Ftracao = 0,80 N
Faderencia_max = 0,60 N
```

então:

```text
Ftracao_util = 0,60 N
```

O modelo limita a força utilizável ao máximo permitido pela aderência.

Isso não significa que o restante da força simplesmente desaparece fisicamente.

Significa apenas que a V5 não permite considerar essa força adicional como tração transmitida ao chão sem ultrapassar o limite de aderência.

---

## 8. Força resultante considerando aderência

Na V4:

```text
Fresultante = Ftracao - Frr
```

Na V5, a força de tração original é substituída pela força de tração utilizável:

```text
Fresultante_V5 = Ftracao_util - Frr
```

Foram criadas:

```python
forca_resultante_aderencia_inicial
forca_resultante_aderencia_atual
```

No código:

```python
forca_resultante_aderencia_inicial = (
    forca_tracao_util_inicial
    - forca_resistencia_rolamento
)
```

e:

```python
forca_resultante_aderencia_atual = (
    forca_tracao_util_atual
    - forca_resistencia_rolamento
)
```

O fluxo passa a ser:

```text
força que a mola tenta transmitir
↓
limite de aderência
↓
força de tração utilizável
↓
resistência ao rolamento
↓
força resultante
```

---

## 9. Aceleração considerando aderência

Depois de calcular a nova força resultante, a V5 reutiliza a Segunda Lei de Newton:

```text
F = m × a
```

Isolando a aceleração:

```text
a = F / m
```

Foram criadas:

```python
aceleracao_aderencia_inicial
aceleracao_aderencia_atual
```

No código:

```python
aceleracao_aderencia_inicial = (
    forca_resultante_aderencia_inicial
    / resultado_aceleracao["massa_total_carrinho_kg"]
)
```

e:

```python
aceleracao_aderencia_atual = (
    forca_resultante_aderencia_atual
    / resultado_aceleracao["massa_total_carrinho_kg"]
)
```

As unidades são:

```text
força resultante = N
massa = kg
aceleração = m/s²
```

---

## 10. Diferença entre V4 e V5

Na V4, o programa assume que toda a força de tração calculada pela mola consegue chegar ao chão.

O fluxo da V4 é:

```text
força de tração
↓
resistência ao rolamento
↓
força resultante
↓
aceleração
```

Na V5, existe uma nova etapa entre a força da mola e a resistência:

```text
força de tração solicitada
↓
limite de aderência
↓
força de tração utilizável
↓
resistência ao rolamento
↓
força resultante
↓
aceleração
```

Se a aderência for suficiente:

```text
Ftracao_util = Ftracao
```

Nesse caso, os resultados da V5 devem ser iguais aos da V4.

Se a aderência for insuficiente:

```text
Ftracao_util < Ftracao
```

Nesse caso, a V5 calcula uma força resultante e uma aceleração menores do que as calculadas na V4.

---

## 11. Exemplo manual

Considere:

```text
massa = 0,20 kg
μs = 0,30
g = 9,81 m/s²
```

A força normal é:

```text
N = m × g
```

```text
N = 0,20 × 9,81
```

```text
N = 1,962 N
```

O limite de aderência é:

```text
Faderencia_max = μs × N
```

```text
Faderencia_max = 0,30 × 1,962
```

```text
Faderencia_max = 0,5886 N
```

Se a mola tentar transmitir:

```text
Ftracao = 0,80 N
```

então:

```text
Ftracao > Faderencia_max
```

Logo:

```text
Ftracao_util = min(0,80, 0,5886)
```

```text
Ftracao_util = 0,5886 N
```

Se a resistência ao rolamento for:

```text
Frr = 0,05 N
```

a nova força resultante será:

```text
Fresultante_V5 = 0,5886 - 0,05
```

```text
Fresultante_V5 = 0,5386 N
```

E a aceleração será:

```text
a = F / m
```

```text
a = 0,5386 / 0,20
```

```text
a = 2,693 m/s²
```

---

## 12. Validação das entradas

A V5 valida o coeficiente de atrito estático.

Se:

```text
μs < 0
```

o valor é considerado inválido.

No código:

```python
if coeficiente_atrito_estatico < 0:
    print(
        "O coeficiente de atrito estático (μ) "
        "não pode ser negativo."
    )
    exit()
```

O valor:

```text
μs = 0
```

é permitido.

Nesse caso:

```text
Faderencia_max = 0
```

e:

```text
Ftracao_util = 0
```

Isso representa, dentro deste modelo simplificado, uma situação em que nenhuma força de tração consegue ser transmitida ao chão.

---

## 13. Testes realizados

A V5 foi testada nos seguintes casos:

### Coeficiente negativo

```text
μs < 0
```

Resultado esperado:

```text
entrada inválida
```

### Coeficiente igual a zero

```text
μs = 0
```

Resultado esperado:

```text
Faderencia_max = 0
Ftracao_util = 0
```

### Tração abaixo do limite

```text
Ftracao < Faderencia_max
```

Resultado esperado:

```text
Ftracao_util = Ftracao
```

### Tração aproximadamente no limite

```text
Ftracao ≈ Faderencia_max
```

Resultado esperado:

```text
situação identificada como limite de aderência
```

### Tração acima do limite

```text
Ftracao > Faderencia_max
```

Resultado esperado:

```text
Ftracao_util = Faderencia_max
```

### Aderência muito alta

Quando o limite de aderência é muito superior à força de tração:

```text
Faderencia_max >> Ftracao
```

a aderência não interfere.

Nesse caso:

```text
Ftracao_util = Ftracao
```

e os resultados da V5 coincidem com os da V4.

Esse teste confirma que a V5 não altera artificialmente os resultados quando a aderência é suficiente.

---

## 14. Interpretação de força resultante negativa

A V5 pode produzir:

```text
Fresultante_V5 < 0
```

Isso ocorre quando:

```text
Ftracao_util < Frr
```

Uma força resultante negativa não significa automaticamente que o carrinho começa a se mover para trás.

Se ele já estiver se deslocando para frente, isso indica uma tendência de desaceleração.

A V5 ainda não conhece:

- velocidade;
- posição;
- tempo;
- estado de movimento do carrinho.

Esses elementos serão introduzidos nas próximas versões.

---

## 15. Limitações da V5

A V5 ainda utiliza um modelo simplificado.

Ela considera:

- força produzida pela mola;
- massa;
- resistência ao rolamento;
- limite de aderência;
- força de tração utilizável;
- força resultante;
- aceleração.

Porém, ainda não considera detalhadamente:

- atrito cinético;
- velocidade de escorregamento;
- rotação da roda durante patinagem;
- distribuição real de peso entre os eixos;
- transferência dinâmica de peso;
- posição do centro de massa;
- deformação detalhada das rodas;
- temperatura das rodas;
- resistência do ar;
- inércia rotacional;
- perdas detalhadas nos mancais;
- perdas na transmissão;
- velocidade do carrinho;
- posição do carrinho;
- evolução temporal do movimento.

A aproximação:

```text
Ntracao ≈ Ntotal
```

também tende a superestimar o limite de aderência quando apenas parte do peso está apoiada sobre o eixo tracionado.

---

## 16. Resultado da V5

Ao final da V5, o fluxo físico acumulado do RatoeiraLab é:

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
Quanto da força pode realmente ser transmitido ao chão
sem ultrapassar o limite de aderência?
```

A cadeia principal de cálculo da V5 é:

```text
μs + N
↓
Faderencia_max

Ftracao + Faderencia_max
↓
Ftracao_util = min(Ftracao, Faderencia_max)

Ftracao_util - Frr
↓
Fresultante_V5

Fresultante_V5 / m
↓
aceleracao_V5
```

---

## 17. Próxima versão

A próxima etapa do RatoeiraLab será:

```text
V6 — Movimento ao longo do tempo
```

Até a V5, o programa calcula forças e acelerações em estados específicos.

A V6 começará a estudar como essas grandezas evoluem ao longo do tempo.

Ela deverá preparar o simulador para, nas versões seguintes, calcular:

- velocidade;
- posição;
- distância percorrida;
- comportamento do carrinho durante o movimento.

---

## V5 — Aderência das rodas e limite de tração ✅ CONCLUÍDA

A V5 adiciona ao RatoeiraLab uma nova limitação física importante:

a força produzida pela mola não pode ser considerada automaticamente como força de tração disponível.

Agora o simulador verifica primeiro quanto dessa força pode ser transmitida ao chão respeitando o limite de aderência do modelo.

Com isso, o RatoeiraLab se aproxima mais de uma previsão física realista do carrinho, sem introduzir ainda uma simulação excessivamente complexa de derrapagem.
