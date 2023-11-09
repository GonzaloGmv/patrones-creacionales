# patrones-creacionales

El link a este repositorio es [github](https://github.com/GonzaloGmv/patrones-creacionales)

### Ejercicio 1: Análisis Modular de las Activaciones del SAMUR-Protección Civil en Madrid con Abstract Factory

Este ejercicio pedía desarrollar un programa en Python que hiciera uso del patrón de diseño "Abstract Factory" para modularizar y estandarizar el análisis de unos datos del samur.

Para esto, lo primero era leer estos datos y modelizarlos. 

Lo que hice para limpiar estos datos es lo siguiente:
- Eliminar la columna 'Año': Al ser todos los datos de 2023, esta columna estaba repetida y no aportaba nada.
- Sustituir por 0 los valores nulos de la columna 'Hospital': Si esta columna está vacía significa que el paciente no ha sido hospitalizado.
- Eliminar las filas con valores nulos.
- Crea una nueva columna 'Tiempo(minutos)' para ver la diferencia entre las columnas "Hora Solicitud" y "Hora Intervención".
- Corregir las diferencias a través de la medianoche sumando un día cuando es necesario.
- Eliminar las filas con 0.0 en la columna Tiempo(minutos).
- Eliminar las filas cuyo Tiempo(minutos) sea mayor que 60: al ser un servicio de emergencia no debería superar esa cifra, por lo que se considera un error.

El código es el siguiente:
```
import pandas as pd
import numpy as np

# Carga el csv de la URL y lo guarda en un objeto de tipo DataFrame
URL = "https://datos.madrid.es/egob/catalogo/300178-12-samur-activaciones.csv"
data = pd.read_csv(URL, sep=';', encoding='UTF-8')

# Elimina la columna Año ya que es siempre el mismo
data = data.drop(columns=['Año'])

# Los valores nulos de la columna "Hospital" se sustituyen por 0
data['Hospital'] = data['Hospital'].fillna(0)

# Elimina las filas con valores nulos
data = data.dropna()

# Convierte las columnas "Hora Solicitud" y "Hora Intervención" a objetos de tipo datetime
data['Hora Solicitud'] = pd.to_datetime(data['Hora Solicitud'], format='%H:%M:%S')
data['Hora Intervención'] = pd.to_datetime(data['Hora Intervención'], format='%H:%M:%S')

# Calcula la diferencia entre las columnas y crea una nueva columna "Tiempo Espera"
data['Tiempo Espera'] = data['Hora Intervención'] - data['Hora Solicitud']

# Corrige las diferencias a través de la medianoche sumando un día cuando es necesario
data['Tiempo Espera'] = np.where(data['Hora Intervención'] < data['Hora Solicitud'], data['Tiempo Espera'] + pd.Timedelta(days=1), data['Tiempo Espera'])

# Elimina las columnas "Hora Solicitud" y "Hora Intervención" ya que no son necesarias
data = data.drop(columns=['Hora Solicitud'])
data = data.drop(columns=['Hora Intervención'])

# Añade la columna Tiempo(minutos) con el tiempo de espera en minutos
data['Tiempo(minutos)'] = data['Tiempo Espera'].dt.seconds / 60

# Elimina las filas con 0.0 en la columna Tiempo(minutos)
data = data[data['Tiempo(minutos)'] != 0.0]

# Elimina las filas cuyo Tiempo(minutos) sea mayor que 60, ya que al ser un servicio de emergencia no debería superar esa cifra, por lo que se considera un error
data = data[data['Tiempo(minutos)'] < 60]

# Guarda el DataFrame en un archivo csv
data.to_csv('samur/data.csv', index=False)
```
Lo siguiente es hacer el patrón Abstract Factory.

Para este proyecto he creado dos fábricas que fabrican los productos de dos maneras distintas. Los productos son Mes y Distrito.

Las fábricas tienen dos funciones cada una, una para la media y otra para la mediana.

En la primera fábrica, la función de la media imprime en la terminal el valor medio de Tiempo de espera para cada mes o distrito respectivamente, y lo mismo para la mediana.

La segunda fábrica hace lo mismo pero de otra forma, por lo quee también calcula la media y la mediana de Tiempo de espera para cada mes o distrito, pero en vez de imprimirlo en la terminal, hace un histograma.

De esta forma, con el Abstract Factory, teniendo dos productos, podemos fabricar sus variantes en distintas fábricas, es decir, de los productos mes y distrito, hemos fabricado las variantes gráficas y numéricas en distintas fábricas, tanto para la media como para la mediana.

El código es el siguiente:
```
import pandas as pd
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

# Abstract Factory
class AbstractFactory(ABC):
    @abstractmethod
    def create_mes(self):
        pass

    @abstractmethod
    def create_distrito(self):
        pass

# Concrete Factory de análisis estadístico
class ConcreteFactoryAnálisis(AbstractFactory):
    def create_mes(self):
        return ConcreteProductAnalisisMes()

    def create_distrito(self):
        return ConcreteProductAnalisisDistrito()

# Concrete Factory de visualización gráfica
class ConcreteFactoryGrafica(AbstractFactory):
    def create_mes(self):
        return ConcreteProductGraficaMes()

    def create_distrito(self):
        return ConcreteProductGraficaDistrito()

# Abstract Product: Mes
class AbstractProductMes(ABC):
    @abstractmethod
    def media_mes(self):
        pass

    @abstractmethod
    def mediana_mes(self):
        pass

# El producto Mes hecho por la fábrica de análisis estadístico
class ConcreteProductAnalisisMes(AbstractProductMes):
    def media_mes(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        return media
    
    def mediana_mes(self, data):
        mediana = data.groupby('Mes')['Tiempo(minutos)'].median()
        return mediana

# El producto Mes hecho por la fábrica de visualización gráfica   
class ConcreteProductGraficaMes(AbstractProductMes):
    def media_mes(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/MediaGraficaMes.png')
        plt.close()
    
    def mediana_mes(self, data):
        mediana = data.groupby('Mes')['Tiempo(minutos)'].median()
        mediana.plot(kind='bar')
        plt.title('Mediana de Tiempo(minutos) por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/MedianaMes.png')
        plt.close()

# Abstract Product: Distrito
class AbstractProductDistrito(ABC):
    @abstractmethod
    def media_distrito(self):
        pass

    @abstractmethod
    def mediana_distrito(self):
        pass

# El producto Distrito hecho por la fábrica de análisis estadístico
class ConcreteProductAnalisisDistrito(AbstractProductDistrito):
    def media_distrito(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        return media
    
    def mediana_distrito(self, data):
        mediana = data.groupby('Distrito')['Tiempo(minutos)'].median()
        return mediana

# El producto Distrito hecho por la fábrica de visualización gráfica   
class ConcreteProductGraficaDistrito(AbstractProductDistrito):
    def media_distrito(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Distrito')
        plt.xlabel('Distrito')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/MediaDistrito.png')
        plt.close()
    
    def mediana_distrito(self, data):
        mediana = data.groupby('Distrito')['Tiempo(minutos)'].median()
        mediana.plot(kind='bar')
        plt.title('Mediana de Tiempo(minutos) por Distrito')
        plt.xlabel('Distrito')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/MedianaDistrito.png')
        plt.close()

def client_code(factory: AbstractFactory):
    # Carga el csv
    data = pd.read_csv('samur/data.csv')

    # Crea los productos mes y distrito para posteriormente crearlos en las fabricas
    productMes = factory.create_mes()
    productDistrito = factory.create_distrito()
    
    # Condicionales para utilizar la fabrica correspondiente en cada caso
    if isinstance(factory, ConcreteFactoryAnálisis):
        # La fabrica de análisis estadístico crea los productos mes y distrito. Tanto la media como la mediana
        mes_media = productMes.media_mes(data)
        mes_mediana = productMes.mediana_mes(data)
        distrito_media = productDistrito.media_distrito(data)
        distrito_mediana = productDistrito.mediana_distrito(data)
        print(f"Análisis de Mes - Media:")
        print(mes_media)
        print(f"Análisis de Mes - Mediana:")
        print(mes_mediana)
        print(f"Análisis de Distrito - Media:")
        print(distrito_media)
        print(f"Análisis de Distrito - Mediana:")
        print(distrito_mediana)

        
    elif isinstance(factory, ConcreteFactoryGrafica):
        # La fabrica de visualización gráfica crea los productos mes y distrito 
        print(f"Visualización de Mes - Histograma de media de Tiempo(minutos) por mes creado")
        productMes.media_mes(data)
        print(f"Visualización de Distrito - Histograma de mediana de Tiempo(minutos) por mes creado")
        productMes.mediana_mes(data)
        print(f"Visualización de Distrito - Histograma de media de Tiempo(minutos) por distrito creado")
        productDistrito.media_distrito(data)
        print(f"Visualización de Distrito - Histograma de mediana de Tiempo(minutos) por distrito creado")
        productDistrito.mediana_distrito(data)
```

### Ejercicio 2: Sistema Integral de Creación y Gestión de Pizzas Gourmet con Almacenamiento en CSV utilizando el Patrón Builder

Este ejercicio pedía diseñar una pizzería, que mediante el patrón builder, permitiera al cliente hacer su propio pedido.

Para este ejercicio, el patrón builder es necesario, ya que nos permite un objeto paso a paso, en este caso el pedido.

Dentro del método builder hay cuatro clases importantes:
- Clase Builder: Esta es una clase abstrcta que declara los pasos de construcción de producto que todos los tipos de objetos constructores tienen en común. Aunque en este caso sólo hay un tipo de objeto constructor.
- Clase ConcreteBuilder(Builder): Esta clase hereda los métodos de la clase Builder y los implementa. Si hubiera más de un ConcreteBuilder, implementarían las funciones de distintas maneras. Por ejemplo, uno podría crear la pizza a través del terminal y otro a través de una interfaz gráfica.
- Clase Product: En este caso es la clase Pizza, y es el producto resultante.
- Clase Director: Es el que coordina la construcción, es decir, el que decide el orden de los procesos.

Las funciones que he creado yo dentro de este patrón, son funciones que permiten al usuario mediante inputs crear su pizza.

Una de estas funciones, la funcion produce_ingredientes(), además de pedir al usuario los ingredientes, realiza una sugerencia de qué ingredientes pedir, basándose en sus pedidos anteriores.

El código del patrón builder es el siguiente:
```
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

        # Bucle para seleccionar los ingredientes. En caso de que seleccione más de 8, se le pide que seleccione de nuevo
        while True:
            print("Seleccione hasta 8 ingredientes principales para su pizza (ingrese números separados por comas, máximo 8):")
            # Imprime los ingredientes
            for i, ingrediente in enumerate(ingredientes_principales, 1):
                print(f"{i}. {ingrediente}")

            # Llama a la funcion acceder_pedidos para obtener los ingredientes de los pedidos anteriores del cliente
            ingredientes_anteriores = cliente.acceder_pedidos(pedido)
            # Cuenta la frecuencia de cada ingrediente
            contador_ingredientes = Counter(ingredientes_anteriores)
            # Obtiene los 5 ingredientes más comunes
            ingredientes_repes = contador_ingredientes.most_common(5)
            # Imprime los ingredientes más comunes
            if ingredientes_repes:
                print("\nNuestras sugerencias basándonos en tus anteriores pedidos:", ", ".join(f"{ingrediente}" for ingrediente, frecuencia in ingredientes_repes))

            opcion = input("\nIngrese los números de los ingredientes deseados: ")
            ingredientes_elegidos = []

            if opcion:
                try:
                    seleccion = [int(x) for x in opcion.split(',')]
                    # Lee los números ingresados y los añade a una lista
                    for num in seleccion:
                        if 1 <= num <= len(ingredientes_principales):
                            ingredientes_elegidos.append(ingredientes_principales[num - 1])
                        else:
                            print(f"Opción {num} no válida. Se omitirá.")
                    # Verifica que no se hayan seleccionado más de 8 ingredientes
                    if len(ingredientes_elegidos) <= 8:
                        self._pizza.add("Ingredientes " + "/".join(ingredientes_elegidos))
                        print('\n')
                        break
                    else:
                        print("Seleccione un máximo de 8 ingredientes principales. \n")
                except ValueError:
                    print("Entrada no válida. Inténtelo de nuevo.")
            else:
                print("No se seleccionaron ingredientes principales. \n")
    
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

            opcion = input("Ingrese los números de los extras deseados: ")
            extras_elegidos = []

            if opcion:
                try:
                    seleccion = [int(x) for x in opcion.split(',')]
                    # Lee los números ingresados y los añade a una lista
                    for num in seleccion:
                        if 1 <= num <= len(extras):
                            extras_elegidos.append(extras[num - 1])
                        else:
                            print(f"Opción {num} no válida. Se omitirá.")
                    # Verifica que no se hayan seleccionado más de 3 extras
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
```

Otra parte importante de este ejercicio es la realizada en el módulo guardar_pedido. Este módulo consta de una clase Pedido que se encarga de guardar el pedido en un csv además de mostrarlo en el csv. Esta clase cuenta con 5 funciones. Las funciones son las siguientes:
- numero_pedido(): Esta función se utiliza para generar un número de pedido. Su funcionamiento se basa en leer el csv que contiene todos los pedidos, ver cual es el último número de pedido, y crear un nuevo número sumándole 1 a este último.
- diccionario(): Esta función, a partir del builder, crea un diccionario para cada parte de la pizza.
- guardar(): Esta función recibe el diccionario y el número de pedido de las funciones anteriores y lo guarda todo en un csv.
- ingredientes_anteriores(): Esta función recibe una lista de pedidos y devuelve los ingredientes de estos pedidos.
- mostrar(): Por último esta función muestra el pedido en la terminal.

El código de esta parte es el siguiente:
```
import pandas as pd

# Clase Pedido
class Pedido():
    def __init__(self, builder):
        # Inicializa la pizza
        self.pizza_pedido = builder.pizza
    
    # Funcion que genera el numero de pedido
    def numero_pedido(self):
        try:
            pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
            if not pedidos_df.empty:
                ultimo_id = pedidos_df['numero'].max()
                nuevo_id = ultimo_id + 1
            else:
                nuevo_id = 1
        except FileNotFoundError:
            nuevo_id = 1

        return nuevo_id
    
    # Funcion que crea un diccionario con las partes de la pizza
    def diccionario(self):
        pedido_dict = {'Masa': [part for part in self.pizza_pedido.parts if 'Masa' in part],
                    'Salsa': [part for part in self.pizza_pedido.parts if 'Salsa' in part],
                    'Ingredientes': [part for part in self.pizza_pedido.parts if 'Ingredientes' in part],
                    'Cocción': [part for part in self.pizza_pedido.parts if 'Poco Hecha' in part or 'En su Punto' in part or 'Muy Hecha' in part],
                    'Presentación': [part for part in self.pizza_pedido.parts if 'En Plato' in part or 'En Caja' in part or 'Para Llevar' in part],
                    'Maridaje': [part for part in self.pizza_pedido.parts if 'Vino Tinto' in part or 'Cerveza' in part or 'Agua' in part or 'Refresco' in part or 'Sin bebida' in part],
                    'Borde': [part for part in self.pizza_pedido.parts if 'Borde de Queso' in part or 'Borde Relleno de Jamón y Queso' in part or 'Borde de Ajo y Mantequilla' in part or 'Borde Clásico' in part],
                    'Extras Gourmet': [part for part in self.pizza_pedido.parts if 'Extra' in part]}
        # Cada valor del diccionario es una lista, por lo que se convierte a string
        for key in pedido_dict:
            pedido_dict[key] = ' '.join(pedido_dict[key])
        # Elimina las palabras Ingredientes y Extras Gourmet del valor del diccionario
        pedido_dict['Ingredientes'] = pedido_dict['Ingredientes'][13:]
        pedido_dict['Extras Gourmet'] = pedido_dict['Extras Gourmet'][7:]
        return pedido_dict

    # Funcion que guarda el pedido en un archivo csv a partir del diccionario
    def guardar(self):
        # Llama a la funcion diccionario para obtener el diccionario
        pedido_dict = self.diccionario()
        try:
            pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
        except FileNotFoundError:
            pedidos_df = pd.DataFrame(columns=pedido_dict.keys())

        # Crea una nueva clave-valor en el diccionario con el numero de pedido. Para ello llama a la funcion numero_pedido
        pedido_dict['numero'] = self.numero_pedido()

        # Concatea el diccionario con el DataFrame de pedidos y lo guarda en el archivo CSV
        pedidos_df = pd.concat([pedidos_df, pd.DataFrame([pedido_dict])], ignore_index=True)
        pedidos_df['numero'] = pedidos_df['numero'].astype(int)
        pedidos_df.to_csv('pizzeria/pedidos.csv', index=False)
    
    # Funcion que accede a unos pedidos dada una lista de id y devuelve una lista con los ingredientes
    def ingredientes_anteriores(self, lista_id):
        pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
        if lista_id == 0:
            return []
        else:
            ingredientes = []
            for num in lista_id:
                num = int(float(num))
                # Accede a la fila del DataFrame que corresponde al numero de pedido y obtiene los ingredientes de esa fila
                ingredientes_num = pedidos_df[pedidos_df['numero'] == num]['Ingredientes'].iloc[0]
                # Separa los ingredientes por /
                ingredientes.extend(ingredientes_num.split('/'))
            return ingredientes
    
    # Muestra el pedido en la terminal
    def mostrar(self):
        print("Esta es tu pizza: ")
        pedido_dict = self.diccionario()
        for key, value in pedido_dict.items():
            print(f'{key}: {value}')
```

La última parte de este ejercicio se encuentra en el módulo cliente.py. Este módulo tiene una clase Cliente que se encarga de iniciar sesión o registrarte, guardar los datos en un csv, y de ver los pedidos de ese cliente. Las funciones que tiene esta clase son las siguientes:
- iniciar(): En primer lugar esta función te pregunta si eres nuevo o no, y en función de eso te permite iniciar sesión con tu usuario y contraseña, o registrarse en caso de que seas nuevo. Además, si es un nuevo usuario, añade los datos a un csv donde están todos los clientes.
- pedido_cliente(): Esta función obtiene el número de pedido y lo añade a la información del cliente en el csv. Primero llama a la función numero_pedido de la clase Pedido, a continuación, actualiza la columna pedidos del cliente y le añade este pedido.
- acceder_pedidos(): Esta función accede a la información del cliente en el csv y obtiene todos los ingredientes que ha pedido. En primer lugar, accede a la fila del csv donde está el usuario y obtiene los números de pedido. Después llama a la función ingredientes_anteriores de la clase Pedido y convierte esos números de pedidos en la lista con los ingredientes, que es lo que devolverá.

El código de esta parte es el siguiente:
```
import pandas as pd
import numpy as np

# Clase Cliente
class Cliente():
    def __init__(self):
        # Inicializa las variables vacias que luego se llenaran
        self.usuario = ''
        self.contraseña = ''
        self.telefono = ''
        self.domicilio = ''
        self.pedidos = []
        # Lee el archivo CSV clientes.csv y lo guarda en una variable
        self.clientes_df = pd.read_csv('pizzeria/clientes.csv')

    # Funcion para iniciar sesion o crear un nuevo usuario
    def iniciar(self):
        # Bucle para iniciar sesion o crear un nuevo usuario
        while True:
            nuevo = input('¿Eres un cliente nuevo? (S/N): ')
            if nuevo.lower() == 's':
                # Si es un nuevo cliente, lo registra
                self.telefono = input('Teléfono: ')
                self.domicilio = input('Dirección: ')
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                # Crea un DataFrame con los datos del nuevo cliente
                nuevo_cliente = pd.DataFrame({'Usuario': [self.usuario], 'Contraseña': [self.contraseña], 'Telefono': [self.telefono], 'Domicilio': [self.domicilio]})
                # Concatena el nuevo DataFrame con el DataFrame de clientes
                self.clientes_df = pd.concat([self.clientes_df, nuevo_cliente], ignore_index=True)
                # Guarda el DataFrame actualizado en el archivo CSV
                self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
                break
            elif nuevo.lower() == 'n':
                # Si no es un nuevo cliente, inicia sesion
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                # Verifica si el usuario existe
                if self.usuario in self.clientes_df['Usuario'].values.tolist():
                    # Verifica si la contraseña coincide
                    index = self.clientes_df.index[self.clientes_df['Usuario'] == self.usuario].tolist()[0]
                    stored_password = self.clientes_df.at[index, 'Contraseña']
                    if self.contraseña == stored_password:
                        print('Inicio de sesión exitoso. ¡Bienvenido de nuevo!')
                        break
                    else:
                        print('La contraseña no coincide. Intenta de nuevo.')
                else:
                    print('El usuario no existe. Intenta de nuevo.')
            else:
                print('Opción no válida. Intenta de nuevo.')
    
    # Funcion que obtiene el numero de pedido y lo guarda en el archivo CSV
    def pedido_cliente(self, pedido):
        # Obtiene el numero de pedido del pedido recientemente guardado
        n_pedido = pedido.numero_pedido() -1
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        # Verifica si el cliente tiene pedidos anteriores
        if pd.notna(pedidos_anteriores):
            nuevos_pedidos = f"{pedidos_anteriores}/{n_pedido}"
        else:
            nuevos_pedidos = n_pedido

        # Actualiza la columna 'Pedidos' con los nuevos pedidos
        self.clientes_df.at[user_index, 'Pedidos'] = nuevos_pedidos

        # Guarda el DataFrame actualizado en el archivo CSV
        self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
    
    # Funcion que obtiene los pedidos anteriores del cliente y devuelve los ingredientes de estos pedidos
    def acceder_pedidos(self, pedido):
        # Obtiene los pedidos anteriores del cliente
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        # Verifica si el cliente tiene pedidos anteriores
        if pd.isna(pedidos_anteriores):
            numero_ped = 0
        else:
            # Verificar si hay solo un pedido
            if isinstance(pedidos_anteriores, (int, np.int64)):
                numero_ped = [pedidos_anteriores]
            else:
                # Si hay mas de un pedido, los separa
                numero_ped = str(pedidos_anteriores).split('/')
        # Llama a la funcion ingredientes_anteriores de la clase Pedido que le devuelve los ingredientes
        ingredientes = pedido.ingredientes_anteriores(numero_ped)
        return ingredientes
```

