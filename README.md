# Conseil Immo Belgique 🇧🇪

Skill IA (format `SKILL.md`) de **conseil immobilier spécialisé dans le marché belge** — compatible Kimi, Claude Code et tout agent supportant le format Agent Skills.

Adapté du projet [ai-realestate-claude](https://github.com/zubair-trabzada/ai-realestate-claude) (marché US) vers le contexte belge : trois régions, trois fiscalités, PEB, revenu cadastral, notaire.

## Fonctionnalités

- **Analyse complète d'un bien** avec score 0-100 pondéré pour la Belgique (prix vs comparables, PEB, rendement, quartier, marché local)
- **Estimation par comparables** (prix au m² par commune)
- **Rendement locatif** brut et net (précompte immobilier, vacance, entretien)
- **Simulation de crédit hypothécaire** et frais d'acte
- **Frais d'achat par région** — droits d'enregistrement 2026 :

| Région | Habitation propre et unique | Autre achat |
|---|---|---|
| Wallonie | 3 % | 12,5 % |
| Bruxelles | Abattement 200 000 € | 12,5 % |
| Flandre | 2 % | 12 % |

- **Analyse de commune/quartier** (Statbel, criminalité, écoles, mobilité)
- **Rédaction d'annonces** immobilières professionnelles

## Structure

```
├── SKILL.md                        # Orchestrateur principal (FR)
├── references/
│   ├── fiscalite.md                # Droits d'enregistrement, PrI, RC, plus-values, baux
│   ├── sources-donnees.md          # Statbel, Immoweb, Realo, grilles de loyers...
│   └── credit-notaire.md           # Barème notaire, acte de crédit, compromis
└── scripts/
    └── calcul_immo.py              # Calculs déterministes (frais, crédit, rendement)
```

## Utilisation du script

```bash
# Frais d'achat (droits + notaire) par région
python3 scripts/calcul_immo.py frais --prix 350000 --region wallonie --propre

# Mensualité et frais d'acte de crédit
python3 scripts/calcul_immo.py credit --montant 300000 --taux 3.1 --duree 20

# Rendement locatif brut et net
python3 scripts/calcul_immo.py rendement --prix 350000 --region bruxelles --loyer 1400 --rc 1200

# Analyse financière complète avec cash-flow
python3 scripts/calcul_immo.py complet --prix 350000 --region flandre --montant 280000 --taux 3.1 --duree 20 --loyer 1400 --rc 1200
```

## Installation

- **Kimi** : Paramètres → Skills → Importer le dossier (ou le fichier `.skill` packagé)
- **Claude Code** : copier le dossier dans `~/.claude/skills/conseil-immo-belgique/`

## Avertissement

Skill fourni à titre informatif uniquement — **pas un conseil financier, fiscal ou juridique**. La fiscalité régionale belge évolue fréquemment : vérifier les chiffres auprès d'un notaire avant toute décision. Chiffres fiscaux vérifiés au 1er semestre 2026.

## Licence

MIT
