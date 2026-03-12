
Mécanique envisagé de base :

-Physique de la boule : Intégration d'Euler ou Verlet pour le mouvement (gravité, accélération).
-Gestion des matériaux : Système de friction et de restitution (rebond) paramétrable pour la boule.

Interface : 

-Rendu sdl2 : Affichage propre des textures et rendu fluide des pixels sable ect ...
-menu de configuration sur le haut ou coté de la fenetre ou on peut choisir le matériaux.

Spécification techniques: 

-langage: Python 3 
-rendu: pysdl2
-Mathématiques: utilisation de numpy 

Conseil de l'ia :
### Le dilemme du sable : Automate Cellulaire vs Particules

C'est le choix technique le plus critique de ton projet.

- **L'approche "Falling Sand" (Automate Cellulaire) :** Tu divises ton écran en une grille (ex: 200x200). Chaque case est soit vide, soit du sable. C'est très performant et facile à coder en Python/NumPy.
    
- **L'approche "DEM" (Particules réelles) :** Chaque grain est un petit cercle avec une vitesse et une masse. C'est magnifique, mais au-delà de 500 grains, Python va commencer à bégayer sérieusement sans optimisation massive.
    

> **Conseil :** Pars sur une **grille (Automate Cellulaire)** pour le sable, et une **entité physique réelle** pour la boule. C'est le meilleur compromis performance/rendu.


### L'astuce mathématique : L'intégration de Verlet

Oublie l'intégration d'Euler classique (v=v+a×dt). Pour une simulation physique stable, utilise l'**Intégration de Verlet**. Elle est beaucoup plus stable pour les collisions et évite que ta boule ne "s'enfonce" ou ne "rebondisse" à l'infini à cause d'erreurs d'arrondi.


### Gestion des Matériaux

Pour que le changement de matériau soit crédible, ne change pas juste la couleur. Joue sur trois variables clés dans ton code :

- **La Masse (m) :** Impacte l'inertie (une boule de plomb déplace plus de sable qu'une boule de polystyrène).
    
- **Le Coefficient de Restitution (e) :** Définit si la boule rebondit ou "s'écrase" (ex: 0.1 pour du plomb, 0.8 pour du caoutchouc).
    
- **La Friction (μ) :** Définit comment le sable "accroche" la surface de la boule.

### Optimisation PySDL2 + NumPy

Puisque tu es en Python, évite les boucles `for` pour traiter tes grains de sable un par un.

- Utilise **NumPy** pour traiter des tableaux entiers de données.
    
- Avec PySDL2, utilise les **SDL_RenderDrawPoints** ou les **Textures** pour l'affichage groupé. Si tu dessines chaque grain avec une commande individuelle, ton processeur va surchauffer avant même que la boule ne touche le sol.


# Tache 

-Gérer la data des matériaux

-Gérer la colision la masse la vitesse

-gérer l'interface 

-gérer la liaison entre les calculs et l'interface 