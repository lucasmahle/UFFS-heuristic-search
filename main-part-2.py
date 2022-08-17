import os
import time
from core.buscaheuristica import BuscaHeuristica
from probe import Probe

def main():
  print('Processo iniciado!')
  busca_heuristica = BuscaHeuristica()

  instances_path = os.path.abspath('./final-instance/')
  busca_heuristica.load_instances(instances_path)
  print('Instâncias calculadas')
  
  for instance in busca_heuristica.get_instances():
    instance_name = instance['name']
    results_file_path = os.path.abspath('./reports/' + instance_name.lower() + '.csv')
    busca_heuristica.set_results_file_path(results_file_path)

    melhores_configs = [
      # Western Sahara
      (15,  20, 90),
      (80,  20,  5),
      (85, 100, 15),
      
      # Djibouti
      (80,  20, 85),
      ( 5,  20, 15),
      ( 5, 100, 20),
      
      # Qatar
      (15,  20, 90),
      (15,  10, 80),
      (80, 100, 85),
      
    ]
    for melhor_config in melhores_configs:
      (alfa, filhos, mutacao) = melhor_config
      timeout_base = time.process_time()
      parameters = {
        'alfa': alfa, 
        'mutacao': mutacao / 100, 
        'filhos': filhos / 100
      }

      print(f'Processando instância {instance_name}; Alfa={alfa}%; Filhos={filhos}%; Mutação={mutacao}%')
      alg = Probe(table=instance['data'], instance_name=instance_name, parameters=parameters)
      alg_results = alg.run()
      print('Resultado instância:', alg_results)

      process_time = time.process_time() - timeout_base

      busca_heuristica.append_result({
        'name': instance_name,
        'q_medio': alg_results['q_medio'],
        'q_desvio': alg_results['q_desvio'],
        'tempo': process_time,
        'alfa': alfa,
        'mutacao': mutacao,
        'filhos': filhos,
      })

if __name__ == '__main__':
  main()