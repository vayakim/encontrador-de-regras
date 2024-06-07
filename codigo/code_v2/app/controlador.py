


class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo
    
    def set_dados_originais(self, dados, metadata, origem, destino):
        self.modelo.set_dados_originais(dados, metadata, origem, destino)
    
    def set_dados_modificados(self, dados, metadata, origem, destino):
        self.modelo.set_dados_modificados(dados, metadata, origem, destino)

    def set_regras_parametros(self, min_rep, min_conf, janela_tempo):
        self.modelo.set_regras_parametros(min_rep, min_conf, janela_tempo)

    def get_regras(self):
        return self.modelo.buscar_regras()

    
    def get_itemsets(self):
        return self.modelo.get_itemsets()

    def get_dados_originais(self):
        return self.modelo.dados_originais.data
    
    def get_dados_originais_ordenados(self):
        return self.modelo.get_dados_originais_ordenado()
    
    def get_dados_com_cluster(self):
        return self.modelo.get_dados_com_cluster()


