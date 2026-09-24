# DOE aplicado ao modelo de déficit hídrico

Uma linha de investigação proposta é aplicar Design of Experiments diretamente ao modelo de déficit hídrico, sem depender do modelo de otimização.

Isso reforça a necessidade de manter o núcleo agronômico independente, parametrizado e validado.

## Hipótese de arquitetura experimental

O núcleo permanece fixo:

[
CAD, CRA, D, K_s
]

e os fatores experimentais alteram apenas parâmetros ou métodos de entrada.

Um fator metodológico particularmente relevante é:

[
	ext{método de parametrização do limiar}
]

com níveis candidatos:

[
	ext{FAO-56}
]

e:

[
	ext{SBMI}.
]

Mantendo todas as demais entradas constantes, esse fator permite medir diretamente o efeito de:

[
p_{FAO56}
quad	ext{versus}quad
F_{SBMI}.
]

Outros fatores candidatos, ainda não congelados, incluem parâmetros de solo, profundidade radicular, demanda evaporativa, coeficiente de cultura, precipitação e estado hídrico inicial.

Possíveis respostas, também ainda não congeladas, incluem:

- depleção máxima;
- tempo acima do limiar CRA;
- evapotranspiração real acumulada;
- diferença acumulada entre ETc e ETr;
- frequência e duração de condições de estresse;
- sensibilidade da trajetória de D às diferentes parametrizações.

A definição formal do delineamento, fatores, níveis, replicações e respostas será realizada posteriormente. Este arquivo apenas registra que o modelo de déficit deve ser construído de modo compatível com essa linha de DOE.
