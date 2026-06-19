# Software Metrics Lab (LR-5 + LR-6)

Unified Streamlit app for code complexity audit and architecture metrics.

## Modules

| Lab | Metrics |
|-----|---------|
| **LR-5** | Halstead (V, D, E, B), McCabe V(G) + CFG, Chapin Q |
| **LR-6** | Lorenz & Kidd SI, CK, MOOD, UCP, PERT |

## Run

```bash
pip install -r app/requirements.txt
streamlit run app/main.py
```

## Presets

- **LR-5:** бічна панель → *Load LR-5 demo code* (`process_bulk_orders`)
- **LR-6:** бічна панель → *Load CryptoWallet preset (v13)*

## Structure

```
app/
├── main.py           # unified navigation
├── presets.py        # CryptoWallet v13 + LR-5 demo code
├── metrics/          # pure calculation modules
│   ├── halstead.py
│   ├── mccabe.py
│   ├── chapin.py
│   └── ...
└── views/
    └── lr5_audit.py  # LR-5 UI
```
