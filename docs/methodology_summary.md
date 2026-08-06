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

Key interpretation:

- Estrés nodal y prioridad operativa son señales descriptivas relativas, no probabilidades.
- Estabilidad del resultado no equivale a validez del dato.
- Un resultado variable significa que la posición depende más del criterio analítico; no invalida los precios COES.
- El grado A funciona como control interno de publicación para las 217 barras. La interfaz muestra dimensiones que sí discriminan entre casos: familia de evidencia, fuentes aceptadas, alcance temporal y advertencias.
