import os
import pandas as pd
import polars as pl
from tqdm import tqdm
from datetime import datetime
import pyarrow.parquet as pq
import pyarrow.csv as pc
import pyarrow as pa
import pyarrow.dataset as ds

def combine_dicts(dict1, dict2):
    # Inicializamos el diccionario resultante
    combined_dict = {}

    # Iteramos sobre las claves de ambos diccionarios (sin duplicados)
    for key in dict1.keys() | dict2.keys():
        # Fusionamos los valores correspondientes
        combined_dict[key] = {**dict1.get(key, {}), **dict2.get(key, {})}

    return combined_dict


def get_top_frequencies(df):
    def get_top_frequency(column):
        value_counts = column.value_counts()
        if not value_counts.empty:
            return value_counts.iloc[0]
        else:
            return 0

    top_frequencies = df.apply(get_top_frequency)
    result_series = pd.Series(top_frequencies)
    return result_series

def concatenate_row_with_keys(row):
        result = []
        for index, value in row.items():
            # Si el valor es una lista o un string, lo dejamos en su forma original
            if isinstance(value, list):
                result.append(f"{value}")
            else:
                result.append(f"{str(value)}")
        return "[" + " ".join(result) + "]"    

# Función para calcular el porcentaje de True, False y Otros
def calcular_porcentaje_true_false_otros(df):
    # Crear una lista para almacenar los porcentajes
    porcentajes = []

    for col in df.columns:
        try:
            # Convertir la columna a string, luego a minúsculas
            boolean_col = df.select(
                pl.col(col).cast(pl.Utf8).str.to_lowercase().alias(col)
            )

            # Contar True y False mapeando los valores
            true_count = boolean_col.select(
                pl.col(col).filter(pl.col(col) == "true").count()
            )[0, 0]
            
            false_count = boolean_col.select(
                pl.col(col).filter(pl.col(col) == "false").count()
            )[0, 0]

            # Calcular el total de la columna
            total_count = df.select(pl.col(col).count())[0, 0]

            # Calcular los valores "Otros" (ni True ni False)
            otros_count = total_count - true_count - false_count

            # Si no hay valores True o False, asignamos 0 al porcentaje de Otros
            if true_count + false_count == 0:
                otros_count = 0

            # Calcular los porcentajes de True, False y Otros
            porcentajes.append({
                "Col": col,
                "True%": (true_count / total_count) * 100 if total_count > 0 else 0,
                "False%": (false_count / total_count) * 100 if total_count > 0 else 0,
                "Others%": (otros_count / total_count) * 100 if total_count > 0 else 0
            })

        except Exception as e:
            # Si hay un error, asignamos NaN
            porcentajes.append({
                "Col": col,
                "True%": None,
                "False%": None,
                "Others%": None
            })
            print(f"Error en la columna {col}: {e}")

    # Convertir la lista de diccionarios en un DataFrame de Polars
    porcentajes_df = pl.DataFrame(porcentajes)

    return porcentajes_df


# Crear una función para reordenar columnas en base a las columnas comunes
def reorder_columns_by_common(df_list):
    # Obtener las columnas comunes entre todos los DataFrames y capitalizar
    common_columns = sorted([word.capitalize() for word in list(set.intersection(*[set(df.columns) for df in df_list]))])
    
    # Definir una función para reordenar las columnas del DataFrame con prioridad en tipo de datos
    def reorder_columns(df, common_columns):
        # Capitalizar todas las columnas del DataFrame
        df.columns = [word.capitalize() for word in df.columns]
        
        # Filtrar y clasificar las columnas comunes por su tipo de dato (string, int, otros)
        common_str_columns = [col for col in common_columns if pd.api.types.is_string_dtype(df[col])]
        common_int_columns = [col for col in common_columns if pd.api.types.is_integer_dtype(df[col])]
        common_other_columns = [col for col in common_columns if col not in common_str_columns + common_int_columns]
        
        # Combinar los tres tipos de columnas
        new_common_order = common_str_columns + common_int_columns + common_other_columns
        
        # Crear el nuevo orden combinando las comunes primero, luego el resto
        new_order = new_common_order + sorted([col for col in df.columns if col not in common_columns])
        return df[new_order]
    
    # Reordenar cada DataFrame en la lista
    reordered_dfs = [reorder_columns(df, common_columns) for df in df_list]
    
    return reordered_dfs


def save_dataframe_to_csv(dataframe, filename):
    """
    Guarda un DataFrame en un archivo CSV.
    
    Args:
    - dataframe: El DataFrame a guardar.
    - filename: El nombre del archivo CSV (incluyendo la extensión .csv).
    """
    try:
        dataframe.to_csv(filename, index=False)  # Guarda sin el índice en el CSV
        print(f"Archivo guardado correctamente: {filename}")
    except Exception as e:
        print(f"Error al guardar el archivo {filename}: {e}")



def is_date(string):
    """
    Verifica si una cadena se puede interpretar como una fecha válida.
    """
    date_formats = [
        "%Y-%m-%d",                  # Año-Mes-Día
        "%d/%m/%Y",                  # Día/Mes/Año
        "%Y-%m-%d %H:%M:%S",         # Año-Mes-Día Hora:Minuto:Segundo
        "%m/%d/%Y",                  # Mes/Día/Año
        "%Y-%m-%d %H:%M:%S.%f",      # Año-Mes-Día Hora:Minuto:Segundo.Milisegundos
        "%Y-%m-%d %H:%M",            # Año-Mes-Día Hora:Minuto
        "%d/%m/%Y %H:%M:%S",         # Día/Mes/Año Hora:Minuto:Segundo
        "%Y/%m/%d %H:%M:%S",         # Año/Mes/Día Hora:Minuto:Segundo
    ]
    for fmt in date_formats:
        try:
            datetime.strptime(string, fmt)
            return True
        except ValueError:
            pass
    return False

def is_numeric(string):
    """
    Verifica si una cadena se puede interpretar como un valor numérico.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def validate_examples_data_type(examples):
    """
    Valida si los ejemplos de una columna corresponden a un tipo de dato específico.
    """
    example_list = examples.split(", ")
    
    if all(is_date(ex) for ex in example_list):
        return "date"
    elif all(is_numeric(ex) for ex in example_list):
        return "numeric"
    else:
        return "string"

def map_data_type(data_type, examples=None):
    """
    Mapea el tipo de dato de la columna a las categorías generales. 
    También valida el tipo de los ejemplos, si están disponibles.
    """
    str_types = ["nvarchar", "varchar", "text", "string", "char", "str", "object", "object_", "varchar2"]
    numeric_types = ["int", "float", "decimal", "double", "numeric", "number", "float64", "int64"]
    date_types = ["datetime", "date", "timestamp", "datetime64", "timedelta", "datetime64[ns]", "datetime(time_unit='ns', time_zone=none)", "Datetime(time_unit='ns', time_zone='UTC')"]

    data_type_str = str(data_type).lower()

    if examples:  # Si se proveen ejemplos, validamos su tipo de dato
        example_type = validate_examples_data_type(examples)
        if example_type != "string":  # Si el tipo de los ejemplos no es string, sobreescribimos el tipo de dato
            return example_type

    if data_type_str in str_types:
        return "string"
    elif data_type_str in numeric_types:
        return "numeric"
    elif data_type_str in date_types:
        return "date"
    else:
        try:
            if example_type:
                return example_type
            else:
                return "other"
        except:
            "other"

# Función para filtrar los datos por tipo de dato y convertirlos a DataFrame
def create_dataframe_by_type(data_dict, general_type):
    """
    Crea un DataFrame filtrando las columnas según el tipo de dato y validando los ejemplos.
    """
    # Filtra las columnas según el tipo de dato mapeado a categorías generales
    filtered_data = [
        {**data_dict["Columns"][i]["EDA_Statistics"], "col": i, "datatype": data_dict["Columns"][i]["DataType"]}
        for i in data_dict["Columns"]
        if map_data_type(data_dict["Columns"][i]["DataType"], data_dict["Columns"][i]["EDA_Statistics"].get('Examples', None)) == general_type
    ]
    # Convierte a DataFrame y lo devuelve
    return pd.DataFrame(filtered_data)



def convert_column_types(df):
    transformations = []
    
    for col in df.columns:
        # Obtener algunos valores de ejemplo para validar el tipo de dato
        examples = ', '.join([str(x) for x in df[col].drop_nulls().head(100).to_list()])
        inferred_type = map_data_type(df[col].dtype, examples)

        # Crear la transformación adecuada para cada tipo
        if inferred_type == "numeric":
            transformations.append(pl.col(col).cast(pl.Float64, strict=False))  # convierte a numérico
        elif inferred_type == "date":
            # Convertir primero a cadena para evitar errores de incompatibilidad y luego a datetime
            transformations.append(pl.col(col).cast(pl.Utf8).str.strptime(pl.Datetime, strict=False))
        elif inferred_type == "string":
            transformations.append(pl.col(col).cast(pl.Utf8, strict=False))  # asegura que sea texto

    # Aplicar todas las transformaciones a la vez con with_columns
    df = df.with_columns(transformations)
    return df

# Leer el archivo CSV en fragmentos
def process_chunks_optimized_polars2(csv_file_path, formato, limite=None):
    """
    Optimización de la lectura de CSV en fragmentos grandes directamente con Polars,
    permitiendo establecer un límite en el número de filas leídas.
    
    Parameters:
    - csv_file_path (str): Ruta del archivo CSV o Parquet.
    - formato (str): Formato del archivo ('csv' o 'parquet').
    - limite (int): Número máximo de filas a leer.
    """

    # Crear una lista para almacenar los DataFrames procesados
    all_chunks = []
    if formato == 'csv':
    # Leer el archivo CSV en fragmentos usando solo Polars
        file_reader = pl.scan_csv(csv_file_path, ignore_errors=True)  # Utiliza lectura en modo perezoso (scan_csv)
    elif formato == 'parquet':
        file_reader = pl.scan_parquet(csv_file_path)
    else:
        raise ValueError("Formato no soportado. Usa 'csv' o 'parquet'.")
        
    # Aplicar límite si se especifica
    if limite:
        file_reader = file_reader.limit(limite)
    # Convertir el CSV escaneado en fragmentos más pequeños para procesar
    result_df = file_reader.collect(streaming=True)  # Procesa en modo streaming si es compatible
    
    
    return result_df


# Leer el archivo CSV en fragmentos
def process_chunks_optimized_polars(csv_file_path, formato, limite=None):
    """
    Optimización de la lectura de CSV en fragmentos grandes directamente con Polars,
    permitiendo establecer un límite en el número de filas leídas.
    
    Parameters:
    - csv_file_path (str): Ruta del archivo CSV o Parquet.
    - formato (str): Formato del archivo ('csv' o 'parquet').
    - limite (int): Número máximo de filas a leer.
    """

    # Crear una lista para almacenar los DataFrames procesados
    all_chunks = []
    if formato == 'csv':
        # Leer el archivo CSV en fragmentos usando solo Polars
        file_reader = pl.scan_csv(csv_file_path, ignore_errors=True)  # Utiliza lectura en modo perezoso (scan_csv)
    elif formato == 'parquet':
        file_reader = pl.scan_parquet(csv_file_path)
    else:
        raise ValueError("Formato no soportado. Usa 'csv' o 'parquet'.")
        
    # Aplicar límite si se especifica
    if limite:
        file_reader = file_reader.limit(limite)
        
    # Convertir el CSV escaneado en fragmentos más pequeños para procesar
    # Procesa en modo streaming si es compatible y muestra progreso con tqdm
    with tqdm(total=limite or file_reader.collect().shape[0], desc="Procesando Fragmentos") as pbar:
        result_df = file_reader.collect(streaming=True)
        pbar.update(result_df.shape[0])
    
    return result_df


def process_chunks_optimized_polars(file_path, formato, limite=None, chunk_size=100000):
    """
    Optimización de la lectura de CSV o Parquet en fragmentos grandes directamente con Polars y PyArrow,
    permitiendo establecer un límite en el número de filas leídas.

    Parameters:
    - file_path (str): Ruta del archivo CSV o Parquet.
    - formato (str): Formato del archivo ('csv' o 'parquet').
    - limite (int): Número máximo de filas a leer.
    - chunk_size (int): Tamaño de los fragmentos en número de filas.

    Returns:
    - Polars DataFrame procesado.
    """
    if formato not in ["csv", "parquet"]:
        raise ValueError("Formato no soportado. Usa 'csv' o 'parquet'.")

    # Manejar CSV con Polars
    if formato == "csv":
        # Crear un LazyFrame para lectura perezosa
        if limite is not None:
            file_reader = pl.read_csv(file_path, ignore_errors=True, n_rows=limite)
        else:
            file_reader = pl.read_csv(file_path, ignore_errors=True)
        total_rows = file_reader.shape[0]

        # Mostrar progreso con tqdm
        with tqdm(total=total_rows, desc="Procesando Fragmentos") as pbar:
            # No es necesario iterar, ya que hemos leído el número de filas especificado
            pbar.update(total_rows)
            result_df = file_reader

    # Manejar Parquet con PyArrow
    elif formato == "parquet":
        parquet_file = pq.ParquetFile(file_path)
        total_rows_in_file = parquet_file.metadata.num_rows
        total_rows = min(limite, total_rows_in_file) if limite is not None else total_rows_in_file
        collected_chunks = []
        rows_read = 0

        with tqdm(total=total_rows, desc="Procesando Fragmentos") as pbar:
            for batch in parquet_file.iter_batches(batch_size=chunk_size):
                batch_num_rows = batch.num_rows
                remaining_rows = total_rows - rows_read

                if batch_num_rows > remaining_rows:
                    # Ajustar el batch para no exceder el límite
                    batch = batch.slice(0, remaining_rows)
                    batch_num_rows = remaining_rows

                df_chunk = pl.from_arrow(batch)
                collected_chunks.append(df_chunk)

                rows_read += batch_num_rows
                pbar.update(batch_num_rows)

                if rows_read >= total_rows:
                    break

        # Combinar todos los fragmentos en un único DataFrame de Polars
        result_df = pl.concat(collected_chunks)

    return result_df




def categorize_dataframes_by_type(df, table_info_gpt):
    """
    Clasifica el DataFrame en tipos de datos (string, numeric, date, other).

    Args:
        table_info_gpt (dict): Diccionario con información EDA.

    Returns:
        list: Lista de DataFrames categorizados.
    """
    table_info_gpt_str_df = create_dataframe_by_type(table_info_gpt, "string")
    table_info_gpt_int_df = create_dataframe_by_type(table_info_gpt, "numeric")
    table_info_gpt_date_df = create_dataframe_by_type(table_info_gpt, "date")
    table_info_gpt_other_df = create_dataframe_by_type(table_info_gpt, "other")

    # Reordenar columnas
    df_list = reorder_columns_by_common([table_info_gpt_str_df, table_info_gpt_int_df, table_info_gpt_date_df, table_info_gpt_other_df])
    
    # Establecer el orden específico de columnas para cada tipo de DataFrame
    column_orders = {
        "numeric": [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                'Notnulls', 'Unique', 'Unicidad%', 'Completitud%',
                'Nullwarning', 'Mean', 'Stddev', 'Variance', 'Min', 'Max', 
                'Skewness', 'Kurtosis', 'Zeros'
            ],
        "date": [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                'Notnulls', 'Unique', 'Unicidad%', 'Completitud%',
                'Nullwarning', 'Min', 'Max', 'Mean'
            ],
        "string": [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                       'Notnulls', 'Unique', 'Unicidad%', 'Completitud%',
                       'Nullwarning'],
        "other": [
                "Col", "Datatype","Examples", "Count", "Duplicates", "Missing", 
                    "Notnulls", "Unique", "Unicidad%", "Completitud%", 
                    "Mean", "Nullwarning", "True%", "False%", "Others%"]
    }

    # Aplicar el orden específico a cada DataFrame
    if not df_list[0].empty:
        df_list[0] = df_list[0][column_orders["string"]]
    if not df_list[3].empty:
        columnas_a_seleccionar = df_list[3]["Col"].to_list()
        porcentajes = calcular_porcentaje_true_false_otros(df.select(columnas_a_seleccionar))
        porcentajes = porcentajes.to_pandas()
        df_list[3] = pd.merge(df_list[3], porcentajes, on='Col')
        df_list[3] = df_list[3][column_orders["other"]]
    
    
    # Reasignar el dataframe con el nuevo orden de columnas
    if not df_list[1].empty:
        columnas_a_usar_int = [col for col in column_orders["numeric"] if col in df_list[1].columns]
        df_list[1] = df_list[1][columnas_a_usar_int]
    if not df_list[2].empty:
        columnas_a_usar_date = [col for col in column_orders["date"] if col in df_list[2].columns]
        df_list[2] = df_list[2][columnas_a_usar_date]

    return df_list


def load_and_process_data(file_path, limite):
    """
    Carga y convierte un archivo CSV o Parquet en un DataFrame de Polars.

    Args:
        file_path (str): Ruta del archivo.
        limite (int): Límite opcional de filas a leer.

    Returns:
        df (polars.DataFrame): DataFrame procesado.
    """
    file_extension = os.path.splitext(file_path)[1][1:]

    if file_extension not in ["csv", "parquet"]:
        print(f"Tipo de archivo no soportado: {file_extension}")
        return None

    df = process_chunks_optimized_polars(file_path, file_extension, limite)
    if df is None:
        print("Error al procesar el archivo.")
        return None
                
    # Convertir tipos de columnas si es necesario
    df = convert_column_types(df)
    return df