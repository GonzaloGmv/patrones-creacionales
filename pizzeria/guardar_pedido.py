import pandas as pd

# Clase Pedido
class Pedido():
    def __init__(self, builder):
        # Inicializa la pizza
        self.pizza_pedido = builder.pizza
    
    # Funcion que genera el numero de pedido
    def numero_pedido(self):
        try:
            pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
            if not pedidos_df.empty:
                ultimo_id = pedidos_df['numero'].max()
                nuevo_id = ultimo_id + 1
            else:
                nuevo_id = 1
        except FileNotFoundError:
            nuevo_id = 1

        return nuevo_id
    
    # Funcion que crea un diccionario con las partes de la pizza
    def diccionario(self):
        pedido_dict = {'Masa': [part for part in self.pizza_pedido.parts if 'Masa' in part],
                    'Salsa': [part for part in self.pizza_pedido.parts if 'Salsa' in part],
                    'Ingredientes': [part for part in self.pizza_pedido.parts if 'Ingredientes' in part],
                    'Cocción': [part for part in self.pizza_pedido.parts if 'Poco Hecha' in part or 'En su Punto' in part or 'Muy Hecha' in part],
                    'Presentación': [part for part in self.pizza_pedido.parts if 'En Plato' in part or 'En Caja' in part or 'Para Llevar' in part],
                    'Maridaje': [part for part in self.pizza_pedido.parts if 'Vino Tinto' in part or 'Cerveza' in part or 'Agua' in part or 'Refresco' in part or 'Sin bebida' in part],
                    'Borde': [part for part in self.pizza_pedido.parts if 'Borde de Queso' in part or 'Borde Relleno de Jamón y Queso' in part or 'Borde de Ajo y Mantequilla' in part or 'Borde Clásico' in part],
                    'Extras Gourmet': [part for part in self.pizza_pedido.parts if 'Extra' in part]}
        # Cada valor del diccionario es una lista, por lo que se convierte a string
        for key in pedido_dict:
            pedido_dict[key] = ' '.join(pedido_dict[key])
        # Elimina las palabras Ingredientes y Extras Gourmet del valor del diccionario
        pedido_dict['Ingredientes'] = pedido_dict['Ingredientes'][13:]
        pedido_dict['Extras Gourmet'] = pedido_dict['Extras Gourmet'][7:]
        return pedido_dict

    # Funcion que guarda el pedido en un archivo csv a partir del diccionario
    def guardar(self):
        # Llama a la funcion diccionario para obtener el diccionario
        pedido_dict = self.diccionario()
        try:
            pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
        except FileNotFoundError:
            pedidos_df = pd.DataFrame(columns=pedido_dict.keys())

        # Crea una nueva clave-valor en el diccionario con el numero de pedido. Para ello llama a la funcion numero_pedido
        pedido_dict['numero'] = self.numero_pedido()

        # Concatea el diccionario con el DataFrame de pedidos y lo guarda en el archivo CSV
        pedidos_df = pd.concat([pedidos_df, pd.DataFrame([pedido_dict])], ignore_index=True)
        pedidos_df['numero'] = pedidos_df['numero'].astype(int)
        pedidos_df.to_csv('pizzeria/pedidos.csv', index=False)
    
    # Funcion que accede a unos pedidos dada una lista de id y devuelve una lista con los ingredientes
    def ingredientes_anteriores(self, lista_id):
        pedidos_df = pd.read_csv('pizzeria/pedidos.csv')
        if lista_id == 0:
            return []
        else:
            ingredientes = []
            for num in lista_id:
                num = int(float(num))
                # Accede a la fila del DataFrame que corresponde al numero de pedido y obtiene los ingredientes de esa fila
                ingredientes_num = pedidos_df[pedidos_df['numero'] == num]['Ingredientes'].iloc[0]
                # Separa los ingredientes por /
                ingredientes.extend(ingredientes_num.split('/'))
            return ingredientes
    
    # Muestra el pedido en la terminal
    def mostrar(self):
        print("Esta es tu pizza: ")
        pedido_dict = self.diccionario()
        for key, value in pedido_dict.items():
            print(f'{key}: {value}')