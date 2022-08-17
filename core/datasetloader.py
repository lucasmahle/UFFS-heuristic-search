import math
import re

class loader():
  def __init__(self, file):
    self.__file = file

    with open(self.__file, "r") as input_file:
      self.__file_lines = input_file.read().split('\n')

  def __get_file_points_index(self):
    index_init = 0
    index_end = 0

    for i in range(0, len(self.__file_lines)):
      if not self.__file_lines[i].startswith('NODE_COORD_SECTION'): continue

      index_init = i + 1
      break
    
    for i in range(len(self.__file_lines) - 1, 0, -1):
      if self.__file_lines[i] == '' or self.__file_lines[i] == 'EOF':
        continue
      index_end = i + 1
      break

    return (index_init, index_end)
    
  def get_file_name(self):
    pattern = 'locations\ in (.*)'
    for i in range(0, len(self.__file_lines)):
      if re.search(pattern, self.__file_lines[i]) is not None:
        return re.findall(pattern, self.__file_lines[i])[0]

    return ''

  def processa_data_set(self):
    (index_init, index_end) = self.__get_file_points_index()

    str_points = [l.split(' ') for l in self.__file_lines[index_init:index_end]]
    points = {}
    table = {}

    for i in range(len(str_points)):
      points[int(str_points[i][0])] = [float(str_points[i][1]), float(str_points[i][2])]
    
    for point_source_id in points:
      P1 = (points[point_source_id][0], points[point_source_id][1])
      
      for point_dest_id in points:
        if not point_source_id in table: table[point_source_id] = {}

        P2 = (points[point_dest_id][0], points[point_dest_id][1])
        
        if point_source_id == point_dest_id:
          distancia_P1_P2 = 0
        elif point_dest_id < point_source_id:
          distancia_P1_P2 = table[point_dest_id][point_source_id]
        else:
          distancia_P1_P2 = round(math.sqrt((P1[0]-P2[0])**2 + (P1[1]-P2[1])**2))

        table[point_source_id][point_dest_id] = distancia_P1_P2

    return table