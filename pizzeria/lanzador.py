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
    director.build_full_featured_product()

    # Guarda el pedido y lo muestra
    pedido = guardar_pedido.Pedido(builder)
    pedido.guardar()
    pedido.mostrar()

    mi_cliente.numero_pedido(pedido)
    print(mi_cliente.acceder_pedidos())
    

if __name__ == "__main__":
    main()