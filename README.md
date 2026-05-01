# Proposition Commerciale MCP Server

Serveur MCP (Model Context Protocol) pour générer des propositions commerciales Antipodes Médical au format PPTX. Compatible avec Claude Desktop, Cursor, Windsurf, et tout client MCP.

## Installation

### Option 1 : npm (recommandé)

```bash
npm install -g @antipodes-medical/mcp-proposition-commerciale
```

### Option 2 : depuis les sources

```bash
git clone https://github.com/antipodes-medical/mcp-proposition-commerciale.git
cd mcp-proposition-commerciale
pip install -r requirements.txt
```

### Option 3 : Docker

```bash
docker pull antipodesmedical/mcp-proposition-commerciale
docker run -p 8000:8000 antipodesmedical/mcp-proposition-commerciale
```

## Configuration client MCP

### Mode local (stdio)

```json
{
  "mcpServers": {
    "proposition-commerciale": {
      "command": "npx",
      "args": ["-y", "@antipodes-medical/mcp-proposition-commerciale"]
    }
  }
}
```

Ou avec Python directement :

```json
{
  "mcpServers": {
    "proposition-commerciale": {
      "command": "python",
      "args": ["/chemin/vers/server.py"]
    }
  }
}
```

### Mode cloud (SSE) — accès distant sans installation

Si le serveur est déployé sur le cloud (ex: https://votre-serveur.render.com) :

```json
{
  "mcpServers": {
    "proposition-commerciale": {
      "url": "https://votre-serveur.render.com/sse"
    }
  }
}
```

## Déploiement cloud

### Render (un clic)

1. Fork le repo GitHub
2. Connecter Render au repo
3. Le fichier `render.yaml` configure tout automatiquement
4. L'URL SSE sera : `https://votre-app.onrender.com/sse`

### Docker

```bash
docker build -t proposition-commerciale-mcp .
docker run -p 8000:8000 proposition-commerciale-mcp
```

### Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport : `stdio`, `sse`, ou `streamable-http` |
| `MCP_HOST` | `0.0.0.0` | Host d'écoute (mode SSE) |
| `MCP_PORT` | `8000` | Port d'écoute (mode SSE) |
| `PROPOSITION_WORK_DIR` | `/tmp` | Répertoire de travail pour les sessions |

## Outils disponibles (10)

| Outil | Description |
|-------|-------------|
| `preparer_template` | Copie et décompresse le master template |
| `dupliquer_slide` | Duplique une slide existante |
| `ordonner_slides` | Définit l'ordre des slides dans la présentation |
| `editer_contenu` | Remplace du texte dans une slide |
| `lire_slide` | Lit le contenu textuel d'une slide |
| `lire_xml_brut` | Retourne le XML complet d'une slide |
| `ecrire_xml` | Écrit le XML complet d'une slide |
| `calculer_budget` | Calcule les coûts à partir de la grille tarifaire |
| `empaqueter_pptx` | Génère le fichier PPTX final |
| `lister_sessions` | Liste les sessions de travail |

## Ressources disponibles (5)

| URI | Description |
|-----|-------------|
| `proposition://catalogue` | Catalogue des 21 types de slides |
| `proposition://charte` | Charte graphique (couleurs, polices) |
| `proposition://structure` | Structure type d'une proposition |
| `proposition://guide-edition` | Guide d'édition XML |
| `proposition://pricing` | Grille tarifaire (rôles, TJM) |

## Personnalisation des tarifs

Les TJM sont dans `config/pricing.json`. Modifier les valeurs pour correspondre à vos tarifs :

```json
{
  "heures_par_jour": 7,
  "roles": {
    "Expert SEO technique": {"tjm": 800, "categorie": "Expertise"},
    "Webdesigner senior": {"tjm": 750, "categorie": "Design"}
  }
}
```

## Workflow typique

1. L'IA lit les ressources (catalogue, charte, structure, pricing)
2. `preparer_template("nom-client")` → répertoire de travail
3. `dupliquer_slide(dir, "slide24.xml")` × N → créer les slides
4. `ordonner_slides(dir, [...])` → définir l'ordre
5. `editer_contenu(dir, "slide1.xml", "CLINIQUE DU CHATEAU", "NOM CLIENT")` × N
6. `calculer_budget([...])` → calculer les prix
7. `empaqueter_pptx(dir, "proposition-client.pptx")` → fichier final
