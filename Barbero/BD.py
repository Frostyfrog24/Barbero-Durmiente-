import threading
import time

# Definimos la clase Barbero
class Barbero:
    def __init__(self, sillas):
        self.sillas = sillas
        self.sillas_ocupadas = 0
        self.corte_de_cabello_terminado = threading.Event()
        self.cliente_en_silla = threading.Event()
        self.cliente_en_silla.clear()
    
    def esperar_cliente(self):
        print("El barbero está durmiendo.")
        while True:
            if self.sillas_ocupadas == 0:
                print("No hay clientes, el barbero se queda durmiendo.")
                self.cliente_en_silla.clear()
                self.corte_de_cabello_terminado.clear()
            self.cliente_en_silla.wait()
            self.sillas_ocupadas -= 1
            print("El barbero está cortando el cabello.")
            time.sleep(5)
            self.corte_de_cabello_terminado.set()
        
    def atender_cliente(self):
        while True:
            if self.sillas_ocupadas == self.sillas:
                print("No hay sillas disponibles, el cliente se va.")
                
            self.sillas_ocupadas += 1
            print("Un cliente se sienta en una silla.")
            self.cliente_en_silla.set()
            self.corte_de_cabello_terminado.wait()
            break
# Definimos la clase Cliente
class Cliente:
    def __init__(self, barbero):
        self.barbero = barbero
    
    def entrar_a_la_tienda(self):
        while True:
            self.barbero.atender_cliente()
            print("El cliente está siendo atendido.")
            self.barbero.corte_de_cabello_terminado.wait()
            print("El cliente se va con el cabello cortado.")

# Creamos las instancias de la clase Barbero y Cliente
barbero = Barbero(3)
cliente = Cliente(barbero)

# Creamos los hilos para el barbero y el cliente
hilo_barbero = threading.Thread(target=barbero.esperar_cliente)
hilo_cliente = threading.Thread(target=cliente.entrar_a_la_tienda)

# Iniciamos los hilos
hilo_barbero.start()
hilo_cliente.start()

# Esperamos a que los hilos terminen
hilo_barbero.join()
hilo_cliente.join()
