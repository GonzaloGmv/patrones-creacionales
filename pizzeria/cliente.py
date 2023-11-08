import pandas as pd
import guardar_pedido

class Cliente():
    def __init__(self):
        self.usuario = ''
        self.contraseña = ''
        self.telefono = ''
        self.domicilio = ''
        self.pedidos = []
        self.clientes_df = pd.read_csv('pizzeria/clientes.csv')

    def iniciar(self):
        while True:
            nuevo = input('¿Eres un cliente nuevo? (S/N): ')
            if nuevo.lower() == 's':
                self.telefono = input('Teléfono: ')
                self.domicilio = input('Dirección: ')
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                nuevo_cliente = pd.DataFrame({'Usuario': [self.usuario], 'Contraseña': [self.contraseña], 'Telefono': [self.telefono], 'Domicilio': [self.domicilio]})
                self.clientes_df = pd.concat([self.clientes_df, nuevo_cliente], ignore_index=True)
                self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
                break
            elif nuevo.lower() == 'n':
                self.usuario = input('Usuario: ')
                self.contraseña = input('Contraseña: ')
                if self.usuario in self.clientes_df['Usuario'].values.tolist():
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
    
    def numero_pedido(self, pedido):
        n_pedido = pedido.numero_pedido() -1
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        if pd.notna(pedidos_anteriores):
            nuevos_pedidos = f"{pedidos_anteriores}/{n_pedido}"
        else:
            nuevos_pedidos = n_pedido

        # Actualiza la columna 'Pedidos' con los nuevos pedidos
        self.clientes_df.at[user_index, 'Pedidos'] = nuevos_pedidos

        # Guarda el DataFrame actualizado en el archivo CSV
        self.clientes_df.to_csv('pizzeria/clientes.csv', index=False)
    
    def acceder_pedidos(self):
        user_index = self.clientes_df[self.clientes_df['Usuario'] == self.usuario].index[0]
        pedidos_anteriores = self.clientes_df.at[user_index, 'Pedidos']
        if pedidos_anteriores != 0:
            return pedidos_anteriores
        else:
            return 0