import patron_builder
import guardar_pedido
import cliente

def main():
    mi_cliente = cliente.Cliente()
    mi_cliente.iniciar()


    # Crea el director y el builder
    director = patron_builder.Director()
    builder = patron_builder.ConcreteBuilder()
    director.builder = builder
    
    # Construye una pizza con todos los atributos
    director.build_full_featured_product(mi_cliente, guardar_pedido.Pedido(builder))

    # Guarda el pedido y lo muestra
    pedido = guardar_pedido.Pedido(builder)
    pedido.guardar()
    pedido.mostrar()

    mi_cliente.pedido_cliente(pedido)
    

if __name__ == "__main__":
    main()