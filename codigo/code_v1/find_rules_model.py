# modelo.py
#O modelo é a parte do programa que lida com a lógica de negócios. Ele é responsável por armazenar e manipular os dados.
import threading
import time
import psutil

class Modelo(threading.Thread):
    def __init__(self):
        super().__init__()
        self.dados = {}
        self.running = True

    def run(self):
        while self.running:
            self.process_infos()
    
    def process_infos(self):
        for proc in psutil.process_iter():
            self.dados[proc.pid] = (proc.name(), proc.cpu_percent(), proc.memory_info().rss)

    def get_processos(self):
        texto = ""
        for chave, valor in self.dados.items():
            texto += f"{chave}: {valor}\n"
        return texto

    def parar(self):
        self.running = False