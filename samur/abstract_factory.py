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

# El producto Mes hecho por la fábrica de análisis estadístico
class ConcreteProductAnalisisMes(AbstractProductMes):
    def media_mes(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        return media

# El producto Mes hecho por la fábrica de visualización gráfica   
class ConcreteProductGraficaMes(AbstractProductMes):
    def media_mes(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/GraficaMes.png')
        plt.close()

# Abstract Product: Distrito
class AbstractProductDistrito(ABC):
    @abstractmethod
    def media_distrito(self):
        pass

# El producto Distrito hecho por la fábrica de análisis estadístico
class ConcreteProductAnalisisDistrito(AbstractProductDistrito):
    def media_distrito(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        return media

# El producto Distrito hecho por la fábrica de visualización gráfica   
class ConcreteProductGraficaDistrito(AbstractProductDistrito):
    def media_distrito(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Distrito')
        plt.xlabel('Distrito')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/GraficaDistrito.png')
        plt.close()


def client_code(factory: AbstractFactory):
    # Carga el csv
    data = pd.read_csv('samur/data.csv')

    # Crea los productos mes y distrito para posteriormente crearlos en las fabricas
    productMes = factory.create_mes()
    productDistrito = factory.create_distrito()
    
    # Condicionales para utilizar la fabrica correspondiente en cada caso
    if isinstance(factory, ConcreteFactoryAnálisis):
        # La fabrica de análisis estadístico crea los productos mes y distrito
        mes_analisis = productMes.media_mes(data)
        distrito_analisis = productDistrito.media_distrito(data)
        print(f"Análisis de Mes - Media:")
        print(mes_analisis)
        print(f"Análisis de Distrito - Media:")
        print(distrito_analisis)
        
    elif isinstance(factory, ConcreteFactoryGrafica):
        # La fabrica de visualización gráfica crea los productos mes y distrito 
        print(f"Visualización de Mes - Histograma creado")
        productMes.media_mes(data)
        print(f"Visualización de Distrito - Histograma creado")
        productDistrito.media_distrito(data)