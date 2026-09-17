# RatoeiraLab — Modelo V3

## V3 — Massa e aceleração ideal

A V3 adiciona ao simulador a massa total do carrinho e o cálculo de sua aceleração ideal.

A V2 calcula a força de tração produzida nas rodas.

A V3 utiliza essa força para calcular:

- aceleração ideal inicial;
- aceleração ideal no estado atual.

Nesta versão, ainda não são calculados automaticamente:

- velocidade;
- tempo;
- posição;
- distância real percorrida.

---

## 1. Entradas utilizadas

### Dados reaproveitados da V2

A V3 utiliza dois resultados produzidos pela função `calcular_mola()`:

- força de tração inicial, em newtons;
- força de tração atual, em newtons.

Essas forças representam a força ideal transmitida pela mola até as rodas do carrinho.

### Nova entrada da V3

A nova entrada é:

- massa total do carrinho, em gramas.

A massa total deve incluir todos os componentes do carrinho:

- estrutura;
- ratoeira;
- haste;
- corda;
- rodas;
- eixos;
- peças de fixação;
- demais componentes instalados.

A massa é informada em gramas para facilitar a utilização do programa, pois carrinhos desse tipo normalmente possuem massas relativamente pequenas.

Antes dos cálculos, a massa é convertida para quilogramas.

---

## 2. Massa

A massa representa a quantidade de matéria de um objeto e sua resistência a mudanças de movimento.

Essa resistência é chamada de inércia.

Quanto maior a massa do carrinho, maior será sua resistência à aceleração.

A unidade de massa utilizada pelo Sistema Internacional é o quilograma:

kg

A massa não deve ser confundida com o peso.

A massa é medida em quilogramas, enquanto o peso é uma força medida em newtons.

O peso poderia ser calculado por:

P = m × g

Onde:

- P = peso, em N;
- m = massa, em kg;
- g = aceleração da gravidade, aproximadamente 9,81 m/s².

A V3 não utiliza o peso diretamente, pois considera o movimento do carrinho sobre uma superfície horizontal ideal.

---

## 3. Conversão da massa

Como a massa é informada em gramas, ela precisa ser convertida para quilogramas.

Fórmula:

massa_kg = massa_g / 1000

Onde:

- massa_kg = massa do carrinho em quilogramas;
- massa_g = massa do carrinho em gramas.

Exemplo:

300 g / 1000 = 0,300 kg

Essa conversão é obrigatória porque a unidade do newton utiliza quilogramas:

1 N = 1 kg·m/s²

Se o programa utilizasse diretamente o valor 300 na fórmula, ele interpretaria a massa como 300 kg, e não como 300 g.

---

## 4. Segunda Lei de Newton

A relação entre força, massa e aceleração é descrita pela Segunda Lei de Newton.

Fórmula geral:

F = m × a

Onde:

- F = força resultante, em newtons;
- m = massa, em quilogramas;
- a = aceleração, em metros por segundo ao quadrado.

Para calcular a aceleração, a fórmula é reorganizada:

a = F / m

Nesta versão, a força de tração calculada na V2 é considerada igual à força resultante horizontal.

Assim:

Fresultante = Ftração

Logo:

aideal = Ftração / m

Essa é uma simplificação, pois um carrinho real também sofre forças contrárias ao movimento.

---

## 5. Aceleração

A aceleração representa o quanto a velocidade de um objeto muda durante determinado intervalo de tempo.

Sua unidade é:

m/s²

Uma aceleração de 2 m/s² significa que, enquanto essa aceleração permanecer constante, a velocidade aumenta 2 m/s a cada segundo.

Entretanto, a V3 não calcula a velocidade.

Ela calcula somente a aceleração ideal correspondente à força produzida pela mola em dois estados diferentes.

---

## 6. Aceleração ideal inicial

A aceleração ideal inicial utiliza a força de tração inicial calculada na V2.

Fórmula:

ainicial = Ftração_inicial / m

Onde:

- ainicial = aceleração ideal inicial, em m/s²;
- Ftração_inicial = força de tração inicial, em N;
- m = massa total do carrinho, em kg.

Essa aceleração representa o estado inicial informado para a mola.

Nesse estado, a mola normalmente possui maior ângulo de torção e produz maior força de tração.

---

## 7. Aceleração ideal atual

A aceleração ideal atual utiliza a força de tração correspondente ao ângulo atual da mola.

Fórmula:

aatual = Ftração_atual / m

Onde:

- aatual = aceleração ideal atual, em m/s²;
- Ftração_atual = força de tração atual, em N;
- m = massa total do carrinho, em kg.

Conforme a mola relaxa, seu ângulo diminui.

No modelo atual, isso reduz:

- o torque da mola;
- a tensão na corda;
- o torque transmitido ao eixo;
- a força de tração;
- a aceleração ideal.

---

## 8. Influência da massa

Para a mesma força de tração:

- aumentar a massa reduz a aceleração;
- diminuir a massa aumenta a aceleração.

Exemplo:

Se uma força de 0,60 N atuar sobre uma massa de 0,300 kg:

a = 0,60 / 0,300

a = 2 m/s²

Se a massa for aumentada para 0,600 kg:

a = 0,60 / 0,600

a = 1 m/s²

Nesse exemplo, a massa foi duplicada e a aceleração caiu pela metade.

Isso não significa que o carrinho mais leve será sempre melhor.

No mundo real, uma massa muito baixa pode afetar:

- aderência das rodas;
- estabilidade;
- derrapagem;
- distribuição de peso;
- contato das rodas com o chão.

Esses efeitos ainda não são considerados na V3.

---

## 9. Interpretação da aceleração

O programa compara a aceleração atual com a aceleração inicial.

### Aceleração atual menor que a inicial

Se:

aatual < ainicial

isso significa que a força de tração produzida pela mola diminuiu.

O carrinho ainda pode estar aumentando sua velocidade, mas com menor aceleração.

Uma aceleração menor não significa necessariamente que o carrinho está desacelerando.

### Aceleração atual igual à inicial

Se:

aatual = ainicial

a força de tração permaneceu igual nos dois estados analisados.

Isso normalmente acontece quando o ângulo atual informado é igual ao ângulo inicial.

### Aceleração atual igual a zero

Se:

aatual = 0

a mola não produz mais força de tração no estado analisado.

No modelo ideal, se o carrinho já estiver em movimento, ele poderá continuar com velocidade constante.

No mundo real, o atrito e outras resistências fariam sua velocidade diminuir gradualmente.

Se o carrinho estiver parado e sua aceleração for zero, ele continuará parado.

### Aceleração atual maior que a inicial

Esse resultado não é esperado no modelo atual porque o programa não permite que o ângulo atual seja maior que o ângulo inicial.

Mesmo assim, essa situação é tratada pelo programa como uma proteção adicional.

---

## 10. Cadeia física da V3

A transmissão modelada até esta versão é:

ângulo da mola

→ torque da mola

→ tensão da corda

→ torque no eixo

→ força de tração

→ aceleração ideal do carrinho

A massa participa da última etapa:

aceleração ideal = força de tração / massa

Assim, a V3 conecta o modelo da mola ao movimento translacional ideal do carrinho.

---

## 11. Validação da massa

A massa total do carrinho deve ser maior que zero.

Condição:

massa_total_carrinho_g > 0

Uma massa igual a zero não pode ser utilizada porque causaria uma divisão por zero:

a = F / 0

Uma massa negativa também não possui significado físico para este projeto.

Quando o usuário informa uma massa igual ou menor que zero, o programa mostra uma mensagem de erro e encerra a execução.

---

## 12. Simplificações da V3

A V3 considera:

- movimento em uma superfície plana e horizontal;
- massa total constante durante o movimento;
- força de tração igual à força resultante horizontal;
- toda a força de tração direcionada para a frente;
- ausência de atrito;
- ausência de resistência ao rolamento;
- ausência de resistência do ar;
- ausência de derrapagem;
- ausência de perdas mecânicas;
- ausência de inércia rotacional;
- rodas e eixos girando juntos;
- estrutura perfeitamente rígida;
- massa tratada como um único conjunto;
- aceleração calculada separadamente para cada estado da mola.

A aceleração calculada é idealizada.

Ela não representa exatamente a aceleração que seria medida em um protótipo físico.

---

## 13. Limitações

A V3 ainda não calcula:

- força resultante real;
- atrito nos eixos;
- resistência ao rolamento;
- resistência do ar;
- aderência máxima das rodas;
- derrapagem;
- inércia rotacional das rodas;
- inércia rotacional dos eixos;
- distribuição da massa;
- posição do centro de massa;
- inclinação do chão;
- perdas na transmissão;
- velocidade;
- tempo de percurso;
- posição;
- distância real percorrida;
- variação contínua da aceleração;
- geometria variável entre haste e corda.

A V3 calcula apenas dois estados:

- estado inicial da mola;
- estado atual informado pelo usuário.

Ela ainda não simula todo o movimento do carrinho ao longo do tempo.

---

## 14. Teste de validação principal

Valores utilizados:

- diâmetro da roda: 10 cm;
- diâmetro do eixo: 1 cm;
- comprimento da corda: 100 cm;
- comprimento da haste: 20 cm;
- distância da meta: 10 m;
- constante torsional: 0,20 N·m/rad;
- ângulo inicial: 90°;
- ângulo atual: 45°;
- massa total: 300 g.

Resultados da V2 utilizados pela V3:

- força de tração inicial: aproximadamente 0,1571 N;
- força de tração atual: aproximadamente 0,0785 N.

Conversão da massa:

300 g / 1000 = 0,300 kg

Aceleração ideal inicial:

ainicial = 0,1571 / 0,300

ainicial ≈ 0,5236 m/s²

Aceleração ideal atual:

aatual = 0,0785 / 0,300

aatual ≈ 0,2618 m/s²

Resultados apresentados pelo programa:

- massa total: 0,300 kg;
- aceleração ideal inicial: 0,5236 m/s²;
- aceleração ideal atual: 0,2618 m/s².

Os resultados foram comparados com os cálculos manuais e considerados corretos para as simplificações adotadas.

---

## 15. Testes adicionais

### Teste com massa duplicada

A massa foi alterada de 300 g para 600 g, mantendo as demais entradas iguais.

Resultados:

- aceleração ideal inicial: aproximadamente 0,2618 m/s²;
- aceleração ideal atual: aproximadamente 0,1309 m/s².

Ao duplicar a massa, as acelerações foram reduzidas pela metade.

### Teste com ângulo atual igual a zero

O ângulo atual foi definido como 0°.

Resultado:

- aceleração ideal atual: 0 m/s².

A interpretação específica para aceleração zero foi executada corretamente.

### Teste com ângulo atual igual ao inicial

Os ângulos inicial e atual foram definidos como 90°.

Resultados:

- aceleração ideal inicial: aproximadamente 0,5236 m/s²;
- aceleração ideal atual: aproximadamente 0,5236 m/s².

As acelerações foram iguais porque as forças de tração também eram iguais.

### Teste com massa inválida

A massa total foi definida como 0 g.

Resultado:

- o programa mostrou uma mensagem de validação;
- a execução foi encerrada antes da divisão;
- não ocorreu divisão por zero.

---

## 16. Alterações implementadas na V3

Foi criada a função:

`calcular_aceleracao_ideal()`

Ela recebe:

- massa total do carrinho em gramas;
- força de tração inicial;
- força de tração atual.

Ela devolve um dicionário contendo:

- massa total em gramas;
- massa total em quilogramas;
- aceleração ideal inicial;
- aceleração ideal atual.

A função utiliza os resultados produzidos pela V2 sem modificar os cálculos anteriores.

Também foi adicionada uma interpretação automática para explicar o comportamento da aceleração.

---

## 17. Conclusão

A V3 conecta a força de tração calculada na V2 ao movimento ideal do carrinho.

Agora o RatoeiraLab consegue demonstrar que:

- a força da mola influencia diretamente a aceleração;
- a aceleração diminui conforme a força da mola diminui;
- uma massa maior reduz a aceleração para a mesma força;
- uma massa menor aumenta a aceleração para a mesma força;
- aceleração zero não significa obrigatoriamente que o carrinho está parado.

Os resultados ainda são idealizados, mas a V3 acrescenta ao simulador uma relação fundamental entre a construção física do carrinho e seu comportamento esperado.

---

## Estado da versão

V3 — Massa e aceleração ideal: CONCLUÍDA