# RatoeiraLab — Modelo V10

## V10 — Gráficos e visualização dos resultados

A V10 adiciona ao RatoeiraLab uma camada de visualização dos resultados da simulação.

Até a V9, o programa já conseguia:

- calcular a geometria do carrinho;
- modelar a mola e a transmissão de força;
- calcular aceleração e resistência ao movimento;
- limitar a tração pela aderência;
- simular o movimento ao longo do tempo;
- acompanhar velocidade, posição e distância;
- verificar a meta;
- diagnosticar limitações do design;
- gerar recomendações.

A V10 não adiciona uma nova dinâmica física.

Ela utiliza os dados já armazenados durante a simulação para transformar os resultados numéricos em gráficos.

Os principais gráficos são:

```text
posição × tempo
velocidade × tempo
aceleração × tempo
ângulo da mola × tempo
```

---

## 1. Objetivo da V10

O objetivo principal da V10 é facilitar a interpretação do comportamento do carrinho.

Em vez de observar apenas valores finais como:

```text
distância final
velocidade final
tempo total
ângulo final da mola
```

o usuário passa a conseguir observar como essas grandezas mudam durante toda a simulação.

Isso permite identificar visualmente:

- quando o carrinho acelera;
- quando começa a desacelerar;
- quando termina a fase impulsionada;
- quando a meta é atingida;
- como a mola perde ângulo;
- se a corda termina antes da mola;
- se o carrinho continua em movimento depois do fim da impulsão.

---

## 2. Biblioteca utilizada

A V10 utiliza a biblioteca:

```python
matplotlib
```

Mais especificamente:

```python
import matplotlib.pyplot as plt
```

O módulo `pyplot` fornece as ferramentas utilizadas para criar e exibir os gráficos.

O nome:

```python
plt
```

é um apelido utilizado para deixar os comandos mais curtos.

Por exemplo:

```python
plt.show()
```

em vez de escrever o caminho completo da biblioteca.

---

## 3. Instalação do Matplotlib

Como o Matplotlib não faz parte da biblioteca padrão do Python, pode ser necessário instalá-lo.

No Windows, utilizando o Python Launcher:

```powershell
py -m pip install matplotlib
```

Depois da instalação, o projeto pode importar:

```python
import matplotlib.pyplot as plt
```

A partir da V10, o Matplotlib passa a ser uma dependência externa do RatoeiraLab.

---

## 4. Históricos utilizados

A V10 reaproveita as listas criadas durante a simulação:

```python
historico_tempo
historico_velocidade
historico_aceleracao
historico_angulo
historico_posicao
```

Essas listas são atualizadas durante o movimento do carrinho.

Cada posição das listas representa aproximadamente o mesmo instante da simulação.

Exemplo conceitual:

```text
índice 0
tempo = 0 s
posição = 0 m
velocidade = 0 m/s

índice 1
tempo = 0,005 s
posição = ...
velocidade = ...

índice 2
tempo = 0,010 s
posição = ...
velocidade = ...
```

Isso permite relacionar o tempo com as outras grandezas.

---

## 5. Eixo X e eixo Y

Nos quatro gráficos principais, o tempo é utilizado no eixo X.

A lógica é:

```text
eixo X → variável utilizada para acompanhar a evolução
eixo Y → grandeza observada
```

No RatoeiraLab:

```text
X = tempo
```

e o eixo Y muda de acordo com o gráfico.

Por exemplo:

```text
posição × tempo
X = tempo
Y = posição
```

---

## 6. Primeiro gráfico: posição × tempo

O primeiro gráfico mostra como a posição do carrinho muda ao longo do tempo.

Os dados utilizados são:

```python
historico_tempo
historico_posicao
```

Na versão final organizada:

```python
eixos[0, 0].plot(
    historico_tempo,
    historico_posicao
)
```

Os nomes utilizados são:

```python
eixos[0, 0].set_title(
    "Posição do carrinho ao longo do tempo"
)

eixos[0, 0].set_xlabel("Tempo (s)")
eixos[0, 0].set_ylabel("Posição (m)")
```

---

## 7. Interpretação do gráfico de posição

O gráfico de posição permite observar o deslocamento acumulado do carrinho.

Uma curva cada vez mais inclinada indica que a velocidade está aumentando.

Uma curva que continua subindo, mas começa a perder inclinação, indica que o carrinho continua avançando, porém está desacelerando.

Quando a curva fica horizontal:

```text
posição não muda
```

portanto:

```text
velocidade = 0
```

e o carrinho parou.

---

## 8. Relação entre inclinação e velocidade

No gráfico posição × tempo, a inclinação da curva está relacionada à velocidade.

Conceitualmente:

```text
curva pouco inclinada
→ velocidade baixa

curva muito inclinada
→ velocidade alta

curva horizontal
→ velocidade zero
```

A V10 não calcula uma nova velocidade a partir do gráfico.

Ela apenas representa visualmente a velocidade que já foi calculada pela simulação.

---

## 9. Linha horizontal da meta

O gráfico de posição também mostra a distância escolhida como meta.

Para isso é utilizada:

```python
eixos[0, 0].axhline(
    y=distancia_meta_m,
    linestyle="--",
    label="Meta"
)
```

`axhline()` cria uma linha horizontal.

A posição vertical da linha é:

```python
y=distancia_meta_m
```

Assim, a meta pode ser comparada diretamente com a trajetória da posição.

---

## 10. Marcação do instante em que a meta foi atingida

A V8 já calcula:

```python
tempo_meta_atingida
```

Esse valor pode ser:

```text
um número
```

quando a meta foi atingida, ou:

```python
None
```

quando ela não foi atingida.

Por isso, a V10 verifica:

```python
if tempo_meta_atingida is not None:
```

e somente então desenha:

```python
eixos[0, 0].axvline(
    x=tempo_meta_atingida,
    linestyle=":",
    label="Meta atingida"
)
```

Isso evita mostrar uma marcação de um evento que nunca aconteceu.

---

## 11. Segundo gráfico: velocidade × tempo

O segundo gráfico utiliza:

```python
historico_tempo
historico_velocidade
```

No código:

```python
eixos[0, 1].plot(
    historico_tempo,
    historico_velocidade
)
```

Com:

```python
eixos[0, 1].set_title(
    "Velocidade do carrinho ao longo do tempo"
)

eixos[0, 1].set_xlabel("Tempo (s)")
eixos[0, 1].set_ylabel("Velocidade (m/s)")
```

---

## 12. Interpretação do gráfico de velocidade

Esse gráfico permite visualizar diretamente quando o carrinho:

```text
ganha velocidade
↓
atinge uma velocidade máxima
↓
perde velocidade
↓
para
```

Durante parte da fase impulsionada, a velocidade pode aumentar.

Entretanto, o pico de velocidade não precisa acontecer exatamente no fim da impulsão.

A mola pode continuar atuando, mas com força pequena demais para superar a resistência ao rolamento.

Nesse caso:

```text
a mola ainda atua
```

mas:

```text
força resultante < 0
```

e o carrinho já começa a desacelerar.

---

## 13. Marcação do fim da impulsão

O simulador registra:

```python
tempo_fim_impulsao
```

Esse instante separa:

```text
fase impulsionada
```

de:

```text
fase livre
```

A V10 utiliza:

```python
.axvline()
```

para desenhar uma linha vertical.

No gráfico de velocidade:

```python
eixos[0, 1].axvline(
    x=tempo_fim_impulsao,
    linestyle="--",
    label="Fim da impulsão"
)
```

---

## 14. Fim da impulsão não significa fim do movimento

Uma das informações mais importantes mostradas pelos gráficos é:

```text
fim da impulsão
≠
fim do movimento
```

Depois que a mola ou a corda deixa de impulsionar o carrinho, ele pode continuar com velocidade positiva.

Durante essa segunda fase, a resistência ao rolamento reduz gradualmente sua velocidade.

O carrinho só para quando:

```text
velocidade = 0
```

ou quando o limite máximo de tempo da simulação é atingido.

---

## 15. Terceiro gráfico: aceleração × tempo

O terceiro gráfico utiliza:

```python
historico_tempo
historico_aceleracao
```

No código:

```python
eixos[1, 0].plot(
    historico_tempo,
    historico_aceleracao
)
```

Os eixos são:

```python
eixos[1, 0].set_xlabel("Tempo (s)")
eixos[1, 0].set_ylabel("Aceleração (m/s²)")
```

---

## 16. Interpretação do gráfico de aceleração

Durante a fase impulsionada, a aceleração muda porque a força produzida pela mola também muda.

A relação fundamental continua sendo:

```text
força resultante
↓
aceleração
```

Quando a força de tração diminui, a aceleração também tende a diminuir.

Depois do fim da impulsão, o modelo usa uma aceleração negativa associada à resistência ao rolamento.

---

## 17. Aceleração negativa

No gráfico, uma aceleração negativa não significa automaticamente que o carrinho está andando para trás.

Se:

```text
velocidade > 0
```

e:

```text
aceleração < 0
```

o carrinho ainda está se movendo para frente, mas está perdendo velocidade.

Portanto:

```text
velocidade positiva + aceleração negativa
→ desaceleração
```

---

## 18. Fim da impulsão no gráfico de aceleração

A linha vertical também é desenhada no gráfico de aceleração:

```python
eixos[1, 0].axvline(
    x=tempo_fim_impulsao,
    linestyle="--",
    label="Fim da impulsão"
)
```

Isso facilita a comparação entre:

```text
fim da ação propulsora
```

e:

```text
mudança do comportamento da aceleração
```

---

## 19. Quarto gráfico: ângulo da mola × tempo

O quarto gráfico acompanha o ângulo da mola.

O histórico é armazenado internamente em radianos:

```python
historico_angulo
```

Porém, para facilitar a leitura pelo usuário, a V10 converte cada valor para graus.

---

## 20. Conversão dos ângulos para graus

A conversão é feita com:

```python
[
    math.degrees(angulo)
    for angulo in historico_angulo
]
```

Essa expressão cria uma nova lista.

Ela é equivalente conceitualmente a:

```python
angulos_graus = []

for angulo in historico_angulo:
    angulos_graus.append(
        math.degrees(angulo)
    )
```

A versão compacta é utilizada diretamente no gráfico.

---

## 21. Interpretação do gráfico do ângulo

O gráfico do ângulo permite observar a ação da mola.

No início:

```text
ângulo alto
```

À medida que a corda é desenrolada:

```text
ângulo diminui
```

Se a mola termina sua ação:

```text
ângulo → 0°
```

Se a corda termina primeiro:

```text
ângulo final > 0°
```

e o gráfico permanece aproximadamente horizontal depois do fim da impulsão.

---

## 22. Identificando corda curta pelo gráfico

Quando a corda termina antes da mola, o gráfico do ângulo mostra uma característica importante:

```text
ângulo diminui
↓
corda termina
↓
ângulo permanece acima de 0°
```

Isso significa que ainda existe deformação angular na mola, mas a configuração da corda não permite continuar transmitindo o movimento dentro do modelo atual.

Essa visualização complementa o diagnóstico da V9:

```text
corda terminou primeiro
```

---

## 23. Fim da impulsão no gráfico do ângulo

A V10 também desenha:

```python
eixos[1, 1].axvline(
    x=tempo_fim_impulsao,
    linestyle="--",
    label="Fim da impulsão"
)
```

Assim, é possível observar diretamente qual era o ângulo da mola quando a primeira fase terminou.

---

## 24. Por que utilizar quatro gráficos

Cada gráfico responde uma pergunta diferente.

```text
posição
→ até onde o carrinho chegou?

velocidade
→ quão rápido ele estava?

aceleração
→ como a força resultante afetou o movimento?

ângulo
→ como a mola evoluiu durante a simulação?
```

Analisar os quatro juntos ajuda a entender o comportamento completo do carrinho.

---

## 25. Organização com `subplots`

Inicialmente, cada gráfico podia ser exibido em uma janela separada.

A V10 organiza os quatro em uma única figura:

```python
figura, eixos = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)
```

`2, 2` significa:

```text
2 linhas
2 colunas
```

resultando em quatro áreas para gráficos.

---

## 26. Organização da matriz de gráficos

Os quatro gráficos são organizados assim:

```text
[0, 0] → posição
[0, 1] → velocidade

[1, 0] → aceleração
[1, 1] → ângulo da mola
```

Visualmente:

```text
┌─────────────────────┬─────────────────────┐
│ Posição             │ Velocidade          │
├─────────────────────┼─────────────────────┤
│ Aceleração          │ Ângulo da mola      │
└─────────────────────┴─────────────────────┘
```

A indexação começa em zero, assim como em listas e matrizes do Python.

---

## 27. Diferença entre `plt` e `eixos`

Antes dos `subplots`, comandos como:

```python
plt.plot()
plt.title()
plt.xlabel()
plt.ylabel()
```

atuavam no gráfico atual.

Com vários gráficos na mesma figura, é necessário indicar qual eixo deve receber cada comando.

Exemplo:

```python
eixos[0, 0].plot(...)
```

Para títulos e nomes de eixos, são utilizados:

```python
.set_title()
.set_xlabel()
.set_ylabel()
```

---

## 28. Legendas

As linhas especiais possuem nomes usando:

```python
label="..."
```

Exemplos:

```text
Meta
Meta atingida
Fim da impulsão
```

Para exibir esses nomes:

```python
.legend()
```

é chamado no gráfico correspondente.

É importante utilizar os parênteses:

```python
.legend()
```

e não apenas:

```python
.legend
```

porque os parênteses executam a função.

---

## 29. Grade dos gráficos

A V10 adiciona uma grade com:

```python
.grid(True)
```

A grade facilita a leitura aproximada dos valores nos eixos.

Ela foi aplicada nos quatro gráficos.

Exemplo:

```python
eixos[0, 0].grid(True)
```

---

## 30. Tamanho da figura

O tamanho da janela é configurado com:

```python
figsize=(12, 8)
```

em:

```python
plt.subplots()
```

Isso ajuda a evitar que:

- títulos fiquem muito próximos;
- nomes dos eixos se sobreponham;
- legendas ocupem espaço excessivo;
- os gráficos fiquem pequenos demais.

---

## 31. Organização automática do espaço

A V10 utiliza:

```python
plt.tight_layout()
```

antes de exibir os gráficos.

Esse comando pede ao Matplotlib para ajustar automaticamente os espaços entre:

- gráficos;
- títulos;
- rótulos;
- eixos.

Ele melhora a legibilidade da figura 2×2.

---

## 32. Exibição da figura

Depois de configurar todos os gráficos:

```python
plt.show()
```

exibe a janela.

A V10 utiliza apenas um `plt.show()` para a figura final com os quatro gráficos.

---

## 33. Caso especial: carrinho não sai do lugar

Existe um caso importante:

```text
o carrinho não consegue começar a se mover
```

Isso pode acontecer quando a força útil inicial não consegue produzir aceleração positiva suficiente dentro do modelo.

Nesse caso, os históricos podem conter apenas o estado inicial.

Por exemplo:

```text
tempo = 0
posição = 0
velocidade = 0
```

---

## 34. Problema visual com apenas um ponto

O comando:

```python
.plot()
```

é utilizado principalmente para ligar vários pontos.

Se existe apenas um ponto, não existe uma linha para ser desenhada entre dois valores.

Assim, o gráfico pode parecer vazio mesmo que os dados estejam corretos.

---

## 35. Uso de `scatter()` no caso de um ponto

Para resolver esse caso visual, a V10 verifica:

```python
if len(historico_tempo) == 1:
```

`len()` retorna o número de elementos da lista.

Quando existe apenas um valor, são utilizados pontos com:

```python
.scatter()
```

Exemplo:

```python
eixos[0, 0].scatter(
    historico_tempo,
    historico_posicao
)
```

O mesmo tratamento é aplicado aos quatro gráficos.

---

## 36. Teste normal

Um cenário principal utilizado durante o desenvolvimento foi:

```text
diâmetro da roda = 10 cm
diâmetro do eixo = 1 cm
comprimento da corda = 100 cm
comprimento da haste = 15 cm
meta = 10 m
constante torsional = 0,2 N·m/rad
ângulo inicial = 90°
ângulo atual = 90°
massa = 200 g
coeficiente de atrito estático = 0,6
```

Nesse cenário, os gráficos mostram:

- fase impulsionada;
- fase livre;
- aumento e redução da velocidade;
- redução do ângulo da mola;
- posição final abaixo da meta de 10 m.

---

## 37. Teste com meta atingida

Também foi utilizado um cenário semelhante, porém com:

```text
meta = 5 m
```

Nesse caso, a trajetória de posição cruza a linha horizontal da meta.

A V10 consegue marcar:

```text
Meta
```

e:

```text
Meta atingida
```

O instante da meta é obtido da V8.

---

## 38. Teste com corda curta

Outro cenário importante utiliza:

```text
comprimento da corda = 20 cm
```

mantendo os demais valores principais do teste normal.

O comportamento esperado é:

```text
corda termina primeiro
```

enquanto:

```text
ângulo da mola > 0°
```

O gráfico do ângulo permite observar isso diretamente.

Depois do fim da impulsão, a velocidade ainda pode permanecer positiva durante algum tempo.

---

## 39. Teste com massa elevada

Um teste com massa maior mostra como a visualização reage quando o carrinho apresenta dificuldade para se mover.

Com uma massa suficientemente grande:

```text
força útil inicial
<
resistência necessária para iniciar/acelerar o movimento
```

o carrinho pode não sair do lugar dentro do modelo.

Esse cenário é importante para testar o tratamento com:

```python
scatter()
```

---

## 40. Teste com aderência baixa

Um coeficiente de atrito estático muito baixo reduz a força que pode ser transmitida pelas rodas.

A V10 deve representar o resultado produzido pela V5 e pelas versões seguintes sem alterar a física.

Se o carrinho não conseguir sair do lugar, o caso de um único ponto também deve continuar visível.

---

## 41. Teste com mola mais forte

Uma constante torsional maior pode aumentar a força e a energia disponíveis.

Esse teste verifica se os gráficos continuam funcionando quando:

- a velocidade é maior;
- a distância final cresce;
- a meta é atingida mais cedo;
- os valores dos eixos aumentam.

Como os limites dos eixos são escolhidos automaticamente pelo Matplotlib, a figura deve se adaptar aos novos dados.

---

## 42. Teste de limite máximo de tempo

O simulador possui:

```python
tempo_maximo_simulacao = 60.0
```

Se o carrinho ainda estiver em movimento ao atingir esse limite, o resultado pode permanecer inconclusivo.

Os gráficos devem parar no último instante efetivamente simulado.

Isso evita criar dados além do limite definido pelo modelo.

---

## 43. Consistência dos históricos

Para os gráficos funcionarem corretamente, as listas relacionadas ao tempo devem permanecer compatíveis.

Durante a simulação, são atualizados:

```python
historico_tempo
historico_velocidade
historico_aceleracao
historico_angulo
historico_posicao
```

O objetivo é que os valores correspondentes sejam adicionados juntos.

Assim:

```text
tempo[i]
```

corresponde aos valores observados aproximadamente naquele mesmo passo:

```text
velocidade[i]
aceleração[i]
ângulo[i]
posição[i]
```

---

## 44. O que a V10 não altera

A V10 não modifica:

- força da mola;
- torque;
- aceleração calculada;
- aderência;
- resistência ao rolamento;
- posição;
- velocidade;
- resultado da meta;
- diagnósticos da V9.

Ela apenas transforma dados já existentes em representações visuais.

Portanto:

```text
gráfico
≠
novo cálculo físico
```

---

## 45. Limitações da visualização

Os gráficos representam o modelo numérico atual do RatoeiraLab.

Eles não tornam a simulação fisicamente perfeita.

Continuam existindo as limitações das versões anteriores, como:

- ausência de resistência aerodinâmica detalhada;
- ausência de inércia rotacional das rodas;
- patinagem não modelada de forma completa;
- atrito cinético não detalhado;
- distribuição de peso entre os eixos não modelada;
- outras perdas mecânicas não incluídas.

Além disso, as curvas dependem do passo de tempo utilizado na simulação.

---

## 46. Dependência do passo de tempo

O movimento é calculado em passos discretos.

Na versão atual:

```python
passo_tempo = 0.005
```

Isso significa que os históricos são formados por vários estados separados por aproximadamente:

```text
0,005 s
```

Os gráficos conectam esses pontos e formam uma representação contínua visual.

Entretanto, a simulação continua sendo numericamente discreta.

---

## 47. Resultado acumulado até a V10

O fluxo do projeto agora é:

```text
V1 — Geometria e alcance teórico
↓
V2 — Mola, torque e transmissão de força
↓
V3 — Massa e aceleração ideal
↓
V4 — Resistência ao movimento
↓
V5 — Aderência das rodas e limite de tração
↓
V6 — Movimento ao longo do tempo
↓
V7 — Velocidade, posição e distância percorrida
↓
V8 — Verificação da meta
↓
V9 — Análise do design e recomendações
↓
V10 — Gráficos e visualização
```

---

## 48. Fluxo lógico principal da V10

```text
simulação termina
↓
históricos já estão preenchidos
↓
criar figura 2 × 2
↓
posição × tempo
├── linha da meta
└── instante da meta, se existir
↓
velocidade × tempo
└── fim da impulsão
↓
aceleração × tempo
└── fim da impulsão
↓
ângulo × tempo
├── converter radianos para graus
└── fim da impulsão
↓
adicionar grades e legendas
↓
verificar caso de apenas um ponto
├── NÃO → manter linhas
└── SIM → adicionar scatter
↓
ajustar layout
↓
mostrar figura
```

---

## 49. O que a V10 adicionou ao projeto

Com a V10, o RatoeiraLab passa a fornecer uma interpretação visual da simulação.

Agora é possível observar:

- a trajetória da posição;
- o comportamento da velocidade;
- a evolução da aceleração;
- a descarga angular da mola;
- a distância escolhida como meta;
- o instante em que a meta é atingida;
- o fim da fase impulsionada;
- a continuidade do movimento após a impulsão;
- casos em que a corda termina antes da mola;
- casos em que o carrinho não consegue sair do lugar.

---

## 50. Próxima versão

A próxima etapa planejada é:

```text
V11 — Interface final e integração do RatoeiraLab
```

A V11 deverá transformar os cálculos e gráficos já existentes em uma experiência mais amigável para o usuário.

Entre os pontos que podem ser tratados na V11 estão:

```text
entrada de dados mais organizada
↓
explicações para parâmetros difíceis
↓
cálculo assistido da constante torsional
↓
execução da simulação
↓
resultados principais
↓
diagnósticos e recomendações
↓
gráficos
```

Um dos pontos importantes para a interface será evitar exigir que um usuário comum conheça diretamente todos os parâmetros físicos.

Por exemplo, a constante torsional poderá ter uma opção de cálculo assistido a partir de medições.

---

# V10 — Gráficos e visualização dos resultados ✅ CONCLUÍDA

Com a V10, o RatoeiraLab deixa de apresentar apenas números e passa a mostrar visualmente como o carrinho se comporta durante toda a simulação.

A versão agora possui:

- Matplotlib integrado ao projeto;
- quatro gráficos principais;
- organização em uma janela 2×2;
- títulos e unidades;
- grades;
- legendas;
- linha da meta;
- marcação do instante em que a meta é atingida;
- indicação do fim da impulsão;
- conversão visual do ângulo para graus;
- tratamento para simulações com apenas um ponto;
- testes em diferentes cenários.

A física continua sendo calculada pelas versões anteriores.

A função da V10 é tornar esses resultados mais fáceis de interpretar, comparar e apresentar.

Com isso, o projeto está pronto para avançar para a V11, focada na interface final e na integração completa do RatoeiraLab.
