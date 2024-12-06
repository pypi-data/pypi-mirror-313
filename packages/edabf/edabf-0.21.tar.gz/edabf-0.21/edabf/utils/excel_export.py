import pandas as pd
import os
from datetime import datetime
from ..utils.dataframe_operations import save_dataframe_to_csv
from ..utils.data_validation import calculate_csv_info, analyze_data, validate_data, generate_table_info
from ..utils.dataframe_operations import categorize_dataframes_by_type
from ..data_loader.sql_operations import connect_to_database, execute_sql_queries


##### Configuración de Excel ####
def setup_excel_file(output):
    TAM_LETRA_BASE = 10  # Tamaño letra de todo el informe (excepto títulos)
    ENCABEZ = 1         # Si quieren saltarse líneas antes de poner los encabezados en cada hoja
    SALTO_LADO = 0      # Si quieren saltarse columnas antes de poner los encabezados en cada hoja
    ANCHO_COL = 20      # Ancho de las columnas

    # Nombre del archivo de Excel donde se creará el informe
    os.makedirs(output, exist_ok=True)
    file_name = f'{output}/eda_datos_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    book = writer.book

    # === Formatos a lo largo del informe ===
    format_encabez_titulo = book.add_format({
        'bold': True, 
        'color': '#14B8C4', 
        'font_size': TAM_LETRA_BASE+6,
        'font_name': 'Roboto'  
    })

    format_encabez_subtitulo = book.add_format({
        'bold': True, 
        'color': '#7F7F7F', 
        'font_size': TAM_LETRA_BASE + 4,
        'font_name': 'Roboto'  
    })

    format_encabez_columnas = book.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',  
        'align': 'center',   
        'color': '#FFFFFF',  
        'bg_color': '#19B9CB',  
        'border': 1,  
        'font_size': TAM_LETRA_BASE + 2,
        'font_name': 'Roboto'  
    })
    
    format_encabez_columnas2 = book.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',  
        'align': 'center',   
        'bg_color': '#E7E6E6',  
        'border': 1,  
        'font_size': TAM_LETRA_BASE + 2,
        'font_name': 'Roboto'  
    })

    format_columna_col = book.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',  
        'align': 'center',   
        'bg_color': '#E7E6E6',  
        'border': 1,  
        'font_size': TAM_LETRA_BASE + 2,
        'font_name': 'Roboto'  
    })

    format_celda_datos = book.add_format({
        'align': 'center', 
        'valign': 'vcenter',  
        'border': 1, 
        'text_wrap': True,  
        'font_name': 'Roboto'  
    })

    format_titulo_tabla = book.add_format({
        'bold': True,
        'font_size': TAM_LETRA_BASE + 4,
        'align': 'left',
        'color': '#FFFFFF',  
        'bg_color': '#000000',  # Color negro para el fondo de la fila
        'valign': 'vcenter',
        'border': 1,  
        'font_name': 'Roboto'  
    })

    # Definir formatos con bordes y fuente Roboto 12
    format_roboto_bordered = book.add_format({
        'border': 1,  # Bordes en todos los lados
        'font_name': 'Roboto',  # Cambiar fuente a Roboto
        'font_size': 12,  # Tamaño de la fuente
        'align': 'center'
    })

    # Definir formato para números con separador de miles, bordes y fuente Roboto 12
    format_num_with_thousands = book.add_format({
        'num_format': '#,##0',  # Formato con separador de miles
        'border': 1,  # Bordes en todos los lados
        'font_name': 'Roboto',  # Cambiar fuente a Roboto
        'font_size': 12,  # Tamaño de la fuente
        'align': 'center' 
    })

    format_guide_text = book.add_format({
        'bold': False,           # Texto normal para descripciones
  #      'text_wrap': True,       # Ajustar texto en múltiples líneas
        'valign': 'top',         # Alinear verticalmente al inicio de la celda
        'align': 'left',         # Alinear texto a la izquierda
        'font_color': '#000000', # Color negro para el texto
        'border': 0,             # Sin borde
        'font_size': TAM_LETRA_BASE,  # Tamaño de letra ajustado
        'font_name': 'Roboto',   # Fuente Roboto para consistencia
    })



    return writer, book, format_encabez_titulo, format_encabez_subtitulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, ANCHO_COL, SALTO_LADO, ENCABEZ, format_columna_col, format_roboto_bordered, format_num_with_thousands, format_guide_text


def save_data_to_csv(df_list):
    for i, df in enumerate(df_list):
        save_dataframe_to_csv(df, f"table_info_gpt_{['str', 'int', 'date', 'other'][i]}.csv")


def escribir_dataframe_con_titulo(writer, dataframe, sheet_name, startrow, startcol, titulo_tabla, format_titulo_tabla, format_encabez_columnas, format_encabez_columnas2, ANCHO_COL, format_celda_datos, format_columna_col):
    worksheet = writer.sheets[sheet_name]
    num_columnas = len(dataframe.columns)

    # Combinar las celdas en toda la fila del título, desde la columna 0 hasta la última columna de la tabla
    worksheet.merge_range(startrow, 0, startrow, num_columnas - 1, titulo_tabla, format_titulo_tabla)

    # Ahora ajusta el resto del código para escribir las columnas y datos de la tabla
    startrow += 1  # Incrementar para escribir los encabezados

    traducciones = {
    'Col': 'Columna',
    'Datatype': 'Tipo de Dato',
    'Examples': 'Ejemplos',
    'Count': 'Conteo',
    'Duplicates': 'Duplicados',
    'Freq': 'Frecuencia',
    'Missing': 'Faltantes',
    'Notnulls': 'No Nulos',
    'Unique': 'Únicos',
    'Avglen': 'Longitud Promedio',
    'Unicidad%': 'Porcentaje de Unicidad',
    'Completitud%': 'Porcentaje de Completitud',
    'Nullwarning': 'Advertencia de Nulos',
    'Top': 'Dato Más Frecuente',
    'Mean': 'Media',
    'Stddev': 'Desviación Estándar',
    'Variance': 'Varianza',
    'Min': 'Mínimo',
    'Max': 'Máximo',
    'Skewness': 'Asimetría',
    'Kurtosis': 'Curtosis',
    'Zeros': 'Ceros',
    'True%': 'Porcentaje Verdadero',
    'False%': 'Porcentaje Falso',
    'Others%': 'Porcentaje Otros'
    }
    
    # Escribir los nombres de las columnas originales
    for col_num, value in enumerate(dataframe.columns.values):
        worksheet.write(startrow, startcol + col_num, value, format_encabez_columnas)
    
    # Escribir los nombres de las columnas en español en la fila siguiente (startrow + 1)
    for col_num, value in enumerate(dataframe.columns.values):
        # Escribir el nombre traducido (si existe en el diccionario)
        nombre_traducido = traducciones.get(value, value)  # Si no hay traducción, usar el valor original
        worksheet.write(startrow + 1, startcol + col_num, nombre_traducido, format_encabez_columnas2)

    # Ahora escribimos los datos del dataframe comenzando desde la fila siguiente (startrow + 2)
    dataframe.to_excel(writer, sheet_name=sheet_name, startrow=startrow + 2, startcol=startcol, index=False, header=False)  # Desactivar el header para evitar repetir columnas
    
    # Ajustar ancho de columnas y centrar contenido
    worksheet.set_column(startcol, startcol + len(dataframe.columns) - 1, ANCHO_COL, format_celda_datos)
    
    # Ajustar la altura de las filas que contienen datos del dataframe
    for row_num in range(startrow, startrow + len(dataframe) + 2):  # +2 para incluir el encabezado y la fila con nombres en español
        worksheet.set_row(row_num, 40)  # Establecer la altura de las filas a 40

    # Aplicar formato a la columna 'Col' (valores en negrita)
    if 'Col' in dataframe.columns:
        col_index = dataframe.columns.get_loc('Col')  # Obtener el índice de la columna 'Col'
        for row_num in range(1, len(dataframe) + 1):  # Aplicar formato a las celdas en la columna 'Col'
            worksheet.write(startrow + row_num + 1, startcol + col_index, dataframe.iloc[row_num - 1, col_index], format_columna_col)



def export_to_excel(writer, book, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, df_list, format_titulo_tabla, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_columna_col, ANCHO_COL, SALTO_LADO):
    
    # Segunda hoja para el análisis
    sheet_name2 = 'EDA Tabla'
    worksheet2 = book.add_worksheet(sheet_name2)

    # === Agregar encabezado de la hoja "General" a la hoja "EDA Tabla" ===
    worksheet2.write(ENCABEZ, SALTO_LADO, 'Informe EDA de datos, al ' + datetime.now().strftime('%d %b %Y'), format_encabez_titulo)
    worksheet2.write(ENCABEZ + 1, SALTO_LADO, 'Brain Food', format_encabez_subtitulo)

    # Ajustar el inicio de los dataframes para no sobrescribir el encabezado
    INICIO_1 = ENCABEZ + 3  # Añadimos 3 filas para el encabezado
        
    
    escribir_dataframe_con_titulo(writer, df_list[0], sheet_name2, startrow=INICIO_1, startcol=SALTO_LADO, titulo_tabla="Datos de Texto", format_titulo_tabla=format_titulo_tabla, format_encabez_columnas=format_encabez_columnas, format_encabez_columnas2=format_encabez_columnas2, ANCHO_COL=ANCHO_COL, format_celda_datos=format_celda_datos, format_columna_col=format_columna_col)
    
    escribir_dataframe_con_titulo(writer, df_list[1], sheet_name2, startrow=INICIO_1 + len(df_list[0]) + 4, startcol=SALTO_LADO, titulo_tabla="Datos Numéricos", format_titulo_tabla=format_titulo_tabla, format_encabez_columnas=format_encabez_columnas, format_encabez_columnas2=format_encabez_columnas2, ANCHO_COL=ANCHO_COL, format_celda_datos=format_celda_datos, format_columna_col=format_columna_col)
    
    escribir_dataframe_con_titulo(writer, df_list[2], sheet_name2, startrow=INICIO_1 + len(df_list[0]) + len(df_list[1]) + 8, startcol=SALTO_LADO, titulo_tabla="Datos de Fechas", format_titulo_tabla=format_titulo_tabla, format_encabez_columnas=format_encabez_columnas, format_encabez_columnas2=format_encabez_columnas2, ANCHO_COL=ANCHO_COL, format_celda_datos=format_celda_datos, format_columna_col=format_columna_col)
    
    escribir_dataframe_con_titulo(writer, df_list[3], sheet_name2, startrow=INICIO_1 + len(df_list[0]) + len(df_list[1]) + len(df_list[2]) + 12, startcol=SALTO_LADO, titulo_tabla="Otros Datos", format_titulo_tabla=format_titulo_tabla, format_encabez_columnas=format_encabez_columnas, format_encabez_columnas2=format_encabez_columnas2, ANCHO_COL=ANCHO_COL, format_celda_datos=format_celda_datos, format_columna_col=format_columna_col)

    writer.close()



def export_multiple_dfs_to_excel(writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands, ANCHO_COL, SALTO_LADO, format_columna_col, df_list, table_name, table_info_gpt):
    """
    Exporta múltiples DataFrames en una hoja separada del archivo Excel.
    df_list es una lista de DataFrames (separados por tipo de datos) para una sola tabla.
    table_name es el nombre de la tabla o archivo CSV que se usa como nombre de la hoja.
    """

    # Crear una hoja específica para cada tabla
    sheet_name = f"{table_name}"  # Nombre de la hoja basado en el nombre de la tabla
    worksheet = book.add_worksheet(sheet_name)
    worksheet.set_column(SALTO_LADO, SALTO_LADO, ANCHO_COL)

    # Escribir encabezado en la hoja
    worksheet.write(ENCABEZ, SALTO_LADO, f'Informe EDA de datos para {table_name}, al ' + datetime.now().strftime('%d %b %Y'), format_encabez_titulo)
    worksheet.write(ENCABEZ + 1, SALTO_LADO, 'Brain Food', format_encabez_columnas)


    # Variable para mantener la fila donde se empezará a escribir después del encabezado
    current_row = ENCABEZ + 3

    # Escribir las estadísticas del diccionario table_info_gpt (omitiendo la clave "Columns" y los campos vacíos)
    for key, value in table_info_gpt.items():
        if key != "Columns" and value != []:  # Omitir la clave "Columns" y las listas vacías
            worksheet.write(current_row, SALTO_LADO, f'{key}:', format_encabez_columnas2)  # Escribir la clave con bordes
            
            # Si el valor es numérico, usar el formato con separadores de miles y bordes
            if isinstance(value, (int, float)):
                worksheet.write(current_row, SALTO_LADO + 1, value, format_num_with_thousands)  # Formato numérico
            else:
                worksheet.write(current_row, SALTO_LADO + 1, str(value), format_roboto_bordered)  # Texto con bordes
            
            current_row += 1  # Mover a la siguiente fila para el próximo par clave-valor


    # Ajustar el inicio de los dataframes para no sobrescribir el encabezado
    startrow = current_row + 3  # Añadimos 3 filas para el encabezado
    
    # Ahora verificamos si cada DataFrame en df_list tiene datos antes de intentar escribirlos
    for i, (df, titulo) in enumerate(zip(df_list, ["Datos de Texto", "Datos Numéricos", "Datos de Fechas", "Otros Datos"])):
        if isinstance(df, pd.DataFrame) and not df.empty:  # Verifica si el DataFrame no está vacío
            # Ordenar el DataFrame por la columna 'Col' si existe
            if "Col" in df.columns:
                df = df.sort_values(by="Col")
                
            escribir_dataframe_con_titulo(writer, df, sheet_name, startrow=startrow, startcol=SALTO_LADO, titulo_tabla=titulo, 
                                          format_titulo_tabla=format_titulo_tabla, format_encabez_columnas=format_encabez_columnas, 
                                          format_encabez_columnas2=format_encabez_columnas2, ANCHO_COL=ANCHO_COL, format_celda_datos=format_celda_datos, 
                                          format_columna_col=format_columna_col)
            # Actualizamos el valor de startrow para la siguiente tabla
            startrow += len(df) + 4  # Añade espacio entre los DataFrames


def create_excel_sheet(book, SALTO_LADO, ANCHO_COL, ENCABEZ, format_encabez_titulo, format_encabez_subtitulo, format_num_with_thousands):
    """
    Crea y configura la hoja de Excel para el informe EDA.

    Args:
        book (xlsxwriter.Workbook): Objeto del libro de trabajo de Excel.
        formats (dict): Diccionario de formatos para las celdas de Excel.
        table_name (str): Nombre de la tabla para la hoja de Excel.

    Returns:
        worksheet (xlsxwriter.Worksheet): Hoja de Excel configurada.
    """
    # Crear la hoja principal
    sheet_name1 = 'General'
    worksheet1 = book.add_worksheet(sheet_name1)
    worksheet1.set_column(SALTO_LADO, SALTO_LADO, ANCHO_COL)

    # Escribir encabezado en la hoja General
    worksheet1.write(ENCABEZ, SALTO_LADO, 'Informe EDA de datos, al ' + datetime.now().strftime('%d %b %Y'), format_encabez_titulo)
    worksheet1.write(ENCABEZ + 1, SALTO_LADO, 'Brain Food', format_encabez_subtitulo)

    # === Agregar guía en la hoja General ===
    guia = [
        "Guía para interpretar el Informe EDA:",
        "",
        "Este informe ha sido generado como parte del análisis exploratorio de datos (EDA).",
        "El objetivo es evaluar la calidad, consistencia y estructura de las tablas analizadas.",
        "",
        "Estructura del informe:",
        "- **Hojas individuales por tabla**: Cada tabla analizada tiene su propia hoja en el Excel.",
        "  Estas hojas detallan métricas específicas para cada tipo de dato.",
        "",
        "Subdivisión de los datos en las hojas individuales:",
        "1. **Datos de Texto**: Columnas categorizadas como texto o string. Estas columnas se analizan ",
        "   en términos de ejemplos, valores únicos, duplicados, unicidad y completitud.",
        "2. **Datos Numéricos**: Columnas con valores numéricos. Se incluyen métricas estadísticas como ",
        "   promedio, desviación estándar, valores mínimos y máximos, así como distribución.",
        "3. **Datos de Fechas**: Columnas de tipo fecha o datetime. Este análisis incluye rangos, valores ",
        "   únicos, duplicados y distribuciones temporales.",
        "4. **Otros Datos**: Columnas que no encajan en las categorías anteriores. Estas columnas se ",
        "   analizan según su tipo específico, evaluando valores únicos y unicidad.",
        "",
        "Columnas clave en las hojas de análisis:",
        "- **TableName**: Nombre de la tabla analizada.",
        "- **SizeKB**: Tamaño aproximado de la tabla en kilobytes.",
        "- **RecordCount**: Número total de registros (filas) en la tabla.",
        "- **ColumnCount**: Número de columnas en la tabla.",
        "- **Empty_Columns**: Número de columnas completamente vacías.",
        "- **Unicidad (%)**: Porcentaje de valores no nulos en la tabla.",
        "- **Completitud (%)**: Evaluación del porcentaje de valores consistentes y únicos.",
        "",
        "Sugerencias para usar este informe:",
        "- Use los detalles de unicidad y completitud para identificar columnas problemáticas.",
        "- Las métricas estadísticas ayudan a detectar valores atípicos o anomalías en los datos.",
        "- Analice los ejemplos y distribuciones para entender mejor la naturaleza de los datos.",
        "",
        "Nota: Este informe es una herramienta fundamental para preparar sus datos antes de realizar ",
        "análisis más avanzados o construir modelos de machine learning."
    ]

    # Escribir la guía en el Excel
    for i, linea in enumerate(guia):
        worksheet1.write(ENCABEZ + 3 + i, SALTO_LADO, linea, format_num_with_thousands)



def write_to_excel(df, table_name, writer, book, ENCABEZ, format_encabez_titulo, format_encabez_columnas, format_encabez_columnas2, format_celda_datos, format_titulo_tabla, format_roboto_bordered, format_num_with_thousands,ANCHO_COL, SALTO_LADO, format_columna_col, db_type=None, server=None, user=None, password=None, database=None, schema=None, engine=None, path_instaclient=None):
    """
    Genera un informe EDA de un DataFrame y lo exporta a un archivo Excel.

    Args:
        df (polars.DataFrame): DataFrame a procesar.
        table_name (str): Nombre de la tabla para la hoja en Excel.
        output (str): Ruta de salida para el archivo Excel.
    """
    

    
    # Generar análisis y validación
    eda_statistics_ = analyze_data(df)
    data_standardization_info, empty_columns_count, filled_0_percent_count, filled_4_percent_count, filled_20_percent_count, filled_70_percent_count = validate_data(df)
    
    if server != None:
        #engine = connect_to_database(db_type, server, user, password, database, path_instaclient)
        columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result = execute_sql_queries(engine, table_name, db_type, database, schema)
        #engine.dispose()
    else:
        columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result = calculate_csv_info(df)
    
    # Generar tabla de información
    table_info_gpt = generate_table_info(df, table_name, size_result, record_count_result, column_count_result, columns_info_result, eda_statistics_, data_standardization_info, primary_keys_result, empty_columns_count, foreign_keys_result, filled_0_percent_count, filled_4_percent_count, filled_20_percent_count, filled_70_percent_count)


    # Crear DataFrames categorizados por tipo de datos
    categorized_dfs = categorize_dataframes_by_type(df, table_info_gpt)

    # Escribir los DataFrames en hojas de Excel
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
                categorized_dfs,  
                table_name,
                table_info_gpt
            )

    