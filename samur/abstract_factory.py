import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class AbstractFactory(ABC):
    @abstractmethod
    def create_analisis(self):
        pass

    @abstractmethod
    def create_grafica(self):
        pass

# Concrete Factory para Mes
class ConcreteFactoryMes(AbstractFactory):
    def create_analisis(self):
        return ConcreteProductAnalisisMes()

    def create_grafica(self):
        return ConcreteProductGraficaMes()

# Concrete Factory para Distrito
class ConcreteFactoryDistrito(AbstractFactory):
    def create_analisis(self):
        return ConcreteProductAnalisisDistrito()

    def create_grafica(self):
        return ConcreteProductGraficaDistrito()

# Abstract Product para análisis estadístico
class AbstractProductAnalisis(ABC):
    @abstractmethod
    def calcular_media(self):
        pass

    @abstractmethod
    def calcular_moda(self):
        pass

# Concrete Product para análisis estadísticos de mes
class ConcreteProductAnalisisMes(AbstractProductAnalisis):
    def calcular_media(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        return media
    
    def calcular_moda(self, data):
        moda = data.groupby('Mes')['Tiempo(minutos)'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        return moda

# Concrete Product para análisis estadísticos de distrito
class ConcreteProductAnalisisDistrito(AbstractProductAnalisis):
    def calcular_media(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        return media
    
    def calcular_moda(self, data):
        moda = data.groupby('Distrito')['Tiempo(minutos)'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        return moda

# Abstract Product para visualización gráfica
class AbstractProductGrafica(ABC):
    @abstractmethod
    def calcular_histograma(self):
        pass

    @abstractmethod
    def calcular_lineas(self):
        pass

# Concrete Product para visualización gráfica de mes
class ConcreteProductGraficaMes(AbstractProductGrafica):
    def calcular_histograma(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/HistogramaMes.png')
        plt.close()
    
    def calcular_lineas(self, data):
        media = data.groupby('Mes')['Tiempo(minutos)'].mean()
        media.plot(kind='line')
        plt.title('Media de Tiempo(minutos) por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/LineasMes.png')
        plt.close()

# Concrete Product para visualización gráfica de distrito
class ConcreteProductGraficaDistrito(AbstractProductGrafica):
    def calcular_histograma(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        media.plot(kind='bar')
        plt.title('Media de Tiempo(minutos) por Distrito')
        plt.xlabel('Distrito')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/HistogramaDistrito.png')
        plt.close()
    
    def calcular_lineas(self, data):
        media = data.groupby('Distrito')['Tiempo(minutos)'].mean()
        media.plot(kind='line')
        plt.title('Media de Tiempo(minutos) por Distrito')
        plt.xlabel('Distrito')
        plt.ylabel('Tiempo(minutos)')
        plt.savefig('samur/graficas/LineasDistrito.png')
        plt.close()

def client_code(factory: AbstractFactory):
    # Carga el csv
    data = pd.read_csv('samur/data.csv')

    # Crea los productos para análisis y visualización
    productAnalisis = factory.create_analisis()
    productGrafica = factory.create_grafica()
    
    # Condicionales para utilizar la fabrica correspondiente en cada caso
    if isinstance(factory, ConcreteFactoryMes):
        # Realiza el análisis estadístico de mes
        media_mes = productAnalisis.calcular_media(data)
        moda_mes = productAnalisis.calcular_moda(data)
        print(f"Análisis de Mes - Media:")
        print(media_mes)
        print(f"Análisis de Mes - Moda:")
        print(moda_mes)

        # Realiza la visualización gráfica de mes
        print(f"Visualización de Mes - Histograma creado")
        productGrafica.calcular_histograma(data)
        print(f"Visualización de Mes - Gráfico de Lineas creado")
        productGrafica.calcular_lineas(data)
        
    
    elif isinstance(factory, ConcreteFactoryDistrito):
        # Realiza el análisis estadístico de distrito
        media_distrito = productAnalisis.calcular_media(data)
        moda_distrito = productAnalisis.calcular_moda(data)
        print(f"Análisis de Distrito - Media:")
        print(media_distrito)
        print(f"Análisis de Distrito - Moda:")
        print(moda_distrito)

        # Realiza la visualización gráfica de distrito 
        print(f"Visualización de Distrito - Histograma creado")
        productGrafica.calcular_histograma(data)
        print(f"Visualización de Distrito - Gráfico de Lineas creado")
        productGrafica.calcular_lineas(data)

if __name__ == "__main__":
    # Crea una fabrica de análisis y visualización de mes
    mes_factory = ConcreteFactoryMes()
    client_code(mes_factory)

    # Crea una fabrica de análisis y visualización de distrito
    distrito_factory = ConcreteFactoryDistrito()
    client_code(distrito_factory)