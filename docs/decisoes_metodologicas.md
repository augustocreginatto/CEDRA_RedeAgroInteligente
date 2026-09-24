# Decisões metodológicas

Registro interno das decisões que alteram o significado físico, matemático ou metodológico do projeto.

## DEC-001 — Golden Cases do núcleo hídrico

**Decisão:** exemplos publicados pela FAO-56 serão utilizados como Golden Cases do núcleo agronômico.

**Primeiros casos:** Exemplos 36 e 37 do Capítulo 8.

**Motivo:** permitem validar separadamente capacidade de armazenamento, limite de depleção sem estresse, Ks, ETc ajustada e recorrência da depleção.

**Impacto:** o código do núcleo FAO deve reproduzir esses exemplos antes da inclusão das extensões operacionais.

## DEC-002 — Separação FAO / SBMI

**Decisão:** a validação FAO utiliza nomenclatura e equações FAO sem substituir p pelo fator F do SBMI.

**Motivo:** impedir mistura silenciosa de duas metodologias que possuem papéis diferentes no projeto.

**Impacto:** o SBMI será tratado em módulo/comparação específica, não como Golden Case.

## DEC-003 — Ambiente computacional

**Decisão:** Python é o ambiente principal. Pyomo é a camada de modelagem prevista para o MILP, Gurobi o solver principal e HiGHS um solver alternativo de verificação.

**Impacto:** o núcleo agronômico permanece independente do solver e não possui dependência de Pyomo/Gurobi.

## DEC-004 — Parâmetros de estudo de caso não pertencem ao núcleo

**Decisão:** cultura, localização, número de setores, velocidade e tempo de revolução são entradas/configurações de aplicação, não constantes estruturais do modelo.

**Impacto:** esses valores não devem aparecer hardcoded no núcleo matemático.
