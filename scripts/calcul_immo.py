#!/usr/bin/env python3
"""Calculs immobiliers belges : frais d'achat, crédit hypothécaire, rendement locatif.

Estimations indicatives — la fiscalité régionale évolue ; vérifier avec un notaire.
Chiffres fiscaux vérifiés : 1er semestre 2026.
"""
import argparse

# --- Barème légal des honoraires de notaire (acte de vente, par tranches) ---
BAREME = [
    (7_500, 0.0456), (17_500, 0.0285), (30_000, 0.0228), (45_495, 0.0171),
    (64_500, 0.0114), (250_095, 0.0057), (float("inf"), 0.00057),
]
TVA = 0.21
TAUX_PRI = {"wallonie": 0.0125, "bruxelles": 0.0125, "flandre": 0.025}


def honoraires_notaire(base):
    """Honoraires HTVA selon le barème dégressif légal."""
    total, precedent = 0.0, 0.0
    for plafond, taux in BAREME:
        if base > precedent:
            total += (min(base, plafond) - precedent) * taux
            precedent = plafond
        else:
            break
    return total


def droits_enregistrement(prix, region, propre):
    """Retourne (montant, détail). Hypothèses 2026 — voir references/fiscalite.md."""
    if region == "wallonie":
        taux = 0.03 if propre else 0.125
        return prix * taux, f"Wallonie — taux {'réduit 3 % (habitation propre et unique)' if propre else 'standard 12,5 %'}"
    if region == "bruxelles":
        if propre and prix <= 600_000:
            base = max(0.0, prix - 200_000)
            return base * 0.125, "Bruxelles — 12,5 % avec abattement de 200 000 €"
        return prix * 0.125, "Bruxelles — taux standard 12,5 % (abattement non applicable)"
    # flandre
    if propre:
        montant = prix * 0.02
        note = "Flandre — taux réduit 2 % (enige eigen woning)"
        if prix <= 240_000:
            montant = max(0.0, montant - 1_867)
            note += ", réduction habitation modeste −1 867 €"
        return montant, note
    return prix * 0.12, "Flandre — taux standard 12 %"


def frais_achat(prix, region, propre):
    droits, note = droits_enregistrement(prix, region, propre)
    hon_htva = honoraires_notaire(prix)
    hon_ttc = hon_htva * (1 + TVA)
    debours = 1_150.0  # estimation frais administratifs + transcription
    total = droits + hon_ttc + debours
    lignes = [
        f"Droits d'enregistrement      : {droits:>12,.0f} €  ({note})",
        f"Honoraires notaire (TTC)     : {hon_ttc:>12,.0f} €  (barème légal + TVA 21 %)",
        f"Frais admin./transcription   : {debours:>12,.0f} €  (estimation)",
        f"TOTAL FRAIS D'ACHAT          : {total:>12,.0f} €  ({total / prix * 100:.1f} % du prix)",
        f"Budget total (prix + frais)  : {prix + total:>12,.0f} €",
    ]
    return total, lignes


def mensualite(montant, taux_annuel_pct, duree_ans):
    r = taux_annuel_pct / 100 / 12
    n = duree_ans * 12
    if r == 0:
        return montant / n
    return montant * r / (1 - (1 + r) ** -n)


def frais_acte_credit(montant):
    enreg = montant * 0.01
    hyp = montant * 0.003
    hon_ttc = honoraires_notaire(montant) * (1 + TVA)
    divers = 900.0
    return enreg + hyp + hon_ttc + divers, enreg, hyp, hon_ttc, divers


def cmd_frais(a):
    total, lignes = frais_achat(a.prix, a.region, a.propre)
    print(f"\n=== FRAIS D'ACHAT — {a.prix:,.0f} € ({a.region.capitalize()}"
          f"{', habitation propre et unique' if a.propre else ', investissement/2e résidence'}) ===")
    print("\n".join(lignes))
    print("Estimation indicative — le notaire calcule le montant exact.")


def cmd_credit(a):
    m = mensualite(a.montant, a.taux, a.duree)
    cout = m * a.duree * 12 - a.montant
    frais_cr, enreg, hyp, hon, divers = frais_acte_credit(a.montant)
    print(f"\n=== CRÉDIT HYPOTHÉCAIRE — {a.montant:,.0f} € à {a.taux} % sur {a.duree} ans ===")
    print(f"Mensualité                   : {m:>12,.2f} €")
    print(f"Coût total des intérêts      : {cout:>12,.0f} €")
    print(f"--- Frais d'acte de crédit (estimation) ---")
    print(f"Enregistrement 1 %           : {enreg:>12,.0f} €")
    print(f"Droit d'hypothèque 0,3 %     : {hyp:>12,.0f} €")
    print(f"Honoraires notaire (TTC)     : {hon:>12,.0f} €")
    print(f"Frais divers                 : {divers:>12,.0f} €")
    print(f"TOTAL ACTE DE CRÉDIT         : {frais_cr:>12,.0f} €  ({frais_cr / a.montant * 100:.1f} % du crédit)")
    print("Un mandat hypothécaire (si accepté) réduit fortement ces frais.")


def cmd_rendement(a):
    loyer_an = a.loyer * 12
    frais, _ = frais_achat(a.prix, a.region, a.propre)
    invest = a.prix + frais
    rc_indexe = a.rc * a.coef
    pri = rc_indexe * TAUX_PRI[a.region] * (1 + a.centimes / 100)
    entretien = a.entretien if a.entretien is not None else a.prix * 0.01
    vacance = a.loyer * a.vacance
    charges = a.charges * 12
    net = loyer_an - pri - entretien - vacance - charges
    print(f"\n=== RENDEMENT LOCATIF — {a.prix:,.0f} € ({a.region.capitalize()}), loyer {a.loyer:,.0f} €/mois ===")
    print(f"Rendement brut (prix seul)        : {loyer_an / a.prix * 100:>6.2f} %")
    print(f"Rendement brut (frais inclus)     : {loyer_an / invest * 100:>6.2f} %")
    print(f"--- Charges annuelles estimées ---")
    print(f"Précompte immobilier              : {pri:>10,.0f} € (RC indexé {rc_indexe:,.0f} €, additionnels {a.centimes}c)")
    print(f"Entretien/provision travaux       : {entretien:>10,.0f} €")
    print(f"Vacance locative ({a.vacance:.0f} mois)         : {vacance:>10,.0f} €")
    print(f"Charges propriétaire              : {charges:>10,.0f} €")
    print(f"Revenu net estimé                 : {net:>10,.0f} €/an")
    print(f"RENDEMENT NET (frais inclus)      : {net / invest * 100:>6.2f} %")
    base_imp = rc_indexe * 1.40
    print(f"--- Fiscalité (location à usage privé) ---")
    print(f"Base imposable IPP = RC indexé × 1,40 = {base_imp:,.0f} € (pas les loyers réels),")
    print(f"ajoutée aux autres revenus au taux marginal (jusqu'à ~50 % + additionnels).")


def cmd_complet(a):
    cmd_frais(a)
    if a.montant and a.taux and a.duree:
        cmd_credit(a)
    if a.loyer and a.rc:
        cmd_rendement(a)
        m = mensualite(a.montant, a.taux, a.duree) if a.montant else 0
        if m:
            rc_indexe = a.rc * a.coef
            pri = rc_indexe * TAUX_PRI[a.region] * (1 + a.centimes / 100)
            charges_m = (pri + (a.entretien if a.entretien is not None else a.prix * 0.01)
                         + a.loyer * a.vacance + a.charges * 12) / 12
            cf = a.loyer - m - charges_m
            print(f"\n=== CASH-FLOW MENSUEL ESTIMÉ ===")
            print(f"Loyer {a.loyer:,.0f} € − mensualité {m:,.0f} € − charges {charges_m:,.0f} € = {cf:,.0f} €/mois (avant IPP)")


def main():
    p = argparse.ArgumentParser(description="Calculs immobiliers belges")
    sub = p.add_subparsers(dest="cmd", required=True)

    def commun(s):
        s.add_argument("--prix", type=float, required=True)
        s.add_argument("--region", choices=["wallonie", "bruxelles", "flandre"], required=True)
        s.add_argument("--propre", action="store_true", help="Habitation propre et unique")
        s.add_argument("--invest", action="store_true", help="Investissement (défaut)")

    s = sub.add_parser("frais", help="Frais d'achat (droits + notaire)")
    commun(s)
    s.set_defaults(f=cmd_frais)

    s = sub.add_parser("credit", help="Mensualité et frais d'acte de crédit")
    s.add_argument("--montant", type=float, required=True)
    s.add_argument("--taux", type=float, required=True, help="Taux annuel en %")
    s.add_argument("--duree", type=int, required=True, help="Durée en années")
    s.set_defaults(f=cmd_credit)

    s = sub.add_parser("rendement", help="Rendement locatif brut et net")
    commun(s)
    s.add_argument("--loyer", type=float, required=True, help="Loyer mensuel")
    s.add_argument("--rc", type=float, required=True, help="Revenu cadastral non indexé")
    s.add_argument("--coef", type=float, default=2.24, help="Coefficient d'indexation du RC (à mettre à jour chaque année)")
    s.add_argument("--centimes", type=float, default=2500, help="Centimes additionnels communaux+provinciaux (moyenne ~2000-3500)")
    s.add_argument("--charges", type=float, default=0, help="Charges propriétaire mensuelles")
    s.add_argument("--entretien", type=float, default=None, help="Provision entretien annuelle (défaut: 1 % du prix)")
    s.add_argument("--vacance", type=float, default=1, help="Vacance locative en mois/an")
    s.set_defaults(f=cmd_rendement)

    s = sub.add_parser("complet", help="Frais + crédit + rendement + cash-flow")
    commun(s)
    s.add_argument("--montant", type=float)
    s.add_argument("--taux", type=float)
    s.add_argument("--duree", type=int)
    s.add_argument("--loyer", type=float)
    s.add_argument("--rc", type=float)
    s.add_argument("--coef", type=float, default=2.24)
    s.add_argument("--centimes", type=float, default=2500)
    s.add_argument("--charges", type=float, default=0)
    s.add_argument("--entretien", type=float, default=None)
    s.add_argument("--vacance", type=float, default=1)
    s.set_defaults(f=cmd_complet)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
