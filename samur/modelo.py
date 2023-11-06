import pandas as pd
import numpy as np

# Carga el csv de la URL y lo guarda en un objeto de tipo DataFrame
URL = "https://datos.madrid.es/egob/catalogo/300178-12-samur-activaciones.csv"
data = pd.read_csv(URL, sep=';', encoding='UTF-8')

# Elimina la columna Año ya que es siempre el mismo
data = data.drop(columns=['Año'])

# Los valores nulos de la columna "Hospital" se sustituyen por 0
data['Hospital'] = data['Hospital'].fillna(0)

# Elimina las filas con valores nulos
data = data.dropna()

# Convierte las columnas "Hora Solicitud" y "Hora Intervención" a objetos de tipo datetime
data['Hora Solicitud'] = pd.to_datetime(data['Hora Solicitud'], format='%H:%M:%S')
data['Hora Intervención'] = pd.to_datetime(data['Hora Intervención'], format='%H:%M:%S')

# Calcula la diferencia entre las columnas y crea una nueva columna "Tiempo Espera"
data['Tiempo Espera'] = data['Hora Intervención'] - data['Hora Solicitud']

# Corrige las diferencias a través de la medianoche sumando un día cuando es necesario
data['Tiempo Espera'] = np.where(data['Hora Intervención'] < data['Hora Solicitud'], data['Tiempo Espera'] + pd.Timedelta(days=1), data['Tiempo Espera'])

# Elimina las columnas "Hora Solicitud" y "Hora Intervención" ya que no son necesarias
data = data.drop(columns=['Hora Solicitud'])
data = data.drop(columns=['Hora Intervención'])

# Guarda el DataFrame en un archivo csv
data.to_csv('samur/data.csv', index=False)