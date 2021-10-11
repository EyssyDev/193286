import threading
import random
import time

class Filosofo(threading.Thread):
    cena = True

    def __init__(self, nombreFilosofico, tenedorIzquierdo, tenedorDerecho):
        threading.Thread.__init__(self)
        self.nombre = nombreFilosofico
        self.tenedorIzq = tenedorIzquierdo
        self.tenedorDer = tenedorDerecho
 
    def run(self):
        time.sleep(random.randint(1,10))
        print ('%s esta hambriento.' % self.nombre)
        self.cenar()
 
    def cenar(self):
        tenedor1, tenedor2 = self.tenedorIzq, self.tenedorDer
 
        while self.cena:
            tenedor1.acquire(True)
            ocupado = tenedor2.acquire(False)
            if ocupado: break
            tenedor1.release()
            print ('%s cambia los tenedores.' % self.nombre)
            tenedor1, tenedor2 = tenedor2, tenedor1
        else:
            return
 
        self.cenando()
        tenedor2.release()
        tenedor1.release()
 
    def cenando(self):			
        print ('%s comienza a comer. '% self.nombre)
        time.sleep(random.randint(1,30))
        print ('%s termino de comer y se retiro de la mesa.' % self.nombre)
 
def mesa():
    tenedores = [threading.Lock() for n in range(2)]
    nombreDeLosFilosofos = ('Aristoteles','Kant','Spinoza','Marx', 'Russel')
    filosofos = [Filosofo(nombreDeLosFilosofos[i], tenedores[i%2], tenedores[(i+1)%2]) for i in range(5)]
    Filosofo.cena = True
    for f in filosofos: f.start()

if __name__ == "__main__":
    mesa()