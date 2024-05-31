# main.py
import tkinter as tk
from find_rules_model import Modelo
from find_rules_view import Visao
from find_rules_controller import Controlador

# --------------------------    THREADS    --------------------------
def start_thread():
    modelo.start()
    controlador.start()
def stop_thread():
    modelo.parar()
    controlador.parar()
    modelo.join()
    controlador.join()
# ------------------------------------------------------------------



root = tk.Tk()
root.title("FIND RULES")

modelo = Modelo()
visao = Visao(root)
controlador = Controlador(modelo, visao)

start_thread()
root.mainloop()

stop_thread()
















