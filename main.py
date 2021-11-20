""" Importamos el modelo del archivo en que lo definimos. """
from CellModel import CellModel

""" matplotlib lo usaremos crear una animación de cada uno de los pasos
    del modelo. """
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

""" Importamos los siguientes paquetes para el mejor manejo de valores
    numéricos."""
import numpy as np
import pandas as pd

""" Definimos otros paquetes que vamos a usar para medir el tiempo de
    ejecución de nuestro algoritmo. """
import time
import datetime

""" El usuario define el tamaño de la matriz, numero de agentes, 
    porcentaje de celdas sucias, tiempo maximo de ejecucion """
M = int(input("No. de filas: "))
N = int(input("No. de columnas: "))
numAgents = int(input("No. de agentes: "))
dirtyCellPercentage = float(input("Porcentaje de celdas sucias inicialmente en decimal: "))
MAXTIME = int(input("Tiempo máximo de ejecución en segundos: "))


""" Registramos el tiempo de inicio y ejecutamos la simulación. """
startTime = time.time()
model = CellModel(M, N, numAgents, dirtyCellPercentage)

frames =-1
while datetime.timedelta(seconds=(time.time() - startTime) < MAXTIME):
    frames+=1
    if model.dirtyCells == 0:
        break
    model.step()

""" Imprimimos el tiempo que le tomó correr al modelo, y sus atributos al final """
print('Tiempo de ejecución:', str(datetime.timedelta(seconds=(time.time() - startTime))))
print('Porcentajede celdas limpias:', (model.totalCells-model.dirtyCells)*100/model.totalCells, "%")
print('Movimientos realizados por los agentes:', model.numMovements)

""" Obtenemos la información que almacenó el colector, este nos entregará un
    DataFrame de pandas que contiene toda la información. """
allGrid = model.datacollector.get_model_vars_dataframe()

# Graficamos la información usando `matplotlib`
fig, axs = plt.subplots(figsize=(7,7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(allGrid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(allGrid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames=frames)
plt.show()