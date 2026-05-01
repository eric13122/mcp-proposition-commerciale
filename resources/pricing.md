# Grille Tarifaire Antipodes Medical

## Formule de calcul

```
Cout de vente = THH (heures) / 7 (heures/jour) * TJM (tarif journalier)
```

- **THH** : Total Heures allouees a la prestation
- **TJH** : Equivalent en jours (THH / 7)
- **TJM** : Tarif Journalier Moyen de la ressource

## Roles et TJM

Les tarifs journaliers sont configures dans le fichier `config/pricing.json`.
Source : Grille TJM officielle Antipodes Medical.

| Role | TJM (EUR HT) | Pole |
|------|---------------|------|
| Directeur Conseil general | 1450 | Direction |
| Directeur Communication | 1250 | Marketing |
| Directeur Marketing | 1250 | Marketing |
| Directeur Artistique | 1250 | Marketing |
| Directeur Projet | 1150 | Marketing |
| Growth Marketing Manager | 1250 | Marketing |
| Concepteur Redacteur | 950 | Marketing |
| Expert SEA | 950 | Marketing |
| Expert Social Ads | 950 | Marketing |
| Responsable Marketing | 950 | Marketing |
| Chef de Projet Ads | 750 | Marketing |
| Assistant Responsable Marketing | 400 | Marketing |
| Directeur conseil SEO | 1150 | SEO |
| Expert SEO technique | 850 | SEO |
| Chef de projet Data & Reporting | 650 | SEO |
| Responsable Google My Business | 650 | SEO |
| Chef de projet Digital | 650 | SEO |
| Chef de projet SEO junior | 550 | SEO |
| Operateur de saisie | 350 | SEO |
| Webdesigner senior | 750 | Design |
| UX designer | 750 | Design |
| Chef de projet Design | 650 | Design |
| Webdesigner junior | 550 | Design |
| Graphiste Crea | 850 | Design |
| Graphiste Exe | 700 | Design |
| Expert Social Media | 850 | Social Media |
| Chef de projet Social Media | 750 | Social Media |
| Community Manager | 650 | Social Media |
| Community Manager junior | 450 | Social Media |
| Realisateur | 950 | Audiovisuel |
| Motion Designer 3D Crea | 850 | Audiovisuel |
| Chef de Projet Production audiovisuelle | 750 | Audiovisuel |
| Cadreur | 750 | Audiovisuel |
| Motion Designer 2D Crea | 750 | Audiovisuel |
| Designer 3D senior | 750 | Audiovisuel |
| Monteur | 600 | Audiovisuel |
| Motion Designer 3D Exe | 550 | Audiovisuel |
| Motion Designer 2D Exe | 450 | Audiovisuel |
| DSI | 1250 | Technique |
| Lead developpeur | 850 | Technique |
| Chef de projet Technique senior | 750 | Technique |
| Developpeur / Integrateur senior | 750 | Technique |
| Developpeur / Integrateur junior | 650 | Technique |
| Directeur Scientifique | 1250 | Redaction |
| Chef de projet Redaction | 750 | Redaction |
| Responsable editorial | 750 | Redaction |
| Redacteur | 650 | Redaction |
| Responsable de projet Site internet | 750 | Site internet |
| Responsable controle qualite Site internet | 750 | Site internet |

## Exemples de calcul pour les slides de pricing

### Prestation ponctuelle (setup)
```
Audit SEO : Expert SEO technique x 14h = 14/7 * 850 = 1 700 EUR HT
Site web : Webdesigner senior x 35h + Dev senior x 28h
         = (35/7 * 750) + (28/7 * 750) = 3 750 + 3 000 = 6 750 EUR HT
```

### Prestation mensuelle (recurrente)
```
Social Media : Community Manager x 21h/mois = 21/7 * 650 = 1 950 EUR HT/mois
SEO : Expert SEO x 14h/mois = 14/7 * 850 = 1 700 EUR HT/mois
```

## Notes

- Les TJM sont des tarifs de vente (pas des couts de revient)
- Arrondir les totaux au multiple de 50 EUR le plus proche pour les slides
- Le budget mensuel moyen pour un client mid-market est de 3 000 - 8 000 EUR HT
- Les prestations ponctuelles (audit, branding, site) sont facturees en one-shot
- Les prestations recurrentes (SEO, social, ads) sont facturees mensuellement
