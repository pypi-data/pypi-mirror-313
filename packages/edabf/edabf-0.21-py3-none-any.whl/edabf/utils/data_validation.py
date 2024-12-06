import pandas as pd
import polars as pl
import uuid
from ..data_loader.eda_loader import EDALoader
from ..utils.dataframe_operations import combine_dicts

def eliminar_nan(dic):
    if isinstance(dic, dict):
        # Aplicar recursión de manera eficiente
        cleaned_dict = {}
        for key, value in dic.items():
            if key == "Examples":
                cleaned_dict[key] = value  # No aplicar eliminación en "Examples"
            else:
                nested_value = eliminar_nan(value)
                if nested_value is not None:
                    cleaned_dict[key] = nested_value
        
        # Eliminar claves redundantes
        if cleaned_dict.get("Freq") or "Freq" in cleaned_dict:
            cleaned_dict.pop("freq", None)
        if cleaned_dict.get("Top") or "Top" in cleaned_dict:
            cleaned_dict.pop("top", None)

        cleaned_dict.pop("count", None)  # Eliminar "count" si está presente
        
        return cleaned_dict
    
    elif isinstance(dic, list):
        return [eliminar_nan(item) for item in dic if eliminar_nan(item) is not None]
    
    elif pd.notna(dic):  # Si el valor no es NaN
        return dic
    
    else:
        return None
    

def eliminar_claves_con_porcentaje(dic):
    if isinstance(dic, dict):
        dic_filtrado = {}

        for key, value in dic.items():
            # Tratar la clave 'Top' de manera independiente
#            if key == "Top" and isinstance(value, str) and len(value) > 50:
#                value = value[:50]
#            if key == "Examples":
#                value = [item[:50] if isinstance(item, str) and len(item) > 50 else item for item in value]
            # Aplicar la función de manera recursiva y eliminar claves con '%'
            if '%' not in key:
                dic_filtrado[key] = eliminar_claves_con_porcentaje(value)

        return dic_filtrado
    elif isinstance(dic, list):
        return [eliminar_claves_con_porcentaje(item) for item in dic]
    else:
        return dic
    

# Función para reemplazar el valor "top" por NULL en el EDA
def replace_top_with_null(eda_statistics, column_data_type):
    if column_data_type == 'nvarchar' and 'top' in eda_statistics:
        eda_statistics['top'] = "nan"
    return eda_statistics


def validar_diccionario(diccionario):
    columnas_numericas = []
    columnas_fecha = []
    precision = []
    for columna, detalles in diccionario['Columns'].items():
        if detalles['DataType'] == 'int' or detalles['DataType'] == 'float':
            try:
                columnas_numericas.append(columna)
                if detalles['EDA_Statistics']['min'] <= 0:
                    precision.append(('num',False))
                else:
                    precision.append(('num',True))
            except:
                pass
        elif detalles['DataType'] == 'datetime2' or detalles['DataType'] == 'date':
            try:
                columnas_fecha.append(columna)
                if detalles['EDA_Statistics']['min'].year <= 2000:
                    precision.append(('fecha',False))
                elif detalles['EDA_Statistics']['max'].year >= 2050:
                    precision.append(('fecha',False))
                else:
                    precision.append(('fecha',True))
            except:
                pass                
    return precision


# Función para verificar si una cadena es un UUID
def es_uuid(val):
    try:
        uuid.UUID(str(val))  # Intentamos convertir la cadena a UUID
        return True
    except ValueError:
        return False


def validar_porcentaje(lista):
    total = len(lista)
    count_true = sum(1 for _, value in lista if value)
    # Asegurarnos de no dividir por cero
    if total > 0:
        porcentaje_true = (count_true / total) * 100
    else:
        porcentaje_true = 0  # Si no hay elementos, asignamos 0% como valor predeterminado

    return porcentaje_true



def calculate_csv_info(df):
    """
    Calcula la información equivalente para un archivo CSV utilizando Polars.
    columns_info_result, size_result, record_count_result, column_count_result.
    """
    # Obtener información de las columnas
    columns_info_result = [(col, df.schema[col]) for col in df.columns]

    # Calcular el tamaño del DataFrame en KB
    # Polars no tiene un método directo como pandas para obtener el uso de memoria,
    # pero podemos estimar el tamaño del DataFrame como una aproximación.
    size_result = [[0, df.estimated_size() / 1024]]  # Tamaño en KB

    # Calcular el conteo de registros
    record_count_result = [[df.height]]

    # Calcular el número de columnas
    column_count_result = [[df.width]]

    # Las llaves primarias y foráneas no se pueden obtener del CSV directamente, se pueden dejar como listas vacías
    primary_keys_result = []
    foreign_keys_result = []

    return columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result



def eliminar_key_count(dic, key):
    if isinstance(dic, dict):
        # Eliminar la clave en el nivel actual
        dic.pop(key, None)
        # Recorrer cada valor en el diccionario para buscar subdiccionarios
        for subkey, subvalue in dic.items():
            eliminar_key_count(subvalue, key)  # Recursión para subdiccionarios
    elif isinstance(dic, list):
        # Si el valor es una lista, aplicar la recursión a cada elemento
        for item in dic:
            eliminar_key_count(item, key)
    return dic


def calculate_statistic(dictionary):
    unicidad = []
    completitud = []

    for column, details in dictionary['Columns'].items():
        eda_stats = details.get('EDA_Statistics', {})
        
        # Usar get para evitar KeyError si 'Count', 'Unique' o 'NotNulls' no existen
        count = eda_stats.get('Count', 0)
        unique = eda_stats.get('Unique', 0)
        notnulls = eda_stats.get('NotNulls', 0)
        
        # Evitar realizar cálculos en columnas donde el conteo es cero o no tiene sentido (p.ej. booleanas)
        if count > 0:
            difference = (unique * 100) / count if count != 0 else 0
            difference2 = (notnulls * 100) / count if count != 0 else 0
        else:
            difference = 0
            difference2 = 0

        # Añadir las métricas a EDA_Statistics solo si el cálculo es válido
        if count > 0:
            eda_stats['Unicidad%'] = difference
            eda_stats['Completitud%'] = difference2
            unicidad.append(difference)
            completitud.append(difference2)
        else:
            eda_stats['Unicidad%'] = 0
            eda_stats['Completitud%'] = 0

    # Calcular los promedios totales de unicidad e completitud
    unicidad_total = sum(unicidad) / len(unicidad) if unicidad else 0
    completitud_total = sum(completitud) / len(completitud) if completitud else 0
    
    # Almacenar los resultados en el diccionario
    dictionary['unicidad'] = unicidad_total
    dictionary['completitud'] = completitud_total


def obtener_ejemplos_optimizado(table_info):
    resultados = []

    for column_info in table_info.get('Columns', {}).values():
        ejemplos = column_info.get("EDA_Statistics", {}).get("Examples", [])
        
        # Truncar ejemplos si son cadenas muy largas
        primer_ejemplo = next((str(ejemplo)[:50] for ejemplo in ejemplos if ejemplo != ""), "")
        resultados.append(primer_ejemplo)

    resultado_final = ' | '.join(resultados)
    return resultado_final



def validate_data(df):
    """
    Valida la estandarización de los datos y calcula la cantidad de columnas
    llenas en diferentes porcentajes (0%, 4%, 20%, 70%) en un DataFrame de Polars.
    """
    data_standardization_info = {}
    empty_columns_count = 0
    filled_0_percent_count = 0
    filled_4_percent_count = 0
    filled_20_percent_count = 0
    filled_70_percent_count = 0

    total_rows = len(df)

    for column in df.columns:
        # Verificar si todos los valores son del mismo tipo y contiene palabras
        unique_data_types = {df.schema[column]}
        is_standardized = len(unique_data_types) == 1 and df[column].dtype == pl.Utf8

        # Contar valores nulos y calcular porcentaje de llenado
        missing_count = df[column].null_count()
        filled_count = total_rows - missing_count
        filled_percentage = filled_count / total_rows

        # Clasificar la columna según el porcentaje de llenado
        if filled_percentage == 0:
            empty_columns_count += 1
        elif filled_percentage >= 0.70:
            filled_70_percent_count += 1
        elif filled_percentage >= 0.20:
            filled_20_percent_count += 1
        elif filled_percentage >= 0.04:
            filled_4_percent_count += 1
        else:
            filled_0_percent_count += 1

        # Almacenar la información de estandarización de la columna
        data_standardization_info[column] = {
            "IsStandardized": is_standardized,
            "DataTypes": [dtype for dtype in unique_data_types]
        }

    return (
        data_standardization_info,
        empty_columns_count,
        filled_0_percent_count,
        filled_4_percent_count,
        filled_20_percent_count,
        filled_70_percent_count
    )


def analyze_data(df):
    """
    Optimiza el análisis de datos y devuelve estadísticas descriptivas etiquetadas de manera clara.
    """
    # Obtener estadísticas descriptivas con Polars y convertir a un diccionario de pandas
    eda_statistics_ = df.describe().to_pandas().round(2).set_index("statistic").to_dict()

    
    # Revisar las columnas de tipo datetime y convertir a fechas si es necesario
    timestamp_columns = df.select(pl.col(pl.Datetime)).columns
    if timestamp_columns:
        df = df.with_columns([pl.col(col).dt.date().alias(col) for col in timestamp_columns])

    return eda_statistics_


def generate_table_info(df, table_name, size_result, record_count_result, column_count_result, columns_info_result, eda_statistics_, data_standardization_info, primary_keys_result, empty_columns_count, foreign_keys_result, filled_0_percent_count, filled_4_percent_count, filled_20_percent_count, filled_70_percent_count):
    edaloader = EDALoader(dataframes_dict={'table1':df})
    eda_statistics_df = edaloader.get_table_stats(df)
    eda_statistics_df = eda_statistics_df.to_pandas()
    eda_statistics_df = eda_statistics_df.set_index('Column', drop=True)
    eda_statistics_df.index.name = 'index'
    eda_statistics = eda_statistics_df.to_dict(orient='index')
    
    eda_statistics = combine_dicts(eda_statistics, eda_statistics_)
    eda_statistics = str(eda_statistics).replace("nan","None")
    eda_statistics = eval(eda_statistics)
    # Crear un diccionario para almacenar la información
    table_info = {
        "TableName": table_name,
        "SizeKB": size_result[0][1] if len(size_result[0])>=2 else size_result[0][0],
        "RecordCount": record_count_result[0][0],
        "ColumnCount": column_count_result[0][0],
        "Columns": {column[0]: {"DataType": column[1], "EDA_Statistics": eda_statistics.get(column[0], {}), "DataStandardization": data_standardization_info.get(column[0], {})} for column in columns_info_result},
        "PrimaryKeys": [pk[0] for pk in primary_keys_result],
        "Empty_Columns": empty_columns_count,
        "ForeignKeys": [{"ParentColumn": fk[0], "ReferencedTable": fk[1], "ReferencedColumn": fk[2]} for fk in foreign_keys_result if len(fk) >= 3] if foreign_keys_result is not None and foreign_keys_result != [] else [],
        "Columns_Filled_0_percent": filled_0_percent_count,
        "Columns_Filled_4_percent": filled_4_percent_count,
        "Columns_Filled_20_percent": filled_20_percent_count,
        "Columns_Filled_70_percent": filled_70_percent_count
    }

    table_info = eliminar_nan(table_info)

    table_info_gpt = eliminar_claves_con_porcentaje(table_info)
    #table_info_gpt['Columns']

    #table_info['Example'] = obtener_ejemplos_optimizado(table_info_gpt)

    calculate_statistic(table_info_gpt)

    precision_parcial = validar_diccionario(table_info_gpt)

    precision = validar_porcentaje(precision_parcial)

    table_info_gpt['Precision'] = precision

    [table_info_gpt["Columns"][i]["EDA_Statistics"].update({"Examples": ", ".join(map(str, table_info_gpt["Columns"][i]["EDA_Statistics"]["Examples"]))})
     for i in table_info_gpt["Columns"] if isinstance(table_info_gpt["Columns"][i]["EDA_Statistics"].get("Examples"), list)]

    return table_info_gpt