# RatoeiraLab — Modelo V2

## V2 — Ratoeira e mola

A V2 adiciona ao simulador o modelo físico da mola da ratoeira e da transmissão de força até as rodas.

A V1 calcula principalmente o alcance geométrico do carrinho.

A V2 calcula:

- torque produzido pela mola;
- energia armazenada na mola;
- tensão na corda;
- torque transmitido ao eixo;
- força de tração ideal nas rodas.

---

## 1. Entradas utilizadas

### Dados geométricos reaproveitados da V1

- diâmetro da roda, em cm;
- diâmetro do eixo, em cm;
- comprimento da haste, em cm.

### Novas entradas da V2

- constante torsional da mola, em N·m/rad;
- ângulo inicial da mola, em graus;
- ângulo atual da mola, em graus.

Os ângulos fornecidos pelo usuário são convertidos para radianos antes dos cálculos.

---

## 2. Constante torsional da mola

A constante torsional é representada por:

kθ

Sua unidade é:

N·m/rad

Ela representa o quanto a mola resiste à rotação.

Quanto maior a constante torsional, maior será o torque produzido para o mesmo ângulo de torção.

A constante real da ratoeira não será inventada.

Ela deverá ser medida ou calibrada experimentalmente usando o protótipo físico.

---

## 3. Torque da mola

Fórmula:

τ = kθ × θ

Onde:

- τ = torque da mola, em N·m;
- kθ = constante torsional, em N·m/rad;
- θ = ângulo de torção da mola, em radianos.

A V2 calcula:

- torque inicial;
- torque atual.

Conforme a mola relaxa e o ângulo diminui, o torque também diminui.

---

## 4. Energia potencial elástica

Fórmula:

E = 1/2 × kθ × θ²

Onde:

- E = energia armazenada, em joules (J);
- kθ = constante torsional;
- θ = ângulo da mola em radianos.

A V2 calcula:

- energia inicial;
- energia atual;
- energia liberada;
- percentual de energia restante.

A energia liberada é:

energia_liberada = energia_inicial - energia_atual

O percentual restante é:

(energia_atual / energia_inicial) × 100

---

## 5. Tensão na corda

A fórmula geral para o torque produzido por uma força é:

τ = F × L × sen(α)

Onde:

- F = força;
- L = comprimento da haste;
- α = ângulo entre a haste e a direção da força.

### Simplificação da V2

Nesta versão, consideramos:

α = 90°

Como:

sen(90°) = 1

a fórmula é simplificada para:

τ = T × L

Logo:

T = τ / L

Onde:

- T = tensão da corda, em N;
- τ = torque da mola, em N·m;
- L = comprimento da haste, em metros.

A V2 calcula:

- tensão inicial da corda;
- tensão atual da corda.

---

## 6. Torque transmitido ao eixo

A corda é enrolada no eixo das rodas.

Quando a corda é puxada, ela produz torque no eixo.

Fórmula:

τeixo = T × reixo

Onde:

- τeixo = torque transmitido ao eixo, em N·m;
- T = tensão da corda, em N;
- reixo = raio do eixo, em metros.

A V2 calcula:

- torque inicial no eixo;
- torque atual no eixo.

Um eixo de maior raio produz mais torque para a mesma tensão da corda.

Entretanto, conforme demonstrado na V1, um eixo maior também reduz a distância teórica percorrida.

---

## 7. Força de tração

O torque transmitido pelo eixo é convertido em força de tração nas rodas.

Fórmula:

Ftração = τeixo / rroda

Onde:

- Ftração = força de tração ideal, em N;
- τeixo = torque no eixo, em N·m;
- rroda = raio da roda, em metros.

A V2 calcula:

- força de tração inicial;
- força de tração atual.

Para o mesmo torque:

- uma roda menor produz maior força de tração;
- uma roda maior produz menor força de tração.

Por outro lado, rodas maiores aumentam a distância percorrida por rotação.

Isso representa um compromisso entre força e alcance.

---

## 8. Cadeia física da V2

A transmissão modelada pelo programa é:

ângulo da mola
→ torque da mola
→ tensão da corda
→ torque no eixo
→ força de tração

A energia da mola também é calculada separadamente a partir do ângulo.

---

## 9. Simplificações da V2

A V2 considera:

- mola de torção ideal e linear;
- constante torsional constante;
- posição relaxada da mola igual a θ = 0;
- haste rígida;
- corda sem elasticidade;
- corda sem massa;
- corda tangente ao eixo;
- eixo e rodas girando juntos;
- transmissão sem perdas;
- ausência de derrapagem;
- ausência de resistência do ar;
- ausência de atrito;
- ausência de massa e inércia rotacional;
- ângulo entre haste e corda constante em 90°.

Na realidade, o ângulo entre a haste e a direção da corda muda durante o movimento.

Esse efeito será considerado em uma versão futura.

---

## 10. Limitações

A V2 ainda não calcula:

- aceleração;
- velocidade;
- tempo de percurso;
- influência da massa;
- atrito;
- resistência ao rolamento;
- aderência máxima das rodas;
- derrapagem;
- inércia das rodas;
- perdas mecânicas;
- variação real do ângulo entre haste e corda.

Portanto, os resultados representam um modelo físico idealizado.

---

## 11. Teste de validação

Valores utilizados:

- constante torsional: 0,10 N·m/rad;
- ângulo inicial: 60°;
- ângulo atual: 30°;
- comprimento da haste: 25 cm;
- diâmetro do eixo: 1 cm;
- diâmetro da roda: 10 cm.

Resultados aproximados:

- torque inicial: 0,1047 N·m;
- torque atual: 0,0524 N·m;
- energia inicial: 0,0548 J;
- energia atual: 0,0137 J;
- energia liberada: 0,0411 J;
- energia restante: 25%;
- tensão inicial da corda: 0,4189 N;
- tensão atual da corda: 0,2094 N;
- torque inicial no eixo: 0,0021 N·m;
- torque atual no eixo: 0,0010 N·m;
- força de tração inicial: 0,0419 N;
- força de tração atual: 0,0209 N.

Os resultados foram comparados com cálculos manuais e considerados corretos para as simplificações adotadas.

---

## Estado da versão

V2 — Ratoeira e mola: CONCLUÍDA