"""
Serveur MCP — Générateur de Propositions Commerciales Antipodes Médical

Ce serveur expose des outils et ressources permettant à n'importe quelle IA
compatible MCP de construire des présentations PowerPoint (.pptx) professionnelles
à partir d'un brief client texte.

Workflow typique pour l'IA cliente :
  1. Lire les ressources (catalogue, charte, structure, guide-edition)
  2. preparer_template() → obtenir un répertoire de travail
  3. dupliquer_slide() × N → créer les slides nécessaires
  4. ordonner_slides() → définir l'ordre final
  5. editer_contenu() × N → injecter le contenu du brief
  6. empaqueter_pptx() → générer le fichier final
  7. (optionnel) lire_slide() pour vérifier le contenu
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SERVER_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = SERVER_DIR / "assets"
SCRIPTS_DIR = SERVER_DIR / "scripts"
MASTER_TEMPLATE = ASSETS_DIR / "master_template.pptx"

# Répertoire de travail pour les sessions (configurable via env)
WORK_DIR = Path(os.environ.get(
    "PROPOSITION_WORK_DIR",
    tempfile.gettempdir()
)) / "proposition-commerciale-sessions"

# ---------------------------------------------------------------------------
# Serveur MCP
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "proposition-commerciale",
    instructions=(
        "Générateur de propositions commerciales Antipodes Médical. "
        "Fournit des outils pour construire des présentations PPTX "
        "professionnelles à partir d'un brief client. "
        "Commencez par lire les ressources (catalogue, charte, structure, "
        "guide-edition, pricing) pour comprendre les layouts, règles et tarifs."
    ),
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8000")),
)

# ---------------------------------------------------------------------------
# Ressources
# ---------------------------------------------------------------------------

@mcp.resource("proposition://catalogue")
def resource_catalogue() -> str:
    """Catalogue des 21 types de slides disponibles dans le master template."""
    path = SERVER_DIR / "resources" / "catalogue.md"
    return path.read_text(encoding="utf-8")


@mcp.resource("proposition://charte")
def resource_charte() -> str:
    """Charte graphique Antipodes Médical : couleurs, polices, règles visuelles."""
    path = SERVER_DIR / "resources" / "charte.md"
    return path.read_text(encoding="utf-8")


@mcp.resource("proposition://structure")
def resource_structure() -> str:
    """Structure type d'une proposition commerciale et mapping leviers → layouts."""
    path = SERVER_DIR / "resources" / "structure.md"
    return path.read_text(encoding="utf-8")


@mcp.resource("proposition://guide-edition")
def resource_guide_edition() -> str:
    """Guide technique d'édition XML des slides PPTX."""
    path = SERVER_DIR / "resources" / "guide-edition.md"
    return path.read_text(encoding="utf-8")


@mcp.resource("proposition://pricing")
def resource_pricing() -> str:
    """Grille tarifaire : rôles, TJM, formules de calcul, exemples."""
    path = SERVER_DIR / "resources" / "pricing.md"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

@mcp.tool()
def preparer_template(session_name: str = "default") -> str:
    """Copie et décompresse le master template dans un répertoire de travail.

    Args:
        session_name: Nom de la session (pour identifier le projet).

    Returns:
        JSON avec le chemin du répertoire de travail (working_dir)
        et la liste des slides disponibles dans le template.
    """
    session_dir = WORK_DIR / session_name
    unpacked_dir = session_dir / "unpacked"

    # Nettoyer si une session précédente existe
    if session_dir.exists():
        shutil.rmtree(session_dir)
    session_dir.mkdir(parents=True)

    # Copier le template
    template_copy = session_dir / "master_template.pptx"
    shutil.copy2(MASTER_TEMPLATE, template_copy)

    # Décompresser
    unpacked_dir.mkdir()
    with zipfile.ZipFile(template_copy, "r") as zf:
        zf.extractall(unpacked_dir)

    # Pretty-print XML pour faciliter l'édition
    _pretty_print_all_xml(unpacked_dir)

    # Lister les slides existantes
    slides_dir = unpacked_dir / "ppt" / "slides"
    slides = sorted(
        f.name for f in slides_dir.glob("slide*.xml")
        if re.match(r"slide\d+\.xml", f.name)
    )

    return json.dumps({
        "working_dir": str(unpacked_dir),
        "template_copy": str(template_copy),
        "slides": slides,
        "message": f"Template prêt dans {unpacked_dir}. {len(slides)} slides disponibles."
    }, ensure_ascii=False)


@mcp.tool()
def dupliquer_slide(working_dir: str, source_slide: str) -> str:
    """Duplique une slide existante pour créer une nouvelle slide.

    Args:
        working_dir: Chemin du répertoire unpacké (retourné par preparer_template).
        source_slide: Nom du fichier slide à dupliquer (ex: "slide24.xml").

    Returns:
        JSON avec le nom de la nouvelle slide, le sldId à ajouter
        dans presentation.xml, et les instructions.
    """
    unpacked = Path(working_dir)
    slides_dir = unpacked / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"

    source_path = slides_dir / source_slide
    if not source_path.exists():
        return json.dumps({
            "error": f"Slide {source_slide} introuvable dans {slides_dir}"
        }, ensure_ascii=False)

    # Trouver le prochain numéro de slide
    existing = [
        int(m.group(1))
        for f in slides_dir.glob("slide*.xml")
        if (m := re.match(r"slide(\d+)\.xml", f.name))
    ]
    next_num = max(existing) + 1 if existing else 1
    new_name = f"slide{next_num}.xml"
    new_path = slides_dir / new_name

    # Copier le contenu de la slide
    shutil.copy2(source_path, new_path)

    # Copier les rels (en supprimant les notes)
    source_rels = rels_dir / f"{source_slide}.rels"
    new_rels = rels_dir / f"{new_name}.rels"
    if source_rels.exists():
        rels_content = source_rels.read_text(encoding="utf-8")
        # Supprimer les relations notes
        rels_content = re.sub(
            r'\s*<Relationship[^>]*Type="[^"]*notesSlide"[^>]*/>\s*',
            "\n", rels_content
        )
        new_rels.write_text(rels_content, encoding="utf-8")

    # Ajouter au Content_Types
    ct_path = unpacked / "[Content_Types].xml"
    ct = ct_path.read_text(encoding="utf-8")
    override = (
        f'<Override PartName="/ppt/slides/{new_name}" '
        f'ContentType="application/vnd.openxmlformats-officedocument.'
        f'presentationml.slide+xml"/>'
    )
    if f"/ppt/slides/{new_name}" not in ct:
        ct = ct.replace("</Types>", f"  {override}\n</Types>")
        ct_path.write_text(ct, encoding="utf-8")

    # Ajouter la relation dans presentation.xml.rels
    pres_rels_path = unpacked / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels = pres_rels_path.read_text(encoding="utf-8")
    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels)]
    next_rid = max(rids) + 1 if rids else 1
    rid = f"rId{next_rid}"
    new_rel = (
        f'<Relationship Id="{rid}" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        f'relationships/slide" Target="slides/{new_name}"/>'
    )
    if f"slides/{new_name}" not in pres_rels:
        pres_rels = pres_rels.replace(
            "</Relationships>", f"  {new_rel}\n</Relationships>"
        )
        pres_rels_path.write_text(pres_rels, encoding="utf-8")

    # Calculer le prochain sldId
    pres_path = unpacked / "ppt" / "presentation.xml"
    pres = pres_path.read_text(encoding="utf-8")
    slide_ids = [int(m) for m in re.findall(r'<p:sldId[^>]*id="(\d+)"', pres)]
    next_id = max(slide_ids) + 1 if slide_ids else 256

    sld_id_xml = f'<p:sldId id="{next_id}" r:id="{rid}"/>'

    return json.dumps({
        "new_slide": new_name,
        "sld_id_xml": sld_id_xml,
        "rid": rid,
        "slide_id": next_id,
        "source": source_slide,
        "message": (
            f"Slide {new_name} créée à partir de {source_slide}. "
            f"Ajoutez {sld_id_xml} dans <p:sldIdLst> de presentation.xml."
        )
    }, ensure_ascii=False)


@mcp.tool()
def ordonner_slides(working_dir: str, slide_order: list[str]) -> str:
    """Définit l'ordre des slides dans la présentation.

    Args:
        working_dir: Chemin du répertoire unpacké.
        slide_order: Liste ordonnée des éléments <p:sldId> en XML.
            Exemple: ['<p:sldId id="256" r:id="rId7"/>', ...]

    Returns:
        JSON confirmant l'opération avec le nombre de slides ordonnées.
    """
    unpacked = Path(working_dir)
    pres_path = unpacked / "ppt" / "presentation.xml"
    pres = pres_path.read_text(encoding="utf-8")

    # Construire le nouveau sldIdLst
    entries = "\n      ".join(slide_order)
    new_list = f"<p:sldIdLst>\n      {entries}\n    </p:sldIdLst>"

    # Remplacer l'ancien sldIdLst
    pres = re.sub(
        r"<p:sldIdLst>.*?</p:sldIdLst>",
        new_list,
        pres,
        flags=re.DOTALL,
    )
    pres_path.write_text(pres, encoding="utf-8")

    return json.dumps({
        "slides_count": len(slide_order),
        "message": f"{len(slide_order)} slides ordonnées dans presentation.xml."
    }, ensure_ascii=False)


@mcp.tool()
def editer_contenu(
    working_dir: str,
    slide_file: str,
    rechercher: str,
    remplacer: str,
    tout_remplacer: bool = False,
) -> str:
    """Remplace du texte dans une slide (recherche dans les éléments <a:t>).

    Args:
        working_dir: Chemin du répertoire unpacké.
        slide_file: Nom du fichier slide (ex: "slide1.xml").
        rechercher: Texte à trouver (dans les balises <a:t>).
        remplacer: Texte de remplacement.
            Utiliser les entités XML : &amp; pour &, &#x20AC; pour €,
            &#x2019; pour ', etc.
        tout_remplacer: Si True, remplace toutes les occurrences.
            Si False, remplace seulement la première.

    Returns:
        JSON avec le nombre de remplacements effectués.
    """
    unpacked = Path(working_dir)
    slide_path = unpacked / "ppt" / "slides" / slide_file

    if not slide_path.exists():
        return json.dumps({
            "error": f"Slide {slide_file} introuvable."
        }, ensure_ascii=False)

    content = slide_path.read_text(encoding="utf-8")

    if tout_remplacer:
        count = content.count(rechercher)
        new_content = content.replace(rechercher, remplacer)
    else:
        count = 1 if rechercher in content else 0
        new_content = content.replace(rechercher, remplacer, 1)

    slide_path.write_text(new_content, encoding="utf-8")

    return json.dumps({
        "slide": slide_file,
        "recherche": rechercher,
        "remplacements": count,
        "message": (
            f"{count} remplacement(s) effectué(s) dans {slide_file}."
            if count > 0
            else f"Texte '{rechercher}' non trouvé dans {slide_file}."
        )
    }, ensure_ascii=False)


@mcp.tool()
def lire_slide(working_dir: str, slide_file: str) -> str:
    """Lit le contenu textuel d'une slide (extrait les valeurs <a:t>).

    Args:
        working_dir: Chemin du répertoire unpacké.
        slide_file: Nom du fichier slide (ex: "slide1.xml").

    Returns:
        JSON avec la liste des textes trouvés dans la slide,
        et le contenu XML brut si besoin d'édition fine.
    """
    unpacked = Path(working_dir)
    slide_path = unpacked / "ppt" / "slides" / slide_file

    if not slide_path.exists():
        return json.dumps({
            "error": f"Slide {slide_file} introuvable."
        }, ensure_ascii=False)

    content = slide_path.read_text(encoding="utf-8")

    # Extraire tous les textes <a:t>
    texts = re.findall(r"<a:t>(.*?)</a:t>", content)

    # Détecter s'il y a un tableau
    has_table = "<a:tbl>" in content
    table_cells = re.findall(r"<a:tc[^>]*>.*?</a:tc>", content, re.DOTALL)

    return json.dumps({
        "slide": slide_file,
        "texts": texts,
        "has_table": has_table,
        "table_cells_count": len(table_cells),
        "xml_length": len(content),
    }, ensure_ascii=False)


@mcp.tool()
def lire_xml_brut(working_dir: str, slide_file: str) -> str:
    """Retourne le contenu XML brut complet d'une slide.

    Utile pour les éditions complexes (tableaux, ajout de paragraphes, etc.)
    où il faut voir la structure XML exacte.

    Args:
        working_dir: Chemin du répertoire unpacké.
        slide_file: Nom du fichier slide (ex: "slide64.xml").

    Returns:
        Le contenu XML de la slide.
    """
    unpacked = Path(working_dir)
    slide_path = unpacked / "ppt" / "slides" / slide_file

    if not slide_path.exists():
        return f"Erreur: {slide_file} introuvable dans {unpacked}/ppt/slides/"

    return slide_path.read_text(encoding="utf-8")


@mcp.tool()
def ecrire_xml(working_dir: str, slide_file: str, contenu_xml: str) -> str:
    """Écrit le contenu XML complet d'une slide.

    Utile pour les modifications structurelles complexes (tableaux, ajout
    de shapes, etc.) où editer_contenu ne suffit pas.

    Args:
        working_dir: Chemin du répertoire unpacké.
        slide_file: Nom du fichier slide (ex: "slide64.xml").
        contenu_xml: Le contenu XML complet à écrire.

    Returns:
        JSON confirmant l'écriture.
    """
    unpacked = Path(working_dir)
    slide_path = unpacked / "ppt" / "slides" / slide_file

    slide_path.write_text(contenu_xml, encoding="utf-8")

    return json.dumps({
        "slide": slide_file,
        "xml_length": len(contenu_xml),
        "message": f"Slide {slide_file} écrite ({len(contenu_xml)} caractères)."
    }, ensure_ascii=False)


@mcp.tool()
def calculer_budget(prestations: list[dict]) -> str:
    """Calcule le budget d'une proposition à partir des prestations.

    Utilise la grille tarifaire configurée dans config/pricing.json.

    Args:
        prestations: Liste de prestations, chacune étant un dict avec :
            - nom (str): Nom de la prestation (ex: "Audit SEO")
            - role (str): Rôle de la ressource (ex: "Expert SEO technique")
            - heures (float): Nombre d'heures allouées
            - type (str): "ponctuel" ou "mensuel"
            - tjm_override (float, optionnel): TJM personnalisé

    Returns:
        JSON avec le détail des coûts par prestation et les totaux.
    """
    config_path = SERVER_DIR / "config" / "pricing.json"
    if not config_path.exists():
        return json.dumps({"error": "Fichier config/pricing.json introuvable."})

    config = json.loads(config_path.read_text(encoding="utf-8"))
    heures_par_jour = config.get("heures_par_jour", 7)
    roles = config.get("roles", {})

    resultats = []
    total_ponctuel = 0
    total_mensuel = 0

    for p in prestations:
        nom = p.get("nom", "Sans nom")
        role = p.get("role", "")
        heures = p.get("heures", 0)
        type_presta = p.get("type", "ponctuel")
        tjm_override = p.get("tjm_override")

        # Trouver le TJM
        if tjm_override:
            tjm = tjm_override
        elif role in roles:
            tjm = roles[role]["tjm"]
        else:
            # Chercher une correspondance partielle
            matches = [r for r in roles if role.lower() in r.lower()]
            if matches:
                tjm = roles[matches[0]]["tjm"]
                role = matches[0]
            else:
                tjm = 750  # TJM par défaut

        jours = heures / heures_par_jour
        cout = round(jours * tjm)

        # Arrondir au multiple de 50 le plus proche
        cout_arrondi = round(cout / 50) * 50

        resultat = {
            "nom": nom,
            "role": role,
            "heures": heures,
            "jours": round(jours, 2),
            "tjm": tjm,
            "cout_exact": cout,
            "cout_arrondi": cout_arrondi,
            "type": type_presta,
        }
        resultats.append(resultat)

        if type_presta == "mensuel":
            total_mensuel += cout_arrondi
        else:
            total_ponctuel += cout_arrondi

    return json.dumps({
        "prestations": resultats,
        "total_ponctuel_ht": total_ponctuel,
        "total_mensuel_ht": total_mensuel,
        "total_annuel_ht": total_ponctuel + (total_mensuel * 12),
        "message": (
            f"{len(resultats)} prestation(s) calculée(s). "
            f"Setup: {total_ponctuel:,} EUR HT, "
            f"Mensuel: {total_mensuel:,} EUR HT/mois, "
            f"Total annuel: {total_ponctuel + total_mensuel * 12:,} EUR HT."
        )
    }, ensure_ascii=False)


@mcp.tool()
def empaqueter_pptx(
    working_dir: str,
    output_filename: str = "proposition.pptx",
) -> str:
    """Empaquette le répertoire de travail en un fichier PPTX final.

    Args:
        working_dir: Chemin du répertoire unpacké.
        output_filename: Nom du fichier de sortie (défaut: "proposition.pptx").

    Returns:
        JSON avec le chemin du fichier PPTX généré.
    """
    unpacked = Path(working_dir)
    session_dir = unpacked.parent
    output_path = session_dir / output_filename
    template_copy = session_dir / "master_template.pptx"

    # Condensation XML + empaquetage
    with tempfile.TemporaryDirectory() as tmp:
        tmp_content = Path(tmp) / "content"
        shutil.copytree(unpacked, tmp_content)

        # Condenser le XML (supprimer les indentations inutiles)
        for pattern in ["*.xml", "*.rels"]:
            for xml_file in tmp_content.rglob(pattern):
                _condense_xml(xml_file)

        # Créer le ZIP
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in tmp_content.rglob("*"):
                if f.is_file():
                    zf.write(f, f.relative_to(tmp_content))

    return json.dumps({
        "output_path": str(output_path),
        "size_kb": round(output_path.stat().st_size / 1024, 1),
        "message": f"Présentation générée : {output_path} ({round(output_path.stat().st_size / 1024)}KB)"
    }, ensure_ascii=False)


@mcp.tool()
def lister_sessions() -> str:
    """Liste les sessions de travail existantes.

    Returns:
        JSON avec la liste des sessions et leurs fichiers.
    """
    if not WORK_DIR.exists():
        return json.dumps({"sessions": [], "message": "Aucune session."})

    sessions = []
    for d in WORK_DIR.iterdir():
        if d.is_dir():
            pptx_files = list(d.glob("*.pptx"))
            sessions.append({
                "name": d.name,
                "path": str(d),
                "has_unpacked": (d / "unpacked").exists(),
                "pptx_files": [f.name for f in pptx_files],
            })

    return json.dumps({
        "sessions": sessions,
        "work_dir": str(WORK_DIR),
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Fonctions utilitaires internes
# ---------------------------------------------------------------------------

def _pretty_print_all_xml(directory: Path) -> None:
    """Pretty-print tous les fichiers XML pour faciliter l'édition."""
    try:
        import defusedxml.minidom
    except ImportError:
        return  # Skip si defusedxml n'est pas installé

    for xml_file in list(directory.rglob("*.xml")) + list(directory.rglob("*.rels")):
        try:
            content = xml_file.read_text(encoding="utf-8")
            dom = defusedxml.minidom.parseString(content)
            xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="utf-8"))
        except Exception:
            pass


def _condense_xml(xml_file: Path) -> None:
    """Condense le XML en supprimant les espaces blancs inutiles."""
    try:
        import defusedxml.minidom
        with open(xml_file, encoding="utf-8") as f:
            dom = defusedxml.minidom.parse(f)

        for element in dom.getElementsByTagName("*"):
            if element.tagName.endswith(":t"):
                continue
            for child in list(element.childNodes):
                if (
                    child.nodeType == child.TEXT_NODE
                    and child.nodeValue
                    and child.nodeValue.strip() == ""
                ) or child.nodeType == child.COMMENT_NODE:
                    element.removeChild(child)

        xml_file.write_bytes(dom.toxml(encoding="UTF-8"))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport not in ("stdio", "sse", "streamable-http"):
        print(f"Transport inconnu: {transport}. Utilisation de stdio.", flush=True)
        transport = "stdio"
    mcp.run(transport=transport)
