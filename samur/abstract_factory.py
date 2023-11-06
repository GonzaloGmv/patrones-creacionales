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