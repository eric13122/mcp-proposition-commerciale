# Structure Type d'une Proposition Commerciale

## Plan standard

```
PARTIE 1 — L'AGENCE (standard, peu modifie)
  1. TITLE (slide1)               -> Couverture avec nom du client
  2. AGENCE_INTRO (slide2)        -> Notre Agence
  3. AGENCE_FORCES (slide4)       -> Nos Forces
  4. SECTION_DARK_DESC (slide7)   -> Notre Equipe / Expertise
  5. PROCESS_DIAGRAM (slide9)     -> Prise en charge integrale
  6. LOGO_GRID (slide11)          -> References

PARTIE 2 — LE PROJET CLIENT (100% personnalise)
  7. SECTION_DARK (slide22)       -> "[CLIENT] / Votre Projet"
  8-N. CONTENT_TEXT (xN)          -> Contexte, enjeux, objectifs

PARTIE 3 — LA RECOMMANDATION (personnalise)
  N+1. SECTION_DARK (slide22)    -> "[CLIENT] / Notre Recommandation"
  Pour chaque levier :
    - SECTION_ACCENT (slide28)   -> Titre du levier
    - CONTENT_* (variable)       -> Detail du levier

PARTIE 4 — LE BUDGET (personnalise)
  M. SECTION_DARK_BUDGET (slide57)  -> Proposition budgetaire
  M+1 a M+N. PRICING_TABLE         -> Un tableau par categorie
  M+N+1. BUDGET_TABLE (slide87)     -> Recapitulatif
  DERNIER. CLOSING (slide93)        -> Merci
```

## Mapping Leviers -> Layouts

| Levier | Layout recommande | Slide master a dupliquer |
|--------|-------------------|--------------------------|
| Branding / Identite | CONTENT_TEXT | slide24.xml |
| Audit & Analyse | CONTENT_BULLETS | slide16.xml |
| Site Internet | CONTENT_FEATURE | slide19.xml |
| SEO / Referencement | CONTENT_STRUCTURED | slide29.xml |
| Social Media | CONTENT_STRUCTURED | slide29.xml |
| Social Selling | CONTENT_3COL | slide38.xml |
| Nurturing / Emailing | CONTENT_3COL | slide38.xml |
| Webinaires / Lead Magnet | CONTENT_3COL | slide38.xml |
| Landing Pages | CONTENT_STRUCTURED | slide29.xml |
| Google Ads | CONTENT_TEXT | slide24.xml |
| Social Ads (Meta/LinkedIn) | CONTENT_STRUCTURED | slide29.xml |
| E-commerce | CONTENT_2COL | slide48.xml |
| Production audiovisuelle | CONTENT_FEATURE | slide19.xml |
| Exemples / Cas | CONTENT_EXAMPLES | slide40.xml |

## Regles de construction

1. **Toujours commencer par la couverture** (slide1) et **finir par MERCI** (slide93)
2. **Chaque levier** est precede d'une slide d'accent (SECTION_ACCENT = slide28)
3. **Les slides de section sombre** (slide22) separent les grandes parties
4. **Les tableaux de prix** : un PRICING_TABLE_PONCTUEL (slide64) pour le setup,
   un PRICING_TABLE_MENSUEL (slide65) pour les recurrents
5. **Le recap budget** (slide87) totalise toutes les lignes
6. **Dupliquer** les slides autant que necessaire — ne jamais modifier les originaux
   du template, toujours travailler sur des copies
