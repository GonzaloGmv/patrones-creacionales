# patrones-creacionales

El link a este repositorio es [github](https://github.com/GonzaloGmv/patrones-creacionales)

### Ejercicio 1: Análisis Modular de las Activaciones del SAMUR-Protección Civil en Madrid con Abstract Factory

Este ejercicio pedía desarrollar un programa en Python que hiciera uso del patrón de diseño "Abstract Factory" para modularizar y estandarizar el análisis de unos datos del samur.

Para esto, lo primero era leer estos datos y modelizarlos. 

Lo que hice para limpiar estos datos es lo siguiente:
- Eliminar la columna 'Año': Al ser todos los datos de 2023, esta columna estaba repetida y no aportaba nada
- Sustituir por 0 los valores nulos de la columna 'Hospital': Si esta columna esta vacía significa que el paciente no ha sido hospitalizado.
- Eliminar las filas con valores nulos
- Crea una nueva columna 'Tiempo(minutos)' para ver la diferencia entre las columnas "Hora Solicitud" y "Hora Intervención"
- Corregir las diferencias a través de la medianoche sumando un día cuando es necesario
- Eliminar las filas con 0.0 en la columna Tiempo(minutos)
- Eliminar las filas cuyo Tiempo(minutos) sea mayor que 60: al ser un servicio de emergencia no debería superar esa cifra, por lo que se considera un error.

El código es el siguiente:
```
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

# Añade la columna Tiempo(minutos) con el tiempo de espera en minutos
data['Tiempo(minutos)'] = data['Tiempo Espera'].dt.seconds / 60

# Elimina las filas con 0.0 en la columna Tiempo(minutos)
data = data[data['Tiempo(minutos)'] != 0.0]

# Elimina las filas cuyo Tiempo(minutos) sea mayor que 60, ya que al ser un servicio de emergencia no debería superar esa cifra, por lo que se considera un error
data = data[data['Tiempo(minutos)'] < 60]

# Guarda el DataFrame en un archivo csv
data.to_csv('samur/data.csv', index=False)
```
