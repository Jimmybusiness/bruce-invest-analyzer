# 📈 Bruce Invest Analyzer

Application d'analyse boursière mobile-first avec scoring intelligent et avis personnalisé.

## Fonctionnalités

- **Recherche d'entreprises** : Recherche en temps réel avec auto-complétion Yahoo Finance
- **Données financières clés** : Prix actuel, dividende par action, rendement, ratio P/E
- **Score Bruce** : Scoring intelligent sur 10 basé sur la valorisation et le rendement
- **Graphique interactif** : Historique du cours sur 1 an avec Plotly
- **Avis de Bruce** : Analyse automatique avec verdict personnalisé
- **Design dark mode** : Interface moderne iOS-like, optimisée mobile

## Métriques analysées

| Métrique | Description |
|----------|-------------|
| Prix Actuel | Cours de l'action en temps réel |
| Dividende/Action | Montant du dividende annuel par action |
| Rendement | Pourcentage de rendement du dividende |
| Ratio P/E | Price-to-Earnings ratio (valorisation) |
| Score Bruce | Note globale sur 10 |

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technologies

- Python 3.10+
- Streamlit
- yfinance (données Yahoo Finance)
- Plotly (graphiques interactifs)
- Requests

## Licence

MIT