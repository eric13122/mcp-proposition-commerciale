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
Voici les roles disponibles avec leurs TJM par defaut :

| Role | TJM (EUR HT) | Categorie |
|------|---------------|-----------|
| Directeur Conseil general | 1200 | Direction |
| Directeur Communication | 1100 | Direction |
| Directeur Marketing | 1100 | Direction |
| Directeur Artistique | 1000 | Direction |
| Directeur Projet | 1000 | Direction |
| Directeur conseil SEO | 1100 | Direction |
| Directeur Scientifique | 1200 | Direction |
| DSI | 1100 | Direction |
| Responsable Marketing | 850 | Management |
| Responsable de projet Site internet | 850 | Management |
| Responsable controle qualite Site internet | 800 | Management |
| Responsable Google My Business | 750 | Management |
| Responsable editorial | 800 | Management |
| Growth Marketing Manager | 850 | Management |
| Chef de projet Digital | 750 | Projet |
| Chef de projet Design | 750 | Projet |
| Chef de projet Social Media | 700 | Projet |
| Chef de Projet Ads | 750 | Projet |
| Chef de projet SEO junior | 600 | Projet |
| Chef de projet Data & Reporting | 750 | Projet |
| Chef de projet Technique senior | 850 | Projet |
| Chef de Projet Production audiovisuelle | 800 | Projet |
| Chef de projet Redaction | 700 | Projet |
| Assistant Responsable Marketing | 550 | Projet |
| Expert SEA | 800 | Expertise |
| Expert SEO technique | 800 | Expertise |
| Expert Social Ads | 750 | Expertise |
| Expert Social Media | 700 | Expertise |
| Lead developpeur | 900 | Tech |
| Developpeur / Integrateur senior | 800 | Tech |
| Developpeur / Integrateur junior | 550 | Tech |
| UX designer | 800 | Design |
| Webdesigner senior | 750 | Design |
| Webdesigner junior | 500 | Design |
| Designer 3D senior | 800 | Design |
| Graphiste Crea | 700 | Design |
| Graphiste Exe | 550 | Design |
| Concepteur Redacteur | 700 | Contenu |
| Redacteur | 550 | Contenu |
| Operateur de saisie | 350 | Contenu |
| Community Manager | 600 | Social |
| Community Manager junior | 450 | Social |
| Realisateur | 900 | Production |
| Cadreur | 700 | Production |
| Monteur | 650 | Production |
| Motion Designer 3D Crea | 800 | Production |
| Motion Designer 3D Exe | 600 | Production |
| Motion Designer 2D Crea | 750 | Production |
| Motion Designer 2D Exe | 550 | Production |

## Exemples de calcul pour les slides de pricing

### Prestation ponctuelle (setup)
```
Audit SEO : Expert SEO technique x 14h = 14/7 * 800 = 1 600 EUR HT
Site web : Webdesigner senior x 35h + Dev senior x 28h
         = (35/7 * 750) + (28/7 * 800) = 3 750 + 3 200 = 6 950 EUR HT
```

### Prestation mensuelle (recurrente)
```
Social Media : Community Manager x 21h/mois = 21/7 * 600 = 1 800 EUR HT/mois
SEO : Expert SEO x 14h/mois = 14/7 * 800 = 1 600 EUR HT/mois
```

## Notes

- Les TJM sont des tarifs de vente (pas des couts de revient)
- Arrondir les totaux au multiple de 50 EUR le plus proche pour les slides
- Le budget mensuel moyen pour un client mid-market est de 3 000 - 8 000 EUR HT
- Les prestations ponctuelles (audit, branding, site) sont facturees en one-shot
- Les prestations recurrentes (SEO, social, ads) sont facturees mensuellement
