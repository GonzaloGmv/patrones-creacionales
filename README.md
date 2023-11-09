# patrones-creacionales

El link a este repositorio es [github](https://github.com/GonzaloGmv/patrones-creacionales)

### Ejercicio 1: Análisis Modular de las Activaciones del SAMUR-Protección Civil en Madrid con Abstract Factory

Este ejercicio pedía desarrollar un programa en Python que hiciera uso del patrón de diseño "Abstract Factory" para modularizar y estandarizar el análisis de unos datos del samur.

Para esto, lo primero era leer estos datos y modelizarlos. 

Lo que hice para limpiar estos datos es lo siguiente:
- Eliminar la columna 'Año': Al ser todos los datos de 2023, esta columna estaba repetida y no aportaba nada
- Sustituir por 0 los valores nulos de la columna 'Hospital': Si esta columna esta vacía significa que el paciente no ha sido hospitalizado.
- Eliminar las filas con valores nulos
- Crea una nueva columna 'Tiempo(minutos)' para ver la diferencia entre las columnas "Hora Solicitud" y "Hora Intervención"
- Corregir las diferencias a través de la medianoche sumando un día cuando es necesario
- Eliminar las filas con 0.0 en la columna Tiempo(minutos)
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
Lo siguiente es hacer el patrón abstracr factory.

Para este proyecto he creado dos fábricas que fabricaran los productos de dos maneras distintas. Los productos son Mes y Distrito.

Las fábricas tienen dos funciones cada una, una para la media y otra para la mediana.

En la primera fábrica, la función de la media imprime en la terminal el valor medio de Tiempo de espera para cada mes o distrito respectivamente, y lo mismo para la mediana.

La segunda fábrica hace lo mismo pero de otra forma, por lo quee también calculaba la media y la mediana de Tiempo de espera para cada mes o distrito, pero en vez de imprimirlo en la terminal, hace un histograma.

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
