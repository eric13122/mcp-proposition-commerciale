# Charte Graphique Antipodes Medical

## Couleurs

| Role | Hex | Usage |
|------|-----|-------|
| Bleu marine principal | #1E2044 | Fonds des slides de section, texte titre |
| Texte sombre | #0A1846 | Texte courant sur fond blanc |
| Bleu accent lavande | #8B9FD4 | Fonds des slides d'accent/transition |
| Blanc | #FFFFFF | Fonds de contenu, texte sur fond sombre |
| Noir texte | #000000 / #333333 | Texte secondaire |

## Polices

| Police | Usage | Tailles courantes |
|--------|-------|-------------------|
| Poppins SemiBold | Titres de couverture et section | 19-28pt |
| Raleway | Titres de contenu, sous-titres | 12-18pt |
| Raleway Bold | Sous-titres gras dans le corps | 12pt |
| Montserrat | Accents, badges | 10-14pt |

## Regles visuelles

- Les slides de section (fond sombre) utilisent le watermark "M" cursif en arriere-plan
- Les slides d'accent utilisent un fond bleu lavande #8B9FD4
- Les slides de contenu ont un fond blanc avec le logo "M" en filigrane en bas
- Le logo Antipodes Medical apparait sur la slide de couverture et de cloture
- Les titres sont toujours en MAJUSCULES
- L'interligne standard est 115% (spcPct val="115000")
- L'espacement avant paragraphe est 12pt (spcBef spcPts val="1200")

## Codes couleur XML

Dans le XML des slides, les couleurs sont referencees ainsi :
- `<a:srgbClr val="0A1846"/>` — texte sombre
- `<a:srgbClr val="FFFFFF"/>` — texte blanc
- `<a:srgbClr val="1E2044"/>` — bleu marine
- Attribut `b="1"` sur `<a:rPr>` pour le gras
