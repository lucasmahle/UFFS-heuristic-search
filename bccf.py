import random
import time
from core import Base

ALGORITHM = 'bccf'

class BCCF(Base):
  def __init__(self, table, instance_name, alfa):
    super().__init__(table, instance_name)
    self.alpha_update = alfa

  def __alg(self, nr_solutions):
    table_len = len(self._table)
    process_timeout = table_len * (60 / 1000)

    process_time = 0
    timeout_base = time.process_time()
    best_path_cost = None
    solutions = []

    generating_new_path = True

    # Calculate a factor value to multiply
    # It's necessary cuz when eligibles are
    # calculated, the value can be less  
    # than 0
    eligibles_proportion = 10 ** len(str(table_len))

    while process_timeout > process_time or len(solutions) < nr_solutions:
      # Initializing new path solution
      if generating_new_path:
        # Randomize first node and start with it
        start_node = random.randint(1, table_len)
        solution_path = [start_node]
        last_node_added = start_node
        
        # Generate pheromone data
        # Initilize pheromone value with data len 
        pheromone = {i: ({j: table_len for j in range(1, table_len + 1)}) for i in range(1, table_len + 1)}

        # Avoid to restart solution path
        generating_new_path = False   
      
      # Copy node's neighbors
      node_table = self._table[last_node_added].copy()

      # Remove nodes already in use
      [node_table.pop(i, None) for i in solution_path]

      # Calculate V value (V = t/j)
      sum_v = 0
      for node in node_table:
        node_table[node] = pheromone[last_node_added][node] / node_table[node]
        sum_v = sum_v + node_table[node]
      
      # Generate eligibles nodes by V value
      # More chances to be selected (by V),
      # more times the node is inserted
      # on eligibles_nodes list
      eligibles_nodes = []
      for node in node_table:
        percentage = round((node_table[node] / sum_v) * eligibles_proportion)
        eligibles_nodes = eligibles_nodes + [node] * percentage
      
      # Get a random value of list
      last_node_added = random.choice(eligibles_nodes)

      # Append to solution path
      solution_path.append(last_node_added)
      
      # Solution was made
      if len(solution_path) == table_len:
        generating_new_path = True
        path_cost = super().quality(solution_path)
        solutions.append((path_cost, solution_path))
        if best_path_cost is None or path_cost < best_path_cost:
          best_path_cost = path_cost
          # When a new best path is made
          # update pheromones values
          pheromone_alfa_update = (100 + self.alpha_update) / 100
        else:
          # Otherwise, decrease pheromones values
          pheromone_alfa_update = (100 - self.alpha_update) / 100
        
        for i in range(1, table_len): 
          previous_node = solution_path[i - 1]
          current_node = solution_path[i]
          
          pheromone[previous_node][current_node] = pheromone[previous_node][current_node] * pheromone_alfa_update
          pheromone[current_node][previous_node] = pheromone[previous_node][current_node]

      process_time = time.process_time() - timeout_base

    return solutions
    
  def run(self, nr_solutions):
    population = self.__alg(nr_solutions)
    
    # sort solutions
    population.sort(key=lambda path: path[0])

    # return only the path
    return [path[1] for path in population[:nr_solutions]]
