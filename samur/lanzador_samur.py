import samur.abstract_factory as abstract_factory

def main_lanzador():
    # Crea la fabrica de análisis estadístico
    analisis_factory = abstract_factory.ConcreteFactoryAnálisis()
    abstract_factory.client_code(analisis_factory)

    # Crea una fabrica de visualización gráfica
    grafica_factory = abstract_factory.ConcreteFactoryGrafica()
    abstract_factory.client_code(grafica_factory)