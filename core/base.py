class Base:
  def __init__(self, table, instance_name):
    self._table: 'dict[int, dict[int, float]]' = table
    self._instance_name: 'str' = instance_name
    self._alg_report: 'dict[str, list[float]]' = {
      'custos': [], 
      'tempos': []
    }

  def quality(self, base_path):
    path = base_path[:]
    path_cost = 0
    for i in range(len(path) - 1):
      current_point = path[i]
      next_point = path[i + 1]
      path_cost += self._table[current_point][next_point]
    
    return path_cost