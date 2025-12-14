# Backlog - PyPaint

## Légende
- **P0** : Critique (MVP)
- **P1** : Important
- **P2** : Nice to have
- **S** : Taille (XS, S, M, L, XL)

---

## Sprint 1 - Setup & Canvas de base

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 001 | Créer la structure du projet (main.py) | P0 | XS | DONE |
| 002 | Créer la fenêtre principale Tkinter | P0 | S | DONE |
| 003 | Ajouter un canvas blanc | P0 | S | DONE |
| 004 | Implémenter le dessin libre à la souris | P0 | M | DONE |

---

## Sprint 2 - Couleurs & Épaisseur

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 005 | Ajouter une palette de couleurs (8 couleurs) | P0 | S | DONE |
| 006 | Permettre de changer la couleur active | P0 | S | DONE |
| 007 | Ajouter un slider pour l'épaisseur du trait | P0 | S | DONE |
| 008 | Afficher la couleur/épaisseur actuelle | P1 | XS | DONE |

---

## Sprint 3 - Outils de dessin

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 009 | Créer une barre d'outils | P0 | M | DONE |
| 010 | Outil crayon (défaut) | P0 | S | DONE |
| 011 | Outil gomme | P0 | S | DONE |
| 012 | Outil ligne droite | P0 | M | DONE |
| 013 | Outil rectangle | P0 | M | DONE |
| 014 | Outil ellipse | P1 | M | DONE |
| 015 | Outil remplissage | P1 | L | DONE |
| 016 | Outil texte | P2 | M | DONE |

---

## Sprint 4 - Gestion fichiers

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 017 | Bouton "Nouveau" (effacer canvas) | P0 | XS | DONE |
| 018 | Installer/intégrer Pillow | P0 | XS | DONE |
| 019 | Sauvegarder en PNG | P0 | M | DONE |
| 020 | Ouvrir une image | P1 | M | DONE |
| 021 | Dialogue de confirmation avant fermeture | P1 | S | DONE |

---

## Sprint 5 - Annuler/Rétablir

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 022 | Implémenter historique des actions | P1 | L | DONE |
| 023 | Fonction Annuler (Ctrl+Z) | P1 | M | DONE |
| 024 | Fonction Rétablir (Ctrl+Y) | P1 | M | DONE |

---

## Sprint 6 - Polish

| ID | Tâche | Priorité | Taille | Status |
|----|-------|----------|--------|--------|
| 025 | Color picker complet | P2 | M | DONE |
| 026 | Raccourcis clavier (C, E, L, R, etc.) | P2 | S | DONE |
| 027 | Curseurs personnalisés par outil | P2 | M | DONE |
| 028 | Barre de statut (coords souris) | P2 | S | DONE |
| 029 | Menu Fichier/Edition/Aide | P2 | M | DONE |
| 030 | Zoom canvas | P2 | L | TODO |

---

## Backlog Ice Box (futur)

| ID | Tâche | Notes |
|----|-------|-------|
| F01 | Calques | Complexe, v2 |
| F02 | Filtres (flou, contraste) | Nécessite PIL avancé |
| F03 | Sélection rectangulaire | Copier/coller |
| F04 | Spray/aérographe | Effet particules |
| F05 | Formes prédéfinies (étoile, flèche) | Nice to have |

---

## Résumé MVP (Sprints 1-4)
**22 tâches** pour avoir une application fonctionnelle avec :
- Dessin libre
- Couleurs et épaisseur
- Outils de base (crayon, gomme, formes)
- Sauvegarde/ouverture de fichiers

## Status actuel
**29/30 tâches complétées** - Application fonctionnelle !
