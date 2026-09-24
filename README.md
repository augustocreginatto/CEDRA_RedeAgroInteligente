# Mestrado Augusto

Repositório de desenvolvimento do projeto de mestrado de Augusto Reginatto no PROMEC/UFRGS.

Atualmente, o desenvolvimento da dissertação ocorre de forma integrada às atividades conduzidas pelo autor no âmbito do CEDRA — Centro de Competência EMBRAPII — e do programa Rede Agro. Para fins deste repositório, esses trabalhos são tratados como um único projeto.

Este repositório não representa o CEDRA ou o Rede Agro como um todo. Ele contém exclusivamente os modelos, dados, documentação, testes e experimentos relacionados ao projeto de pesquisa do autor.

## Objetivo deste README

Este documento funciona como referência interna para a arquitetura metodológica do projeto.

Seu objetivo é registrar:

- o que pertence ao modelo geral;
- o que pertence à metodologia de validação;
- o que é simplificação de uma versão;
- o que pertence apenas ao estudo de caso;
- quais decisões foram modificadas ao longo do desenvolvimento.

Valores associados ao estudo de caso não devem ser incorporados como características estruturais do modelo.

---

# Fluxo metodológico

O desenvolvimento será organizado em seis etapas.

## 1. Modelo de déficit hídrico

Implementação independente do núcleo agronômico do modelo.

Características:

- independente de cultura específica;
- independente de localização;
- independente do sistema de irrigação;
- independente da tarifa de energia;
- independente do método de otimização.

A implementação será validada contra exemplos numéricos publicados pela FAO.

Os exemplos FAO constituirão os **Golden Cases** do núcleo hídrico.

O objetivo desta etapa é verificar se a implementação computacional reproduz corretamente o modelo agronômico de referência.

---

## 2. Modelo de otimização

O núcleo hídrico validado será incorporado a um modelo operacional de irrigação.

O problema será inicialmente formulado como **Programação Linear Inteira Mista (MILP)**.

O modelo deverá receber como parâmetros, entre outros:

- geometria e discretização espacial;
- características do equipamento;
- vazão;
- eficiência;
- tempo de revolução;
- potência;
- tarifa;
- previsão climática.

Esses valores não devem ser fixados estruturalmente no código.

A implementação principal será realizada em Python, com Pyomo como camada de modelagem e Gurobi como solver principal. A escolha do ambiente computacional não altera a formulação matemática do problema.

---

## 3. Comparação com SBMI

Será criada uma configuração do modelo compatível com as hipóteses e entradas utilizadas pelo Sistema Brasileiro de Manejo da Irrigação — SBMI.

Funcionalidades adicionais do modelo proposto deverão ser travadas ou desativadas quando não houver equivalente direto na metodologia utilizada para comparação.

A lógica da comparação será:

**modelo completo -> redução controlada -> configuração comparável ao SBMI**

O SBMI será tratado como **benchmark de manejo**, e não como referência de validação matemática.

A comparação deverá explicitar:

- quais equações e entradas são equivalentes;
- quais extensões do modelo foram desativadas;
- quais parâmetros foram igualados;
- quais variáveis de saída são efetivamente comparáveis.

---

## 4. Estudo de caso

Após a validação dos modelos, será realizada uma aplicação com dados reais.

A configuração inicial considerada atualmente envolve:

- cultura: soja;
- localização: Alegrete/RS;
- pivô central;
- dados locais de solo;
- dados climáticos;
- dados hidráulicos e energéticos do equipamento;
- discretização espacial preliminar em 36 setores.

Esses valores pertencem ao estudo de caso e não à estrutura geral do modelo.

Parâmetros como cultura, localização, número de setores, velocidade do pivô, tempo de revolução, vazão, eficiência e demais características operacionais devem permanecer parametrizáveis.

---

## 5. Resultados

Serão avaliados os resultados do modelo de referência, das comparações com o SBMI e das estratégias otimizadas.

As variáveis-resposta serão definidas conforme a evolução do estudo, incluindo indicadores hídricos, energéticos, econômicos e computacionais.

Exemplos de respostas candidatas:

- custo de energia;
- energia consumida;
- volume irrigado;
- número de revoluções;
- máxima depleção;
- margem em relação à CRA;
- distribuição temporal das irrigações;
- utilização de períodos tarifários favoráveis;
- tempo computacional;
- gap de otimização.

---

## 6. Design of Experiments — DOE

O DOE será aplicado ao modelo previamente validado.

Parâmetros do modelo ou do estudo de caso poderão ser tratados como fatores experimentais.

A estrutura matemática do modelo deve permanecer independente dos valores escolhidos para os fatores.

O DOE será utilizado para identificar:

- efeitos principais;
- interações;
- sensibilidade das respostas;
- robustez das estratégias de otimização.

Assim:

**modelo != experimento**

O modelo permanece definido. O DOE modifica fatores e observa respostas.

---

# Separação conceitual

## FAO

A metodologia FAO constitui a principal referência para o núcleo físico/agronômico.

Seu papel no projeto é:

- fundamentar as equações;
- fornecer parâmetros e relações agronômicas;
- fornecer exemplos numéricos para validação.

Casos publicados pela FAO serão utilizados como **Golden Cases**.

A pergunta respondida nesta etapa é:

> A implementação computacional reproduz corretamente o modelo agronômico de referência?

## SBMI

O SBMI é tratado como **benchmark de manejo**.

O modelo proposto possui elementos adicionais em relação ao SBMI. Portanto, comparações deverão utilizar uma configuração reduzida, contendo apenas elementos equivalentes entre as duas metodologias.

A pergunta nesta etapa é:

> Sob premissas e entradas equivalentes, como o modelo se comporta em relação à metodologia de manejo adotada no SBMI?

## Modelo proposto

É o modelo desenvolvido nesta pesquisa.

Ele parte do núcleo agronômico validado e adiciona progressivamente elementos operacionais, energéticos, preditivos e de otimização.

## DOE

O DOE utiliza o modelo validado como objeto experimental.

Parâmetros são modificados de forma controlada para avaliação de efeitos e interações, sem redefinir o núcleo físico do modelo.

---

# Classificação das decisões do projeto

Para evitar misturar níveis diferentes, toda decisão deve ser classificada em uma das categorias abaixo.

## Decisão metodológica

Define como a pesquisa será conduzida.

Exemplos atuais:

- FAO como referência para validação do balanço hídrico;
- exemplos FAO como Golden Cases;
- SBMI como benchmark de manejo;
- MILP como abordagem inicial de otimização;
- Python como ambiente principal de implementação;
- separação entre formulação matemática e solver;
- DOE como componente central da metodologia.

## Estrutura do modelo

Define a matemática ou a arquitetura genérica do sistema.

Exemplos:

- depleção D como variável de estado do balanço hídrico;
- uso parametrizado de ETo, Pe, Kc, Z, CAD e CRA;
- separação entre núcleo hídrico e otimização operacional;
- parâmetros do equipamento e do estudo de caso fornecidos externamente ao núcleo matemático.

## Configuração da V1

Simplificações escolhidas para a primeira implementação do modelo de otimização.

Atualmente:

- velocidade do pivô considerada constante durante uma revolução;
- uma revolução iniciada é concluída;
- na primeira versão, a bomba permanece ligada durante toda a revolução;
- consumo energético exclusivo das torres de deslocamento é desprezado;
- previsão meteorológica inicialmente tratada como perfeita;
- nenhuma violação de CRA é permitida na primeira formulação otimizada.

Essas escolhas podem ser revistas sem alterar o núcleo agronômico.

## Parâmetros do estudo de caso

Valores específicos de uma aplicação.

Configuração atualmente em discussão:

- cultura: soja;
- localização: Alegrete/RS;
- discretização espacial preliminar: 36 setores.

Esses valores não são características estruturais do modelo.

---

# Núcleo agronômico

A variável principal de estado do balanço hídrico é a depleção:

```text
D
```

representando a quantidade de água necessária para que a zona radicular retorne à capacidade de campo.

O balanço básico é:

```text
D(t+1) = D(t) + ETr(t) - Pe(t) - IRN(t)
```

sujeito a:

```text
0 <= D(t) <= CAD(t)
```

Principais grandezas:

- ETo — evapotranspiração de referência;
- Kc — coeficiente de cultura;
- ETc — evapotranspiração da cultura;
- Ks — coeficiente associado à disponibilidade hídrica;
- ETr — evapotranspiração real;
- Z — profundidade efetiva do sistema radicular;
- CAD — Capacidade de Água Disponível;
- CRA — Capacidade Real de Água no Solo;
- Pe — precipitação efetiva;
- D — depleção.

A formulação completa deverá ser mantida separadamente em `docs/equacionamento_hidrico.md`.

---

# Estratégia de validação

A validação será realizada em camadas.

## V1 — Golden Cases FAO

Reproduzir exemplos publicados pela FAO.

Objetivos:

- validar equações;
- validar unidades;
- validar evolução temporal;
- validar condições de estresse hídrico.

A implementação deverá reproduzir os resultados de referência dentro de tolerâncias previamente definidas.

O código deve ser ajustado ao caso de referência, e não o caso de referência ao código.

## V2 — Testes analíticos e sintéticos

Casos simples com resultado conhecido, por exemplo:

- ausência de chuva;
- ausência de irrigação;
- ET constante;
- irrigação suficiente para retornar a D = 0;
- diferentes valores de CAD;
- diferentes tipos de solo.

## V3 — Comparação com SBMI

Construção de um modo reduzido e compatível com as premissas do SBMI.

Comparar somente grandezas equivalentes.

## V4 — Modelo operacional completo

Adicionar progressivamente:

- pivô;
- discretização espacial;
- energia;
- tarifa;
- previsão meteorológica;
- otimização.

---

# Otimização

A estratégia escolhida para a primeira versão é MILP.

A primeira formulação operacional considera como decisão fundamental o instante de início de uma revolução.

Exemplo conceitual:

```text
y(t) = 1 -> iniciar uma revolução no instante t
y(t) = 0 -> não iniciar
```

As variáveis de estado hídrico permanecem contínuas.

A função objetivo inicial será baseada na minimização do custo de energia elétrica das irrigações, respeitando as restrições agronômicas e operacionais.

Arquitetura proposta:

- Python — ambiente principal;
- Pyomo — formulação algébrica;
- Gurobi — solver principal;
- HiGHS — solver alternativo para validação e reprodutibilidade.

---

# Previsão meteorológica

O modelo deverá ser capaz de utilizar previsão futura de:

- precipitação efetiva;
- evapotranspiração.

Na primeira etapa metodológica, poderá ser assumida previsão perfeita.

A previsão permitirá avaliar se uma irrigação deve ocorrer imediatamente ou se pode ser postergada devido à evolução futura esperada do balanço hídrico.

Essa funcionalidade deverá ser desenvolvida separadamente da validação agronômica básica.

---

# Estrutura prevista do repositório

```text
/
├── README.md
├── docs/
│   ├── equacionamento_hidrico.md
│   ├── formulacao_milp.md
│   ├── comparacao_sbmi.md
│   ├── validacao.md
│   ├── doe.md
│   └── decisoes_metodologicas.md
│
├── src/
│   └── irrigation_model/
│       ├── crop/
│       ├── soil/
│       ├── water_balance/
│       ├── pivot/
│       ├── energy/
│       ├── optimization/
│       └── doe/
│
├── tests/
│   ├── validation/
│   │   └── fao56/
│   ├── unit/
│   └── integration/
│
├── data/
│   ├── validation/
│   ├── synthetic/
│   └── processed/
│
├── experiments/
│   ├── prototypes/
│   ├── sbmi/
│   ├── optimization/
│   └── doe/
│
├── notebooks/
└── outputs/
```

---

# Controle de mudanças

As decisões registradas neste README não são necessariamente imutáveis.

Entretanto, qualquer alteração que modifique o significado físico, matemático ou metodológico do projeto deverá ser registrada.

Antes de alterar uma decisão relevante, registrar:

- decisão ou premissa anterior;
- nova decisão;
- motivo da alteração;
- impactos esperados;
- componentes afetados;
- necessidade ou não de repetir validações e experimentos.

O arquivo `docs/decisoes_metodologicas.md` deverá manter esse histórico.

A finalidade é evitar que mudanças realizadas durante o desenvolvimento contradigam silenciosamente decisões anteriores.
