import numpy as np
import pandas as pd
import random
import datetime
import names
from tqdm import tqdm
from fim import arules
import time

# Generate synthetic data
start = datetime.datetime(2023, 1, 1)
end = datetime.datetime(2023, 12, 30)
antecedentes = [names.get_full_name() for i in tqdm(range(0,5000), desc='Gerando antecedentes')]
consequentes = [random.randint(1,5000) for i in tqdm(range(0,10000), desc='Gerando consequentes')]


def random_dataset(tamanho):
  """Generate a random dataset
  """

  def random_date():
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
  
  start_time2 = time.time()
  timestamps = [random_date() for i in range(0,tamanho)] 
  end_time2 = time.time()
  print("Tempo de geração de datas: {}".format(end_time2 - start_time2))

  data = []

  start_time3 = time.time()
  for timestamp in timestamps:
      antecedente = antecedentes[random.randint(0,4999)]
      consequente = consequentes[random.randint(0,9999)]
      data.append({'timestamp': timestamp, 'o': antecedente, 'd': consequente})
  end_time3 = time.time()
  print("Tempo de geração de dados: {}".format(end_time3 - start_time3))

  # Create DataFrame
  df = pd.DataFrame(data)
  return df


# with open('results2.txt', 'w') as f:
#   f.close()

# for itens_it in tqdm(range(50,400,50), desc='Execução 1'): #400
#   for buckets_it in range(2000, 100000, 2000): #100000
#     print("Itens: {} | Buckets: {}".format(itens_it, buckets_it))
#     linhas = itens_it * buckets_it
#     # Gerar o arquivo de dados sinteticos de tamanho 'linhas'
#     start_time = time.time()
#     data_teste = random_dataset(linhas)
#     end_time = time.time()
#     print("Tempo de geração: {}".format(end_time - start_time))
#     # Gerar a quantidade de 'buckets' com a quantidade de 'itens'
#     buckets = np.array_split(data_teste, buckets_it)
#     # Aplicar o apriori 
#     start_time = time.time()
#     results =  arules(buckets,supp=-int(3), conf=70, report='ab' , zmin=2)
#     end_time = time.time()

#     # Registrar a quantidade de 'itens', 'buckets' e o tempo de execução (Unico a fazer em arquivo)
#     print("Tempo Apriori: {}".format(end_time - start_time))
#     # Registrar o resultado em um arquivo           
#     with open('results2.txt', 'a') as f:
#       f.write("{},{},{}\n".format(itens_it, buckets_it, end_time - start_time))
#       f.close()
# print("Fim da execução 1")

for buckets_it in tqdm(range(58000, 102000, 2000), desc='Execução 2'): #400
  for itens_it in range(400,1000,50): #100000
    linhas = itens_it * buckets_it
    # Gerar o arquivo de dados sinteticos de tamanho 'linhas'
    start_time = time.time()
    data_teste = random_dataset(linhas)
    end_time = time.time()
    print("Tempo de geração: {}".format(end_time - start_time))
    # Gerar a quantidade de 'buckets' com a quantidade de 'itens'
    buckets = np.array_split(data_teste, buckets_it)
    # Aplicar o apriori 
    start_time = time.time()
    results =  arules(buckets,supp=-int(3), conf=70, report='ab' , zmin=2)
    end_time = time.time()

    # Registrar a quantidade de 'itens', 'buckets' e o tempo de execução (Unico a fazer em arquivo)
    print("Itens: {} | Buckets: {} | Tempo Apriori: {}".format(itens_it, buckets_it, end_time - start_time))
    # Registrar o resultado em um arquivo           
    with open('results.txt', 'a') as f:
      f.write("{},{},{}\n".format(itens_it, buckets_it, end_time - start_time))
      f.close()
