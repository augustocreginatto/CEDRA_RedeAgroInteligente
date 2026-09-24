# Decisões metodológicas

Registro interno das decisões que alteram o significado físico, matemático ou metodológico do projeto.

## DEC-001 — Golden Cases do núcleo hídrico

**Decisão:** exemplos publicados pela FAO-56 serão utilizados como Golden Cases do núcleo agronômico.

**Primeiros casos:** Exemplos 36 e 37 do Capítulo 8.

**Motivo:** permitem validar capacidade de armazenamento, limiar de depleção, Ks, evapotranspiração ajustada e recorrência da depleção.

**Impacto:** o modelo de déficit deve reproduzir esses exemplos antes da inclusão das extensões operacionais.

## DEC-002 — Separação FAO / SBMI

**Status:** substituída pela DEC-005.

**Decisão original:** a validação FAO utilizaria nomenclatura FAO separada da nomenclatura do projeto.

**Motivo da substituição:** verificou-se que TAW/CAD, RAW/CRA e Dr/D podem ser representados por um único núcleo físico, deixando a diferença metodológica na parametrização do limiar.

## DEC-003 — Ambiente computacional

**Decisão:** Python é o ambiente principal. Pyomo é a camada de modelagem prevista para o MILP, Gurobi o solver principal e HiGHS um solver alternativo de verificação.

**Impacto:** o modelo de déficit permanece independente do solver e não possui dependência de Pyomo/Gurobi.

## DEC-004 — Parâmetros de estudo de caso não pertencem ao núcleo

**Decisão:** cultura, localização, número de setores, velocidade e tempo de revolução são entradas/configurações de aplicação, não constantes estruturais do modelo.

**Impacto:** esses valores não devem aparecer hardcoded no núcleo matemático.

## DEC-005 — Núcleo único CAD / CRA / D / Ks

**Decisão:** o projeto adota um único núcleo de balanço hídrico baseado em CAD, CRA, D e Ks.

**Estrutura:**

- CAD representa a capacidade total de água disponível na zona radicular;
- CRA é calculada como uma fração de CAD;
- D é a variável de estado de depleção;
- Ks é calculado a partir de D, CAD e CRA pela mesma lei de estresse na V1.

**Parametrizações:**

- FAO-56: CRA = p * CAD;
- SBMI: CRA = F * CAD, com F obtido pela tabela de grupo de cultura e ETc_max adotada no projeto;
- metodologias futuras poderão gerar CRA por outra calibração sem duplicar o núcleo.

**Motivo:** isolar diferenças metodológicas sem duplicar a física do reservatório.

## DEC-006 — Comparação controlada FAO-56 x SBMI

**Decisão:** na comparação inicial entre parametrizações, a equação de Ks permanece fixa e apenas a forma de obter o limiar CRA é alterada.

**Motivo:** permitir responder quanto da diferença de resultado decorre exclusivamente de p_FAO56 versus F_SBMI.

**Cuidado:** esta é uma decisão experimental do projeto e não uma afirmação de que o SBMI possua apenas uma metodologia possível de Ks.

## DEC-007 — DOE também no modelo de déficit

**Decisão:** a arquitetura do modelo de déficit deve permitir DOE independentemente do modelo de otimização.

**Motivo:** orientação discutida com o professor e interesse científico em avaliar sensibilidade, efeitos principais e interações do próprio balanço hídrico.

**Impacto:** parâmetros do solo, cultura, clima e método de parametrização devem permanecer externos ao núcleo e configuráveis.
