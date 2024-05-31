import pandas as pd


# fazer analise de series temporais usando ARIMA
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

# Carregar os dados
data = pd.read_csv('../datasets/Divisão [MConverter.eu].csv')
metadata = 'DataHora'
origem = 'Conta Origem'
destino = 'Conta Destino'
df = pd.DataFrame(data)

# Converter a coluna referente a metadata para o tipo datetime
df[metadata] = pd.to_datetime(df[metadata], dayfirst=True)

# Agrupar as colunas de origem e destino em uma unica coluna chamada 'Valor'
# exemplo: 'Conta Origem' = 'A' e 'Conta Destino' = 'B' -> 'Valor' = 'A,B'
df['Valor'] = df[origem] + ',' + df[destino]

# dropar as colunas de origem e destino
df.drop([origem, destino], axis=1, inplace=True)


# Definir a coluna 'Data' como índice
df.set_index(metadata, inplace=True)

# Visualizar os dados
print(df)

# Plotar a série temporal
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Valor'], marker='o')
plt.title('Série Temporal das Transações Financeiras')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.grid(True)
plt.show()

print(df)
# co2 = pd.Series(
#     co2, index=pd.date_range("1-1-1959", periods=len(co2), freq="M"), name="CO2"
# )
# co2.describe()

#transformar cada valor unico em um valor numerico
df['Valor'] = pd.Categorical(df['Valor'])
df['Valor'] = df['Valor'].cat.codes
print(df)

#transformar df em uma serie temporal
series = pd.Series(df['Valor'], index=df.index)

# Decompor a série temporal
stl = STL(series, seasonal=13)
result = stl.fit()

# Plotar os componentes da decomposição
result.plot()
plt.show()





# # Plotar os componentes da decomposição
# result.plot()
# plt.show()
