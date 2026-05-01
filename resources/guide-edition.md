# Guide d'Edition XML des Slides PPTX

## Principe general

Les fichiers PPTX sont des archives ZIP contenant des fichiers XML.
Le contenu texte se trouve dans les elements `<a:t>` des slides.

## Remplacer du texte simple

Utiliser l'outil `editer_contenu` avec le texte exact a chercher.
Exemple : remplacer "CLINIQUE DU CHATEAU" par "MON CLIENT" dans slide1.xml.

## Entites XML obligatoires

Le XML ne tolere pas certains caracteres bruts. Toujours utiliser :

| Caractere | Entite XML |
|-----------|------------|
| & | `&amp;` |
| < | `&lt;` |
| > | `&gt;` |
| " | `&quot;` |
| ' (apostrophe courbe) | `&#x2019;` |
| euro | `&#x20AC;` |
| e accent aigu | `&#xE9;` |
| e accent grave | `&#xE8;` |
| a accent grave | `&#xE0;` |
| oe ligature | `&#x153;` |

## Structure XML d'un texte

```xml
<a:p>                          <!-- Paragraphe -->
  <a:pPr algn="l">            <!-- Proprietes paragraphe -->
    <a:lnSpc>
      <a:spcPct val="115000"/> <!-- Interligne 115% -->
    </a:lnSpc>
    <a:spcBef>
      <a:spcPts val="1200"/>   <!-- Espacement avant 12pt -->
    </a:spcBef>
  </a:pPr>
  <a:r>                        <!-- Run (segment de texte) -->
    <a:rPr lang="fr" sz="1200" b="1">  <!-- Proprietes : taille, gras -->
      <a:solidFill>
        <a:srgbClr val="0A1846"/>      <!-- Couleur -->
      </a:solidFill>
      <a:latin typeface="Raleway"/>     <!-- Police -->
    </a:rPr>
    <a:t>MON TEXTE ICI</a:t>           <!-- Le texte visible -->
  </a:r>
</a:p>
```

## Regles d'edition

1. **Garder les `<a:rPr>` existants** — ne pas changer taille, police, couleur
2. **Pour les sous-titres gras** : `b="1"` sur `<a:rPr>`
3. **Separer les paragraphes** avec des elements `<a:p>` distincts
4. **Copier le `<a:pPr>`** du paragraphe original pour l'interligne
5. **Ne jamais utiliser de bullets unicode** — utiliser `<a:buChar>` ou `<a:buNone>`
6. **Saut de ligne dans un paragraphe** : utiliser `<a:br/>` entre deux `<a:r>`

## Tableaux de prix

Les tableaux utilisent `<a:tbl>` avec des lignes `<a:tr>` et cellules `<a:tc>`.
Pour modifier un tableau :
- Utiliser `lire_xml_brut` pour voir la structure
- Modifier les `<a:t>` dans chaque `<a:tc>`
- Dupliquer ou supprimer des `<a:tr>` pour ajuster le nombre de lignes
- Utiliser `ecrire_xml` pour reecrire la slide complete

## Workflow recommande

1. `lire_slide` pour voir les textes existants
2. `editer_contenu` pour les remplacements simples (titre, nom client)
3. `lire_xml_brut` + `ecrire_xml` pour les modifications complexes (tableaux)
4. Verifier avec `lire_slide` apres chaque modification
