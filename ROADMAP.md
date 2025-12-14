# Roadmap - Application de Dessin (Paint-like)

## Vision
Une application de dessin simple et intuitive en Python, inspirée de Paint.

## Stack Technique
- **Python 3.x**
- **Tkinter** (interface graphique native, pas de dépendances externes)

---

## Phase 1 : Fondations
> Objectif : Avoir une fenêtre fonctionnelle avec un canvas de dessin basique

- [ ] Créer la fenêtre principale avec Tkinter
- [ ] Implémenter le canvas de dessin
- [ ] Dessiner au clic/glisser de souris (trait libre)
- [ ] Choisir la couleur du trait (palette basique)
- [ ] Choisir l'épaisseur du trait

---

## Phase 2 : Outils de base
> Objectif : Avoir les outils essentiels d'un logiciel de dessin

- [ ] Outil crayon (trait libre)
- [ ] Outil gomme
- [ ] Outil ligne droite
- [ ] Outil rectangle
- [ ] Outil ellipse/cercle
- [ ] Outil remplissage (seau de peinture)
- [ ] Outil texte

---

## Phase 3 : Gestion des fichiers
> Objectif : Pouvoir sauvegarder et ouvrir ses créations

- [ ] Nouveau document (effacer le canvas)
- [ ] Sauvegarder en PNG/JPG
- [ ] Ouvrir une image existante
- [ ] Exporter dans différents formats

---

## Phase 4 : Fonctionnalités avancées
> Objectif : Améliorer l'expérience utilisateur

- [ ] Annuler (Ctrl+Z)
- [ ] Rétablir (Ctrl+Y)
- [ ] Sélecteur de couleur complet (color picker)
- [ ] Palette de couleurs personnalisée
- [ ] Zoom avant/arrière

---

## Phase 5 : Polish & UX
> Objectif : Rendre l'application agréable à utiliser

- [ ] Barre d'outils avec icônes
- [ ] Raccourcis clavier
- [ ] Curseurs personnalisés selon l'outil
- [ ] Barre de statut (position souris, taille canvas)
- [ ] Menu Fichier/Edition/Aide

---

## Priorités
1. **MVP (Phase 1-2)** : Application utilisable avec les outils de base
2. **Sauvegarde (Phase 3)** : Indispensable pour garder ses dessins
3. **UX (Phase 4-5)** : Nice to have, améliore le confort

## Notes techniques
- Tkinter est inclus dans Python, pas d'installation nécessaire
- Pour sauvegarder en image, utiliser `Pillow` (PIL)
- Canvas Tkinter supporte nativement les formes géométriques
