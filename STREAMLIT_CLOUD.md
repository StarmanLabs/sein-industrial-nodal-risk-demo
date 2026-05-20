# Streamlit Cloud Deployment Guide

Use this guide after the public demo repository has been created.

## Repository

Recommended repository:

```text
StarmanLabs/sein-industrial-nodal-risk-demo
```

Deploy only the public demo repository. Do not deploy the private analytical repository.

## Streamlit Cloud Settings

Use these settings:

| Setting | Value |
|---|---|
| Repository | `StarmanLabs/sein-industrial-nodal-risk-demo` |
| Branch | `main` |
| Main file path | `app.py` |
| Python dependencies | `requirements.txt` |
| Secrets | none required |

## Pre-Deploy Check

Before connecting the repository to Streamlit Cloud, confirm the public repository contains:

```text
app.py
requirements.txt
README.md
DEPLOYMENT.md
PUBLICATION_MANIFEST.md
data/public_demo/
docs/
docs_public/
sample_outputs/
assets/
```

It must not contain:

```text
data/raw/
data/interim/
data/manual/
data/final/
scripts/
src/
app/
.env
.streamlit/secrets.toml
browser profiles
local cache folders
```

## First Launch QA

After the Streamlit app is live, check:

- the app loads without errors;
- the Executive Overview appears first;
- the claim boundary is visible near the top;
- charts render correctly;
- `data/public_demo/` is the only data source;
- the public metric names are used;
- no local paths appear in the UI;
- the demo does not ask for credentials or secrets;
- the app URL can be opened from a private/incognito browser session.

## Recommended App Description

```text
Public demo of SEIN Industrial Nodal Risk Intelligence: a decision-support dashboard for industrial due diligence on relative nodal electricity price-stress signals in Peru.
```

## Claim Boundary

This dashboard is a public demo of a larger private analytical system. It uses sanitized or reduced outputs for portfolio demonstration. Scores are relative screening indicators for due diligence, not causal grid diagnosis, price forecasts, billing estimates or engineering network studies.

## After Deployment

Add the public app URL to:

- `README.md`;
- portfolio case study;
- LinkedIn launch post;
- private project documentation.
