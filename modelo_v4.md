# RatoeiraLab — Modelo V4

## V4 — Resistência ao movimento e força resultante

A V4 adiciona ao simulador a primeira resistência física contrária ao movimento do carrinho: a resistência ao rolamento.

Até a V3, o modelo considerava que toda a força de tração produzida pela ratoeira era utilizada diretamente para acelerar o carrinho.

Isso significava que:

Fresultante = Ftração

Essa aproximação era útil para calcular uma aceleração ideal, mas não representa completamente o comportamento de um carrinho real.

Na V4, parte da força de tração passa a ser utilizada para vencer a resistência ao rolamento.

O modelo passa a utilizar:

Fresultante = Ftração - Frr

onde Frr representa a força de resistência ao rolamento.

A V4 calcula:

- força peso;
- força normal;
- resistência ao rolamento;
- força resultante inicial;
- força resultante atual;
- aceleração inicial considerando resistência;
- aceleração atual considerando resistência.

A versão também interpreta situações em que:

- a tração supera a resistência;
- a tração é igual à resistência;
- a resistência supera a tração.

---

## 1. Dados utilizados

### Dados reaproveitados das versões anteriores

A V4 utiliza resultados que já eram calculados anteriormente.

Da V2:

- força de tração inicial;
- força de tração atual.

Da V3:

- massa total do carrinho.

### Nova variável da V4

A nova variável utilizada é:

- coeficiente de resistência ao rolamento.

No programa:

`coeficiente_resistencia_rolamento`

Esse coeficiente é representado fisicamente por:

Crr

O Crr é adimensional, ou seja, não possui unidade.

Durante o desenvolvimento da V4 foi utilizado:

Crr = 0,02

apenas como valor de exemplo para os testes.

Esse número não deve ser interpretado como o coeficiente real de qualquer carrinho específico.

O valor real depende de fatores como:

- material das rodas;
- superfície do chão;
- deformação das rodas;
- qualidade dos eixos;
- montagem do carrinho.

Em versões futuras, o programa poderá utilizar valores estimados de acordo com os materiais ou permitir calibração experimental.

---

## 2. Gravidade

A V4 utiliza a aceleração gravitacional aproximada:

g = 9,81 m/s²

No programa:

`gravidade = 9.81`

A gravidade não é tratada como uma escolha de projeto do usuário.

Ela é utilizada para calcular a força peso do carrinho.

---

## 3. Conversão da massa

A massa continua sendo informada pelo usuário em gramas.

Antes dos cálculos físicos, ela é convertida para quilogramas:

massa_kg = massa_g / 1000

Isso é necessário porque as fórmulas utilizadas trabalham com unidades do Sistema Internacional.

Exemplo:

300 g = 0,300 kg

---

## 4. Força peso

A força peso representa a força gravitacional exercida sobre o carrinho.

A fórmula utilizada é:

P = m × g

Onde:

- P = força peso, em newtons;
- m = massa do carrinho, em quilogramas;
- g = aceleração da gravidade, em m/s².

Exemplo para um carrinho de 0,300 kg:

P = 0,300 × 9,81

P = 2,943 N

Portanto, a força peso é aproximadamente:

2,943 N

---

## 5. Força normal

A força normal representa a força que a superfície exerce sobre o carrinho.

Nesta versão, o programa considera:

- superfície plana;
- superfície horizontal;
- ausência de outras forças verticais relevantes.

Nessas condições:

N = P

Como:

P = m × g

também podemos escrever:

N = m × g

No exemplo de 300 g:

N = 2,943 N

É importante observar que peso e força normal possuem o mesmo valor neste modelo, mas representam forças diferentes.

A força peso atua verticalmente para baixo.

A força normal atua verticalmente para cima.

---

## 6. Resistência ao rolamento

Mesmo quando as rodas giram sem deslizar, existe uma resistência contrária ao movimento.

Essa resistência pode surgir devido a fatores como:

- deformação das rodas;
- deformação da superfície;
- perdas nos eixos;
- perdas nos materiais;
- pequenas imperfeições mecânicas.

A V4 representa essas perdas utilizando uma aproximação por resistência ao rolamento.

A fórmula utilizada é:

Frr = Crr × N

Onde:

- Frr = força de resistência ao rolamento, em newtons;
- Crr = coeficiente de resistência ao rolamento;
- N = força normal, em newtons.

### Exemplo

Utilizando:

Crr = 0,02

N = 2,943 N

Temos:

Frr = 0,02 × 2,943

Frr = 0,05886 N

Portanto:

Frr ≈ 0,0589 N

Essa força atua no sentido contrário ao movimento considerado.

---

## 7. Diferença entre resistência ao rolamento e atrito

A resistência ao rolamento não deve ser confundida com outras formas de atrito.

### Atrito de deslizamento

O atrito de deslizamento ocorre quando duas superfícies escorregam uma sobre a outra.

Um exemplo seria uma roda travada sendo arrastada pelo chão.

Esse fenômeno não é modelado na V4.

### Atrito estático

O atrito estático é necessário para que a roda consiga transmitir força ao chão sem derrapar.

Ele permite que a roda empurre o chão e produza tração.

Entretanto, o limite de aderência das rodas ainda não é calculado na V4.

Esse fenômeno será tratado posteriormente em:

V5 — Aderência das rodas e limite de tração.

### Resistência ao rolamento

A resistência ao rolamento pode existir mesmo quando a roda está girando normalmente e sem derrapar.

É essa resistência que a V4 considera.

---

## 8. Força resultante

Na V3, o modelo utilizava:

Fresultante = Ftração

Na V4, a resistência ao rolamento é subtraída da força de tração:

Fresultante = Ftração - Frr

Como o programa possui uma força de tração inicial e uma força de tração atual, são calculadas duas forças resultantes.

### Força resultante inicial

Fresultante_inicial =
Ftração_inicial - Frr

### Força resultante atual

Fresultante_atual =
Ftração_atual - Frr

Essas forças representam quanto da força de tração permanece disponível depois de considerar a resistência ao rolamento.

---

## 9. Exemplo de força resultante

Utilizando aproximadamente:

Ftração_inicial = 0,1571 N

Ftração_atual = 0,0785 N

Frr = 0,05886 N

### Estado inicial

Fresultante_inicial =
0,1571 - 0,05886

Fresultante_inicial ≈ 0,09824 N

### Estado atual

Fresultante_atual =
0,0785 - 0,05886

Fresultante_atual ≈ 0,01964 N

Nos dois casos, a força resultante permanece positiva.

Isso significa que, nesses estados, a força de tração ainda supera a resistência ao rolamento.

---

## 10. Aceleração considerando resistência

A V4 continua utilizando a Segunda Lei de Newton:

F = m × a

Isolando a aceleração:

a = F / m

Entretanto, em vez da força de tração ideal, agora é utilizada a força resultante.

### Aceleração inicial

aceleração_resistência_inicial =
Fresultante_inicial / m

### Aceleração atual

aceleração_resistência_atual =
Fresultante_atual / m

---

## 11. Exemplo de aceleração com resistência

Utilizando:

m = 0,300 kg

Fresultante_inicial ≈ 0,09824 N

Fresultante_atual ≈ 0,01964 N

### Aceleração inicial

a = 0,09824 / 0,300

a ≈ 0,3275 m/s²

### Aceleração atual

a = 0,01964 / 0,300

a ≈ 0,0655 m/s²

Portanto:

aceleração inicial com resistência ≈ 0,3275 m/s²

aceleração atual com resistência ≈ 0,0655 m/s²

---

## 12. Comparação com a V3

Na V3, para os mesmos parâmetros, os valores ideais eram aproximadamente:

aceleração ideal inicial ≈ 0,5236 m/s²

aceleração ideal atual ≈ 0,2618 m/s²

Na V4:

aceleração inicial com resistência ≈ 0,3275 m/s²

aceleração atual com resistência ≈ 0,0655 m/s²

A redução ocorre porque parte da força de tração precisa vencer a resistência ao rolamento.

A V3 representa um cenário idealizado sem resistência.

A V4 acrescenta a primeira perda mecânica ao modelo.

A análise percentual dessa redução não faz parte da V4.

Esse tipo de análise ficará reservado para:

V9 — Análise do design e recomendações de ajustes.

---

## 13. Interpretação da força resultante

A V4 analisa separadamente a força resultante inicial e a força resultante atual.

Existem três situações principais.

### Caso 1 — Força resultante positiva

Se:

Fresultante > 0

então:

Ftração > Frr

Isso significa que a força de tração supera a resistência ao rolamento.

Existe aceleração resultante no sentido considerado positivo do movimento.

---

### Caso 2 — Força resultante aproximadamente igual a zero

Se:

Fresultante ≈ 0

então a força de tração e a resistência ao rolamento estão aproximadamente equilibradas.

Nesse caso:

a ≈ 0

Isso não significa necessariamente que o carrinho esteja parado.

Se ele já estiver em movimento, aceleração aproximadamente igual a zero indica que sua velocidade não está sendo alterada significativamente naquele instante pelo modelo.

Como números do tipo `float` podem apresentar pequenas imprecisões computacionais, o programa utiliza `math.isclose()` para verificar se a força resultante está suficientemente próxima de zero.

---

### Caso 3 — Força resultante negativa

Se:

Fresultante < 0

então:

Frr > Ftração

Isso significa que a resistência ao rolamento supera a força de tração naquele estado.

Uma força resultante negativa não significa automaticamente que o carrinho esteja andando para trás.

Se ele estiver se movendo para frente, esse resultado representa tendência à desaceleração.

A V4 ainda não calcula velocidade e, portanto, não determina:

- o instante em que o carrinho para;
- a distância percorrida até parar;
- uma possível mudança de sentido.

Esses aspectos dependem das versões futuras de movimento.

---

## 14. Função adicionada na V4

Foi criada a função:

`calcular_resistencia_movimento()`

Ela recebe:

- massa total do carrinho em gramas;
- coeficiente de resistência ao rolamento;
- força de tração inicial;
- força de tração atual.

Ela calcula:

- massa em quilogramas;
- força peso;
- força normal;
- força de resistência ao rolamento;
- força resultante inicial;
- força resultante atual;
- aceleração inicial considerando resistência;
- aceleração atual considerando resistência.

---

## 15. Resultados apresentados pela V4

A V4 exibe:

- coeficiente de resistência ao rolamento;
- força peso;
- força normal;
- resistência ao rolamento;
- força resultante inicial;
- força resultante atual;
- aceleração inicial com resistência;
- aceleração atual com resistência.

Esses resultados permitem comparar diretamente a aceleração ideal da V3 com a aceleração obtida após considerar a resistência ao rolamento.

---

## 16. Validação do coeficiente de resistência

O programa verifica se:

Crr >= 0

Valores negativos não são aceitos.

Se:

Crr < 0

o programa encerra a execução e informa que o coeficiente de resistência ao rolamento não pode ser negativo.

O valor:

Crr = 0

é permitido.

Esse caso representa um modelo sem resistência ao rolamento e é útil para verificar a consistência entre a V3 e a V4.

---

## 17. Teste com Crr igual a zero

Quando:

Crr = 0

temos:

Frr = 0

Portanto:

Fresultante = Ftração

Consequentemente:

aceleração da V4 = aceleração ideal da V3

Esse teste confirmou que a V4 é consistente com o modelo anterior quando a nova resistência é removida.

---

## 18. Teste com Crr igual a 0,02

Foram utilizados aproximadamente:

- massa: 300 g;
- gravidade: 9,81 m/s²;
- Crr: 0,02;
- força de tração inicial: 0,1571 N;
- força de tração atual: 0,0785 N.

Resultados principais:

- força peso: 2,943 N;
- força normal: 2,943 N;
- resistência ao rolamento: 0,05886 N;
- força resultante inicial: aproximadamente 0,09824 N;
- força resultante atual: aproximadamente 0,01964 N;
- aceleração inicial com resistência: aproximadamente 0,3275 m/s²;
- aceleração atual com resistência: aproximadamente 0,0655 m/s².

Os resultados foram considerados coerentes com as fórmulas utilizadas.

---

## 19. Teste com resistência superior à tração atual

Também foi testada uma situação em que a resistência ao rolamento supera a força de tração atual.

Nesse caso:

Fresultante_atual < 0

O programa informa que a resistência supera a tração naquele estado.

Também informa que, se o carrinho estiver se movimentando para frente, isso representa tendência à desaceleração.

O programa não afirma que o carrinho se move para trás.

---

## 20. Teste com resistência superior à tração inicial

Também foi considerado um caso em que:

Frr > Ftração_inicial

Nesse cenário, a força resultante inicial fica negativa.

O resultado indica que, dentro das simplificações da V4, a resistência considerada supera a força de tração inicial.

A V4 não transforma esse resultado em uma simulação completa de partida, pois ainda não acompanha velocidade nem posição.

---

## 21. Distância teórica e distância realmente percorrida

Uma correção conceitual importante foi mantida na V4.

A função de geometria calcula:

distância teórica

Esse resultado representa o alcance geométrico produzido pela relação entre:

- comprimento da corda;
- diâmetro da roda;
- diâmetro do eixo.

Ele não representa ainda a distância real percorrida pelo carrinho.

Por isso, o programa deve interpretar o resultado como:

“a geometria possui alcance teórico suficiente para a meta”

e não como:

“o carrinho certamente alcançou a meta”.

Determinar a distância realmente percorrida exigirá acompanhar o movimento do carrinho ao longo do tempo.

---

## 22. Simplificações mantidas na V4

A V4 ainda considera:

- mola de torção linear;
- constante torsional constante;
- haste rígida;
- corda sem massa;
- corda sem elasticidade;
- corda tangente ao eixo;
- eixo e rodas girando juntos;
- ângulo entre haste e corda constante em 90°;
- superfície plana;
- superfície horizontal;
- massa constante;
- gravidade constante;
- resistência ao rolamento representada por um único coeficiente constante;
- ausência de resistência do ar;
- ausência de derrapagem;
- ausência de limite de aderência;
- ausência de inércia rotacional;
- ausência de perdas adicionais nos componentes;
- ausência de cálculo temporal;
- ausência de velocidade;
- ausência de posição;
- ausência de integração numérica.

---

## 23. Limitações do coeficiente Crr

O coeficiente de resistência ao rolamento utilizado na V4 é uma aproximação.

O programa ainda não calcula automaticamente esse coeficiente a partir dos materiais do carrinho.

Portanto, valores utilizados em simulações devem ser tratados como estimativas.

No futuro, o RatoeiraLab poderá:

- sugerir valores aproximados com base nos materiais;
- permitir seleção de tipos de superfície;
- permitir seleção de tipos de roda;
- permitir que usuários avançados informem um valor manual;
- utilizar testes físicos para calibrar o modelo.

---

## 24. O que a V4 não pretende determinar

A V4 ainda não consegue responder diretamente:

- qual será a velocidade do carrinho;
- quanto tempo ele levará para percorrer determinada distância;
- em qual posição ele estará em determinado instante;
- exatamente quando o carrinho irá parar;
- a distância real final percorrida;
- se haverá derrapagem das rodas;
- se a tração disponível ultrapassa o limite de aderência;
- se o carrinho realmente alcançará os 10 metros.

Essas respostas dependem das próximas etapas do projeto.

---

## 25. Resultado da V4

Com a V4, o RatoeiraLab deixa de considerar que toda a força produzida pela ratoeira está disponível para acelerar o carrinho.

Agora o modelo possui a sequência:

massa
→ força peso
→ força normal
→ resistência ao rolamento
→ força resultante
→ aceleração considerando resistência

Isso torna o modelo mais realista que a V3 sem introduzir ainda uma simulação temporal completa.

A V4 prepara o projeto para a próxima etapa:

V5 — Aderência das rodas e limite de tração.

Nessa versão será analisado se a força transmitida às rodas pode realmente ser aplicada ao chão sem provocar perda de aderência ou derrapagem.