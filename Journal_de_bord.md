# Voici le Journal de Bord

### Semaine 1 

Premièrement, on a commencé à réfléchir à comment mettre en place la physique dans le moteur de jeu en informatique (Matteo).
Nous avons ensuite effectué des recherches concernant les librairies à utiliser comme PySDL,
qui sera utilisé pour l'interface (Milo) et la création du cahier des charges (Ayoub et Milo).
Et début de la réflexion sur l'architecture du projet (Youness).
En fin de semaine, nous avons finaliser le premier prototype V0 (Milo et Matteo).

Lien du prototype v0 : https://github.com/milomessin-fr/Projet-Moteur-Physique-Python/tree/prototype-v0

---
### Semaine 2

Nous avons démarrer le prototype V1 incluant plusieurs fonctionnalités du cahier des charges ; 
multi-threading, système de scène(s). 
On a aussi modifié les entités pour qu'elle possèdent seulement
des paramètres sans aucune logique physique. Par exemple, l'ajout du paramètre "static" pour désactiver la logique
physique sur les entitées. (Matteo, Milo, Ayoub).

Lien du prototype v1 :  https://github.com/milomessin-fr/Projet-Moteur-Physique-Python/tree/prototype-v1

---
### Semaine 3

Nous avons fabriqué une factory (Milo) qui permet de dessiner et générer des sprite autant qu'on le veut comme dans un moteur de jeu, 
nous avons reçu la première version de l'architecture (youness) elle sera mise en place dans le prototype v2. 
Créations de la grille hachage (matteo)

---
### Semaine 4

Cette semaine, nous avons avancé sur les différents systèmes qui serviront à l'optimisation du moteur, comme par exemple la grille de hachage ou on a  ajouté une nouvelle méthode pour
actualiser la grille de hachage chaque frame. (matteo), ainsi que la nouvelle stratégie qui ne consiste plus a avoir une instance pour chaque grains mais plutot une liste qui 
contiendra un id pour chaque grains avec leur positions, ce sera beaucoup plus performant de faire comme ceci. 


