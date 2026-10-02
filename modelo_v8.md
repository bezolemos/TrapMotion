# RatoeiraLab — Modelo V8

## V8 — Verificação da meta de distância

A V8 utiliza a distância final simulada pela V7 para verificar se o carrinho atingiu a meta definida pelo usuário.

Até a V7, o RatoeiraLab já conseguia simular o movimento completo do carrinho:

- fase impulsionada pela ratoeira;
- movimento por inércia;
- desaceleração por resistência ao rolamento;
- posição ao longo do tempo;
- distância total percorrida;
- tempo total de movimento.

A V8 não adiciona uma nova dinâmica física ao carrinho.

Seu objetivo é **interpretar os resultados da simulação** e responder:

```text
O carrinho atingiu a distância desejada?
```

Embora a meta original do projeto seja de 10 metros, o programa continua permitindo que o usuário informe qualquer valor positivo para a meta.

---

## 1. Distância utilizada pela V8

A V8 utiliza como distância oficial da simulação:

```python
distancia_simulada_m = posicao_atual_m
```

`posicao_atual_m` é a posição final produzida pela V7.

Como o carrinho começa em:

```text
x = 0 m
```

e o modelo atual não permite movimento para trás, a posição final é numericamente igual à distância total percorrida.

---

## 2. Distância simulada x alcance geométrico teórico

É importante distinguir dois resultados diferentes existentes no RatoeiraLab.

### Alcance geométrico teórico — V1

A V1 calcula:

```python
resultado_geometria["distancia_teorica_m"]
```

Esse valor indica quanto o sistema roda/eixo/corda permitiria percorrer geometricamente.

Ele não considera toda a dinâmica física adicionada nas versões posteriores.

### Distância simulada — V7/V8

A V8 utiliza:

```python
distancia_simulada_m
```

Esse valor vem da simulação temporal e considera, dentro das simplificações atuais:

- força da mola;
- massa;
- resistência ao rolamento;
- limite de aderência;
- evolução da força ao longo do tempo;
- fase impulsionada;
- movimento livre após o fim da impulsão.

Portanto, é possível existir uma situação como:

```text
alcance geométrico teórico >= meta
```

mas:

```text
distância simulada < meta
```

Isso significa que a geometria permitiria teoricamente aquela distância, mas as limitações físicas do modelo impediram o carrinho de alcançá-la.

---

## 3. Diferença para a meta

A V8 calcula:

```text
diferença = distância simulada - distância da meta
```

No código:

```python
diferenca_meta_m = (
    distancia_simulada_m - distancia_meta_m
)
```

A interpretação é:

```text
diferença > 0
→ o carrinho ultrapassou a meta

diferença = 0
→ o carrinho chegou exatamente à meta

diferença < 0
→ faltou distância
```

Exemplo:

```text
distância simulada = 12 m
meta = 10 m

diferença = +2 m
```

O carrinho ultrapassou a meta em 2 metros.

Outro exemplo:

```text
distância simulada = 7 m
meta = 10 m

diferença = -3 m
```

Faltaram 3 metros.

---

## 4. Percentual da meta atingido

A V8 também calcula quanto da meta foi alcançado em porcentagem:

```text
percentual =
(distância simulada / distância da meta) × 100
```

No código:

```python
porcentagem_meta_simulada = (
    distancia_simulada_m / distancia_meta_m
) * 100
```

Exemplos:

```text
8 m de uma meta de 10 m
→ 80%
```

```text
10 m de uma meta de 10 m
→ 100%
```

```text
12 m de uma meta de 10 m
→ 120%
```

A entrada `distancia_meta_m` já é validada para ser maior que zero, evitando divisão por zero.

---

## 5. Variável booleana da meta

A V8 cria:

```python
meta_atingida = (
    distancia_simulada_m >= distancia_meta_m
)
```

Essa expressão produz um valor booleano:

```text
True
```

quando a distância simulada é maior ou igual à meta,

ou:

```text
False
```

quando a distância simulada é menor que a meta.

Assim:

```text
meta_atingida = True
→ atingiu ou ultrapassou a meta

meta_atingida = False
→ ainda não atingiu a meta
```

---

## 6. Resultado final da análise

A V8 armazena a interpretação em:

```python
resultado_meta
```

São utilizados três estados possíveis.

### Meta atingida

```python
resultado_meta = "meta_atingida"
```

Ocorre quando:

```text
distância simulada >= meta
```

### Meta não atingida

```python
resultado_meta = "meta_nao_atingida"
```

Ocorre quando:

```text
distância simulada < meta
```

e a simulação terminou porque:

```text
carrinho_parou
```

Nesse caso, dentro do modelo atual, o carrinho realmente terminou seu movimento antes da meta.

### Resultado inconclusivo

```python
resultado_meta = "resultado_inconclusivo"
```

Ocorre quando a meta ainda não foi alcançada, mas a simulação terminou por:

```text
tempo_maximo_atingido
```

Nesse caso, o carrinho ainda poderia estar em movimento.

Por isso, a V8 não afirma automaticamente que ele falhou em atingir a meta.

---

## 7. Por que existe o resultado inconclusivo

A simulação possui um limite de segurança:

```python
tempo_maximo_simulacao = 60.0
```

Esse limite evita execuções excessivamente longas ou loops que não terminem em situações extremas.

Imagine:

```text
meta = 100 m
tempo = 60 s
distância = 80 m
velocidade ainda > 0
```

O carrinho ainda está andando quando a simulação termina.

Nesse caso, afirmar:

```text
META NÃO ATINGIDA
```

seria incorreto.

O resultado apropriado é:

```text
INCONCLUSIVO
```

porque a simulação terminou antes de observar a parada real.

---

## 8. Histórico usado para encontrar o instante da meta

A V7 já mantém duas listas importantes:

```python
historico_tempo
historico_posicao
```

Essas listas permanecem sincronizadas.

Assim, o mesmo índice representa o mesmo instante físico.

Exemplo:

```text
historico_tempo[i]
```

e:

```text
historico_posicao[i]
```

representam, respectivamente, o tempo e a posição do mesmo passo da simulação.

A V8 aproveita esses históricos para descobrir **quando** a meta foi atingida.

---

## 9. Busca pelo primeiro instante em que a meta foi atingida

Quando:

```python
meta_atingida == True
```

a V8 percorre o histórico de posições.

A lógica utilizada é:

```python
for i in range(len(historico_posicao)):
    if historico_posicao[i] >= distancia_meta_m:
        tempo_meta_atingida = historico_tempo[i]
        break
```

O programa verifica as posições em ordem temporal.

Quando encontra a primeira posição que atingiu ou ultrapassou a meta:

```text
posição >= meta
```

ele guarda o tempo correspondente.

---

## 10. Função do `break`

O comando:

```python
break
```

interrompe o `for` assim que o primeiro instante válido é encontrado.

Isso é necessário porque queremos:

```text
primeiro instante em que o carrinho atingiu a meta
```

e não o último instante em que ele permaneceu além dela.

Sem o `break`, o programa continuaria percorrendo o histórico mesmo depois de encontrar a meta.

---

## 11. Precisão do tempo em que a meta foi atingida

O instante calculado pela V8 está limitado pela resolução temporal da simulação:

```text
Δt = 0,005 s
```

Portanto, o valor representa o primeiro passo registrado em que:

```text
posição >= meta
```

A meta pode ter sido fisicamente cruzada em algum instante entre dois passos.

Por isso, o tempo encontrado é uma aproximação dentro da discretização utilizada pelo RatoeiraLab.

---

## 12. Meta atingida durante a fase impulsionada

A busca nos históricos cobre toda a simulação.

Assim, a meta pode ser alcançada enquanto a ratoeira ainda fornece tração.

Nesse caso:

```text
tempo_meta_atingida <= tempo_fim_impulsao
```

A V8 encontra normalmente esse instante no histórico.

---

## 13. Meta atingida durante a fase livre

A V7 continua registrando posição e tempo depois que a ratoeira deixa de impulsionar.

Por isso, a V8 também consegue detectar situações como:

```text
fim da impulsão
↓
carrinho ainda não atingiu a meta
↓
movimento por inércia
↓
carrinho ultrapassa a meta
```

Isso é importante porque o fim da ação da mola não significa o fim do movimento do carrinho.

---

## 14. Resultados exibidos pela V8

A seção da V8 apresenta:

```text
Meta definida
Distância simulada
Percentual da meta atingido
Margem acima da meta ou distância faltante
Resultado final
Tempo para atingir a meta, quando aplicável
```

Exemplo de sucesso:

```text
---------------- RESULTADOS DA V8 ----------------

Meta definida: 10.0000 m
Distância simulada: 12.3500 m
Percentual da meta atingido: 123.50%
Margem acima da meta: 2.3500 m
Resultado: META ATINGIDA
Tempo para atingir a meta: ...
```

---

## 15. Resultado quando a meta não é atingida

Exemplo:

```text
---------------- RESULTADOS DA V8 ----------------

Meta definida: 10.0000 m
Distância simulada: 7.8000 m
Percentual da meta atingido: 78.00%
Distância faltante para a meta: 2.2000 m
Resultado: META NÃO ATINGIDA
```

Esse resultado só é considerado definitivo quando o carrinho realmente terminou seu movimento dentro da simulação.

---

## 16. Resultado inconclusivo

Quando a simulação atinge o limite máximo antes da parada:

```text
Resultado: INCONCLUSIVO
```

A V8 também informa que:

```text
A simulação atingiu o limite máximo de tempo
antes de o carrinho parar.
```

Isso evita interpretar incorretamente um limite computacional como uma falha física do projeto.

---

## 17. Comparação entre a V1 e a V8

As duas análises respondem perguntas diferentes.

### V1

```text
A geometria roda/eixo/corda possui alcance teórico suficiente?
```

### V8

```text
A simulação física completa atingiu a meta?
```

A V1 é útil para avaliar o potencial geométrico do projeto.

A V8 utiliza o resultado acumulado das versões posteriores para avaliar o desempenho simulado.

Manter as duas análises permite identificar situações em que a geometria é suficiente, mas outros fatores físicos limitam o carrinho.

---

## 18. Casos importantes de teste

A lógica da V8 deve ser verificada com:

- distância exatamente igual à meta;
- distância maior que a meta;
- distância menor que a meta;
- carrinho que não consegue sair do lugar;
- meta pequena;
- meta grande;
- meta atingida durante a fase impulsionada;
- meta atingida durante a fase livre;
- simulação encerrada por limite máximo de tempo;
- margem positiva;
- distância faltante;
- percentual abaixo de 100%;
- percentual igual a 100%;
- percentual acima de 100%;
- primeiro instante registrado em que a meta é atingida.

---

## 19. Consistências verificadas na V8

A análise deve manter as seguintes relações:

```text
distância simulada = posição final da V7
```

```text
diferença = distância simulada - meta
```

```text
percentual =
(distância simulada / meta) × 100
```

Se:

```text
meta_atingida == True
```

deve existir pelo menos um ponto do histórico com:

```text
posição >= meta
```

Caso o carrinho pare antes da meta:

```text
resultado = meta_nao_atingida
```

Caso o limite temporal seja atingido antes da meta:

```text
resultado = resultado_inconclusivo
```

---

## 20. Limitações da V8

A V8 não aumenta a precisão física da simulação.

Sua conclusão depende diretamente da qualidade do modelo construído nas versões anteriores.

Portanto, continuam válidas as limitações já documentadas, incluindo:

- resistência do ar não simulada;
- inércia rotacional das rodas não simulada;
- perdas detalhadas nos mancais não simuladas;
- transmissão simplificada;
- aderência simplificada;
- distribuição real de peso não modelada;
- transferência de peso não modelada;
- dinâmica detalhada de derrapagem não modelada;
- relação simplificada entre corda e mola;
- integração temporal discreta.

Assim, dizer:

```text
META ATINGIDA
```

significa:

```text
a meta foi atingida dentro do modelo atual do RatoeiraLab
```

e não uma garantia de que um carrinho físico real terá exatamente o mesmo desempenho.

---

## 21. O que não entra na V8

A V8 não deve ainda responder:

```text
Por que o carrinho falhou?
```

nem:

```text
O que deve ser alterado para melhorar o projeto?
```

Também não deve decidir automaticamente alterações como:

- aumentar roda;
- reduzir eixo;
- modificar comprimento da corda;
- aumentar força da mola;
- reduzir massa;
- aumentar aderência.

Essas análises pertencem à próxima versão.

Também não entram ainda:

- gráficos;
- interface gráfica;
- otimização automática;
- resistência do ar;
- inércia rotacional;
- novas dinâmicas avançadas.

---

## 22. Resultado acumulado até a V8

O fluxo do RatoeiraLab agora é:

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
Como o movimento evolui durante a impulsão?

V7 — Velocidade, posição e distância
↓
Até onde o carrinho realmente chega na simulação?

V8 — Verificação da meta
↓
Essa distância simulada atingiu a meta definida?
```

---

## 23. Fluxo lógico principal da V8

```text
posição final da V7
↓
distancia_simulada_m

↓
comparar com distancia_meta_m

↓
calcular diferenca_meta_m

↓
calcular porcentagem_meta_simulada

↓
meta_atingida?

├── SIM
│   ↓
│   resultado = meta_atingida
│   ↓
│   procurar primeiro instante da meta
│
└── NÃO
    ↓
    como a simulação terminou?

    ├── carrinho_parou
    │   ↓
    │   resultado = meta_nao_atingida
    │
    └── tempo_maximo_atingido
        ↓
        resultado = resultado_inconclusivo
```

---

## 24. Próxima versão

A próxima etapa do RatoeiraLab será:

```text
V9 — Análise do design e recomendações de ajustes
```

A V8 responde:

```text
O carrinho atingiu a meta?
```

A V9 deverá utilizar os resultados acumulados para analisar:

```text
Por que conseguiu?
```

ou:

```text
Por que não conseguiu?
```

e então fornecer recomendações coerentes com o modelo físico.

---

## V8 — Verificação da meta de distância ✅ CONCLUÍDA

A V8 transforma a distância produzida pela simulação em uma avaliação objetiva da meta do projeto.

Agora o RatoeiraLab consegue:

- comparar distância simulada e meta;
- calcular quanto faltou ou sobrou;
- calcular o percentual alcançado;
- identificar se a meta foi atingida;
- distinguir falha real de encerramento inconclusivo;
- identificar aproximadamente quando a meta foi atingida;
- diferenciar alcance geométrico teórico de desempenho físico simulado.

Com isso, o simulador já consegue responder se um determinado projeto, **dentro das simplificações atuais do modelo**, alcança a distância definida pelo usuário.
