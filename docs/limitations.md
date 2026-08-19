# Limitations

- Nodal stress and operational priority are decision-support indicators, not proof of physical congestion.
- The dashboard does not forecast future electricity prices.
- Industrial exposure scenarios are conditional and illustrative; they are not facility-specific billing calculations.
- Topology evidence is used as reviewed context, not as validation of electrical flows, limits or contingencies.
- The 217 price keys are canonically identified and the topology context passed the public screening gate. Evidence depth still varies by barra; source count, evidence family and case-specific caveats should be reviewed before a stronger technical interpretation.
- Result stability is a screening measure across alternative analytical criteria. It does not prove a physical cause; it indicates whether the barra remains analytically relevant under reasonable scoring assumptions. Internally, this layer is based on robustness and sensitivity checks.
- Public outputs are intentionally sanitized relative to the private product while preserving the 217-barra analytical universe.
- The public package does not include a complete plant-level generation, fuel-cost, hydrology, reservoir, dispatch, flow-limit or contingency model. Marginal-price signals therefore cannot be attributed to a specific thermal or hydroelectric plant from this dashboard alone.
- Mining scenarios use explicit archetype assumptions, including assumed consumption and spot participation. They are not observed load profiles for a named mine and cannot determine a technically feasible or economically optimal connection point.
