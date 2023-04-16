import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class proie:
    VIE = 30
    AGE_DIVISION = 5
    
    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
    
class pred:
    VIE = 100
    AGE_DIVISION = 20
    RESERVES_DIVISION = 10
    RESERVES_SATIETE = 20

    def __init__(self, x, y, age, reserves):
        self.x = x
        self.y = y
        self.age = age
        self.reserves = reserves
    
    def __str__(self):
        return "age: " + str(self.age)+ " reserve: " + str(self.reserves)

# Simluation

L = 50 # nb de points sur chaque côté de la grille

n_pred0 = 10
n_proie0 = 200
reserves0 = 6.0 # Réserves données aux prédateurs initiaux
perte_par_cycle = 0.5 # réserves perdues par les prédateurs à chaque itération
n_iter = 1000 # Nombre d'itérations (temps de simlulation)

# Initialisation de la grille
fig, ax = plt.subplots()
ax.set_aspect(1)
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.grid()

pred_ref = np.empty((L, L), dtype=pred)
proie_ref = np.empty((L, L), dtype=proie)

# Note: cette façon de faire privilégie proie, qui est exécuté en 2e.
for i in range(n_pred0) :
    x = int(np.random.rand()*L)
    y = int(np.random.rand()*L)
    age = int(np.random.rand()*pred.VIE)
    pred_ref[x,y] = pred(x, y, age, reserves0)

for i in range(n_proie0) :
    x = int(np.random.rand()*L)
    y = int(np.random.rand()*L)
    age = int(np.random.rand()*proie.VIE)
    proie_ref[x,y] = proie(x, y, age)

# Boucle sur le temps / animation
def run(t) :
    global proie_ref, pred_ref

    # Retirer les morts
    for i in range(L) :
        for j in range(L) :
            if (proie_ref[i, j] != None and proie_ref[i, j].age > proie.VIE) :
                proie_ref[i, j] = None
            if (pred_ref[i, j] != None and (pred_ref[i, j].age > pred.VIE or pred_ref[i, j].reserves <= 0)) :
                pred_ref[i, j] = None

    # Reproduire au site voisin
    # Proie division
    for i in range(L) :
        for j in range(L) :
            # Proies: Age > age de division
            if (proie_ref[i, j] != None and proie_ref[i, j].age > proie.AGE_DIVISION) :
                for k in range(5) :
                    positionXVisitee = (i + np.random.choice([-1, 0, 1])) % 50
                    positionYVisitee = (j + np.random.choice([-1, 0, 1])) % 50
                    if (proie_ref[positionXVisitee, positionYVisitee] == None) :
                        proie_ref[positionXVisitee, positionYVisitee] = proie(positionXVisitee, positionYVisitee, 0)
                        proie_ref[i, j].age = 0
                        break
    # Pred division
    for i in range(L) :
        for j in range(L) :
            if (pred_ref[i, j] != None and (pred_ref[i, j].age > pred.AGE_DIVISION and pred_ref[i, j].reserves > pred.RESERVES_DIVISION)) :
                for k in range(5) :
                    positionXVisitee = (i + np.random.choice([-1, 0, 1])) % 50
                    positionYVisitee = (j + np.random.choice([-1, 0, 1])) % 50
                    if (pred_ref[positionXVisitee, positionYVisitee] == None) :
                        pred_ref[positionXVisitee, positionYVisitee] = pred(positionXVisitee, positionYVisitee, 0, pred_ref[i,j].reserves / 2.0)
                        pred_ref[i, j].age = 0
                        pred_ref[i, j].reserves = pred_ref[i, j].reserves / 2.0
                        break

    # Nourrir les pred
    # Si à la même case pred et proies: augmenter réserve de pred et éliminer proie
    for i in range(L) :
        for j in range(L) :
            if (pred_ref[i, j] != None and proie_ref[i, j] != None) :
                proie_ref[i, j] = None
                pred_ref[i, j].reserves += 1.0

    # Déplacer les pred
    for i in range(L) :
        for j in range(L) :
            if (pred_ref[i, j] != None) :
                for k in range(5) :
                    positionXVisitee = (i + np.random.choice([-1, 0, 1])) % 50
                    positionYVisitee = (j + np.random.choice([-1, 0, 1])) % 50
                    if (pred_ref[positionXVisitee, positionYVisitee] == None and proie_ref[positionXVisitee, positionYVisitee] != None) :
                        pred_ref[positionXVisitee, positionYVisitee] = pred_ref[i, j]
                        pred_ref[i, j] = None
                        break

    # Appliquer vieilliessement pour tous et perte réserve pour pred
    for i in range(L) :
        for j in range(L) :
            if (proie_ref[i, j] != None) :
                proie_ref[i, j].age += 1
            if (pred_ref[i, j] != None) :
                pred_ref[i, j].age += 1
                pred_ref[i, j].reserves -= perte_par_cycle

    plt.clf()
    proie_x = []
    proie_y =[]
    pred_x = []
    pred_y = []
    for i in range(L) :
        for j in range(L) :
            if (proie_ref[i, j] != None) :
                proie_x.append(i)
                proie_y.append(j)
            if (pred_ref[i, j] != None) :
                pred_x.append(i)
                pred_y.append(j)
    
    print(np.count_nonzero(pred_ref), np.count_nonzero(proie_ref))
    plt.plot(proie_x, proie_y, "bo", markersize=3)
    plt.plot(pred_x, pred_y, "rs", markersize=3)
        
    # Prendre en note proie et pred pour graphique en fonction du temps
    plt.title('t = {0:4.1f}'.format(t))

ani = animation.FuncAnimation(fig, run, frames=np.arange(0, n_iter), interval = 10, repeat=False)

plt.show()
