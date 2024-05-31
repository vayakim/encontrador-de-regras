# controller.py
# O controller é responsável por processar os dados recebidos da view e enviá-los para o model.
import threading
import time

class Controlador(threading.Thread):
    def __init__(self, modelo, visao):
        super().__init__()
        self.modelo = modelo
        self.visao = visao
        self.running = True

    def run(self):
        while self.running:
            dados = self.modelo.dados
            texto = self.modelo.get_processos()
            self.visao.atualizar_dados(texto)
            time.sleep(5)

    
    def parar(self):
        self.running = False

