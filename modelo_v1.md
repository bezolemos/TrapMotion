# Projeto 15 — Simulador do Carrinho Ratoeira

## 1. Objetivo da V1

Calcular a distância teórica que o carrinho pode percorrer considerando apenas:

- o tamanho da roda;
- o tamanho do eixo;
- o comprimento útil da corda.

Nesta versão, ainda não serão considerados massa, atrito, força ou velocidade.

## 2. Variáveis de entrada

- Diâmetro da roda: 20 cm 
- Diâmetro do eixo: 0,5 cm 
- Comprimento útil da corda: 50 cm 
- Comprimento da haste: 30 cm - 0,3m
- Distância da meta: 10 m

Observação: o comprimento da haste será usado nas versões futuras.

## 3. Resultados que serão calculados

- Raio da roda em metros
- Raio do eixo em metros
- Circunferência do eixo
- Número de rotações
- Circunferência da roda
- Distância teórica
- Verificação da meta de 10 metros

## 4. Fórmulas

Raio:

`raio = diâmetro / 2`

Circunferência:

`circunferência = 2 × π × raio`

Número de rotações:

`rotações = comprimento da corda / circunferência do eixo`

Distância teórica:

`distância = número de rotações × circunferência da roda`

## 5. Simplificações

- As rodas não derrapam.
- Não existe atrito.
- A corda não estica.
- Toda a corda consegue ser desenrolada.
- A roda e o eixo giram juntos.
- Não existem perdas de energia.

## 6. Teste manual

Para os cálculos, será utilizado:

`π = 3,1416`

### Conversão das medidas

- Diâmetro da roda: `20 cm ÷ 100 = 0,2 m`
- Raio da roda: `0,2 ÷ 2 = 0,1 m`
- Diâmetro do eixo: `0,5 cm ÷ 100 = 0,005 m`
- Raio do eixo: `0,005 ÷ 2 = 0,0025 m`
- Comprimento útil da corda: `50 cm ÷ 100 = 0,5 m`
- Comprimento da haste: `30 cm ÷ 100 = 0,3 m`
- Distância-meta: `10 m`

### 1. Raio da roda

`raio da roda = diâmetro da roda ÷ 2`

`raio da roda = 0,2 ÷ 2`

`raio da roda = 0,1 m`

### 2. Raio do eixo

`raio do eixo = diâmetro do eixo ÷ 2`

`raio do eixo = 0,005 ÷ 2`

`raio do eixo = 0,0025 m`

### 3. Circunferência do eixo

`circunferência do eixo = 2 × π × raio do eixo`

`circunferência do eixo = 2 × 3,1416 × 0,0025`

`circunferência do eixo = 0,015708 m`

### 4. Número de rotações

`rotações = comprimento útil da corda ÷ circunferência do eixo`

`rotações = 0,5 ÷ 0,015708`

`rotações ≈ 31,83 voltas`

### 5. Circunferência da roda

`circunferência da roda = 2 × π × raio da roda`

`circunferência da roda = 2 × 3,1416 × 0,1`

`circunferência da roda = 0,62832 m`

### 6. Distância teórica

`distância teórica = número de rotações × circunferência da roda`

`distância teórica = 31,83 × 0,62832`

`distância teórica ≈ 20 m`

### 7. Diagnóstico

✅ A geometria permite alcançar a meta de 10 metros.

A distância máxima teórica é de aproximadamente 20 metros, o dobro da meta. Entretanto, esse resultado ainda não considera atrito, massa, derrapagem ou perdas de energia. Portanto, não significa que o carrinho real percorrerá exatamente 20 metros.