from .dados_originais import dadosOriginais
from .dados_modificados import dadosModificados
from .buscador_de_regras import buscadorRegras
import time

class Modelo:
    def __init__(self):
        self.dados_originais = None
        self.dados_modificados = None
        self.buscador_regras = None
        self.regras = None

    def set_dados_originais(self, data, metadata, origem, destino):
        self.dados_originais = dadosOriginais(data, metadata, origem, destino)

    def set_dados_modificados(self, data, metadata, origem, destino):
        self.dados_modificados = dadosModificados(data, metadata, origem, destino)


    def set_regras_parametros(self, min_rep, min_conf, janela_tempo):
        if self.buscador_regras is None:
            self.buscador_regras = buscadorRegras(janela_tempo, min_rep, min_conf)
        else:
            self.buscador_regras.set_infos_regras(janela_tempo, min_rep, min_conf)

    def buscar_regras(self):
        self.buscador_regras.set_dataset(self.dados_modificados.get_dados_ordenados())
        self.buscador_regras.set_infos_dados(self.dados_modificados.metadata, self.dados_modificados.origem, self.dados_modificados.destino)
        inicio_baldes = time.time()
        self.buscador_regras.gerar_baldes()
        final_baldes = time.time()

        print('Tempo para gerar baldes: ', final_baldes - inicio_baldes)

        numero_de_baldes = len(self.buscador_regras.baldes)
        print('Numero de baldes gerados: ', numero_de_baldes)

        print('Gerando regras com os parametros: ', self.buscador_regras.janela_tempo, self.buscador_regras.min_rep, self.buscador_regras.min_conf)
        self.regras = self.buscador_regras.gerar_regras()
        return self.regras
    
    def get_itemsets(self):
        if self.regras is None:
            return None
        
        itemsets = self.regras.copy()

        padroes = []
        for index, row in itemsets.iterrows():
            padroes.append(row['Antecedente'] + (row['Consequente'],))

        itemsets['Padrão'] = padroes
        itemsets.drop(columns=['Antecedente', 'Consequente', 'Conf'], inplace=True)

        #remover duplicatas e permutações entre os elementos
        padroes_sem_duplicatas = []
        indices_para_remover = []
        for index, row in itemsets.iterrows():
            if tuple(sorted(row['Padrão'])) not in padroes_sem_duplicatas:
                padroes_sem_duplicatas.append(tuple(sorted(row['Padrão'])))
            else:
                indices_para_remover.append(index)
        itemsets.drop(indices_para_remover, inplace=True)
        itemsets.reset_index(drop=True, inplace=True)
        itemsets.apply(lambda x: tuple(sorted(x['Padrão'])), axis=1)

        padroes_arvore = []
        for index, row in itemsets.iterrows():
            padroes_arvore.append((list(row['Padrão']), row['Frequência']))


        self.itemsets = itemsets
        self.itemsets_tree_view = None

        return self.itemsets, self.itemsets_tree_view
    
    def gerar_arvore_dos_itemsets(self, lista_tuplas):
        # Função para encontrar os conjuntos com o maior número de elementos distintos
        def encontrar_nos_pais(lista_tuplas):
            conjuntos_info = [(set(tupla), info_adicional) for tupla, info_adicional in lista_tuplas]
            max_tamanho = max(len(conjunto) for conjunto, _ in conjuntos_info)
            return [(list(tupla), info_adicional) for tupla, info_adicional in lista_tuplas if len(set(tupla)) == max_tamanho]

        # Função para encontrar os subconjuntos de um conjunto
        def subconjuntos(conjunto):
            subconjuntos = [[]]
            for elemento in conjunto:
                subconjuntos.extend([subset + [elemento] for subset in subconjuntos])
            return subconjuntos[1:]  # Remova o conjunto vazio

        # Encontre os nós pais
        nos_pais = encontrar_nos_pais(lista_tuplas)

        # Construa a árvore
        arvore = []
        for no_pai, info_pai in nos_pais:
            subconjuntos_pai = subconjuntos(set(no_pai))
            no_pai_e_filhos = [(no_pai, info_pai)]
            for subconjunto in subconjuntos_pai:
                if list(subconjunto) in [tupla for tupla, _ in lista_tuplas]:
                    info_filho = [info for tupla, info in lista_tuplas if list(tupla) == list(subconjunto)][0]
                    no_pai_e_filhos.append((list(subconjunto), info_filho))
            arvore.append(no_pai_e_filhos)

       # Função para imprimir a árvore de forma recursiva
        def imprimir_arvore(arvore, nivel=0):
            if arvore is None:
                return
            for no_pai_e_filhos in arvore:
                print("  " * nivel + str(no_pai_e_filhos[0]))
                for filho, info_filho in no_pai_e_filhos[1:]:
                    print("  " * (nivel + 1) + str(filho) + " - " + info_filho)

        # Imprimir a árvore
        imprimir_arvore(arvore)
        return arvore

    def get_regras(self):
        if self.regras is None:
            return None
    
        return self.regras
    
    def get_dados_originais_ordenado(self):
        return self.dados_originais.get_data_original_ordenado()
    
    def get_dados_com_cluster(self):
        return self.buscador_regras.dados_com_cluster