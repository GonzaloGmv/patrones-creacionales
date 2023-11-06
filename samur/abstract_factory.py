import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class AbstractFactory(ABC):
    @abstractmethod
    def create_mes(self):
        pass

    @abstractmethod
    def create_distrito(self):
        pass

# Concrete Factory para análisis estadísticos
class ConcreteFactoryAnalisis(AbstractFactory):
    def create_mes(self):
        return ConcreteProductMesAnalisis()

    def create_distrito(self):
        return ConcreteProductDistritoAnalisis()

# Concrete Factory para visualizaciones gráficas
class ConcreteFactoryGrafica(AbstractFactory):
    def create_mes(self):
        return ConcreteProductMesGrafica()

    def create_distrito(self):
        return ConcreteProductDistritoGrafica()

# Abstract Product para mes
class AbstractProductMes(ABC):
    @abstractmethod
    def calcular_mediaMes(self):
        pass

    @abstractmethod
    def calcular_modaMes(self):
        pass

    @abstractmethod
    def calcular_histogramaMes(self):
        pass

    @abstractmethod
    def calcular_barrasMes(self):
        pass

# Concrete Product para análisis estadísticos de mes
class ConcreteProductMesAnalisis(AbstractProductMes):
    def calcular_mediaMes(self):
        pass
    
    def calcular_modaMes(self):
        pass

# Concrete Product para visualización gráfica de mes
class ConcreteProductMesGrafica(AbstractProductMes):
    def calcular_histogramaMes(self):
        pass
    
    def calcular_barrasMes(self):
        pass

# Abstract Product para distrito
class AbstractProductDistrito(ABC):
    @abstractmethod
    def calcular_mediaDistrito(self):
        pass

    @abstractmethod
    def calcular_modaDistrito(self):
        pass

    @abstractmethod
    def calcular_histogramaDistrito(self):
        pass

    @abstractmethod
    def calcular_barrasDistrito(self):
        pass

# Concrete Product para análisis estadísticos de distrito
class ConcreteProductDistritoAnalisis(AbstractProductMes):
    def calcular_mediaDistrito(self, data):
        pass
    
    def calcular_modaDistrito(self, data):
        pass

# Concrete Product para visualización gráfica de distrito
class ConcreteProductDistritoGrafica(AbstractProductMes):
    def calcular_histogramaDistrito(self, data):
        pass
    
    def calcular_barrasDistrito(self, data):
        pass

def client_code(factory: AbstractFactory):
    data = pd.read_csv('samur/data.csv')

    productMes = factory.create_mes()
    productDistrito = factory.create_distrito()
    
    if isinstance(factory, ConcreteFactoryAnalisis):
        # Realizar análisis estadísticos y generar visualizaciones
        media_mes = productMes.calcular_mediaMes(data)
        moda_mes = productMes.calcular_modaMes(data)

        media_distrito = productDistrito.calcular_mediaDistrito(data)
        moda_distrito = productDistrito.calcular_modaDistrito(data)

        print(f"Análisis de Mes - Media: {media_mes}, Moda: {moda_mes}")
        print(f"Análisis de Distrito - Media: {media_distrito}, Moda: {moda_distrito}")
    
    elif isinstance(factory, ConcreteFactoryGrafica):
        # Generar visualizaciones
        print(f"Visualización de Mes - Histograma: )")
        productMes.calcular_histogramaMes(data)
        print(f"Visualización de Mes - Gráfico de Barras: )")
        productMes.calcular_barrasMes(data)

        print(f"Visualización de Distrito - Histograma: )")
        productDistrito.calcular_histogramaDistrito(data)
        print(f"Visualización de Distrito - Gráfico de Barras: )")
        productDistrito.calcular_barrasDistrito(data)

if __name__ == "__main__":
    analisis_factory = ConcreteFactoryAnalisis()
    client_code(analisis_factory)

    grafica_factory = ConcreteFactoryGrafica()
    client_code(grafica_factory)