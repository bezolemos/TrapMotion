# TrapMotion

O **TrapMotion** é um simulador em Python desenvolvido para analisar o funcionamento de um carrinho movido por ratoeira.

O projeto utiliza conceitos de física, matemática e programação para estimar como diferentes parâmetros do carrinho influenciam seu desempenho, como diâmetro das rodas, diâmetro do eixo, comprimento da corda, comprimento da haste, massa total e características da mola.

## Funcionalidades

- Cálculo da geometria e do alcance teórico
- Análise da mola, torque e energia
- Cálculo de força e aceleração
- Resistência ao rolamento
- Limite de aderência das rodas
- Simulação do movimento ao longo do tempo
- Verificação da distância-meta
- Diagnósticos e recomendações para o projeto
- Gráficos de:
  - posição
  - velocidade
  - aceleração
  - ângulo da mola
- Interface gráfica desenvolvida com Tkinter

## Estrutura do projeto

```text
TrapMotion/
├── simulador.py
├── interface_v11.py
├── simulacao.py
├── README.md
└── README_PT-BR.md
```

- `simulador.py` — arquivo principal usado para iniciar o programa.
- `interface_v11.py` — contém a interface gráfica e a visualização dos resultados.
- `simulacao.py` — contém os cálculos físicos e a lógica da simulação.

## Requisitos

- Python 3.x
- Matplotlib

Para instalar o Matplotlib:

```bash
py -m pip install matplotlib
```

## Como executar

Abra a pasta do projeto no VS Code ou em um terminal e execute:

```bash
py simulador.py
```

A interface gráfica será aberta.

Depois, basta preencher os dados do carrinho e clicar em **SIMULAR CARRINHO** para visualizar os resultados, diagnósticos, recomendações e gráficos.

## Objetivo do projeto

O objetivo do TrapMotion é funcionar como uma ferramenta de apoio ao desenvolvimento de carrinhos movidos por ratoeira, permitindo testar diferentes configurações antes da construção física do carrinho.

Além de calcular resultados, o programa busca ajudar a entender **por que** determinadas escolhas de projeto melhoram ou limitam o desempenho do carrinho.

## Limitações do modelo

O TrapMotion utiliza um modelo físico simplificado.

A simulação considera resistência ao rolamento e limite de aderência, mas não representa detalhadamente todos os efeitos presentes em um carrinho real, como:

- resistência do ar
- inércia rotacional das rodas
- distribuição de peso entre os eixos
- atrito cinético detalhado
- derrapagem real das rodas
- outras perdas mecânicas

Por isso, os resultados devem ser utilizados como estimativas para auxiliar no projeto.

## Status

✅ **Versão final — Projeto 15**
