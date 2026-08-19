# Portfolio Case Study

## Problem

Industrial electricity exposure is shaped by location, timing, and contract structure. Average system prices can hide nodal stress patterns that matter for due diligence.

## Product

I built a decision-support system that converts COES marginal-price data into a 217-barra, 36-month analytical panel and a dashboard for industrial due-diligence prioritization.

## Method

The product combines relative nodal stress, system-adjusted operational priority, result-stability checks, reviewed topology context, and industrial sector-contract scenarios.

## Decision Value

The product helps an analyst decide which barras should be reviewed first, what evidence supports that priority, and what limitations must be considered before commercial or engineering conclusions.

## Illustrative mining case

`TINTAYA EXISTENTE 138` is a real barra in the product layer, with 138 kV transmission-substation context and a `mining_continuous_load` scenario. Its relative signal is strong and it remains in the Top 20 of all seven diagnostic weight scenarios. This supports a careful due-diligence walkthrough only. A real plant-location recommendation would still require the site coordinates, feasible connection, contract and settlement terms, hourly load, network studies, connection CAPEX/OPEX, permits and a project-specific economic comparison.

The complete public walkthrough is documented in [`mining_siting_screening_case.md`](mining_siting_screening_case.md). It deliberately separates observed data, scenario assumptions and missing decision evidence.

## Validation evidence

The review queue was challenged under seven alternative weight profiles. Its Top 20 retains 98.6% overlap on average with the balanced reference and never falls below 95.0%. `TINTAYA EXISTENTE 138` remains between positions 7 and 8 and appears in the Top 20 under all seven scenarios. These results support stability of analytical prioritization; they do not validate physical causality or future prices.
