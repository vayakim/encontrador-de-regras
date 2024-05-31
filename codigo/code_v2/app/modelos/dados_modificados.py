import pandas as pd

class dadosModificados:
    def __init__(self, data, metadata, origem, destino):
        self.data = data
        self.metadata = metadata
        self.origem = origem
        self.destino = destino
        
        #retirando colunas que não serão usadas
        self.data = self.data[[self.metadata, self.origem, self.destino]]

        #colocando os dados em ordem cronológica
        self.data.loc[:, metadata] = pd.to_datetime(self.data[metadata], dayfirst=True)
        self.data.sort_values(by=metadata, inplace=True)
        self.data.reset_index(inplace=True, drop=True)

        self.data_ordenado = self.data.copy()

    def get_dados_ordenados(self):
        return self.data_ordenado