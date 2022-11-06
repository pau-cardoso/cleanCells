# Importamos las clases que se requieren para manejar los agentes (Agent) y su entorno (Model).
# Cada modelo puede contener múltiples agentes.
from typing import Tuple
from mesa import Agent, Model, model 

# Debido a que necesitamos que existe un solo agente por celda, elegimos ''SingleGrid''.
from mesa.space import Grid, MultiGrid

# Con ''SimultaneousActivation, hacemos que todos los agentes se activen ''al mismo tiempo''.
from mesa.time import SimultaneousActivation

# Haremos uso de ''DataCollector'' para obtener información de cada paso de la simulación.
from mesa.datacollection import DataCollector

# Importamos los siguientes paquetes para el mejor manejo de valores numéricos.
import numpy as np
import pandas as pd

# Definimos otros paquetes que vamos a usar para medir el tiempo de ejecución de nuestro algoritmo.
import time
import datetime
import random


def get_grid(model):
    width = model.gridAgents.width
    height = model.gridAgents.height
    grid = np.zeros( (width,height) )
    for i in range(width):
        for j in range(height):
            grid[i][j] = model.gridCells[i][j]
    return grid


class CleanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wasCleaning = False

    def step(self):
        if self.wasCleaning or self.model.gridCells[self.pos[0]][self.pos[1]] == 0:
            choicePositions = [-1, 0, 1]
            xPosition = random.choice(choicePositions)
            if xPosition == 0:
                choicePositions.remove(0)
            yPosition = random.choice(choicePositions)

            if self.isValid(self.pos[0]+xPosition, self.pos[1]+yPosition):
                self.pos = (self.pos[0]+xPosition, self.pos[1]+yPosition)
                self.model.numMovements += 1
            
            self.wasCleaning = False
        
        else:
            self.wasCleaning = True
            self.model.gridCells[self.pos[0]][self.pos[1]] = 0
            self.model.dirtyCells -= 1

    def isValid(self, x, y):
        if x >=0 and x< self.model.gridAgents.width and y >= 0 and y < self.model.gridAgents.height:
            return True
        return False


class CellModel(Model):
    def __init__(self, width, height, numAgents, dirtyPercentage):
        self.numAgents = numAgents
        self.gridAgents = MultiGrid(width, height, False)
        self.gridCells = np.zeros((width, height), bool)
        self.schedule = SimultaneousActivation(self)
        self.dirtyPercentage = dirtyPercentage
        self.numMovements = 0
        self.totalCells = width*height
        self.dirtyCells = np.floor(self.totalCells * dirtyPercentage)

        dirtyCellsLeft = self.dirtyCells
        while dirtyCellsLeft > 0:
            
        for row in range(width):
            for col in range(height):
                if dirtyCellsLeft > 0:
                    self.gridCells[row][col] = 1
                    dirtyCellsLeft -= 1
        
        np.random.shuffle(self.gridCells)

        for agent in range(self.numAgents):
            a = CleanAgent(agent, self)
            self.gridAgents.place_agent(a, (0, 0))
            self.schedule.add(a)

        # Aquí definimos el recolector para obtener el grid completo.
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def isDirty(self, row, col):
        if self.gridCells[row][col] == 1:
            return True
        else:
            return False