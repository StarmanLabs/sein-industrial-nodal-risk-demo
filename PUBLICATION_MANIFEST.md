# Closed-Code Publication Manifest

## Status

This folder is a controlled public showcase. It does not include the closed production pipeline, raw files, manual topology registers or private audit materials.

The current public demo layer contains 217 barras, 36 monthly periods and 6,779 barra-month screening rows. These rows are sanitized final-product outputs for portfolio interaction, not raw or interim analytical data.

## Public Files

- `README.md`
- `app.py`
- `requirements.txt`
- `DEPLOYMENT.md`
- `docs/`
- `docs_public/`
- `sample_outputs/`
- `assets/`
- `data/public_demo/`

## Files That Must Remain Private

- raw COES downloads;
- interim processing outputs;
- full `data/final/` datasets;
- ingestion, parsing, feature-engineering and validation scripts;
- exploratory notebooks;
- complete manual topology review materials;
- local browser profiles, caches or credentials.

## Pre-Publication Checklist

- Run `python scripts/audit_public_demo_package.py` from the private project root.
- Confirm the public demo runs locally with `streamlit run app.py`.
- Confirm no private data, local paths or credentials appear in the public package.
- Confirm the claim boundary is visible in the app and documentation.
- Recapture screenshots after any visual redesign.

## Publication Rule

Deploy only the contents of this folder. Do not deploy the private repository root.
