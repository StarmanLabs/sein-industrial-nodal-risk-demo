# Public Methodology Summary

## Analytical Target

The product supports industrial due diligence by identifying barras with elevated relative nodal marginal-price stress and translating those signals into review priorities.

## Data Logic

The private pipeline processes COES marginal-price files into a monthly barra-level panel. The product layer then connects:

1. **Estrés nodal:** intensidad relativa de la señal de precio marginal de cada barra frente al universo comparable.
2. **Prioridad operativa:** la misma base de precios leída bajo el régimen mensual del sistema.
3. **Estabilidad del resultado:** cuánto cambia la relevancia de una barra al probar criterios alternativos.
4. **Contexto topológico revisado:** tipo de activo o conexión, familia de evidencia, cantidad de fuentes aceptadas y advertencias específicas.
5. Industrial scenarios: sector and contract archetype assumptions.

## Interpretation

The indicators are screening tools. They help decide where to investigate deeper. They are not causal estimates, price forecasts, invoice calculations, or engineering studies.

## Index Audit

The project includes a reproducible index audit in `docs/index_methodology_audit.md`. It validates coverage, score ranges, relationships between the two public signals, threshold sensitivity, reference-price sensitivity, component correlations and all-bar result stability.

## Review-queue weight sensitivity

`src/validation/build_priority_weight_sensitivity.py` is a separate diagnostic: it tests seven transparent weighting profiles across operational priority, an ICPI-based relative exposure proxy, extremes, continuity and stability. It does not replace the productive score, thresholds or review categories. The weights are stress tests, not universal preferences or investment weights; the proxy is not an invoice or facility cost estimate.

For the current layer, the alternative Top 20 lists retain 98.6% overlap on average with the balanced reference (95.0% minimum). This is ranking-stability evidence, not causal validation or a price forecast.

The public scenario-by-scenario results and interpretation rules are available in [`weight_sensitivity_evidence.md`](weight_sensitivity_evidence.md). The reproducible diagnostic remains in the private analytical repository; the public package exposes only sanitized evidence.

## Mining-location use boundary

The public data can screen real barras, compare explicit industrial and contract archetypes, inspect monthly recurrence and attach reviewed topology context. It does not contain the full information required to choose a mine location or connection alternative. In particular, the product does not model available network capacity, flows, contingencies, hourly plant dispatch, reservoir hydrology, project load, connection cost or permit feasibility.

The [`TINTAYA EXISTENTE 138` walkthrough](mining_siting_screening_case.md) shows the strongest defensible use: converting a real barra and an illustrative continuous-load mining scenario into a structured evidence request.

Key interpretation:

- Estrés nodal y prioridad operativa son señales descriptivas relativas, no probabilidades.
- Estabilidad del resultado no equivale a validez del dato.
- Un resultado variable significa que la posición depende más del criterio analítico; no invalida los precios COES.
- El grado A funciona como control interno de publicación para las 217 barras. La interfaz muestra dimensiones que sí discriminan entre casos: familia de evidencia, fuentes aceptadas, alcance temporal y advertencias.
