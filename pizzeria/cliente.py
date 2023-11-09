import pandas as pd
import numpy as np

# Clase Cliente
class Cliente():
    def __init__(self):
        # Inicializa las variables vacias que luego se llenaran
        self.usuario = ''
        self.contraseña = ''
        self.telefono = ''
        self.domicilio = ''
        self.pedidos = []
        # Lee el archivo CSV clientes.csv y lo guarda en una variable
        self.clientes_df = pd.read_csv('pizzeria/clientes.csv')

    # Funcion para iniciar sesion o crear un nuevo usuario
    def iniciar(self):
        # Bucle para iniciar sesion o crear un nuevo usuario
        while True:
            nuevo = input('¿Eres un cliente nuevo? (S/N): ')
            if nuevo.lower() == 's':
                # Si es un nuevo cliente, lo registra
                self.telefono = input('Teléfono: ')
                self.domicilio = input('Dirección: ')
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                # Crea un DataFrame con los datos del nuevo cliente
                nuevo_cliente = pd.DataFrame({'Usuario': [self.usuario], 'Contraseña': [self.contraseña], 'Telefono': [self.telefono], 'Domicilio': [self.domicilio]})
                # Concatena el nuevo DataFrame con el DataFrame de clientes
                self.clientes_df = pd.concat([self.clientes_df, nuevo_cliente], ignore_index=True)
                # Guarda el DataFrame actualizado en el archivo CSV
                self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
                break
            elif nuevo.lower() == 'n':
                # Si no es un nuevo cliente, inicia sesion
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                # Verifica si el usuario existe
                if self.usuario in self.clientes_df['Usuario'].values.tolist():
                    # Verifica si la contraseña coincide
                    index = self.clientes_df.index[self.clientes_df['Usuario'] == self.usuario].tolist()[0]
                    stored_password = self.clientes_df.at[index, 'Contraseña']
                    if self.contraseña == stored_password:
                        print('Inicio de sesión exitoso. ¡Bienvenido de nuevo!')
                        break
                    else:
                        print('La contraseña no coincide. Intenta de nuevo.')
                else:
                    print('El usuario no existe. Intenta de nuevo.')
            else:
                print('Opción no válida. Intenta de nuevo.')
    
    # Funcion que obtiene el numero de pedido y lo guarda en el archivo CSV
    def pedido_cliente(self, pedido):
        # Obtiene el numero de pedido del pedido recientemente guardado
        n_pedido = pedido.numero_pedido() -1
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        # Verifica si el cliente tiene pedidos anteriores
        if pd.notna(pedidos_anteriores):
            nuevos_pedidos = f"{pedidos_anteriores}/{n_pedido}"
        else:
            nuevos_pedidos = n_pedido

        # Actualiza la columna 'Pedidos' con los nuevos pedidos
        self.clientes_df.at[user_index, 'Pedidos'] = nuevos_pedidos

        # Guarda el DataFrame actualizado en el archivo CSV
        self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
    
    # Funcion que obtiene los pedidos anteriores del cliente y devuelve los ingredientes de estos pedidos
    def acceder_pedidos(self, pedido):
        # Obtiene los pedidos anteriores del cliente
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        # Verifica si el cliente tiene pedidos anteriores
        if pd.isna(pedidos_anteriores):
            numero_ped = 0
        else:
            # Verificar si hay solo un pedido
            if isinstance(pedidos_anteriores, (int, np.int64)):
                numero_ped = [pedidos_anteriores]
            else:
                # Si hay mas de un pedido, los separa
                numero_ped = str(pedidos_anteriores).split('/')
        # Llama a la funcion ingredientes_anteriores de la clase Pedido que le devuelve los ingredientes
        ingredientes = pedido.ingredientes_anteriores(numero_ped)
        return ingredientes