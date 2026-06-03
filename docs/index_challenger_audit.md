# Auditoria Challenger de ICPI/OANRI

## Objetivo

Evaluar si existe una formulacion alternativa mas defendible que el baseline actual sin modificar las formulas productivas.

Esta auditoria compara candidatos por:

- estabilidad de ranking mensual;
- overlap de Top 20 mensual;
- preservacion de top barras a nivel perfil;
- claridad conceptual;
- interpretabilidad para dashboard y due diligence.

No busca causalidad, prediccion de precios ni diagnostico fisico de red.

## Formulas Challenger Recomendadas

### Estres nodal

Baseline privado:

`0.30*costo + 0.25*volatilidad + 0.25*estres + 0.20*criticidad`, con ajuste de calidad.

Challenger recomendado:

`0.80*promedio(costo, volatilidad, estres) + 0.20*criticidad`, con el mismo ajuste de calidad.

Por que mejora: mantiene el peso economico de la familia de precios y criticidad, pero reduce la critica de doble conteo entre costo, volatilidad y estres, porque primero los agrupa como una sola familia de senal nodal.

### Prioridad operativa

Baseline privado:

`sqrt(exposicion_nodal * regimen_sistemico)`, con ajuste de calidad.

Challenger recomendado:

`sqrt(exposicion_nodal * (0.25 + 0.75*regimen_sistemico))`, con el mismo ajuste de calidad.

Por que mejora: conserva la logica de interaccion entre barra y regimen del sistema, pero evita que un mes de baja presion sistemica suprima demasiado una senal nodal relevante. Es mas coherente con un sistema de screening: baja el peso del contexto operativo, pero no borra la senal local.

## Veredicto Ejecutivo

El baseline actual sigue siendo defendible. La mejor mejora potencial no es reemplazar todo de inmediato, sino promover un challenger controlado para pruebas:

- ICPI challenger recomendado: `icpi_ch_price_family_80_criticality_20`.
- OANRI challenger recomendado: `oanri_ch_geometric_floor`.

## Resultado ICPI

El mejor challenger ICPI es `icpi_ch_price_family_80_criticality_20` con suitability `0.958`.

Lectura: Keeps the baseline 80/20 price-family versus criticality balance with lower double-counting risk.

Metricas clave:

- Mean top-20 overlap: 0.982.
- Min top-20 overlap: 0.900.
- Profile top-20 overlap: 1.000.
- Profile Spearman: 1.000.

Implicancia: si el objetivo es reducir critica de doble conteo, el challenger de familia de precio + criticidad es mas limpio conceptualmente que el baseline. Si el objetivo es maxima continuidad operacional, el baseline o pesos iguales conservan mejor la cola.

## Resultado OANRI

El mejor challenger OANRI es `oanri_ch_geometric_floor` con suitability `0.959`.

Lectura: Keeps geometric interaction but avoids over-penalizing nodal stress during low-system-regime months.

Metricas clave:

- Mean top-20 overlap: 1.000.
- Min top-20 overlap: 1.000.
- Profile top-20 overlap: 0.950.
- Profile Spearman: 0.995.

Implicancia: OANRI puede mejorar si el regimen del sistema se comunica como amplificador suave o contexto operativo, no como interaccion dura que parezca causalidad localizada.

## Tabla Comparativa

| index_family | candidate | suitability_score | mean_top20_overlap | min_top20_overlap | profile_top20_overlap | profile_spearman | conceptual_score | interpretability_score | logic |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ICPI | icpi_ch_price_family_80_criticality_20 | 0.958 | 0.982 | 0.900 | 1.000 | 1.000 | 0.880 | 0.900 | Keeps the baseline 80/20 price-family versus criticality balance with lower double-counting risk. |
| ICPI | icpi_ch_equal_blocks | 0.940 | 0.964 | 0.850 | 1.000 | 1.000 | 0.780 | 0.950 | Removes subjective block weights while preserving all dimensions. |
| ICPI | icpi_ch_price_family_criticality | 0.933 | 0.936 | 0.800 | 1.000 | 1.000 | 0.920 | 0.900 | Collapses correlated price-derived dimensions into one family and keeps criticality as context. |
| ICPI | icpi_ch_pca_blocks | 0.848 | 0.929 | 0.750 | 0.950 | 0.999 | 0.720 | 0.450 | Data-driven factor score; statistically compact but less explainable for a decision dashboard. |
| ICPI | icpi_ch_min_redundancy | 0.809 | 0.860 | 0.400 | 0.950 | 0.995 | 0.700 | 0.820 | Drops volatility as an explicit block to reduce redundancy; useful as stress test, not likely as production replacement. |
| OANRI | oanri_ch_geometric_floor | 0.959 | 1.000 | 1.000 | 0.950 | 0.995 | 0.880 | 0.820 | Keeps geometric interaction but avoids over-penalizing nodal stress during low-system-regime months. |
| OANRI | oanri_ch_linear_70_30 | 0.953 | 1.000 | 1.000 | 0.900 | 0.979 | 0.830 | 0.930 | Simple additive version: mostly nodal signal with explicit system context. |
| OANRI | oanri_ch_soft_gate | 0.945 | 1.000 | 1.000 | 0.850 | 0.975 | 0.910 | 0.880 | Preserves nodal signal and uses system regime as a soft amplifier instead of a hard interaction. |
| OANRI | oanri_ch_linear_80_20 | 0.945 | 1.000 | 1.000 | 0.850 | 0.973 | 0.850 | 0.940 | Keeps nodal exposure dominant and uses system context as a lighter modifier. |
| OANRI | oanri_ch_nodal_primary_system_flag | 0.903 | 1.000 | 1.000 | 0.750 | 0.967 | 0.800 | 0.780 | Treats system regime mainly as a contextual flag; useful if local screening should dominate. |

## Recomendacion

1. Mantener ICPI/OANRI actuales como baseline productivo hasta revisar el impacto por barra.
2. Usar los challengers recomendados como capa experimental `v11`.
3. Revisar `data/final/validation_index_challenger_barra_profiles.csv` para identificar cambios de ranking relevantes.
4. Si se migra, hacerlo en una fase separada con:
   - outputs paralelos;
   - comparacion de ranking por barra;
   - actualizacion de metodologia;
   - pruebas unitarias;
   - versionado claro de dashboard.

## Limite De Claim

Ningun challenger convierte el proyecto en modelo causal, analisis electrico de flujos fisicos, prediccion de precios o calculador de facturas. La mejora posible es de medicion, estabilidad y comunicacion para soporte a decisiones.
