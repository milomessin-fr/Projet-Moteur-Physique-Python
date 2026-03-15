
# Titre : système de scene, entité, colision séparé (approche orienté ECS=Entity Component System)

Pour cela j'ai besoin de thread qui sépare le rendu, du calcul de colision
Dans la boucle de jeu, on efface en boucle l'écran et si il ya une scene de chosis alors on la déssine en boucle. En parallèle toujours faire tourner 
le calcul de colision qui sera le coeur de notre moteur, il y aura plusieurs rendu mais un moteur physique. Ne surtout pas mettre calcul dans les entités 
elles doivent rester simple et optimiser. Un dossier config en python me semble le plus pratique car c'est plus simple de modifier les variables en temps réel
qu'un json par exemple mais c'est possible que ce ne soit pas le plus pratique. Dans cette idée, il y aura une class de calcul de colision,vitesse. Ce qui serait 
bien ça serait que les calculs de colisions entre les entités servents aussi pour les calculs de colision avec les bordure et qu'il ne soit pas séparé.
Je me demande si faire en sorte que la bordure sois une entité serait-une bonne idée ou non. Sachant que le système d'apparitions de grains et les calculs 
de leur colision sera réalisé grâce a une grille, cela nous permet de faire une hypothèse comme quoi si il n'y a aucun grains en dessous alors le grains choisit 
prend de la vitesse en augmentent la valeur de la variable v_y qui est un vecteur directionnel sur l'ordonnés, et si le grain rencontre une case remplis alors 
v_y sera multiplié par le coefficient de rigidité. Pour une physique plus poussé du sable il faut également géré le vecteur de l'abscisse v_x, j'ai déjà réfléchis
a comment faire et je pense que vérifier les diagonales et la présence de grains sur les cases de droite et de gauche, pour donner ou non l'ordre au grains de 
descendre en diagonales, je pense que faire un calcul qui joue sur la présence d'un grain en diagonale avec la gravite peut permettre au grains de prendre 
de la vitesse de chute en diagonale si c'est une pile de grains par exemple. Ensuite un autre point dont je n'ai pas vraiment d'hypothèse de comment faire
ça va être le calcul de la force d'explosion, ce que je veux dire c'est quand la boule tombera sur les grains il faudra une force qui affectera le plateau de grains
ma seule piste pour l'instant et de donner une force de répulsion a chaque entité qui sera calculé en fonction de leur vitesse et masse, et donc meme les grains 
auront une force de répulsion cependant elle sera bien inférieur a celle de la boule, car la boule aura une masse et un poid. Je pense que cette partie est la plus 
complexe et difficile a imaginer des recherches approfondis seront nécéssaires.  



### Séparation des Threads: rendu et physique concept a utilisé :
- Double Buffering

### Les Bordures des entités : 
- Oui mais faire un mode Static = True pour les entités

### Le Problème de l'Explosion (Transfert de Force) concept a utilisé :
- Rayon d'explosion
- Vecteur répulsion= Pour chaque grains dans le rayon d'explosion il faudra calculer un vecteur qui du centre de la boule au grains 
- Calcul d'impulsion trouvé : v_grain ​= v_grain​+(V_boule​⋅M_boule / dist**2​​) 

                           - dist = la distance euclidienne entre le centre de la boule et le grain de sable individuel (regarde le calcul de dist sur internet)
                           - V_boule = vecteur vitesse de la boule donc v_y
                           - M_boule = Masse de la boule
                           - v_grain = vecteur de vitesse du grain

- ajouté un coefficient de dissipation (friction) sinon les grains sur l'axe x ne s'arreteront jamais


### Tache 

- Gérer la data des matériaux

- Gérer la colision la masse la vitesse

- gérer l'interface 

- gérer la liaison entre les calculs et l'interface 
