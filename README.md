# eThekwini 2026 Local Government Election ML Project

## Deliverables
- `ethekwini_2026_election_analysis.ipynb` — reproducible analysis notebook.
- `app.py` — professional Streamlit dashboard.
- `requirements.txt` — Python dependencies.
- `data/raw/README_DATA.md` — exact data requirements and official acquisition sources.
- `outputs/` — generated model outputs and charts after the notebook is run.

## Research question
Using historically comparable electoral, demographic and voter-registration data, estimate party vote shares, ward-level leading parties and voter turnout for the 4 November 2026 local government election in eThekwini Metropolitan Municipality.

## Critical geographic rule
Do NOT join 2021, 2024 and 2026 data by ward number alone. The notebook requires a geographic crosswalk based on voting districts / spatial overlap. It classifies each relationship as EXACT, AGGREGATED, DISAGGREGATED or UNRESOLVED and excludes unresolved units from ward-level comparison.

## Important election-type rule
2021 is a Local Government Election. 2024 is a National and Provincial Election. 2024 results are therefore treated as a historical political-signal feature, not as a directly comparable municipal vote.

## Required raw files
Place the following in `data/raw/` after downloading them from the official sources listed in `README_DATA.md`:

1. `lge2021_ethekwini_vd.csv`
2. `npe2024_ethekwini_vd.csv`
3. `registration_2021_2026.csv`
4. `census2022_ward.csv`
5. `vd_2021.csv`
6. `vd_2024.csv`
7. `vd_2026.csv`
8. `ward_2021.csv`
9. `ward_2026.csv`
10. `candidates_2026.csv` (optional; independent candidates are included only if supported)

The notebook validates schemas and stops with a clear message if required fields are absent.

## Execution
### Jupyter
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook
```
Open `ethekwini_2026_election_analysis.ipynb` and run all cells from top to bottom.

### Streamlit
```bash
streamlit run app.py
```

The dashboard reads the CSV files created by the notebook in `outputs/`.

## Required output distinction
The notebook labels:
- HISTORICAL OBSERVATION
- DERIVED / ALIGNED HISTORICAL ESTIMATE
- 2026 MODEL OUTPUT

No 2026 result is presented as an observed fact.

## Modelling
- Party vote share: Random Forest regression, with Linear Regression benchmark.
- Ward leader: Random Forest multiclass classification.
- Turnout rate: Gradient Boosting regression, with Random Forest benchmark.
- Projected voters = projected turnout rate × latest available 2026 registered voters.
- Party shares are non-negative and normalised to sum to 100%.
- Validation is time-aware/backtested rather than relying only on a random train/test split.

## Coalition wording
The dashboard reports only whether the projected vote distribution crosses a mathematical 50% threshold. It does NOT predict coalition negotiations or who will govern.
