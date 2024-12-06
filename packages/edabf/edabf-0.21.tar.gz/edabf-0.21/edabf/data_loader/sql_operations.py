import pandas as pd
import polars as pl
import oracledb
from tqdm import tqdm
from sqlalchemy import create_engine
from ..utils.data_validation import es_uuid

def execute_query(cursor, query, table_name):
    query_data = query.replace("table_name", f"[{table_name}]")
    cursor.execute(query_data)
    return cursor.fetchall()


def validate_and_convert_uuids(chunk):
    """
    Valida las columnas del chunk, buscando columnas con UUIDs y las convierte a string si es necesario.
    """
    for col in chunk.columns:
        # Si la columna es de tipo objeto, verificamos si contiene UUIDs
        if chunk[col].dtype == 'object':
            non_null_values = chunk[col].dropna()
            if len(non_null_values) > 0 and es_uuid(non_null_values.iloc[0]):
                chunk[col] = chunk[col].astype(str)  # Convertir a string si contiene UUIDs
    return chunk



def read_sql_query_chunked(engine, query, chunk_size=1000):
    """
    Lee una tabla SQL en chunks, asegurando que todos los chunks tengan el mismo formato,
    y convierte automáticamente columnas incompatibles a string si es necesario.

    Args:
        engine: Motor SQLAlchemy.
        query: Consulta SQL.
        chunk_size: Tamaño del chunk a leer.

    Returns:
        Un DataFrame Polars concatenado a partir de todos los chunks.
    """
    # Inicializar una lista para almacenar los chunks procesados
    all_chunks = []
    column_types = None  # Esquema estándar basado en el primer chunk

    try:
        # Crear una conexión desde el motor
        with engine.connect() as connection:
            # Obtener el número total de filas (para configurar tqdm)
            total_rows_query = f"SELECT COUNT(*) FROM ({query})"
            total_rows = pd.read_sql(total_rows_query, connection).iloc[0, 0]
            
            # Leer la base de datos en chunks con tqdm
            with tqdm(total=total_rows, desc="Descargando datos", unit="fila") as pbar:
                for i, chunk in enumerate(pd.read_sql_query(query, connection, chunksize=chunk_size)):
                    # Si es el primer chunk, establece el esquema inicial
                    if column_types is None:
                        column_types = {col: "string" if chunk[col].dtype == "object" else chunk[col].dtype for col in chunk.columns}

                    # Normalizar los tipos de cada columna según el esquema inicial
                    for col in chunk.columns:
                        expected_type = column_types[col]
                        if pd.api.types.is_object_dtype(chunk[col]) or pd.api.types.is_string_dtype(chunk[col]):
                            # Convertir a string si el tipo esperado es string
                            chunk[col] = chunk[col].astype("string")
                        elif chunk[col].dtype != expected_type:
                            try:
                                # Intentar convertir al tipo esperado
                                chunk[col] = chunk[col].astype(expected_type)
                            except Exception:
                                # Si falla, convertir a string
                                chunk[col] = chunk[col].astype("string")
                                column_types[col] = "string"

                    # Asegurar que todas las columnas del esquema estén presentes en el chunk
                    for col in column_types.keys():
                        if col not in chunk.columns:
                            # Agregar la columna faltante como NaN con el tipo del esquema
                            chunk[col] = pd.NA
                            chunk[col] = chunk[col].astype(column_types[col])

                    # Convertir el chunk a Polars
                    chunk_polars = pl.from_pandas(chunk)

                    # Añadir el chunk procesado a la lista
                    all_chunks.append(chunk_polars)

                    # Actualizar la barra de progreso con el tamaño del chunk
                    pbar.update(len(chunk))
        
        # Concatenar todos los chunks en un solo DataFrame Polars
        df_polars = pl.concat(all_chunks, how="vertical")
        return df_polars

    except:# Exception as e:
        #print(f"Error durante la ejecución de la consulta: {e}")
        raise
        
        
        
def read_execute(cursor, query, table_name):
    # Cargar datos en un DataFrame de pandas
    try:
        query_data = query.replace("table_name",table_name)
        cursor.execute(query_data)
        columns_info_result = cursor.fetchall()
    except:
        query_data = query.replace("table_name",f"[{table_name}]")
        cursor.execute(query_data)
        columns_info_result = cursor.fetchall()
    return columns_info_result


def connect_to_database(db_type, server, user, password, database, path_instaclient=None, port=None):
    """
    Establece la conexión con la base de datos según el tipo (MySQL, PostgreSQL, SQL Server, Oracle).
    
    Args:
        db_type: El tipo de base de datos ('mysql', 'postgresql', 'sqlserver', 'oracle').
        server: Dirección del servidor de la base de datos.
        user: Usuario de la base de datos.
        password: Contraseña de la base de datos.
        database: Nombre de la base de datos.
        port: Puerto de conexión (opcional, depende del tipo de base de datos).
        
    Returns:
        conn: Conexión establecida con la base de datos.
    """

    # Definir el puerto predeterminado para cada tipo de base de datos si no se proporciona

    if db_type == "mysql" and port is None:
        port = 3306
    elif db_type == "postgresql" and port is None:
        port = 5432
    elif db_type == "sqlserver" and port is None:
        port = 1433
    elif db_type == "oracle" and port is None:
        port = 1521
    

    # Conexión para MySQL
    if db_type == "mysql":
        connection_string = f"mysql+pymysql://{user}:{password}@{server}:{port}/{database}"

    # Conexión para PostgreSQL
    elif db_type == "postgresql":
        connection_string = f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{database}"
    
    # Conexión para SQL Server
    elif db_type == "sqlserver":
        connection_string = f"mssql+pymssql://{user}:{password}@{server}:{port}/{database}"
    
    # Conexión para Oracle
    elif db_type == "oracle":
        connection_string = f"oracle+cx_oracle://{user}:{password}@{server}:{port}/?service_name={database}"
        oracledb.init_oracle_client(lib_dir=path_instaclient)

    
    else:
        raise ValueError("Tipo de base de datos no soportado. Utilice 'mysql', 'postgresql', 'sqlserver' o 'oracle'.")

    # Crear el motor de conexión SQLAlchemy
    engine = create_engine(connection_string)

    return engine


def load_data_from_sql(engine, query):
    df = read_sql_query_chunked(engine, query)
    return df


def validate_df(df):
    try:
        return list(set(df.iter_rows()))
    except:
        return []

def execute_sql_queries(engine, table_name, db_type, database=None, schema=None):
    """
    Ejecuta las consultas necesarias en la base de datos para obtener la información 
    sobre columnas, tamaño, conteo de registros, llaves primarias, etc.
    """
    queries = {}

    if db_type.split("_")[0] == "mysql":
        queries = {
            "query_columns_info": f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}'
                AND TABLE_SCHEMA = '{database}';
            """,
            "query_size": f"""
                SELECT TABLE_NAME AS TableName,
                    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024, 2) AS TotalSpaceKB
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = '{table_name}'
                AND TABLE_SCHEMA = '{database}';

            """,
            "query_column_count": f"""
                SELECT COUNT(*) AS ColumnCount
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                AND TABLE_SCHEMA = '{database}';


            """,
            "query_record_count": f"""
                SELECT COUNT(*) AS RecordCount
                FROM `{table_name}`;
            """,
            "query_primary_keys": f"""
                SELECT COLUMN_NAME AS PrimaryKeyColumn
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                AND TABLE_SCHEMA = '{database}'
                AND COLUMN_KEY = 'PRI';
            """,
            "query_foreign_keys": f"""
                SELECT k.COLUMN_NAME AS ParentColumn, 
                    k.REFERENCED_TABLE_NAME AS ReferencedTable, 
                    k.REFERENCED_COLUMN_NAME AS ReferencedColumn
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS k
                WHERE k.TABLE_NAME = '{table_name}'
                AND k.TABLE_SCHEMA = '{database}'
                AND k.REFERENCED_TABLE_NAME IS NOT NULL;

            """
        }

    elif db_type.split("_")[0] == "sqlserver":
        queries = {
            "query_columns_info": f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}';
            """,
            "query_size": f"""
                SELECT t.NAME AS TableName, SUM(a.total_pages) * 8 AS TotalSpaceKB
                FROM sys.tables t
                INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
                INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
                INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
                WHERE t.NAME = '{table_name}'
                GROUP BY t.NAME;
            """,
            "query_column_count": f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';",
            "query_record_count": f"SELECT COUNT(*) FROM [{table_name}];",
            "query_primary_keys": f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                AND TABLE_NAME = '{table_name}';
            """,
            "query_foreign_keys": f"""
                SELECT COL_NAME(fc.parent_object_id, fc.parent_column_id) AS ParentColumn, t.name AS ReferencedTable, COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS ReferencedColumn
                FROM sys.foreign_keys AS fk
                INNER JOIN sys.foreign_key_columns AS fc ON fk.object_id = fc.constraint_object_id
                INNER JOIN sys.tables AS t ON fk.referenced_object_id = t.object_id
                WHERE OBJECT_NAME(fc.parent_object_id) = '{table_name}';
            """
        }

    elif db_type.split("_")[0] == "postgresql":
        queries = {
            "query_columns_info": f"""
                SELECT column_name, data_type
                FROM information_schema.columns 
                WHERE table_name = '{table_name}';
            """,
            "query_size": f"""
                SELECT
                    pg_class.relname AS TableName,
                    pg_total_relation_size(pg_class.oid) AS TotalSpaceBytes
                FROM
                    pg_class
                JOIN
                    pg_namespace ON pg_namespace.oid = pg_class.relnamespace
                WHERE
                    pg_class.relname = '{table_name}';
            """,
            "query_column_count": f"""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """,
            "query_record_count": f"""
                SELECT COUNT(*)
                FROM {table_name};
            """,
            "query_primary_keys": f"""
                SELECT a.attname AS column_name
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = '{table_name}'::regclass AND i.indisprimary;
            """,
            "query_foreign_keys": f"""
                SELECT
                    kcu.column_name AS ParentColumn,
                    ccu.table_name AS ReferencedTable,
                    ccu.column_name AS ReferencedColumn
                FROM
                    information_schema.table_constraints AS tc
                JOIN
                    information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
                JOIN
                    information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
                WHERE
                    tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = '{table_name}';
            """
        }


    elif db_type.split("_")[0] == "oracle":
        queries = {
            # Información de columnas y tipos de datos
            "query_columns_info": f"""
                SELECT column_name, data_type
                FROM ALL_TAB_COLUMNS
                WHERE table_name = '{table_name.upper()}' AND owner = '{schema.upper()}'
            """,

            # Tamaño de la tabla en bytes ###NO FUNCIONA
            "query_size": f"""
                SELECT 
                    table_name,
                    blocks * 8192 / 1024 AS TotalSpaceBytes
                FROM all_tables
                WHERE table_name = '{table_name.upper()}'
            """,

            # Conteo de columnas
            "query_column_count": f"""
                SELECT COUNT(*)
                FROM all_tab_columns
                WHERE table_name = '{table_name.upper()}' AND owner = '{schema.upper()}'
            """,

            # Conteo de registros (filas) en la tabla
            "query_record_count": f"""
                SELECT COUNT(*) AS RecordCount
                FROM {schema}.{table_name}
            """,

            # Llaves primarias
            "query_primary_keys": f"""
                SELECT cols.column_name
                FROM all_cons_columns cols
                JOIN all_constraints cons ON cols.constraint_name = cons.constraint_name
                WHERE cons.constraint_type = 'P'
                AND cons.table_name = '{table_name.upper()}'
                AND cons.owner = '{schema.upper()}'
            """,

            # Llaves foráneas
            "query_foreign_keys": f"""
                SELECT a.column_name AS ParentColumn,
                    c_pk.table_name AS ReferencedTable,
                    b.column_name AS ReferencedColumn
                FROM all_constraints c
                JOIN all_cons_columns a ON c.constraint_name = a.constraint_name
                JOIN all_cons_columns b ON c.r_constraint_name = b.constraint_name
                JOIN all_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
                WHERE c.constraint_type = 'R'
                AND c.table_name = '{table_name.upper()}'
                AND c.owner = '{schema.upper()}'
            """
        }
    
    
    # Ejecutar las consultas y obtener los resultados
    print("Extrayendo información de columnas y tipos de datos")
    columns_info_result = validate_df(read_sql_query_chunked(engine, queries["query_columns_info"]))
    columns_info_result = [(item[0].lower(), item[1].lower()) if item else [] for item in columns_info_result]
    print("Extrayendo tamaño de la tabla en bytes")
    size_result = validate_df(read_sql_query_chunked(engine, queries["query_size"]))
    print("Extrayendo conteo de filas en la tabla")
    record_count_result =  validate_df(read_sql_query_chunked(engine, queries["query_record_count"]))
    print("Extrayendo llaves primarias")
    primary_keys_result = validate_df(read_sql_query_chunked(engine, queries["query_primary_keys"]))
    primary_keys_result = [(item[0].lower(),) if item else [] for item in primary_keys_result]
    print("Extrayendo conteo de columnas")
    column_count_result =  validate_df(read_sql_query_chunked(engine, queries["query_column_count"]))
    print("Extrayendo llaves foraneas")
    foreign_keys_result = validate_df(read_sql_query_chunked(engine, queries["query_foreign_keys"]))
    foreign_keys_result = [(item[0].lower(), item[1].lower()) if item else [] for item in foreign_keys_result]

    return columns_info_result, size_result, record_count_result, primary_keys_result, column_count_result, foreign_keys_result



# Función para obtener la consulta de tabla adecuada según el tipo de base de datos
def get_table_query(db_type, schema):
    db_type_prefix = db_type.split("_")[0]

    if db_type_prefix in {"mysql", "postgresql", "sqlserver"}:
        return f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';"
    elif db_type_prefix == "oracle":
        return f"SELECT table_name FROM all_tables WHERE owner = '{schema.upper()}'"
    else:
        raise ValueError("Tipo de base de datos no soportado")
