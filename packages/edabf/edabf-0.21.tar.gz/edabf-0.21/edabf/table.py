# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:35 2024

@author: nicol
"""


import time
from .utils.dataframe_operations import convert_column_types
from .data_loader.sql_operations import connect_to_database, load_data_from_sql
from .utils.excel_export import write_to_excel, setup_excel_file, create_excel_sheet



def process_single_table(db_type, server, user, password, database, schema, table_name, path_instaclient=None, port=None, output=None):
    """
    Procesa una tabla única de una base de datos y genera un informe EDA en Excel.

    Args:
        db_type (str): Tipo de base de datos ('mysql', 'postgresql', 'sqlserver', 'oracle').
        server (str): Dirección del servidor de la base de datos.
        user (str): Usuario de la base de datos.
        password (str): Contraseña de la base de datos.
        database (str): Nombre de la base de datos.
        schema (str): Esquema de la base de datos.
        table_name (str): Nombre de la tabla a procesar.
        port (int): Número del puerto a conectarse.
        path_instaclient (str): Ruta de instalación de InstaClient (Solo para OracleDB).
        output (str): Ruta de salida para el archivo Excel.
    """
    start_time = time.time()
    
    # Conectar a la base de datos y cargar la tabla
    engine = connect_to_database(db_type, server, user, password, database, path_instaclient, port)
    df = None

    print("Accediendo a la base de datos...")
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

    print("Calculando EDA...")
    writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands, format_guide_text = setup_excel_file(output)
    create_excel_sheet(book, SALTO_LADO, ANCHO_COL, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, format_guide_text)
    
    # Configurar y escribir en el archivo Excel
    write_to_excel(df, table_name, writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands,ANCHO_COL, SALTO_LADO, format_columna_col, db_type, server, user, password, database, schema, engine, path_instaclient)
       
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")
    # Cerrar el archivo Excel
    writer.close() 




    


