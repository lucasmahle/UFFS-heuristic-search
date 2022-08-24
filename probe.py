from math import sqrt, ceil
import random
import time
import numpy as np
from core import Base

from crossover import Crossover
from bccf import BCCF

PATH_COST_INDEX = 0
PATH_INDEX = 1

class Probe(Base):
  def __init__(self, table, instance_name, parameters):
    super().__init__(table, instance_name)
    self.bccf = BCCF(table, instance_name, parameters['alfa'])
    self.mutation = parameters['mutacao'] / 100
    self.sons = parameters['filhos'] / 100
   
  def __alg(self):
    table_len = len(self._table)
    
    # 1 - Gerar população de soluções
    n_solutions = self.calculate_number_solutions(table_len)
    population = self.generate_population(n_solutions)

    process_timeout = table_len * (180 / 1000)
    process_time = 0
    timeout_base = time.process_time()

    while process_timeout > process_time:
      random.shuffle(population)
      old_generation = []
      next_generation = []

      while len(population) > 0:
        # 2 - Selecionar os reprodutores
        p1, p2 = population.pop(), population.pop()
        old_generation.append(p1)
        old_generation.append(p2)

        # 3 - Aplicar operador de recombinação
        crossover = Crossover(p1[PATH_INDEX], p2[PATH_INDEX])
        child1, child2 = crossover.get_children()
        next_generation.append((None, child1))
        next_generation.append((None, child2))

      # 4 - Mutação
      mutation_length = ceil(len(next_generation) * self.mutation)
      random.shuffle(next_generation)
      for i in range(mutation_length):
        self.cause_mutation(next_generation[i])

      # 5 - Seleção natural
      next_generation_length = ceil(len(next_generation) * self.sons)
      old_generation_length = len(old_generation) - next_generation_length
      
      for i in range(n_solutions):
        old_generation[i] = (super().quality(old_generation[i][PATH_INDEX]), old_generation[i][PATH_INDEX])
        next_generation[i] = (super().quality(next_generation[i][PATH_INDEX]), next_generation[i][PATH_INDEX])

      old_generation.sort(key=lambda path: path[PATH_COST_INDEX])
      next_generation.sort(key=lambda path: path[PATH_COST_INDEX])
      population = old_generation[:old_generation_length] + next_generation[:next_generation_length]

      process_time = time.process_time() - timeout_base
    
    population.sort(key=lambda path: path[PATH_COST_INDEX])
    
    self._alg_report['custos'].append(population[0][PATH_COST_INDEX])

  def cause_mutation(self, child):
    child_len = len(child)
    node1 = random.randint(0, child_len)
    node2 = node1
    while node2 == node1:
      node2 = random.randint(0, child_len)
    
    child[PATH_INDEX][node1], child[PATH_INDEX][node2] = child[PATH_INDEX][node2], child[PATH_INDEX][node1]
  
  def generate_population(self, n):
    return [(None, path) for path in self.bccf.run(n)]

  def calculate_number_solutions(self, table_len):
    n = ceil(sqrt(table_len))

    if n % 2 > 0: n += 1
    
    return n

  def run(self):
    for _ in range(10):
      self.__alg()

    return {
      'q_medio': round(np.mean(self._alg_report['custos'])),
      'q_desvio': round(np.std(self._alg_report['custos']), 2),
    }