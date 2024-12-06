import polars as pl


class EDALoader:
    def __init__(self, dataframes_dict, glob=True):
        self.dfs = dataframes_dict
        # self.dfs_valid = {key: df for key, df in self.dfs.items() if df.height > 1}
        # self.__dict__.update(self.dfs)
        # if glob:
        #     globals().update(self.dfs)
        # self.identifiers = {key: [df.columns[0]] for key, df in self.dfs_valid.items()}

        # self.table_stats = {}
        # self.fill_data_table()

    def fill_data_table(self):
        self.data_table = pl.DataFrame({
            "Name": list(self.dfs.keys()),
            "Total Rows": [df.height for df in self.dfs.values()],
            "Total Columns": [df.width for df in self.dfs.values()],
            "Empty Columns": [df.width - df.drop_nulls().width for df in self.dfs.values()],
            "Columns Filled 4%": [(df.null_count().sum() <= (1 - 0.04) * df.height).sum() for df in self.dfs.values()],
            "Columns Filled 20%": [(df.null_count().sum() <= (1 - 0.20) * df.height).sum() for df in self.dfs.values()],
            "Columns Filled 70%": [(df.null_count().sum() <= (1 - 0.70) * df.height).sum() for df in self.dfs.values()],
            "Duplicated IDs": [df.select(pl.col(self.identifiers[key])).unique(keep="none").height for key, df in self.dfs.items()],
            
            # Convertir todas las columnas a strings, aplanando listas y asegurando que todo esté en formato compatible
            "Duplicated Data": [
                df.with_columns([
                    # Si la columna es de tipo lista, convertimos la lista a una cadena unida por comas
                    pl.col(col).arr.join(", ").alias(col) if isinstance(df.schema[col], pl.List)
                    else pl.col(col).cast(pl.Utf8).alias(col)  # Convertir a cadena para otros tipos
                    for col in df.columns
                ])
                .select([pl.col(col) for col in df.columns if col not in self.identifiers[key]])  # Seleccionar las columnas que no son IDs
                .unique(keep="none")  # Remover duplicados
                .height
                for key, df in self.dfs.items()
            ],
        })
        
        # Actualizar el índice (aunque en Polars no es necesario en la mayoría de los casos)
        self.data_table = self.data_table.with_columns(pl.col("Name").alias("index"))
        
        # Filtrar para mantener solo las tablas con filas
        self.data_table_valid = self.data_table.filter(pl.col("Total Rows") > 0)

    def update_identifiers(self, new_identifiers):
        for key in new_identifiers:
            self.identifiers[key] = list(set(self.identifiers[key] + new_identifiers[key]))
            

    def get_table_stats(self, df):

        def get_unique_examples(df, col):
            """
            Obtiene hasta 3 ejemplos únicos de una columna en un solo paso.
            """
            # Obtener los primeros 3 valores únicos no nulos de la columna
            unique_examples = (
                df.select(pl.col(col).drop_nulls().unique().limit(3))
                .to_series()
                .to_list()
            )

            # Convertir los valores únicos a una cadena separada por comas
            return ", ".join(map(str, unique_examples))


        def get_examples_random_with_retries(df):
            """
            Obtiene ejemplos únicos de cada columna del DataFrame de manera eficiente.
            """
            return [get_unique_examples(df, col) for col in df.columns]

        # Paso 1: Calcular los valores nulos y no nulos en cada columna
        missing_values = df.select([pl.col(col).null_count().alias(f"{col}_missing") for col in df.columns]).to_dict()
        non_nulls = {col: df.height - missing_values[f"{col}_missing"][0] for col in df.columns}

        # Paso 2: Seleccionar columnas numéricas
        numeric_columns = [col for col in df.columns if df.schema[col] in [pl.Float64, pl.Int64, pl.Int32, pl.Float32]]
    
        # Paso 3: Calcular ceros, valores únicos, y duplicados en un solo paso
        zero_and_unique_stats = df.select(
            [
                pl.col(col).filter(pl.col(col) == 0).count().alias(f"{col}_zeros") if col in numeric_columns else pl.lit(None).alias(f"{col}_zeros")
                for col in df.columns
            ] + [
                pl.col(col).n_unique().alias(f"{col}_unique") for col in df.columns
            ]
        ).to_dict()

        # Calcular duplicados como la diferencia entre el total de filas y los valores únicos por columna
        duplicates = {col: df.height - zero_and_unique_stats[f"{col}_unique"][0] for col in df.columns}

        # Paso 4: Crear el DataFrame de estadísticas básicas
        stats_df = pl.DataFrame({
            "Column": df.columns,
            "NotNulls": [non_nulls[col] for col in df.columns],
            "Missing": [missing_values[f"{col}_missing"][0] for col in df.columns],
            "Zeros": [zero_and_unique_stats.get(f"{col}_zeros", [None])[0] for col in df.columns],
            "Unique": [zero_and_unique_stats[f"{col}_unique"][0] for col in df.columns],
            "Count": [df.height] * len(df.columns),
            "Duplicates": [duplicates[col] for col in df.columns]
        })

        # Paso 5: Calcular estadísticas adicionales para columnas numéricas
        if numeric_columns:
            additional_stats = df.select(
                # Asegurar que col esté definido en cada expresión
                [
                    pl.col(col).var().alias(f"{col}_variance") if col in numeric_columns else pl.lit(None).alias(f"{col}_variance")
                    for col in df.columns
                ] + [
                    pl.col(col).std().alias(f"{col}_stddev") if col in numeric_columns else pl.lit(None).alias(f"{col}_stddev")
                    for col in df.columns
                ] + [
                    pl.col(col).skew().alias(f"{col}_skew") if col in numeric_columns else pl.lit(None).alias(f"{col}_skew")
                    for col in df.columns
                ] + [
                    pl.col(col).kurtosis().alias(f"{col}_kurtosis") if col in numeric_columns else pl.lit(None).alias(f"{col}_kurtosis")
                    for col in df.columns
                ]
            ).to_dict()

            # Agregar al DataFrame de estadísticas
            stats_df = stats_df.with_columns([
                pl.Series("Variance", [additional_stats.get(f"{col}_variance", [None])[0] for col in df.columns]),
                pl.Series("StdDev", [additional_stats.get(f"{col}_stddev", [None])[0] for col in df.columns]),
                pl.Series("Skewness", [additional_stats.get(f"{col}_skew", [None])[0] for col in df.columns]),
                pl.Series("Kurtosis", [additional_stats.get(f"{col}_kurtosis", [None])[0] for col in df.columns])
            ])

        # Paso 6: Calcular los ejemplos únicos
        examples_list = get_examples_random_with_retries(df)

        stats_df = stats_df.with_columns([
            pl.Series("Examples", examples_list)
        ])


        null_warning_list = [(missing_values[f"{col}_missing"][0] / df.height > 0.8) for col in df.columns]

        stats_df = stats_df.with_columns([
            pl.Series("NullWarning", null_warning_list)
        ])

        return stats_df


    def get_all_tables_stats(self):
        for name in self.dfs:
            self.table_stats[name] = self.get_table_stats(self.dfs[name])
