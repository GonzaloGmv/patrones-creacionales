import patron_builder
import guardar_pedido

def main():
    # Crea el director y el builder
    director = patron_builder.Director()
    builder = patron_builder.ConcreteBuilder()
    director.builder = builder

    # Construye una pizza con todos los atributos
    director.build_full_featured_product()

    # Guarda el pedido y lo muestra
    pedido = guardar_pedido.Pedido(builder)
    pedido.guardar()
    pedido.mostrar()
    

if __name__ == "__main__":
    main()