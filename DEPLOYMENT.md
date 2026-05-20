# Controlled Demo Deployment

This folder is the deployable public demo package for SEIN Industrial Nodal Risk Intelligence.

The production repository remains private. Deploy only this folder, not the full project root.

## Recommended Deployment Options

### Option A: Streamlit Community Cloud

Use this option for a fast interactive portfolio demo.

1. Create a separate public GitHub repository, for example `sein-nodal-risk-demo`.
2. Copy only the contents of `product/public_repo/` into that repository.
3. Confirm that the repository root contains:
   - `app.py`
   - `requirements.txt`
   - `data/public_demo/`
   - `docs/`
   - `docs_public/`
   - `sample_outputs/`
   - `assets/`
4. In Streamlit Community Cloud, set:
   - Main file path: `app.py`
   - Python dependencies: `requirements.txt`
5. Do not add Streamlit secrets unless a future version requires authentication.

### Option B: Hugging Face Spaces

Use this option if the demo should live next to other portfolio or ML projects.

1. Create a public Space with SDK `Streamlit`.
2. Upload only the files from this folder.
3. Keep the full private pipeline out of the Space.

## Pre-Publication Gate

Before publishing, run this from the private project root:

```bash
python scripts/audit_public_demo_package.py
```

The audit checks for:

- required public files;
- accidental private folders;
- local machine paths;
- common secret/token patterns;
- overclaiming phrases;
- demo data size limits.

## Security Boundary

The public demo should never include:

- raw COES downloads;
- full processed datasets;
- private extraction or transformation scripts;
- topology review workbooks beyond sanitized summaries;
- `.env`, Streamlit secrets, API keys or GitHub tokens;
- browser profiles, caches or local machine paths.

## Claim Boundary

The demo is a screening and prioritization product. It is not a causal grid diagnosis, forward price model, billing estimate, engineering network study or investment recommendation.

## Operational Note

If a public host requires environment variables, create them directly in the host dashboard. Do not commit secrets to the repository.
