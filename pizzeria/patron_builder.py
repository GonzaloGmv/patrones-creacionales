from __future__ import annotations
from abc import ABC, abstractmethod
from collections import Counter

# Abstract Builder
class Builder(ABC):
    @property
    @abstractmethod
    def pizza(self):
        pass

    # Definición de métodos abstractos para construir partes de la pizza
    @abstractmethod
    def produce_masa(self):
        pass

    @abstractmethod
    def produce_salsa(self):
        pass

    @abstractmethod
    def produce_ingredientes(self):
        pass

    @abstractmethod
    def produce_coccion(self):
        pass

    @abstractmethod
    def produce_presentacion(self):
        pass

    @abstractmethod
    def produce_maridaje(self):
        pass

    @abstractmethod
    def produce_borde(self):
        pass

    @abstractmethod
    def produce_extra(self):
        pass

# Clase ConcreteBuilder que implementa la interfaz Builder
class ConcreteBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._pizza = Pizza()

    @property
    def pizza(self):
        pizza = self._pizza
        self.reset()
        return pizza

    # Implementación de métodos para construir partes de la pizza
    def produce_masa(self):
        while True:
            print("\n Seleccione el número correspondiente al tipo de masa de pizza:")
            print("1. Masa Fina")
            print("2. Masa Gruesa")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("Masa Fina")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("Masa Gruesa")
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")


    def produce_salsa(self):
        while True:
            print("Seleccione el número correspondiente al tipo de salsa de pizza:")
            print("1. Salsa de Tomate")
            print("2. Salsa de Pesto")
            print("3. Salsa Barbacoa")
            print("4. Salsa Ranch")
            print("5. Salsa Alfredo")
            print("6. Salsa Carbonara")
            print("7. Ninguna")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("Salsa de Tomate")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("Salsa de Pesto")
                print('\n')
                break
            elif opcion == "3":
                self._pizza.add("Salsa Barbacoa")
                print('\n')
                break
            elif opcion == "4":
                self._pizza.add("Salsa Ranch")
                print('\n')
                break
            elif opcion == "5":
                self._pizza.add("Salsa Alfredo")
                print('\n')
                break
            elif opcion == "6":
                self._pizza.add("Salsa Carbonara")
                print('\n')
                break
            elif opcion == "7":
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")


    def produce_ingredientes(self, cliente, pedido):
        ingredientes_principales = ["Jamón", "Pepperoni", "Champiñones", "Aceitunas", "Pimientos", "Cebolla", "Tomate", "Maíz","Pollo", "Salchichas", "Atún", "Pavo", "Anchoas", "Espinacas", "Albóndigas", "Broccoli", "Huevos", "Alcaparras", "Piña", "Rúcula", "Chorizo", "Carne de res", "Carne de cerdo","Aguacate", "Camarones", "Ajo", "Ricotta", "Jalapeños", "Queso Mozzarella", "Queso Cheddar", "Queso Parmesano", "Queso Gouda", "Ingrediente especial: La 33", "Queso Provolone", "Queso Feta"]

        while True:
            print("Seleccione hasta 8 ingredientes principales para su pizza (ingrese números separados por comas, máximo 8):")
            
            for i, ingrediente in enumerate(ingredientes_principales, 1):
                print(f"{i}. {ingrediente}")

            ingredientes_anteriores = cliente.acceder_pedidos(pedido)
            # Contar la frecuencia de cada ingrediente
            contador_ingredientes = Counter(ingredientes_anteriores)

            # Obtener los 5 ingredientes más comunes
            ingredientes_repes = contador_ingredientes.most_common(5)


            # Imprimir los ingredientes más comunes
            if ingredientes_repes:
                print("\n Nuestras sugerencias basándonos en tus anteriores pedidos:", ", ".join(f"{ingrediente}" for ingrediente, frecuencia in ingredientes_repes))

            opcion = input("\n Ingrese los números de los ingredientes deseados o presione Enter para omitir: ")
            ingredientes_elegidos = []

            if opcion:
                try:
                    seleccion = [int(x) for x in opcion.split(',')]
                    for num in seleccion:
                        if 1 <= num <= len(ingredientes_principales):
                            ingredientes_elegidos.append(ingredientes_principales[num - 1])
                        else:
                            print(f"Opción {num} no válida. Se omitirá.")
                    if len(ingredientes_elegidos) <= 8:
                        self._pizza.add("Ingredientes " + "/".join(ingredientes_elegidos))
                        print('\n')
                        break
                    else:
                        print("Seleccione un máximo de 8 ingredientes principales. \n")
                except ValueError:
                    print("Entrada no válida. Inténtelo de nuevo.")
            else:
                print("No se seleccionaron ingredientes principales. Continuar sin ingredientes. \n")

    
    def produce_coccion(self):
        while True:
            print("Seleccione el número correspondiente al grado de cocción de la pizza:")
            print("1. Poco hecha")
            print("2. En su punto")
            print("3. Muy hecha")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("Poco Hecha")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("En su Punto")
                print('\n')
                break
            elif opcion == "3":
                self._pizza.add("Muy Hecha")
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")



    def produce_presentacion(self) -> None:
        while True:
            print("Seleccione el número correspondiente a la opción de presentación de la pizza:")
            print("1. En plato")
            print("2. En caja")
            print("3. Para llevar")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("En Plato")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("En Caja")
                print('\n')
                break
            elif opcion == "3":
                self._pizza.add("Para Llevar")
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")

    def produce_maridaje(self):
        while True:
            print("Seleccione el número correspondiente al maridaje deseado con la pizza:")
            print("1. Vino tinto")
            print("2. Cerveza")
            print("3. Agua")
            print("4. Refresco")
            print("5. Ninguno (sin maridaje)")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("Vino Tinto")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("Cerveza")
                print('\n')
                break
            elif opcion == "3":
                self._pizza.add("Agua")
                print('\n')
                break
            elif opcion == "4":
                self._pizza.add("Refresco")
                print('\n')
                break
            elif opcion == "5":
                self._pizza.add("Sin bebida")
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")

    
    def produce_borde(self):
        while True:
            print("Seleccione el número correspondiente al tipo de borde de la pizza:")
            print("1. Borde de queso")
            print("2. Borde relleno de jamón y queso")
            print("3. Borde de ajo y mantequilla")
            print("4. Borde clásico")

            opcion = input("Ingrese el número de la opción deseada: ")

            if opcion == "1":
                self._pizza.add("Borde de Queso")
                print('\n')
                break
            elif opcion == "2":
                self._pizza.add("Borde Relleno de Jamón y Queso")
                print('\n')
                break
            elif opcion == "3":
                self._pizza.add("Borde de Ajo y Mantequilla")
                print('\n')
                break
            elif opcion == "4":
                self._pizza.add("Borde Clásico")
                print('\n')
                break
            else:
                print("Opción no válida. Por favor, seleccione un número válido. \n")

    
    def produce_extra(self):
        extras = ["Trufas", "Queso de cabra", "Setas", "Caviar", "Salmón Ahumado"]

        while True:
            print("Seleccione hasta 3 extras gourmet para su pizza (ingrese números separados por comas, máximo 3):")
            
            for i, extra in enumerate(extras, 1):
                print(f"{i}. {extra}")

            opcion = input("Ingrese los números de los extras deseados (ejemplo: 1, 3, 5) o presione Enter para omitir: ")
            extras_elegidos = []

            if opcion:
                try:
                    seleccion = [int(x) for x in opcion.split(',')]
                    for num in seleccion:
                        if 1 <= num <= len(extras):
                            extras_elegidos.append(extras[num - 1])
                        else:
                            print(f"Opción {num} no válida. Se omitirá.")
                    if len(extras_elegidos) <= 3:
                        self._pizza.add("Extras " + "/".join(extras_elegidos))
                        print('\n')
                        break
                    else:
                        print("Seleccione un máximo de 3 extras gourmet.")
                except ValueError:
                    print("Entrada no válida. Inténtelo de nuevo. \n")
            else:
                print("No se seleccionaron extras gourmet. Continuar sin extras. \n")

# Clase que representa una pizza y mantiene un registro de sus partes
class Pizza():
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

# Clase Director que coordina la construcción de la pizza
class Director:
    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def build_full_featured_product(self, cliente, pedido):
        self.builder.produce_masa()
        self.builder.produce_salsa()
        self.builder.produce_ingredientes(cliente, pedido)
        self.builder.produce_coccion()
        self.builder.produce_presentacion()
        self.builder.produce_maridaje()
        self.builder.produce_borde()
        self.builder.produce_extra()