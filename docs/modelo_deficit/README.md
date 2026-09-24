# Modelo de déficit hídrico

Este diretório documenta o núcleo agronômico do projeto. Ele deve permanecer independente do modelo de otimização, do estudo de caso e do DOE específico que vier a ser definido.

## Arquitetura definida

O projeto adota um único núcleo:

[
oxed{CAD, CRA, D, K_s}
]

A intenção é evitar a existência de um "modelo FAO" e de um "modelo SBMI" duplicando as mesmas equações de reservatório.

O núcleo contém:

[
CAD=(	heta_{CC}-	heta_{PMP})Zcdot10
]

com (Z) em cm, e:

[
CRA=f_{dep},CAD
]

onde (f_{dep}) é uma fração de depleção fornecida pela parametrização escolhida.

A variável de estado é:

[
0leq Dleq CAD
]

e a lei de estresse adotada na V1 é:

[
K_s=
egin{cases}
1, & Dleq CRA\
dfrac{CAD-D}{CAD-CRA}, & D>CRA
end{cases}
]

A evapotranspiração potencial da cultura é:

[
ET_c=ET_oK_c
]

e a evapotranspiração efetiva utilizada no balanço é:

[
ET_r=ET_oK_cK_s.
]

O balanço genérico é:

[
D^*=D+ET_r-P_e-IRN-CR+DP
]

seguido da limitação física de (D) ao intervalo ([0,CAD]). O código expõe separadamente excesso de água acima da capacidade de campo e eventual extrapolação além de CAD para que o truncamento numérico não fique oculto.

## Parametrizações

O núcleo não determina sozinho o valor de (f_{dep}).

### FAO-56

Na parametrização FAO-56:

[
f_{dep}=p_{FAO56}
]

e:

[
CRA=p_{FAO56},CAD.
]

Quando aplicável, o ajuste de (p) em função de (ET_c) é realizado fora do núcleo.

### SBMI

Na parametrização SBMI adotada nesta pesquisa:

[
f_{dep}=F_{SBMI}
]

e:

[
CRA=F_{SBMI},CAD.
]

O valor de (F) é obtido pela tabela de grupo de cultura em função de (ETc_{max}), com interpolação linear entre os pontos tabulados.

## Comparação controlada

Na comparação inicial FAO-56 x SBMI, todas as demais equações permanecem iguais e somente a forma de obter (CRA) é alterada.

Assim, a pergunta experimental pode ser escrita como:

[
oxed{
	ext{quanto do resultado decorre apenas de }
p_{FAO56}
	ext{ versus }
F_{SBMI}?
}
]

Essa é uma escolha metodológica do projeto. Não significa afirmar que o SBMI possua apenas uma formulação possível de (K_s). O objetivo da V1 é deliberadamente fixar a lei de estresse para isolar o efeito da parametrização do limiar.

## Validação

Os Golden Cases permanecem sendo os exemplos publicados da FAO-56.

Nos testes:

[
TAWightarrow CAD,qquad
RAWightarrow CRA,qquad
D_rightarrow D.
]

A equivalência é usada somente como tradução de nomenclatura; os valores publicados continuam sendo a referência de validação.

## Princípio de implementação

Parâmetros de cultura, solo, clima, localização e equipamento não devem ser codificados como constantes estruturais do núcleo.

O mesmo núcleo deverá aceitar diferentes culturas, solos, profundidades radiculares, séries climáticas e metodologias de parametrização.
