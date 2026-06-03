# Auditoria Metodologica de Indices ICPI/OANRI

## Veredicto Ejecutivo

ICPI/OANRI son defendibles para un producto de screening y priorizacion de due diligence industrial. No requieren cambio de formula antes del siguiente paso, pero si requieren comunicacion metodologica mas precisa.

El punto mas importante: OANRI no debe venderse como diagnostico causal o localizado de red. Debe presentarse como senal nodal leida junto con contexto mensual del regimen operativo del sistema.

## Resultados Clave

- Filas barra-mes auditadas: 6,779.
- Barras auditadas: 217.
- Meses auditados: 36.
- Share de baja informacion: 0.018.
- Spearman ICPI vs OANRI: 0.669.
- Spearman OANRI vs OANRI alternativo: 0.952.
- Overlap promedio top-20 ICPI/OANRI: 0.929.
- Overlap minimo top-20 ICPI/OANRI: 0.800.

## Lectura Tecnica

ICPI mide estres nodal relativo usando precio, cola/tail, volatilidad, dispersion, primas de estres y ventanas criticas. Es una escala 0-100 relativa al universo observado, no una probabilidad.

OANRI combina exposicion nodal con regimen operativo mensual mediante una interaccion geometrica. Esto es metodologicamente prudente porque un nodo con senal alta importa mas cuando el sistema tambien esta bajo mayor presion, pero no permite atribuir causalidad fisica local.

## Criticas Principales Y Como Quedan Resueltas

| Critica | Prueba aplicada | Resultado | Veredicto |
|---|---|---|---|
| ICPI podria duplicar senal porque precio, volatilidad y estres estan correlacionados | Sensibilidad de pesos con bloques iguales y una version de familia de precio + criticidad | Bloques iguales conserva top-20 promedio 0.964; familia de precio + criticidad conserva top-20 promedio 0.936 | Defendible: la cola principal no depende solo de los pesos base, aunque los componentes deben explicarse como dimensiones relacionadas de precio |
| OANRI podria parecer causal/local por usar regimen operativo | Descomposicion de variacion: regimen sistemico comun por mes y overlap con exposicion nodal | Maximo de valores de regimen por mes = 1; overlap top-20 OANRI vs exposicion nodal = 1.000 | Defendible: OANRI es contexto operativo mensual aplicado a una cola nodal; no diagnostico fisico localizado |
| Robustez baja podria leerse como dato malo | Separacion entre cobertura, estabilidad y prioridad | La auditoria distingue baja informacion, estabilidad de senal y prioridad de revision | Defendible si el dashboard usa "estabilidad de senal" y no vende baja estabilidad como falla de datos |

## Hallazgos Que Requieren Cuidado

| area | test | value | interpretation | recommended_action |
| --- | --- | --- | --- | --- |
| icpi_defensibility | ICPI sensitivity::no_volatility_component | Spearman 0.989; mean top20 0.879; min top20 0.500 | Removing an economically meaningful price-family component changes the queue more materially. | Do not remove core price components; explain that cost, volatility and stress are related but not redundant for decision screening. |
| icpi_defensibility | ICPI sensitivity::no_cost_component | Spearman 0.974; mean top20 0.819; min top20 0.300 | Removing an economically meaningful price-family component changes the queue more materially. | Do not remove core price components; explain that cost, volatility and stress are related but not redundant for decision screening. |
| sensitivity | spike threshold sensitivity | global max 0.868; monthly max 0.393; barra-month max 1.000 | Spike definitions can materially affect extreme local windows. | Do not let spike frequency be interpreted alone; keep it as one component inside a broader score. |
| construct_validity | strongest block correlation | block_cost_v10 vs block_volatility_v10 = 0.844 | Some nodal blocks are strongly related because they all originate from marginal-price behavior. | Document the construct logic and use sensitivity checks to address possible double-counting criticism. |
| construct_validity | critical-window block relation to ICPI | 0.098 | The critical-window block contributes less to the overall ICPI than cost, volatility and stress blocks. | Keep criticality as a contextual component; do not oversell it as the dominant driver. |
| product_layer | all-bar signal stability distribution | {"Low robustness": 162, "High robustness": 52, "Moderate robustness": 3} | All barras now have a stability label, but low stability should not be communicated as bad data. | Rename dashboard language from robustness to signal stability and distinguish candidate stability from data coverage. |

## Hallazgos Fuertes

| area | test | value | interpretation |
| --- | --- | --- | --- |
| icpi_defensibility | ICPI sensitivity::equal_blocks | Spearman 0.999; mean top20 0.964; min top20 0.850 | The ICPI top candidate queue remains similar under a less granular block-weighting alternative. |
| icpi_defensibility | ICPI sensitivity::price_family_plus_criticality | Spearman 0.998; mean top20 0.936; min top20 0.800 | The ICPI top candidate queue remains similar under a less granular block-weighting alternative. |
| oanri_defensibility | system-regime variation within month | 1 | The system-regime layer is monthly and common across barras, so it is correctly interpreted as system context. |
| oanri_defensibility | OANRI vs nodal exposure monthly top-20 overlap | mean top20 1.000; min top20 1.000 | Within each month, OANRI preserves the nodal candidate queue while changing its system-pressure intensity. |
| oanri_defensibility | OANRI relation to nodal and system layers | nodal Spearman 0.681; system Spearman 0.657 | OANRI is materially related to both nodal exposure and monthly system-regime pressure. |
| coverage | barra-month panel coverage | 6,779 rows; 217 barras; 36 months | The index is built on the intended 217-barra, 36-month analytical universe. |
| coverage | low-information share | 0.018 | Low-information rows are limited relative to the full panel. |
| coverage | missing values in ICPI_v8 | 0 | ICPI_v8 is complete in the final decision panel. |
| coverage | missing values in OANRI_v10 | 0 | OANRI_v10 is complete in the final decision panel. |
| coverage | missing values in mean_price | 0 | mean_price is complete in the final decision panel. |
| coverage | missing values in p95_price | 0 | p95_price is complete in the final decision panel. |
| coverage | missing values in quality_score_v10 | 0 | quality_score_v10 is complete in the final decision panel. |
| scale | ICPI_v8 range | min 5.478; p25 34.917; median 49.945; p75 63.171; max 89.936 | The score has a usable spread for ranking and screening. |
| scale | OANRI_v10 range | min 1.239; p25 26.883; median 43.592; p75 61.899; max 100.000 | The score has a usable spread for ranking and screening. |
| scale | quality_score_v10 range | min 0.450; p25 1.000; median 1.000; p75 1.000; max 1.000 | The score has a usable spread for ranking and screening. |
| relationship | Spearman ICPI vs OANRI | 0.669 | OANRI is related to nodal stress but not identical; it adds system-regime context. |
| sensitivity | Spearman OANRI vs alternative OANRI | 0.952 | The main OANRI ranking is highly similar to the alternative OANRI specification. |
| sensitivity | ICPI vs OANRI monthly top-20 overlap | mean 0.929; min 0.800 | The top candidate queue is broadly consistent, while OANRI still changes prioritization in some months. |
| sensitivity | decision-tier threshold sensitivity | strict changed 0.084; permissive changed 0.097 | Tier labels move moderately under stricter/permissive thresholds, which is expected for screening bands. |
| sensitivity | reference price mean vs median | Spearman 0.949; top20 overlap 1.000 | Changing the internal reference price from mean to median keeps the top queue stable. |
| product_layer | due-diligence priority distribution | {"Priority B": 94, "Monitor": 60, "Watchlist": 38, "Low information": 21, "Priority A": 4} | Priority A remains strict; Priority B is a second-pass pool, not an urgent class. |

## Implicancia Para El Dashboard

1. Usar nombres publicos descriptivos:
   - ICPI: Estres nodal.
   - OANRI: Prioridad operativa.
   - Robustez: Estabilidad de senal.
   - decision_priority_score: Score de revision.

2. Separar tres conceptos:
   - cobertura de datos;
   - estabilidad de senal;
   - prioridad de revision.

3. No usar "robustez baja" como si fuera falla metodologica. En muchos casos significa que la barra no es candidata prioritaria estable, no que sus datos sean invalidos.

4. El siguiente paso metodologico recomendado es crear un score de revision ajustado que incorpore senal base, persistencia temporal y estabilidad de senal, sin modificar ICPI/OANRI.

## Limite De Claim

Estos indices ordenan senales relativas y apoyan priorizacion de revision. No prueban congestion fisica, no predicen precios, no calculan montos de facturacion especificos y no reemplazan revision contractual, operativa o de ingenieria.
