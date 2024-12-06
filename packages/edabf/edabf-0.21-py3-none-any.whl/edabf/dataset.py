# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:35 2024

@author: nicol
"""

import time
from .utils.dataframe_operations import convert_column_types
from .data_loader.sql_operations import connect_to_database, load_data_from_sql, get_table_query
from .utils.excel_export import write_to_excel, setup_excel_file, create_excel_sheet
from .data_loader.sql_operations import read_sql_query_chunked


def process_dataset(db_type, server, user, password, database, schema, path_instaclient=None, port=None, output=None, limit_tables=5):
    """
    Procesa todas las tablas de un esquema en la base de datos y genera un informe EDA en un único archivo Excel.

    Args:
        db_type (str): Tipo de base de datos ('mysql', 'postgresql', 'sqlserver', 'oracle').
        server (str): Dirección del servidor de la base de datos.
        user (str): Usuario de la base de datos.
        password (str): Contraseña de la base de datos.
        database (str): Nombre de la base de datos.
        schema (str): Esquema de la base de datos.
        port (int): Número del puerto a conectarse.
        output (str): Ruta de salida para el archivo Excel.
        limit_tables (int): Límite opcional para el número de tablas a procesar.
    """
    start_time = time.time()

    
    # Conectar a la base de datos y obtener las tablas del esquema
    engine = connect_to_database(db_type, server, user, password, database, path_instaclient, port)
    table_query = get_table_query(db_type, schema)
    tables = list(read_sql_query_chunked(engine, table_query).iter_rows())
 
    # Limitar el número de tablas a procesar si se especifica un límite
    tables = tables[:limit_tables]
    # Configuración inicial del archivo Excel
    writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands, format_guide_text = setup_excel_file(output)
    create_excel_sheet(book, SALTO_LADO, ANCHO_COL, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, format_guide_text)

    # Procesar cada tabla y escribir en el archivo Excel
    for table in tables:
        table_name = table[0]
        print(f"Procesando tabla: {table_name}")
        
        try:
            # Cargar los datos de la tabla
            df = None
            try:
                df = load_data_from_sql(engine, f"SELECT * FROM {schema}.[{table_name}]")
            except:
                try:
                    df = load_data_from_sql(engine, f'SELECT * FROM "{schema.upper()}"."{table_name.upper()}"')
                except:
                    try:
                        df = load_data_from_sql(engine, f"SELECT * FROM {schema}.{table_name}")
                    except:
                        df = load_data_from_sql(engine, f"SELECT * FROM {table_name}")
            # Convertir tipos de columnas si es necesario
            df = convert_column_types(df)
            if len(df) > 0:
                # Escribir en el archivo Excel para cada tabla procesada
                write_to_excel(df, table_name, writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands, ANCHO_COL, SALTO_LADO, format_columna_col, db_type, server, user, password, database, schema, path_instaclient)
            else:
                print(f"tabla: {table_name} vacía")
        except Exception as e:
            print(f"Ocurrió un error al procesar la tabla '{table_name}': {e}")
    
    # Finalizar la conexión a la base de datos
    engine.dispose()
    
    # Cerrar el archivo Excel
    writer.close()
    end_time = time.time()
    print(f"Tiempo de ejecución total: {end_time - start_time} segundos")
