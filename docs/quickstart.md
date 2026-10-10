# Quick start

## Without Python

Complete the forms in this order: project brief, framework applicability,
collection protocol, evidence and approvals, stewardship handoff. Spreadsheet
forms provide optional catalog and provenance entry. All begin as drafts.

## Python and notebooks

From the repository root:

```sh
conda env create -f environment.yml
conda activate tribal-data-sovereignty
pip install -e ".[dev]"
jupyter lab
```

Open `Notebooks/00_orientation.ipynb`. All seven lessons run offline using a
fictional Nation and synthetic data. Work through the exercises and review the
draft artifacts under `outputs/teaching/`. Automatic execution does not establish
approval, complete an exercise, or return findings to a community.

For a working project, follow `docs/adaptation_guide.md`. `nation.yaml` takes
precedence over the teaching example. Configuration errors are explicit.

```sh
python -m toolkit.governance --config config/nation.yaml --validate
pytest
pytest --nbmake Notebooks --nbmake-timeout=180
ruff check toolkit tests
```

Never commit actual restricted data or evidence. `.gitignore` does not protect
already tracked files or enforce storage access. Use Nation-approved systems.
