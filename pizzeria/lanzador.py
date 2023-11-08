import patron_builder
import pandas as pd
import guardar_pedido

def main():
    director = patron_builder.Director()
    builder = patron_builder.ConcreteBuilder()
    director.builder = builder

    director.build_full_featured_product()
    pedido = guardar_pedido.Pedido(builder)

    pedido.guardar()
    pedido.mostrar()
    

if __name__ == "__main__":
    main()