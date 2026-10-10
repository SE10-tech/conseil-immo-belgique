# Crédit hypothécaire et frais de notaire en Belgique — Référence

**Sommaire** : 1. Frais d'achat (acte de vente) · 2. Frais d'acte de crédit · 3. Barème des honoraires de notaire · 4. Capacité d'emprunt et quotité · 5. Processus d'achat (offre, compromis, acte) · 6. Commission d'agence

## 1. Frais d'achat à charge de l'acheteur

| Poste | Ordre de grandeur |
|---|---|
| Droits d'enregistrement | 2-3 % (hab. propre) à 12-12,5 % selon région/usage — voir fiscalite.md |
| Honoraires du notaire | Barème légal dégressif (voir §3) + TVA 21 % sur honoraires |
| Frais administratifs / débours (recherches hypothécaires, extraits cadastraux, urbanistiques) | ~ 800-1 500 € |
| Transcription hypothécaire | forfait ~ 220-270 € |

Règle rapide : « frais d'acte » ≈ droits + ~1-1,5 % du prix (hors droits). Les droits d'enregistrement se paient sur fonds propres (non finançables via le crédit en pratique).

## 2. Frais d'acte de crédit (si emprunt)

Calculés sur le montant emprunté (et non le prix) :

| Poste | Taux |
|---|---|
| Droit d'enregistrement hypothécaire | 1 % du montant inscrit |
| Droit d'hypothèque (bureau des hypothèques) | 0,3 % |
| Honoraires notaire (acte de crédit) | barème spécifique + TVA 21 % |
| Frais divers (hypothécaire, dossier) | ~ 700-1 200 € |

Règle rapide : **~ 2 à 3 % du montant emprunté** pour l'acte de crédit avec inscription hypothécaire (le mandat hypothécaire, quand accepté, réduit fortement ce coût).

## 3. Barème légal des honoraires de notaire (acte de vente, dégressif par tranches)

| Tranche du prix | Taux |
|---|---|
| 0 – 7 500 € | 4,56 % |
| 7 500 – 17 500 € | 2,85 % |
| 17 500 – 30 000 € | 2,28 % |
| 30 000 – 45 495 € | 1,71 % |
| 45 495 – 64 500 € | 1,14 % |
| 64 500 – 250 095 € | 0,57 % |
| > 250 095 € | 0,057 % |

+ TVA 21 % sur les honoraires. Le script `calcul_immo.py` intègre ce barème.

## 4. Capacité d'emprunt

- **Quotité** (montant emprunté / valeur du bien) : souvent ≤ 90 % ; > 100 % rare et réservé aux très bons dossiers (normes Banque Nationale). Les droits et frais viennent en principe des fonds propres.
- **Taux d'endettement** : règle pratique ≈ charges de crédit ≤ 1/3 des revenus nets du ménage.
- **Durées usuelles** : 10, 15, 20, 25 ans (max ~30 ans).
- **Types** : taux fixe (majoritaire en Belgique), variable (formules 1/1/1, 5/5/5, 10/5/5 — caps légaux : max doublement du taux initial).
- Rechercher les taux actuels (voir sources-donnees.md §6) avant toute simulation présentée comme « actuelle ».
- **Réemploi de crédit / refinancement** : frais de mainlevée + wederbeleggingsvergoeding (pénalité max 3 mois d'intérêts).

## 5. Processus d'achat belge

1. **Offre d'achat** (écrite, souvent via l'agence) — engageante si acceptée : attention aux clauses suspensives (obtention de crédit, permis).
2. **Compromis de vente** — avant-contrat engageant ; clause suspensive de crédit standard : ~ 4-6 semaines, montant précisé ; indemnité de dédit usuelle 10 %.
3. **Acte notarié** — dans les ~ 4 mois du compromis ; paiement du solde + droits + frais chez le notaire.
4. Enregistrement de l'acte et transcription hypothécaire.

Vérifications avant compromis : PEB obligatoire, certificat d'urbanisme, état du sol (OVAM/Brufossol — attestations de sol obligatoires), conformité électrique (contrôle obligatoire à la vente), infractions urbanistiques, servitudes.

## 6. Commission d'agence

- En général **à charge du vendeur** : ~ 3 % HTVA du prix (2-3,5 % usuel, négociable) + 21 % TVA.
- Honoraires de location (mise en location) : souvent 1 mois de loyer + TVA à charge du bailleur (les « frais d'agence » à charge du locataire sont interdits pour la résidence principale dans les 3 régions).
