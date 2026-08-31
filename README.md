# iclr_simulations

Contains internal development code for Imperial College London Rocketry Simulations, repo based off a public cookiecutter

## Project Organisation

```text
├── Makefile           <- Makefile with convenience commands like `make paper` and `make slides`
├── README.md          <- The top-level README for this project.
├── data
│   ├── intermediate   <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         iclr_simulations and configuration for tools like ruff
│
├── references         <- Bibliography and citation style
│
├── output             <- Generated outputs like figures and tables as HTML, PDF, LaTeX, etc.
│
├── project_config     <- Global config settings for the project, eg visualisation settings
│
└── src
    └── iclr_simulations        <- Source code for use in this project.
        │
        ├── __init__.py                     <- Makes iclr_simulations a Python module
        │
        └── iclr_simulations.py <- main script
```

--------
