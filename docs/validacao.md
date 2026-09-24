# Estratégia de validação do núcleo agronômico

## Objetivo

O modelo de déficit hídrico deve ser validado antes da inclusão do modelo de otimização.

A validação utiliza exemplos publicados no FAO Irrigation and Drainage Paper 56 como **Golden Cases**. A implementação interna, entretanto, utiliza a nomenclatura comum do projeto:

- CAD — capacidade total de água disponível na zona radicular;
- CRA — limiar de depleção sem estresse adotado na execução;
- D — depleção;
- Ks — coeficiente de estresse hídrico.

Nos Golden Cases FAO-56, a correspondência utilizada é:

- TAW -> CAD;
- RAW -> CRA;
- Dr -> D;
- p -> fração utilizada para calcular CRA.

Isso permite validar a matemática publicada pela FAO sem manter um segundo núcleo de balanço hídrico.

Fonte oficial: https://www.fao.org/4/x0490e/x0490e0e.htm

## Golden Case 1 — FAO-56, Exemplo 36

Valida:

- Eq. 82: TAW = 1000 (theta_FC - theta_WP) Zr;
- Eq. 83: RAW = p TAW;
- equivalência operacional TAW/CAD e RAW/CRA;
- unidades e conversões para diferentes solos e culturas.

O teste reproduz as nove combinações publicadas para cebola, tomate e milho em três classes de solo.

## Golden Case 2 — FAO-56, Exemplo 37

Valida conjuntamente:

- CAD equivalente ao TAW publicado;
- CRA equivalente ao RAW publicado;
- ETc = ETo Kc;
- coeficiente de estresse Ks;
- evapotranspiração ajustada por estresse;
- atualização sequencial de D ao longo de dez dias.

O caso utiliza tomate adulto, Zr = 0,8 m, p = 0,40, theta_FC = 0,32, theta_WP = 0,12, depleção inicial de 55 mm, ETo = 5 mm/d e Kc = 1,2, sem chuva ou irrigação.

Resultados publicados principais:

- TAW/CAD = 160 mm;
- RAW/CRA = 64 mm;
- ETc potencial = 6 mm/d;
- depleção final no décimo dia = aproximadamente 104,5 mm.

As tolerâncias consideram o arredondamento da tabela impressa pela FAO.

## Exemplo 38 — não incluído na V1

O Exemplo 38 utiliza coeficiente dual, crescimento da zona radicular, irrigação no início do dia e percolação profunda. Ele permanece mapeado para uma etapa posterior caso esses elementos sejam incorporados explicitamente.

## Validação das parametrizações

O núcleo CAD/CRA/D/Ks é único.

A comparação FAO-56 x SBMI deve alterar somente a forma de obtenção da fração de depleção usada para calcular CRA, mantendo fixas as demais entradas quando o objetivo do experimento for isolar esse efeito.

Na configuração FAO-56, a fração é p.

Na configuração SBMI adotada no projeto, a fração é F, obtida pela tabela grupo de cultura x ETc_max e interpolação linear.

Essa escolha é deliberada para permitir comparação controlada. Ela não implica afirmar que o SBMI possua apenas uma formulação possível de Ks.
