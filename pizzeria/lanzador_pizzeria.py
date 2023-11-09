import pizzeria.patron_builder as patron_builder
import pizzeria.guardar_pedido as guardar_pedido
import pizzeria.cliente as cliente

def main_pizzeria():
    # Crea un cliente
    mi_cliente = cliente.Cliente()
    # Llama a la funcion iniciar e inicia sesion
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
    # Guarda el numero de pedido en el archivo CSV clientes.csv
    mi_cliente.pedido_cliente(pedido)