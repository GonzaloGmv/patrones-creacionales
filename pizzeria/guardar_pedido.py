import patron_builder
import pandas as pd

class Pedido():
    def __init__(self, builder):
        self.pizza_pedido = builder.pizza
    
    # Crea un diccionario con las partes de la pizza
    def diccionario(self):
        pedido_dict = {'Masa': [part for part in self.pizza_pedido.parts if 'Masa' in part],
                    'Salsa': [part for part in self.pizza_pedido.parts if 'Salsa' in part],
                    'Ingredientes': [part for part in self.pizza_pedido.parts if 'Ingredientes' in part],
                    'Cocción': [part for part in self.pizza_pedido.parts if 'Poco Hecha' in part or 'En su Punto' in part or 'Muy Hecha' in part],
                    'Presentación': [part for part in self.pizza_pedido.parts if 'En Plato' in part or 'En Caja' in part or 'Para Llevar' in part],
                    'Maridaje': [part for part in self.pizza_pedido.parts if 'Vino Tinto' in part or 'Cerveza' in part or 'Agua' in part or 'Refresco' in part or 'Sin bebida' in part],
                    'Borde': [part for part in self.pizza_pedido.parts if 'Borde de Queso' in part or 'Borde Relleno de Jamón y Queso' in part or 'Borde de Ajo y Mantequilla' in part or 'Borde Clásico' in part],
                    'Extras Gourmet': [part for part in self.pizza_pedido.parts if 'Extra' in part]}
        for key in pedido_dict:
            pedido_dict[key] = ' '.join(pedido_dict[key])
        pedido_dict['Ingredientes'] = pedido_dict['Ingredientes'][13:]
        pedido_dict['Extras Gourmet'] = pedido_dict['Extras Gourmet'][7:]

        return pedido_dict

    # Guarda el pedido en un archivo csv a partir del diccionario
    def guardar(self):
        pedido_dict = self.diccionario()
        pedidos_df = pd.read_csv('pizzeria/pedidos.csv')

        pedidos_df = pd.concat([pedidos_df, pd.DataFrame([pedido_dict])], ignore_index=True)
        pedidos_df.to_csv('pizzeria/pedidos.csv', index=False)
    
    # Muestra el pedido en la terminal
    def mostrar(self):
        print("Esta es tu pizza: ")
        pedido_dict = self.diccionario()
        for key, value in pedido_dict.items():
            print(f'{key}: {value}')