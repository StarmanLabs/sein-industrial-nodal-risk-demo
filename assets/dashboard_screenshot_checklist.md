# Dashboard Screenshot Checklist

Use this checklist to recapture public-safe screenshots from the private Streamlit dashboard.

Dashboard URL:

`http://localhost:8501`

## Required Screenshots

Save the files under:

`product/public_repo/assets/dashboard_screenshots/`

Recommended filenames:

1. `01_executive_overview.png`
2. `02_barra_priority_ranking.png`
3. `03_nodal_stress_signal_map.png`
4. `04_monthly_watchlist.png`
5. `05_industrial_exposure.png`
6. `06_barra_case_study_default.png`
7. Optional: `07_barra_case_study_zorritos.png`
8. Optional: `08_barra_case_study_puerto_bravo.png`

Current dashboard routes after Spanish navigation cleanup:

- `/`
- `/Resumen_Ejecutivo`
- `/Ranking_de_Prioridad`
- the signal-map page in the private dashboard, or `System-Adjusted Risk` in the public demo app.
- `/Watchlist_Mensual`
- `/Exposicion_Industrial`
- `/Caso_de_Estudio`

## Capture Rules

- Use a clean browser window at approximately 1440x1000 or larger.
- Hide browser bookmarks and unrelated UI where possible.
- Do not show local file paths, terminals, tokens, or raw-data folders.
- Prefer Spanish dashboard views.
- Use `ZORRITOS 220` for the strong case-study screenshot.
- Use `PUERTO BRAVO 500` for the watchlist case-study screenshot.
- Make sure caveats are visible in at least one screenshot.
- Make sure no table exposes full raw data or unresolved manual review notes.

## Current Automated Status

Automated Edge headless capture was attempted but blocked by local Windows/Crashpad permissions.

Codex in-app browser capture succeeded on 2026-05-17 for:

- `01_executive_overview.png`
- `02_barra_priority_ranking.png`
- `03_icpi_vs_oanri.png`
- `04_monthly_watchlist.png`
- `05_industrial_exposure.png`

`06_barra_case_study_default.png` exists as an earlier capture, but should be manually recaptured after the final Spanish-label cleanup. The live dashboard text was checked after cleanup and correctly renders `driver dominante: nivel de precio`.
