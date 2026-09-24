# Estratégia de validação do núcleo agronômico

## Objetivo

O núcleo agronômico deve ser validado antes de qualquer inclusão de pivô, tarifa, previsão meteorológica, MILP ou DOE.

A validação utiliza exemplos publicados no FAO Irrigation and Drainage Paper 56 como **Golden Cases**. Os testes mantêm a nomenclatura original da FAO (TAW, RAW, Dr e p) para evitar mistura silenciosa com a nomenclatura adotada posteriormente no projeto e no SBMI.

Fonte oficial: https://www.fao.org/4/x0490e/x0490e0e.htm

## Golden Case 1 — FAO-56, Exemplo 36

Valida:

- Eq. 82: TAW = 1000 (theta_FC - theta_WP) Zr;
- Eq. 83: RAW = p TAW;
- unidades e conversões para diferentes solos e culturas.

O teste reproduz as nove combinações publicadas para cebola, tomate e milho em três classes de solo.

## Golden Case 2 — FAO-56, Exemplo 37

Valida conjuntamente:

- TAW;
- RAW;
- ETc = ETo Kc;
- coeficiente de estresse Ks (Eq. 84);
- evapotranspiração ajustada por estresse;
- atualização sequencial da depleção da zona radicular ao longo de dez dias.

O caso utiliza tomate adulto, Zr = 0,8 m, p = 0,40, theta_FC = 0,32, theta_WP = 0,12, depleção inicial de 55 mm, ETo = 5 mm/d e Kc = 1,2, sem chuva ou irrigação.

Resultados publicados principais:

- TAW = 160 mm;
- RAW = 64 mm;
- ETc potencial = 6 mm/d;
- depleção final no décimo dia = aproximadamente 104,5 mm.

As tolerâncias dos testes consideram o arredondamento da tabela impressa pela FAO.

## Exemplo 38 — não incluído na V1 do Golden Case

O Exemplo 38 utiliza a abordagem de coeficiente dual (Kcb + Ke), crescimento da zona radicular, irrigação aplicada no início do dia e percolação profunda. Esses elementos excedem o núcleo de coeficiente único atualmente adotado.

Ele permanece mapeado como candidato para uma etapa posterior de validação caso o projeto implemente explicitamente o procedimento dual completo.

## Relação com a nomenclatura do projeto

Existe correspondência física entre alguns termos, mas ela não deve ser usada para misturar metodologias:

- FAO TAW corresponde conceitualmente à capacidade total de água disponível na zona radicular (CAD);
- FAO RAW é o limite de depleção sem estresse definido por p;
- no modelo baseado no SBMI, a CRA utiliza o fator F da metodologia de manejo adotada no projeto.

RAW e CRA não devem ser considerados numericamente equivalentes por definição, pois p e F podem ser obtidos por metodologias diferentes.
