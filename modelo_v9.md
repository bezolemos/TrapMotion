# RatoeiraLab — Modelo V9

## V9 — Análise do design e recomendações

A V9 adiciona ao RatoeiraLab uma camada de interpretação sobre os resultados produzidos pelas versões anteriores.

Até a V8, o simulador já conseguia responder:

```text
O carrinho atingiu a meta?
```

A V9 passa a responder também:

```text
O que limitou o desempenho do projeto?
```

e, quando a meta não é atingida:

```text
Que aspectos do design merecem ser revisados?
```

A V9 não adiciona uma nova dinâmica física ao movimento.

Ela reutiliza resultados já calculados pelas versões anteriores para produzir:

- diagnósticos;
- interpretação do fim da impulsão;
- identificação de possíveis gargalos;
- recomendações de revisão do design.

---

## 1. Ideia central da V9

A V9 separa duas coisas:

```text
diagnóstico
≠
recomendação
```

### Diagnóstico

O diagnóstico descreve algo que aconteceu durante a simulação.

Exemplos:

```text
aderência limitando
corda terminou primeiro
mola terminou primeiro
alcance geométrico insuficiente
```

Um diagnóstico pode existir mesmo quando o carrinho atinge a meta.

### Recomendação

A recomendação sugere algo que pode ser revisado no projeto.

Na V9, recomendações corretivas são geradas apenas quando:

```text
resultado_meta == "meta_nao_atingida"
```

Isso evita recomendar alterações desnecessárias para um carrinho que já cumpriu a meta.

---

## 2. Verificação do alcance geométrico

A primeira análise compara:

```text
distância geométrica teórica
```

com:

```text
distância da meta
```

No código:

```python
alcance_geometrico_suficiente = (
    resultado_geometria["distancia_teorica_m"] >= distancia_meta_m
)
```

Se o resultado for:

```text
True
```

a geometria roda/eixo/corda possui alcance teórico suficiente.

Se for:

```text
False
```

a geometria, isoladamente, apresenta alcance abaixo da meta.

É importante lembrar que esse valor é geométrico e não representa sozinho a distância final simulada.

O carrinho ainda pode continuar em movimento por inércia depois do fim da impulsão.

---

## 3. Verificação da força inicial

A V9 também verifica se a força útil disponível no início é suficiente para superar a resistência ao rolamento.

A condição utilizada é:

```text
força de tração útil inicial > resistência ao rolamento
```

No código:

```python
forca_inicial_suficiente = (
    forca_tracao_util_inicial > forca_resistencia_rolamento
)
```

Se for verdadeira, existe força resultante positiva no início.

Se for falsa, o carrinho não possui força útil inicial suficiente para produzir aceleração positiva a partir do repouso dentro do modelo atual.

---

## 4. Por que utilizar a força de tração útil

A V9 não compara a resistência apenas com a força ideal produzida pela mola.

Ela utiliza:

```python
forca_tracao_util_inicial
```

porque esse valor já considera o limite de aderência.

A lógica física é:

```text
força produzida pela mola
↓
limite de aderência entre roda e chão
↓
força que realmente pode ser transmitida
```

Assim, uma mola muito forte não significa automaticamente uma força útil igualmente alta.

---

## 5. Identificação de aderência limitante

A V9 verifica:

```python
aderencia_limitando = (
    resultado_mola["forca_tracao_inicial"]
    > forca_aderencia_maxima
)
```

Quando isso é verdadeiro:

```text
força que a mola tenta fornecer
>
força máxima que a aderência suporta
```

Portanto, parte da força disponível não pode ser transmitida ao solo dentro do modelo simplificado.

Isso é tratado como um diagnóstico de possível gargalo.

---

## 6. Aderência limitante não significa necessariamente falha

Um ponto importante da V9 é que:

```text
aderência limitando
```

não significa automaticamente:

```text
meta não atingida
```

O carrinho pode atingir a meta mesmo com a aderência limitando parte da força.

Por isso, o diagnóstico pode ser exibido sem que uma recomendação corretiva seja gerada.

---

## 7. Estado final da mola

A mola é considerada finalizada quando:

```text
ângulo <= 0
```

ou quando o ângulo é tão próximo de zero que pode ser tratado como zero numericamente.

A V9 utiliza:

```python
mola_finalizada_v9 = (
    angulo_atual_rad <= 0
    or math.isclose(
        angulo_atual_rad,
        0,
        abs_tol=1e-9
    )
)
```

O uso de `math.isclose()` evita problemas causados por precisão de ponto flutuante.

---

## 8. Por que usar `math.isclose()`

Durante cálculos numéricos, um valor que matematicamente deveria ser:

```text
0
```

pode aparecer como algo parecido com:

```text
0.000000000000001
```

Para o Python, esse valor ainda é maior que zero.

`math.isclose()` permite considerar valores extremamente próximos como equivalentes.

Com:

```python
abs_tol=1e-9
```

um valor cuja diferença para zero seja menor que essa tolerância pode ser tratado como praticamente zero.

---

## 9. Estado final da corda

A corda é considerada finalizada quando:

```python
corda_finalizada_v9 = (
    corda_desenrolada_total_m >= comprimento_corda_m
)
```

Isso indica que todo o comprimento disponível foi desenrolado.

---

## 10. Análise conjunta de mola e corda

A V9 combina os dois estados:

```python
(mola_finalizada_v9, corda_finalizada_v9)
```

Como cada valor pode ser `True` ou `False`, existem quatro combinações possíveis:

```text
(False, True)
→ corda terminou primeiro

(True, False)
→ mola terminou primeiro

(True, True)
→ ambos finalizaram no mesmo passo da simulação

(False, False)
→ outro tipo de encerramento
```

---

## 11. Uso de `match / case`

A V9 utiliza `match / case` para interpretar essas quatro combinações.

Estrutura:

```python
match (mola_finalizada_v9, corda_finalizada_v9):

    case (False, True):
        estado_fim_impulsao = "corda_terminou_primeiro"

    case (True, False):
        estado_fim_impulsao = "mola_terminou_primeiro"

    case (True, True):
        estado_fim_impulsao = "ambos_finalizados"

    case (False, False):
        estado_fim_impulsao = "outro_encerramento"
```

O `match` compara o par de valores com cada padrão disponível.

---

## 12. Importante: fim da impulsão não é fim do movimento

Se a mola ou a corda terminarem, isso significa apenas que terminou a fase em que a ratoeira fornece tração.

O carrinho ainda pode possuir:

- velocidade;
- energia cinética;
- quantidade de movimento.

Assim:

```text
fim da mola/corda
↓
fim da tração
↓
movimento por inércia
↓
desaceleração por resistência
↓
parada
```

A V7 já simula essa fase livre.

---

## 13. Interpretação: corda terminou primeiro

Quando:

```text
corda_finalizada_v9 = True
mola_finalizada_v9 = False
```

a corda terminou enquanto a mola ainda não havia chegado ao fim de sua ação.

Esse caso é armazenado como:

```text
"corda_terminou_primeiro"
```

A V9 interpreta isso como um sinal de que o comprimento da corda ou a relação de transmissão podem merecer revisão.

Ela não assume automaticamente que a única solução seja aumentar a corda.

---

## 14. Interpretação: mola terminou primeiro

Quando:

```text
mola_finalizada_v9 = True
corda_finalizada_v9 = False
```

a mola terminou sua ação enquanto ainda havia corda disponível.

Esse caso é armazenado como:

```text
"mola_terminou_primeiro"
```

Isso pode indicar que a relação entre mola e corda merece revisão.

---

## 15. Interpretação: ambos finalizados

Quando:

```text
(True, True)
```

a V9 registra:

```text
"ambos_finalizados"
```

Isso significa que, dentro da resolução temporal da simulação, mola e corda chegaram ao fim no mesmo passo.

Como o passo de tempo é discreto, isso não prova que os dois eventos ocorreram no exato mesmo instante físico.

---

## 16. Lista de diagnósticos

A V9 cria:

```python
diagnosticos_v9 = []
```

Essa lista permite registrar vários diagnósticos simultaneamente.

Isso é importante porque um projeto pode apresentar mais de uma limitação.

Exemplo:

```text
alcance geométrico insuficiente
+
força inicial insuficiente
+
aderência limitando
```

Todos podem ser armazenados ao mesmo tempo.

---

## 17. Diagnósticos possíveis

A V9 pode adicionar:

```text
"alcance_geometrico_insuficiente"
"forca_inicial_insuficiente"
"aderencia_limitando"
"corda_terminou_primeiro"
"mola_terminou_primeiro"
```

`"ambos_finalizados"` não é adicionado à lista de problemas porque não representa necessariamente uma limitação.

---

## 18. Por que usar vários `if`

Os principais diagnósticos utilizam vários `if` independentes.

Isso permite que mais de um problema seja identificado.

Exemplo:

```python
if not alcance_geometrico_suficiente:
    ...

if not forca_inicial_suficiente:
    ...

if aderencia_limitando:
    ...
```

Se fosse utilizado um único bloco `if / elif`, o programa poderia encontrar o primeiro problema e deixar de registrar os seguintes.

---

## 19. Lista de recomendações

A V9 cria outra lista:

```python
recomendacoes_v9 = []
```

Essa lista é separada de `diagnosticos_v9`.

A separação permite distinguir:

```text
o que aconteceu
```

de:

```text
o que pode ser revisado
```

---

## 20. Quando recomendações são geradas

As recomendações são geradas somente quando:

```python
resultado_meta == "meta_nao_atingida"
```

Isso exclui dois casos:

### Meta atingida

Se o carrinho atingiu a meta, diagnósticos ainda podem ser mostrados, mas não são tratados automaticamente como falhas que exigem correção.

### Resultado inconclusivo

Se a simulação terminou pelo limite máximo de tempo antes de observar a parada, a V9 evita recomendar alterações como se a falha estivesse confirmada.

---

## 21. Recomendação para alcance geométrico insuficiente

Quando aparece:

```text
"alcance_geometrico_insuficiente"
```

a V9 adiciona:

```text
"ajustar_geometria_para_aumentar_alcance"
```

A recomendação é mantida de forma geral.

Alterações possíveis podem envolver:

- diâmetro da roda;
- diâmetro do eixo;
- comprimento da corda.

A V1 já possui cálculos geométricos específicos para essas alternativas.

---

## 22. Recomendação para força inicial insuficiente

Quando aparece:

```text
"forca_inicial_insuficiente"
```

a V9 verifica primeiro se:

```python
aderencia_limitando
```

é verdadeiro.

Isso evita recomendar simplesmente uma mola mais forte quando a aderência já é o gargalo.

---

## 23. Força insuficiente com aderência limitante

Quando existem simultaneamente:

```text
força inicial insuficiente
+
aderência limitando
```

a V9 recomenda:

```text
"melhorar_aderencia_ou_reduzir_resistencia"
```

A lógica é:

```text
mais força produzida pela mola
↓
aderência continua sendo o limite
↓
força útil pode continuar insuficiente
```

Portanto, atacar o gargalo de aderência ou a resistência é mais coerente do que simplesmente aumentar a mola.

---

## 24. Força insuficiente sem aderência limitante

Quando:

```text
força inicial insuficiente
```

mas:

```text
aderência não está limitando
```

a V9 adiciona:

```text
"aumentar_forca_tracao"
```

Nesse cenário, existe margem para aumentar a força útil transmitida ao solo.

---

## 25. Recomendação quando a corda termina primeiro

Quando o diagnóstico contém:

```text
"corda_terminou_primeiro"
```

a V9 adiciona:

```text
"revisar_comprimento_corda"
```

A recomendação não ordena automaticamente aumentar a corda.

Ela indica que o comprimento e sua relação com o restante do sistema devem ser analisados.

---

## 26. Recomendação quando a mola termina primeiro

Quando aparece:

```text
"mola_terminou_primeiro"
```

a V9 adiciona:

```text
"revisar_relacao_mola_corda"
```

Isso sugere revisar como a ação da mola está sendo aproveitada pelo sistema de transmissão.

---

## 27. Recomendação genérica

Pode acontecer de:

```text
resultado_meta = "meta_nao_atingida"
```

sem que os diagnósticos existentes produzam uma recomendação específica.

Nesse caso:

```python
if not recomendacoes_v9:
```

a V9 adiciona:

```text
"revisar_parametros_gerais_design"
```

Isso impede que uma falha confirmada termine sem nenhuma orientação.

---

## 28. Uso do operador `in`

A V9 utiliza o operador:

```python
in
```

para verificar se determinado diagnóstico existe dentro da lista.

Exemplo:

```python
if "alcance_geometrico_insuficiente" in diagnosticos_v9:
```

Isso significa:

```text
se esse diagnóstico estiver presente na lista
```

O mesmo conceito é utilizado para decidir quais recomendações devem ser adicionadas.

---

## 29. Exibição dos diagnósticos

Os diagnósticos são percorridos com:

```python
for diagnostico in diagnosticos_v9:
```

Cada código interno é transformado em uma mensagem compreensível para o usuário.

Exemplos:

```text
⚠ O alcance geométrico do projeto está abaixo da meta.

⚠ A força de tração inicial é insuficiente para superar
a resistência ao rolamento.

⚠ A força de tração inicial excede a aderência máxima,
o que pode causar derrapagem.
```

---

## 30. Exibição das recomendações

As recomendações também são percorridas com um `for`:

```python
for recomendacao in recomendacoes_v9:
```

Exemplos de mensagens:

```text
💡 Considere ajustar a geometria do projeto para aumentar o alcance.

💡 Considere melhorar a aderência ou reduzir a resistência ao rolamento.

💡 Considere aumentar a força de tração inicial.

💡 Considere revisar o comprimento da corda.

💡 Considere revisar a relação entre a mola e a corda.
```

---

## 31. Evitando títulos vazios

Antes de mostrar:

```text
Diagnósticos:
```

a V9 verifica:

```python
if diagnosticos_v9:
```

Uma lista vazia é considerada falsa em uma condição Python.

Da mesma forma:

```python
if recomendacoes_v9:
```

evita imprimir o título de recomendações quando não existe nenhuma recomendação.

---

## 32. Organização da saída da V9

A seção final segue a estrutura:

```text
---------------- ANÁLISE DA V9 ----------------

situação geral do projeto

Diagnósticos:
...

Recomendações:
...
```

A situação geral utiliza o resultado já calculado na V8.

São considerados:

```text
meta atingida
meta não atingida
resultado inconclusivo
```

---

## 33. Caso: meta atingida

Quando:

```text
resultado_meta = "meta_atingida"
```

a V9 informa:

```text
✅ O projeto atingiu a meta.
```

Diagnósticos ainda podem aparecer.

Porém:

```text
recomendacoes_v9 = []
```

permanece sem recomendações corretivas.

---

## 34. Caso: meta não atingida

Quando:

```text
resultado_meta = "meta_nao_atingida"
```

a V9 informa:

```text
❌ O projeto não atingiu a meta.
```

Nesse caso, os diagnósticos são utilizados para gerar recomendações relacionadas aos problemas encontrados.

---

## 35. Caso: resultado inconclusivo

Quando:

```text
resultado_meta = "resultado_inconclusivo"
```

a V9 informa que não foi possível concluir se o projeto atingiria a meta.

Os diagnósticos observados podem ser mostrados, mas recomendações corretivas não são produzidas automaticamente.

---

## 36. Testes importantes da V9

A V9 deve ser verificada em cenários como:

- meta atingida com diagnósticos presentes;
- meta não atingida;
- alcance geométrico insuficiente;
- força inicial insuficiente;
- aderência limitando;
- força insuficiente com aderência limitando;
- força insuficiente sem aderência limitando;
- corda terminando primeiro;
- mola terminando primeiro;
- mola e corda finalizando no mesmo passo;
- nenhum diagnóstico específico;
- resultado inconclusivo;
- vários diagnósticos simultâneos;
- ausência de recomendações quando a meta é atingida;
- ausência de recomendações quando o resultado é inconclusivo.

---

## 37. Limitações dos diagnósticos

As recomendações da V9 dependem do modelo físico já construído.

Elas não representam uma otimização automática nem garantem que uma alteração específica melhorará um carrinho real.

Por exemplo:

```text
aumentar o diâmetro da roda
```

pode aumentar o alcance geométrico, mas também altera a relação de transmissão e pode reduzir a força disponível nas rodas.

Por isso, a V9 prefere recomendações como:

```text
revisar geometria
revisar relação mola-corda
```

em vez de ordenar alterações específicas sem considerar seus efeitos conjuntos.

---

## 38. O que a V9 ainda não faz

A V9 ainda não:

- procura automaticamente a configuração ótima;
- executa centenas de combinações de parâmetros;
- escolhe sozinho o melhor diâmetro de roda;
- calcula a melhor mola;
- calcula o melhor coeficiente de aderência;
- inclui resistência aerodinâmica;
- inclui inércia rotacional;
- modela detalhadamente a derrapagem;
- gera gráficos;
- possui interface gráfica.

Esses limites mantêm a versão compatível com o objetivo didático do projeto.

---

## 39. Resultado acumulado até a V9

O fluxo do RatoeiraLab agora pode ser resumido assim:

```text
V1 — Geometria e alcance teórico
↓
V2 — Mola, torque e transmissão
↓
V3 — Massa e aceleração ideal
↓
V4 — Resistência ao movimento
↓
V5 — Aderência e limite de tração
↓
V6 — Movimento ao longo do tempo
↓
V7 — Velocidade, posição e distância
↓
V8 — Verificação da meta
↓
V9 — Diagnóstico do design e recomendações
```

---

## 40. Fluxo lógico principal da V9

```text
resultados das versões anteriores
↓
verificar alcance geométrico
↓
verificar força inicial
↓
verificar limite de aderência
↓
verificar estado final da mola
↓
verificar estado final da corda
↓
classificar fim da impulsão
↓
montar lista de diagnósticos
↓
meta não atingida?
├── NÃO
│   ↓
│   não gerar correções automáticas
│
└── SIM
    ↓
    interpretar diagnósticos
    ↓
    montar recomendações
↓
mostrar análise ao usuário
```

---

## 41. Próxima versão

A próxima etapa planejada é:

```text
V10 — Gráficos e visualização dos resultados
```

A V10 deverá aproveitar os históricos já criados pelo simulador, como:

```python
historico_tempo
historico_velocidade
historico_aceleracao
historico_angulo
historico_posicao
```

para representar visualmente a evolução do movimento.

---

# V9 — Análise do design e recomendações ✅ CONCLUÍDA

Com a V9, o RatoeiraLab deixa de apenas calcular resultados e passa a interpretá-los.

O simulador agora consegue:

- avaliar se a geometria é suficiente;
- detectar força inicial insuficiente;
- identificar aderência limitante;
- comparar o fim da mola e da corda;
- registrar vários diagnósticos simultaneamente;
- separar diagnóstico de recomendação;
- evitar correções automáticas quando a meta já foi atingida;
- evitar recomendações definitivas em resultados inconclusivos;
- fornecer orientações de revisão do design quando a meta não é alcançada.

A V9 prepara o projeto para a etapa seguinte, em que os resultados poderão ser apresentados de forma visual por meio de gráficos.
