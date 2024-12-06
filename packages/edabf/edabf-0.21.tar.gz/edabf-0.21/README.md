
# EDA BF - Exploratory Data Analysis Package

Este paquete permite realizar un análisis exploratorio de datos (EDA) sobre archivos (CSV, Parquet) y tablas de bases de datos SQL (MySQL, PostgreSQL, SQL Server, Oracle), generando informes en formato Excel para facilitar el análisis de calidad y características de los datos.

## Funcionalidades Principales

### 1. `process_single_file`
Procesa un archivo individual (CSV o Parquet) y genera un informe EDA en formato Excel.

- **Función**: `process_single_file(file_path, output=None, limite=None)`
- **Parámetros**:
  - `file_path` (str): Ruta del archivo a procesar.
  - `output` (str): Ruta de salida para el archivo Excel (opcional).
  - `limite` (int): Límite opcional de filas a leer.
- **Descripción**: Lee el archivo especificado, genera un análisis exploratorio de datos y lo guarda en un archivo Excel que contiene métricas y estadísticas de los datos.

### 2. `process_folder`
Procesa múltiples archivos en una carpeta (CSV y Parquet) y genera un informe EDA consolidado en un archivo Excel.

- **Función**: `process_folder(folder_path, output=None, limite=None)`
- **Parámetros**:
  - `folder_path` (str): Ruta de la carpeta que contiene los archivos a procesar.
  - `output` (str): Ruta de salida para el archivo Excel consolidado.
  - `limite` (int): Límite opcional de filas a leer por archivo.
- **Descripción**: Busca archivos CSV y Parquet en la carpeta especificada, procesa cada archivo, y genera un informe combinado en Excel con métricas detalladas de cada archivo.

### 3. `process_single_table`
Procesa una única tabla de una base de datos SQL y genera un informe EDA en formato Excel.

- **Función**: `process_single_table(db_type, server, user, password, database, schema, table_name, path_instaclient=None, output=None)`
- **Parámetros**:
  - `db_type` (str): Tipo de base de datos (`mysql`, `postgresql`, `sqlserver`, `oracle`).
  - `server`, `user`, `password`, `database`, `schema`, `table_name` (str): Información de conexión y tabla a procesar.
  - `path_instaclient` (str): Ruta opcional del cliente de Oracle, si es necesario.
  - `output` (str): Ruta de salida para el archivo Excel.
- **Descripción**: Se conecta a la base de datos, extrae la tabla especificada y genera un informe detallado en Excel, incluyendo estadísticas y datos de calidad de la tabla.

### 4. `process_dataset`
Procesa múltiples tablas de un esquema en una base de datos SQL y genera un informe EDA para cada tabla en un único archivo Excel.

- **Función**: `process_dataset(db_type, server, user, password, database, schema, path_instaclient=None, output=None, limit_tables=5)`
- **Parámetros**:
  - `db_type` (str): Tipo de base de datos (`mysql`, `postgresql`, `sqlserver`, `oracle`).
  - `server`, `user`, `password`, `database`, `schema` (str): Información de conexión a la base de datos.
  - `path_instaclient` (str): Ruta opcional del cliente de Oracle, si es necesario.
  - `output` (str): Ruta de salida para el archivo Excel.
  - `limit_tables` (int): Límite opcional para el número de tablas a procesar.
- **Descripción**: Conecta a la base de datos, extrae todas las tablas del esquema especificado, y genera un informe EDA en un solo archivo Excel. Cada tabla se incluye en una hoja diferente, con métricas y análisis de calidad.

### 5. `process_dataframe`
Procesa un DataFrame directamente en memoria y genera un informe EDA en formato Excel.

- **Función**: `process_dataframe(df, output=None, table_name="DataFrame", limite=None)`
- **Parámetros**:
  - `df` (DataFrame): El DataFrame que se desea procesar.
  - `output` (str): Ruta de salida para el archivo Excel.
  - `table_name` (str): Nombre que se asignará al DataFrame en el informe Excel (por defecto: `"DataFrame"`).
  - `limite` (int): Límite opcional de filas a procesar.
- **Descripción**: Procesa un DataFrame cargado en memoria, generando un informe en Excel con estadísticas descriptivas y métricas clave. Si se especifica un límite, solo se procesan las primeras `limite` filas.


## Ejemplos de Uso

### Procesar un Archivo Individual
```python
from edabf import process_single_file
process_single_file("ruta/al/archivo.csv", output="salida", limite=1000)
```

### Procesar una Carpeta de Archivos
```python
from edabf import process_folder
process_folder("ruta/a/carpeta", output="salida_masivo")
```

### Procesar una Tabla de una Base de Datos
```python
from edabf import process_single_table
process_single_table("postgresql", "servidor", "usuario", "contraseña", "base_datos", "esquema", "nombre_tabla", output="salida_table")
```

### Procesar Múltiples Tablas de un Esquema de Base de Datos
```python
from edabf import process_dataset
process_dataset("mysql", "servidor", "usuario", "contraseña", "base_datos", "esquema", output="salida_dataset")
```

### Procesar Múltiples Tablas de un Esquema de Base de Datos
```python
from edabf import process_dataframe
import pandas as pd

# Crear un DataFrame de ejemplo
data = {"Columna1": [1, 2, 3], "Columna2": ["A", "B", "C"]}
df = pd.DataFrame(data)

# Generar el informe EDA
process_dataframe(df, output="reporte_dataframe", table_name="Ejemplo", limite=10)
```
## Licencia
Este proyecto está bajo la licencia MIT.
