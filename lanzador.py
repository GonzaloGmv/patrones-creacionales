from samur.lanzador_samur import main_lanzador
from pizzeria.lanzador_pizzeria import main_pizzeria

def main():
    while True:
        print("Ejercicio 1: Samur")
        print("Ejercicio 2: Pizzería")
        ejer = input("¿Qué ejercicio quieres ejecutar? (1/2): ")
        if ejer == "1":
            main_lanzador()
            break
        elif ejer == "2":
            main_pizzeria()
            break
        else:
            print("Ejercicio no válido")