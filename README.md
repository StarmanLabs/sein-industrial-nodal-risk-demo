# SEIN Industrial Nodal Risk Intelligence

SEIN Industrial Nodal Risk Intelligence is a closed-code data product for industrial electricity due diligence in Peru.

It transforms COES nodal marginal-price outputs into a barra-month analytical panel and translates relative **nodal stress**, **operational priority**, **result stability** and reviewed topology context into an industrial due-diligence queue.

**Product promise:** identify where an industrial analyst should investigate first under explicit location and contract-exposure assumptions, and show why that case entered the review queue.

[Open the interactive dashboard](https://sein-industrial-nodal-risk-demo-edaw4ndep4pm9plvudnyov.streamlit.app/)

## What This Project Does

- Ranks relative nodal marginal-price stress across SEIN barras.
- Combines nodal exposure with system-regime context.
- Produces action-oriented due-diligence candidates.
- Supports industrial exposure scenarios under explicit assumptions.
- Communicates limitations clearly for responsible use.

## What This Project Does Not Do

- It does not prove physical congestion.
- It does not predict electricity prices.
- It does not calculate facility-specific billing amounts.
- It does not identify physical causes.
- It does not perform electrical network-flow studies.

## Public Repository Scope

This public showcase documents the methodology, product design, selected visuals, and sanitized sample outputs. The full processing pipeline, complete analytical dataset, and internal topology review materials are maintained in a private repository.

## Evidence Behind the Queue

- **217 barras and 36 months:** the analytical universe used by the public product.
- **Seven weight scenarios:** transparent stress tests across operational priority, relative price exposure, extremes, continuity and result stability.
- **98.6% mean Top-20 overlap:** 95.0% minimum versus the balanced reference. This supports queue stability, not causal validity.
- **Reviewed topology context:** used to formulate better follow-up questions, not to infer power flows or physical constraints.

See [weight-sensitivity evidence](docs/weight_sensitivity_evidence.md) and the [illustrative mining walkthrough](docs/mining_siting_screening_case.md).

## Product Pages

1. Product Home
2. Executive Overview
3. Barra Priority Ranking
4. Signal Map
5. Monthly Monitoring
6. Industrial Exposure Scenario
7. Barra Case Study

## Portfolio Value

The project demonstrates data engineering, index construction, energy-economics judgment, industrial analytics, dashboard design, closed-code product strategy, and public communication discipline.

## A Concrete Review Path

1. On the Industrial Exposure page, select the visible filter `Minería de carga continua` and choose a contract archetype.
2. Compare the relative exposure ranking and identify the main driver under that scenario.
3. Open the Barra Priority Ranking to check queue position and result stability.
4. Review `TINTAYA EXISTENTE 138` as an evidence-backed illustration of how a real barra can be investigated.
5. Request project-specific contract, load, connection and engineering evidence before any siting or investment conclusion.
