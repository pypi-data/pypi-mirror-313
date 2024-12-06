# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:35 2024

@author: nicol
"""

import time
import polars as pl
from .utils.excel_export import write_to_excel, setup_excel_file, create_excel_sheet


def process_dataframe(df, output=None, table_name="DataFrame", limite=None):
    """
    Procesa un DataFrame y genera un informe EDA en formato Excel.

    Args:
        df (DataFrame): El DataFrame que se desea procesar.
        output (str): Ruta de salida para el archivo Excel.
        table_name (str): Nombre de la tabla para identificar los datos en el informe Excel.
        limite (int): Límite opcional de filas a procesar del DataFrame.
    """
    if df is None or df.empty:
        print("El DataFrame proporcionado está vacío. Finalizando el programa.")
        return
    
    # Convertir a un DataFrame de polars si no lo es
    if not isinstance(df, pl.DataFrame):
        print("Convirtiendo DataFrame a formato Polars...")
        df = pl.from_pandas(df)

    # Aplicar el límite si se especifica
    if limite is not None and limite > 0:
        df = df.head(limite)
        print(f"Se han procesado las primeras {limite} filas del DataFrame.")

    # Configurar y escribir en el archivo Excel
    start_time = time.time()
    # Configuración inicial de Excel
    writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands, format_guide_text = setup_excel_file(output)
    create_excel_sheet(book, SALTO_LADO, ANCHO_COL, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, format_guide_text)
    
    # Escribir el DataFrame en el archivo Excel
    write_to_excel(df, table_name, writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands, ANCHO_COL, SALTO_LADO, format_columna_col)
    
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time} segundos")
    # Cerrar el archivo Excel
    writer.close()
