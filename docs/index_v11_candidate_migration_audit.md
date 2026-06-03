# Auditoria de Capa Candidata v11

## Objetivo

Construir una capa paralela para evaluar si los challengers metodologicos deben reemplazar o complementar el baseline actual.

Esta fase no cambia el dashboard productivo ni las formulas productivas. Produce una capa sombra para comparar:

- baseline actual;
- `Estres nodal v11`;
- `Prioridad operativa v11`;
- cambios de ranking;
- cambios de categoria de revision.

## Formulas usadas

`Estres nodal v11 = 0.80*promedio(costo, volatilidad, estres) + 0.20*criticidad`, con ajuste de calidad.

`Prioridad operativa v11 = sqrt(exposicion_nodal * (0.25 + 0.75*regimen_sistemico))`, con ajuste de calidad.

Los scores v11 usados para categoria y score final estan calibrados por mapeo de cuantiles empiricos contra la escala del baseline. Esto evita comparar thresholds antiguos contra una escala nueva mas alta.

## Resultado ejecutivo

- Filas barra-mes evaluadas: 6779.
- Barras evaluadas: 217.
- Overlap Top 20 por perfil: 0.950.
- Overlap Top 50 por perfil: 0.980.
- Overlap Top 20 mensual promedio: 1.000.
- Overlap Top 20 mensual minimo: 1.000.
- Cambios de categoria: 24.
- Cambios de ranking mayores o iguales a 20 posiciones: 3.

## Lectura

La capa v11 es metodologicamente atractiva porque reduce redundancia en la medicion del estres nodal y trata el regimen operativo como ajuste de contexto, no como supresor fuerte de la senal nodal. La calibracion de escala es necesaria para que `75`, `65` u otros puntos de corte mantengan una lectura comparable con el baseline.

Si el overlap alto se mantiene y los cambios de categoria son pocos, v11 puede reemplazar al baseline con bajo riesgo narrativo. Si aparecen muchos cambios de categoria, conviene mantener v11 como sensibilidad metodologica y no como score principal.

## Top 15 por score v11

| barra | decision_priority_score | decision_priority_score_v11 | rank_decision_priority_score_baseline | rank_decision_priority_score_v11 | due_diligence_priority | due_diligence_priority_v11 | v11_change_flag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZORRITOS 220 | 75.39 | 79.86 | 2.0 | 1.0 | Priority A | Priority A | stable |
| PLANTAETANOL 60 | 75.71 | 79.48 | 1.0 | 2.0 | Priority A | Priority A | stable |
| HUAYLLACHO 15 | 75.35 | 78.96 | 3.0 | 3.0 | Priority A | Priority A | stable |
| NCTUMBES60 | 75.32 | 78.9 | 4.0 | 4.0 | Priority A | Priority A | stable |
| SAN IGNACIO 15 | 74.93 | 78.83 | 5.0 | 5.0 | Priority B | Priority A | category_changed |
| SAN ANTONIO 15 | 74.92 | 78.82 | 6.0 | 6.0 | Priority B | Priority A | category_changed |
| GE1 33 | 73.22 | 77.22 | 8.0 | 7.0 | Priority B | Priority A | category_changed |
| TINTAYA EXISTENTE 138 | 73.64 | 76.5 | 7.0 | 8.0 | Priority B | Priority A | category_changed |
| MISAPUQUIO 33 | 72.67 | 76.43 | 10.0 | 9.0 | Priority B | Priority A | category_changed |
| BELAUNDE 138 | 72.49 | 75.94 | 12.0 | 10.0 | Priority B | Priority A | category_changed |
| PIURA OESTE 220 | 72.26 | 75.79 | 13.0 | 11.0 | Priority B | Priority A | category_changed |
| TALARA13.2 | 72.07 | 75.49 | 17.0 | 12.0 | Priority B | Priority A | category_changed |
| PARIAC 66 | 72.78 | 75.43 | 9.0 | 13.0 | Priority B | Priority A | category_changed |
| TINTAYA NUEVA 220 | 72.62 | 75.27 | 11.0 | 14.0 | Priority B | Priority A | category_changed |
| GALLITO CIEGO 60 | 72.18 | 75.24 | 15.0 | 15.0 | Priority B | Priority A | category_changed |

## Casos que requieren revision antes de migrar

| barra | due_diligence_priority | due_diligence_priority_v11 | rank_decision_priority_score_baseline | rank_decision_priority_score_v11 | rank_shift_priority_score_v11 | delta_decision_priority_score_v11 | v11_change_flag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PLANTA CASA GRANDE 13.8 | Monitor | Monitor | 182.0 | 123.0 | -59.0 | 14.41 | large_rank_shift |
| SANTIAGO DE CAO 138 | Monitor | Monitor | 188.0 | 136.0 | -52.0 | 12.99 | large_rank_shift |
| JAEN 138 | Priority B | Priority B | 50.0 | 29.0 | -21.0 | 5.36 | large_rank_shift |
| CARHUAQUERO 10_S | Watchlist | Priority B | 91.0 | 82.0 | -9.0 | 1.43 | category_changed |
| POMACOCHA 220 | Monitor | Monitor | 163.0 | 170.0 | 7.0 | -5.06 | score_shift_review |
| CT INDEPENDENCIA 60 | Watchlist | Monitor | 136.0 | 142.0 | 6.0 | -3.64 | category_changed |
| TALARA13.2 | Priority B | Priority A | 17.0 | 12.0 | -5.0 | 3.42 | category_changed |
| PARAGSHA2 138 | Watchlist | Monitor | 134.0 | 138.0 | 4.0 | -3.32 | category_changed |
| MARCONA 220 | Watchlist | Monitor | 124.0 | 128.0 | 4.0 | -3.75 | category_changed |
| PARIAC 66 | Priority B | Priority A | 9.0 | 13.0 | 4.0 | 2.65 | category_changed |
| HUAYUCACHI 220 | Monitor | Monitor | 183.0 | 187.0 | 4.0 | -5.45 | score_shift_review |
| PACHACHACA 220 | Monitor | Monitor | 171.0 | 175.0 | 4.0 | -5.23 | score_shift_review |
| HUANCAVELICA 220 | Monitor | Monitor | 184.0 | 188.0 | 4.0 | -5.42 | score_shift_review |
| OLLEROS 500 | Monitor | Monitor | 170.0 | 173.0 | 3.0 | -5.2 | score_shift_review |
| POROMA 220 | Watchlist | Monitor | 123.0 | 126.0 | 3.0 | -3.64 | category_changed |
| CH OROYA 50 | Monitor | Monitor | 179.0 | 182.0 | 3.0 | -5.21 | score_shift_review |
| JULIACA10 | Priority B | Priority A | 14.0 | 17.0 | 3.0 | 2.97 | category_changed |
| TINTAYA NUEVA 220 | Priority B | Priority A | 11.0 | 14.0 | 3.0 | 2.65 | category_changed |
| CHIMAY 220 | Monitor | Monitor | 187.0 | 190.0 | 3.0 | -5.5 | score_shift_review |
| CALLAHUANCA 60 | Monitor | Monitor | 176.0 | 179.0 | 3.0 | -5.09 | score_shift_review |
| HUANCHOR 50 | Priority B | Watchlist | 128.0 | 125.0 | -3.0 | -1.53 | category_changed |
| CERRO DEL AGUILA 220 | Monitor | Monitor | 191.0 | 193.0 | 2.0 | -5.66 | score_shift_review |
| PAQUILLUSI 220 | Priority B | Monitor | 106.0 | 104.0 | -2.0 | -1.09 | category_changed |
| PIURA OESTE 220 | Priority B | Priority A | 13.0 | 11.0 | -2.0 | 3.53 | category_changed |
| BELAUNDE 138 | Priority B | Priority A | 12.0 | 10.0 | -2.0 | 3.46 | category_changed |

## Recomendacion

1. No migrar automaticamente.
2. Revisar las barras con `category_changed` o `large_rank_shift`.
3. Si los cambios tienen sentido economico y operativo, crear una fase `v11-product-migration`.
4. Si no, conservar baseline y usar v11 como prueba de robustez en metodologia publica.

## Limite de interpretacion

La capa v11 mejora medicion y comunicacion. No convierte el dashboard en diagnostico causal, prediccion de precios, calculo de facturas ni estudio tecnico definitivo de red.
