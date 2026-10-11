# EKO — La matrice au service du PGM Follow

Dossier R&D Kreativ Labs (octobre 2026) : comment obtenir de la matrice d'un car une sortie dédiée
portant le PGM, le son international et le LTC des trois LSM en audio, sans toucher au PGM de diffusion.

Document interne, non destiné à la diffusion publique.

## Contenu

| Fichier | Rôle |
|---|---|
| `index.html`, `rapport.html` | Synthèse et rapport complet, en français |
| `en/index.html`, `en/report.html` | Summary and full report, in English |
| `content/summary.*.md` | Sources de la synthèse (marqueurs `{{diagram:nom}}` pour les schémas) |
| `content/report.*.md` | Sources du rapport complet, toutes les références en lien |
| `diagrams.py` | Schémas SVG, en français et en anglais |
| `build.py` | Génère les quatre pages HTML |
| `assets/` | Feuille de style et script (thème clair ou sombre, impression PDF) |
| `middleware.js` | Contrôle d'accès du site : formulaire de code, cookie de 30 jours |

## Mettre à jour

1. Modifier les fichiers de `content/`.
2. Lancer `python3 build.py` (nécessite `pip install markdown`).
3. Valider les quatre pages HTML générées avec les sources.

Le site est statique : Vercel sert les fichiers tels quels, sans étape de build.

## Accès

Le site est réservé à l'équipe. `middleware.js` demande un code d'accès avant de servir la moindre page.
Le code n'est pas dans ce dépôt : il est lu dans la variable d'environnement Vercel `ACCESS_CODE`.
Sans cette variable, le site reste fermé. Changer sa valeur invalide tous les accès déjà ouverts.
