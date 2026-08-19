# Review-Queue Weight Sensitivity

## Question

Would the same barras remain near the front of the review queue if an analyst placed more emphasis on operational priority, relative price exposure, extremes, continuity or result stability?

## Design

The diagnostic evaluates all 217 barra profiles under seven transparent weight scenarios. Every construct remains active in every scenario. Inputs are converted to cross-sectional percentiles before weighting so variables with different units remain comparable.

| Scenario | Operational priority | Relative price exposure | Extremes | Continuity | Result stability | Top-20 overlap vs. reference |
|---|---:|---:|---:|---:|---:|---:|
| Balanced reference | 35% | 20% | 20% | 15% | 10% | 100% |
| Operational-priority heavy | 50% | 15% | 15% | 10% | 10% | 100% |
| Relative-price-exposure heavy | 25% | 40% | 15% | 10% | 10% | 95% |
| Extremes heavy | 25% | 15% | 40% | 10% | 10% | 95% |
| Continuity heavy | 25% | 15% | 15% | 35% | 10% | 100% |
| Result-stability heavy | 25% | 15% | 15% | 10% | 35% | 100% |
| Equal constructs | 20% | 20% | 20% | 20% | 20% | 100% |

## Result

- Mean Top-20 overlap with the balanced reference: **98.6%**.
- Minimum Top-20 overlap: **95.0%**.
- `TINTAYA EXISTENTE 138`: Top 20 in **7 of 7** scenarios; best rank 7, worst rank 8.
- `TINTAYA NUEVA 220`: Top 20 in **7 of 7** scenarios; best rank 13, worst rank 15.
- `TOQUEPALA 138`: stable outside the Top 20; best rank 29, worst rank 32.
- `CERRO VERDE 138`: stable outside the Top 20; best rank 58, worst rank 60.

## Interpretation

The front of the queue is not an artifact of one narrow weighting profile. This supports using the ranking for analytical triage. It does not prove that the weights are universally optimal, that the barras face physical congestion or that future electricity costs will follow the ranking.

The diagnostic does not replace the productive score, thresholds or public review categories. It is a challenge test around them.

## Reproducibility boundary

The complete diagnostic script and full 217-barra output remain in the private analytical repository. The sanitized scenario summary is available in [`../sample_outputs/weight_sensitivity_summary.csv`](../sample_outputs/weight_sensitivity_summary.csv).
