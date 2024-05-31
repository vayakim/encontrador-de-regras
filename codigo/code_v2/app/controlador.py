


class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo
    

    def get_regras(self):
        if self.modelo.get_regras() is None:
            return self.modelo.buscar_regras()
        return self.modelo.get_regras()
    
    def get_itemsets(self):
        return self.modelo.get_itemsets()

    def get_dados_originais(self):
        return self.modelo.dados_originais.data
    
    def get_dados_originais_ordenados(self):
        return self.modelo.get_dados_originais_ordenado()
    
    def get_dados_com_cluster(self):
        return self.modelo.get_dados_com_cluster()


