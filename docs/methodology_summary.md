# Public Methodology Summary

## Analytical Target

The product supports industrial due diligence by identifying barras with elevated relative nodal marginal-price stress and translating those signals into review priorities.

## Data Logic

The private pipeline processes COES marginal-price files into a monthly barra-level panel. The product layer then connects:

1. Nodal Price Stress Score: relative nodal marginal-price stress.
2. System-Adjusted Nodal Risk Score: system-regime adjusted prioritization signal.
3. Robustness evidence: sensitivity inclusion and quality flags.
4. Reviewed topology context: evidence grade and permitted use.
5. Industrial scenarios: sector and contract archetype assumptions.

The private pipeline stores the first two metrics under internal names for traceability, but public-facing material uses descriptive names.

## Interpretation

The indicators are screening tools. They help decide where to investigate deeper. They are not causal estimates, forward price models, billing calculations, or engineering studies.
