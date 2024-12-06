# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:35 2024

@author: nicol
"""


import os
import time
from .utils.dataframe_operations import load_and_process_data
from .utils.excel_export import write_to_excel, setup_excel_file, create_excel_sheet


def process_single_file(file_path, output=None, limite=None):
    """
    Procesa un archivo único (CSV o Parquet) y genera un informe EDA en Excel.

    Args:
        file_path (str): Ruta del archivo a procesar.
        output (str): Ruta de salida para el archivo Excel.
        limite (int): Límite opcional de filas a leer por archivo.
    """
    if not os.path.exists(file_path):
        print("El archivo especificado no existe. Finalizando el programa.")
        return

    # Leer archivo y procesar datos
    df = load_and_process_data(file_path, limite)
    if df is None:
        return
    
    longitud = df.height
    print(f"El DataFrame tiene {longitud} filas.")
    
    table_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Calculando EDA...")
    # Configurar y escribir en el archivo Excel
    start_time = time.time()
    # Configuración inicial de Excel
    writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands, format_guide_text = setup_excel_file(output)
    create_excel_sheet(book, SALTO_LADO, ANCHO_COL, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, format_guide_text)
    
    write_to_excel(df, table_name, writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands,ANCHO_COL, SALTO_LADO, format_columna_col)
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")
    # Cerrar el archivo Excel
    writer.close() 




    


