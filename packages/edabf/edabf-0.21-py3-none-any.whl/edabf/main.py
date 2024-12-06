# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:35 2024

@author: nicol
"""

import pandas as pd
import os
import time
from datetime import datetime
from .data_loader.sql_operations import connect_to_database, load_data_from_sql, execute_sql_queries, get_table_query
from .utils.data_validation import calculate_csv_info, analyze_data, validate_data, generate_table_info
from .utils.dataframe_operations import create_dataframe_by_type, reorder_columns_by_common, calcular_porcentaje_true_false_otros, process_chunks_optimized_polars, convert_column_types
from .utils.excel_export import setup_excel_file, export_multiple_dfs_to_excel



##### Función Principal ####
def main(flag, db_type=None, server=None, user=None, password=None, database=None, schema=None, table_name=None, file_path=None, folder_path=None, output=None, limite=None):
    """
    Función principal que generaliza la lectura de datos desde CSV, tabla o dataset de MySQL, PostgreSQL, SQL Server, o Oracle.

    Args:
        flag: indica el tipo de fuente de datos. Puede ser 'csv', 'csv_masivo', 'mysql_table', 'mysql_dataset', 'postgresql_table', etc.
        db_type: el tipo de base de datos ('mysql', 'postgresql', 'sqlserver', 'oracle').
        server: servidor de la base de datos.
        user: usuario de la base de datos.
        password: contraseña de la base de datos.
        database: nombre de la base de datos.
        schema: esquema de la base de datos.
        table_name: nombre de la tabla a leer (si aplica).
        csv_file_path: ruta del archivo CSV a leer (solo para CSV).
        folder_path: ruta de la carpeta que contiene los archivos CSV (solo para csv_masivo).
    """
    global table_info_gpt, df

    inicio = time.time()

    primary_keys_result = foreign_keys_result = None
    size_result = [[0, 1]]
    record_count_result = [[0]]
    column_count_result = [[0]]
    filled_0_percent_count = filled_4_percent_count = filled_20_percent_count = filled_70_percent_count = 0
    empty_columns_count = 0


    if flag in ["mysql_table", "postgresql_table", "sqlserver_table", "oracle_table"]:
        # Conectar a la base de datos y cargar los datos desde una tabla específica
        conn = connect_to_database(db_type, server, user, password, database)
        df = load_data_from_sql(conn, f"SELECT * FROM {schema}.[{table_name}];", table_name)
        dfs = [df]  # Almacenar en lista para procesar varias hojas
        table_names = [table_name]
        conn.close()

    elif flag in ["mysql_dataset", "postgresql_dataset", "sqlserver_dataset", "oracle_dataset"]:
        # Conectar a la base de datos y cargar los datos de todas las tablas del dataset
        conn = connect_to_database(db_type, server, user, password, database)
        cursor = conn.cursor()
        
        # Obtener la consulta para listar las tablas del esquema según el tipo de base de datos
        query = get_table_query(db_type, schema)
        cursor.execute(query)
        tables = cursor.fetchall()

        # Iterar sobre cada tabla y leer sus datos
        dfs = []
        table_names = []
        for table in tables[:5]:  # Puedes ajustar la cantidad de tablas a cargar
            try:
                table_name = table[0]
                df = load_data_from_sql(conn, f"SELECT * FROM {schema}.[{table_name}];", table_name)
                dfs.append(df)
                table_names.append(table_name)
            except IndexError:
                pass
        conn.close()

    elif flag == "archivo":
        # Cargar los datos desde un archivo CSV
        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[1][1:]
            df = process_chunks_optimized_polars(file_path, file_extension, limite)
            dfs = [df]  # Almacenar en lista para procesar varias hojas
            table_names = [os.path.splitext(os.path.basename(file_path))[0]]  # Nombre de la hoja será el nombre del archivo CSV
        else:
            print("El archivo CSV no existe. Finalizando el programa.")
            return


    elif flag == "masivo":
        # Leer todos los archivos CSV de una carpeta
        if os.path.exists(folder_path):
            dfs = []
            table_names = []
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".csv") or file_name.endswith(".parquet"):
                    file_path = os.path.join(folder_path, file_name)
                    file_extension = os.path.splitext(file_path)[1][1:]
                    df = process_chunks_optimized_polars(file_path, file_extension, limite)
                    dfs.append(df)
                    table_names.append(os.path.splitext(file_name)[0])  # Nombre de la hoja será el nombre del archivo CSV
        else:
            print("La carpeta no existe. Finalizando el programa.")
            return

    else:
        print("Opción no válida. Finalizando el programa.")
        return

    
    # Configurar el archivo Excel
    writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands = setup_excel_file(output)
    
    sheet_name1 = 'General'
    worksheet1 = book.add_worksheet(sheet_name1)
    worksheet1.set_column(SALTO_LADO, SALTO_LADO, ANCHO_COL)

    # Escribir encabezado en la hoja General
    worksheet1.write(ENCABEZ, SALTO_LADO, 'Informe EDA de datos, al ' + datetime.now().strftime('%d %b %Y'), format_encabez_titulo)
    worksheet1.write(ENCABEZ + 1, SALTO_LADO, 'Brain Food', format_encabez_subtitulo)

    # Iterar sobre cada DataFrame y generar los cálculos correspondientes
    for i, df in enumerate(dfs):
        try:
            table_name = table_names[i]

            # Si es una base de datos, ejecutar las consultas SQL para cada tabla
            if flag in ["mysql_table", "mysql_dataset", "postgresql_table", "postgresql_dataset", "sqlserver_table", "sqlserver_dataset", "oracle_table", "oracle_dataset"]:
                conn = connect_to_database(db_type, server, user, password, database)
                cursor = conn.cursor()
                columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result = execute_sql_queries(conn, table_name, db_type)
                conn.close()
    
            # Si es CSV, calcular la información desde el DataFrame directamente
            elif flag == "archivo":
                columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result = calculate_csv_info(df)
                
            df = convert_column_types(df)
            # Realizar el análisis y validación para cada DataFrame
            
            eda_statistics_ = analyze_data(df)
            
            
            data_standardization_info, empty_columns_count, filled_0_percent_count, filled_4_percent_count, filled_20_percent_count, filled_70_percent_count = validate_data(df)

            # Generar la información de la tabla para cada DataFrame
            table_info_gpt = generate_table_info(df, table_name, size_result, record_count_result, column_count_result, columns_info_result, eda_statistics_, data_standardization_info, primary_keys_result, empty_columns_count, foreign_keys_result, filled_0_percent_count, filled_4_percent_count, filled_20_percent_count, filled_70_percent_count)

            
            # Separar los DataFrames por tipo de dato para cada hoja
            table_info_gpt_str_df = create_dataframe_by_type(table_info_gpt, "string")
            table_info_gpt_int_df = create_dataframe_by_type(table_info_gpt, "numeric")
            table_info_gpt_date_df = create_dataframe_by_type(table_info_gpt, "date")
            table_info_gpt_other_df = create_dataframe_by_type(table_info_gpt, "other")
        
            # Lista con DataFrames separados por tipo
            df_list = [table_info_gpt_str_df, table_info_gpt_int_df, table_info_gpt_date_df, table_info_gpt_other_df]
        
            [table_info_gpt_str_df, table_info_gpt_int_df, table_info_gpt_date_df, table_info_gpt_other_df] = reorder_columns_by_common(df_list)
    
            nuevo_orden_columnas_int = [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                'Notnulls', 'Unique', 'Completitud%', 'Integridad%',
                'Nullwarning', 'Mean', 'Stddev', 'Variance', 'Min', 'Max', 
                'Skewness', 'Kurtosis', 'Zeros'
            ]
        
            nuevo_orden_columnas_date = [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                'Notnulls', 'Unique', 'Completitud%', 'Integridad%',
                'Nullwarning', 'Min', 'Max', 'Mean'
            ]
            
            nuevo_columnas_str = [
                'Col', 'Datatype', 'Examples', 'Count', 'Duplicates', 'Missing',
                       'Notnulls', 'Unique', 'Completitud%', 'Integridad%',
                       'Nullwarning']
            
            nuevo_columnas_other = [
                "Col", "Datatype","Examples", "Count", "Duplicates", "Missing", 
                    "Notnulls", "Unique", "Completitud%", "Integridad%", 
                    "Mean", "Nullwarning", "True%", "False%", "Others%"]
            
            if len(table_info_gpt_str_df) > 0:
                table_info_gpt_str_df = table_info_gpt_str_df[nuevo_columnas_str]
            if len(table_info_gpt_other_df) > 0:
                columnas_a_seleccionar = table_info_gpt_other_df["Col"].to_list()
                porcentajes = calcular_porcentaje_true_false_otros(df.select(columnas_a_seleccionar))
                porcentajes = porcentajes.to_pandas()
                table_info_gpt_other_df = pd.merge(table_info_gpt_other_df, porcentajes, on='Col')
                table_info_gpt_other_df = table_info_gpt_other_df[nuevo_columnas_other]
            
            
            # Reasignar el dataframe con el nuevo orden de columnas
            if len(table_info_gpt_int_df) > 0:
                columnas_a_usar_int = [col for col in nuevo_orden_columnas_int if col in table_info_gpt_int_df.columns]
                table_info_gpt_int_df = table_info_gpt_int_df[columnas_a_usar_int]
            if len(table_info_gpt_date_df) > 0:
                columnas_a_usar_date = [col for col in nuevo_orden_columnas_date if col in table_info_gpt_date_df.columns]
                table_info_gpt_date_df = table_info_gpt_date_df[columnas_a_usar_date]
            
            df_list = [table_info_gpt_str_df, table_info_gpt_int_df, table_info_gpt_date_df, table_info_gpt_other_df]
                
                # Escribir los DataFrames en hojas de Excel (pasar df_list como argumento)
            export_multiple_dfs_to_excel(
                writer, 
                book, 
                ENCABEZ, 
                format_encabez_titulo, 
                format_encabez_columnas, 
                format_encabez_columnas2, 
                format_celda_datos, 
                format_titulo_tabla, 
                format_roboto_bordered, 
                format_num_with_thousands,
                ANCHO_COL, 
                SALTO_LADO, 
                format_columna_col, 
                df_list,  
                table_name,
                table_info_gpt
            )
        except Exception as e:
            print(f"Ocurrió un error al procesar la tabla '{table_name}': {e}")

    writer.close()

    salida = time.time()
    print(f"Tiempo de ejecución: {salida - inicio} segundos")
