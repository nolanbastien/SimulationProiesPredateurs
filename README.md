# Simulation proies prédateurs

Dernier travail pratique de la session dans le cadre du cours Calcul Scientifique (2e session au bac en physique). Le projet consiste à simuler la dynamique prédateurs-proies.

# Énoncé du devoir

les règles de la simulation sont les suivantes:

1. Chaque espèce a une vie maximale. De plus, les prédateurs meurent si leurs réserves sont épuisées.
1. Chaque espèce se reproduit par division, si l'espace et les ressources le permettent. 
La division résulte en deux individus, dont l'un reste sur sa position et l'autre est créé sur un site voisin qui n'est pas déjà occupé par un autre individu de la même espèce.
Un âge minimum est requis pour la division. De plus, dans le cas des prédateurs, des réserves suffisantes sont aussi requises. Suite à la division, les réserves sont divisées également entre les deux individus.
Enfin, après la division, les deux individus voient leur âge remis à zéro.
1. Les prédateurs vont manger les proies situées sur le même site, s'il n'ont pas atteint un niveau de réserves suffisant (niveau de satiété). Ce faisant, leurs réserves augmentent d'une unité.
1. Les prédateurs se déplacent, une case à la fois, et uniquement si une proie se trouve sur l'un des huit sites voisins.
1. Les individus des deux espèces vieillissent d'une unité par pas temporel (ou itération). De plus, les réserves des prédateurs diminuent d'une certaine quantité à chaque pas temporel.
1. Au départ de la simulation, un certain nombre de proies et de prédateurs doivent être créés, avec des âges choisis au hasard entre 0 et la vie maximale. Les prédateurs initiaux ont tous une quantité donnée de réserves.

Votre solution doit contenir les éléments suivants:

1. Un programme complet qui effectue la simulation et l'animation. Ce programme doit définir les classes `pred` et `proie` et comporter les étapes et les variables décrites ci-dessus. Le programme doit être fonctionnel et atteindre le temps $t=1000$ sans que l'une des espèces (ou les deux) ait complètement disparu.
2. Un graphique, généré dans une cellule différente, des populations des deux espèces en fonction du temps. Il est pratique d'écrire le tableau dans un fichier lors de la dernière itération et de faire le graphique à partir du fichier dans une cellule séparée.

# Note sur les deux solutions

J'ai d'abord fait une solution avec deux listes bidimensionnelles (TP7_2Darrays.py), en pensant que ce serait environ équivalent à deux listes et deux listes de références bidimensionnelles (TP7.py). Puis, j'ai essayé la deuxième idée. Cette dernière est celle que j'ai remise et complétée.
