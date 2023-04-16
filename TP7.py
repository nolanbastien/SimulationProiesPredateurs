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

preds = []
proies = []
pred_ref = np.full((L, L), False, dtype=bool)
proie_ref = np.full((L, L), None, dtype=proie)

for i in range(n_pred0) :
    x = int(np.random.rand()*L)
    y = int(np.random.rand()*L)
    age = int(np.random.rand()*pred.VIE)
    preds.append(pred(x, y, age, reserves0))
    pred_ref[x,y] = True

for i in range(n_proie0) :
    x = int(np.random.rand()*L)
    y = int(np.random.rand()*L)
    age = int(np.random.rand()*proie.VIE)
    nouvelleProie = proie(x, y, age)
    proies.append(nouvelleProie)
    proie_ref[x,y] = nouvelleProie

tableau = np.zeros((3, n_iter))
elapsed_time1 = []
                
# Boucle sur le temps / animation
def run(t) :
    global proies, preds
    
    # Prendre les données pour le graphique
    tableau[:,t] = [t, len(proies), len(preds)]

    # Retirer les morts
    morts = []
    for p in proies :
        if (p.age > proie.VIE) :
            morts.append(p)
    for mort in morts :
        proie_ref[mort.x, mort.y] = None
        proies.remove(mort)

    morts = []
    for p in preds :
        if (p.age > pred.VIE or p.reserves <= 0) :
            morts.append(p)
    for mort in morts :
        pred_ref[mort.x, mort.y] = None
        preds.remove(mort)

    # Reproduire au site voisin
    # Division proies
    for p in proies :
        if (p.age > proie.AGE_DIVISION) :
            for k in range(5) :
                positionXVisitee = (p.x + np.random.choice([-1, 0, 1])) % 50
                positionYVisitee = (p.y + np.random.choice([-1, 0, 1])) % 50
                if (proie_ref[positionXVisitee, positionYVisitee] == None) :
                    nouvelleProie = proie(positionXVisitee, positionYVisitee, 0)
                    proies.append(nouvelleProie)
                    proie_ref[positionXVisitee, positionYVisitee] = nouvelleProie 
                    p.age = 0
                    break
                     
    # Division preds
    for p in preds :
        if (p.age > pred.AGE_DIVISION and p.reserves > pred.RESERVES_DIVISION) :
            for k in range(5) :
                positionXVisitee = (p.x + np.random.choice([-1, 0, 1])) % 50
                positionYVisitee = (p.y + np.random.choice([-1, 0, 1])) % 50
                if (pred_ref[positionXVisitee, positionYVisitee] == False) :
                    preds.append(pred(positionXVisitee, positionYVisitee, 0, p.reserves / 2.0))
                    pred_ref[positionXVisitee, positionYVisitee] = True 
                    p.age = 0
                    p.reserves = p.reserves / 2.0
                    break

    # Nourrir les pred
    for p in preds :
        if (proie_ref[p.x, p.y] != None and p.reserves <= pred.RESERVES_SATIETE) :
            proies.remove(proie_ref[p.x, p.y])
            proie_ref[p.x, p.y] = None
            p.reserves += 1.0

    # Déplacer les pred
    for p in preds :
        for k in range(5):
            positionXVisitee = (p.x + np.random.choice([-1, 0, 1])) % 50
            positionYVisitee = (p.y + np.random.choice([-1, 0, 1])) % 50
            if (pred_ref[positionXVisitee, positionYVisitee] == False and proie_ref[positionXVisitee, positionYVisitee] != None) :
                pred_ref[p.x, p.y] = False
                pred_ref[positionXVisitee, positionYVisitee] = True
                p.x = positionXVisitee
                p.y = positionYVisitee 
                break

    # Appliquer vieilliessement pour tous et perte réserve pour pred
    for p in proies :
        p.age += 1
    
    for p in preds :
        p.age += 1
        p.reserves -= perte_par_cycle

    # Afficher le graphique
    plt.clf()
    plt.plot([p.x for p in proies], [p.y for p in proies], "bo", markersize=3)
    plt.plot([p.x for p in preds], [p.y for p in preds], "rs", markersize=3)
    plt.title('t = {0:4.1f}'.format(t))

ani = animation.FuncAnimation(fig, run, frames=np.arange(0, n_iter), interval = 10, repeat=False)
plt.show()
np.savetxt("data.csv", tableau)
