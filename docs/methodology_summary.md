# Public Methodology Summary

## Analytical Target

The product supports industrial due diligence by identifying barras with elevated relative nodal marginal-price stress and translating those signals into review priorities.

## Data Logic

The private pipeline processes COES marginal-price files into a monthly barra-level panel. The product layer then connects:

1. ICPI: relative nodal marginal-price stress.
2. OANRI: system-regime adjusted prioritization signal.
3. Signal stability evidence: all-bar rank stability, scenario sensitivity and quality flags.
4. Reviewed topology context: evidence grade and permitted use.
5. Industrial scenarios: sector and contract archetype assumptions.

## Interpretation

The indicators are screening tools. They help decide where to investigate deeper. They are not causal estimates, price forecasts, invoice calculations, or engineering studies.

## Index Audit

The project includes a reproducible index audit in `docs/index_methodology_audit.md`. It validates coverage, score ranges, ICPI/OANRI relationships, threshold sensitivity, reference-price sensitivity, component correlations and all-bar signal stability.

Key interpretation:

- ICPI is a relative nodal price-stress score.
- OANRI is a system-regime-adjusted prioritization score.
- Signal stability is not the same as data validity.
- Low stability means the barra is less stable as a priority candidate under alternative scoring assumptions, not that the COES price data is invalid.
