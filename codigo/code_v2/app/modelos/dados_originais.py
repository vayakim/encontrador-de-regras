import pandas as pd

class dadosOriginais:
    def __init__(self, data, metadata, origem, destino):
        self.data = data
        self.metadata = metadata
        self.origem = origem
        self.destino = destino

        #ordenando cronoologicamente
        self.data_ordenado = self.data.copy()
        self.data_ordenado[metadata] = pd.to_datetime(self.data[metadata], dayfirst=True)
        self.data_ordenado.sort_values(by=metadata, inplace=True)
        self.data_ordenado.reset_index(inplace=True, drop=True)

    def get_data(self):
        return self.data
    
    def get_data_original_ordenado(self):
        return self.data_ordenado