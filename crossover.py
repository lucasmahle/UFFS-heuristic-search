
import random


class Crossover:
  def __init__(self, parent1, parent2):
    self.__parent1 = parent1.copy()
    self.__parent2 = parent2.copy()
    pass
    
  def __swap_parents(self):
    self.__parent1, self.__parent2 = self.__parent2, self.__parent1

  def __generate_child(self):
    solution_length = len(self.__parent1)
    path_options = list(range(1, solution_length + 1))
    child = []
    current_parent = 1

    for i in range(solution_length):
      current_node = self.__parent1[i] if current_parent == 1 else self.__parent2[i]
      
      if current_node in child:
        current_node = random.choice(path_options)

      path_options.remove(current_node)
      child.append(current_node)

      current_parent = 2 if current_parent == 1 else 1

    return child
    
  def get_children(self):
    child1 = self.__generate_child()
    self.__swap_parents()
    child2 = self.__generate_child()
    return child1, child2