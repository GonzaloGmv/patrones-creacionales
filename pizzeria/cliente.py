import pandas as pd

class Cliente():
    def iniciar():
        input('Bienvenido a la pizzería. Presiona ENTER para continuar.')
        while True:
            nuevo = input('¿Eres un cliente nuevo? (S/N): ')
            if nuevo.lower() == 's':
                input('Para registrarte, presiona ENTER.')
                telefono = input('Teléfono: ')
                domicilio = input('Dirección: ')
                usuario = input('Usuario: ')
                contraseña = input('Contraseña: ')
                nuevo_cliente = pd.DataFrame({'Usuario': [usuario], 'Contraseña': [contraseña], 'Telefono': [telefono], 'Domicilio': [domicilio]})
                clientes_df = pd.read_csv('pizzeria/clientes.csv')
                clientes_df = pd.concat([clientes_df, nuevo_cliente], ignore_index=True)
                clientes_df.to_csv('pizzeria/clientes.csv', index=False)
                break
            elif nuevo.lower() == 'n':
                clientes_df = pd.read_csv('pizzeria/clientes.csv')
                input('Para iniciar sesión, presiona ENTER.')
                usuario = input('Usuario: ')
                contraseña = input('Contraseña: ')
                if usuario in clientes_df['Usuario'].values.tolist():
                    index = clientes_df.index[clientes_df['Usuario'] == usuario].tolist()[0]
                    stored_password = clientes_df.at[index, 'Contraseña']
                    if contraseña == stored_password:
                        print('Inicio de sesión exitoso. ¡Bienvenido de nuevo!')
                        break
                    else:
                        print('La contraseña no coincide. Intenta de nuevo.')
                else:
                    print('El usuario no existe. Intenta de nuevo.')
            else:
                print('Opción no válida. Intenta de nuevo.')
