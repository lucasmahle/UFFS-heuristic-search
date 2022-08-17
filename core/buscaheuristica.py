from os import listdir
from os.path import isfile, join
from core.datasetloader import loader

CSV_SEPARATOR = ','

class BuscaHeuristica:
  def __init__(self):
    self.__instances_info = []
  
  def load_instances(self, path):
    instances_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    for instance_file in instances_files:
      instance_dataset = loader(instance_file)
            
      self.__instances_info.append({
        'name': instance_dataset.get_file_name(),
        'data': instance_dataset.processa_data_set(),
      })

  def set_results_file_path(self, results_file_path):
    self.__results_file_path = results_file_path
    # Limpar arquivo resultados
    f = open(self.__results_file_path, 'w')
    f.write(CSV_SEPARATOR.join(['instancia', 'q-medio', 'q-desvio', 'tempo', 'alfa', 'mutacao', 'filhos']))
    f.close()


  def get_instances(self):
    return self.__instances_info

  def append_result(self, result_object):
    # Adicionar info no arquivo resultados
    f = open(self.__results_file_path, 'a+')

    f.write(
      '\n' +
      CSV_SEPARATOR.join([
        result_object['name'],
        str(result_object['q_medio']),
        str(result_object['q_desvio']),
        str(result_object['tempo']),
        str(result_object['alfa']),
        str(result_object['mutacao']),
        str(result_object['filhos']),
      ])
    )

    f.close()
