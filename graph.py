import numpy as np
import matplotlib.pyplot as plt

donnees = np.genfromtxt("data.csv")

t = donnees[0, :]
proies = donnees[1, :]
preds = 10*donnees[2, :]

print(t)
print(proies)
print(preds)

plt.plot(t, proies, label="Nombre de proies")
plt.plot(t, preds, label="Nombre de predateurs (x10)")
plt.legend()
plt.show()
