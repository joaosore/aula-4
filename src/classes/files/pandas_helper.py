import pandas as pd
import yaml


class PandasHelper():

    def __init__(self):
        pass

    @staticmethod
    def concat_df(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
        """Concatena dois dataframes

        Args:
            df_1 (pd.DataFrame): primeiro dataframe a ser concatenado
            df_2 (pd.DataFrame): segundo dataframe a ser concatenado

        Returns:
            pd.DataFrame: dataframe completo
        """
        df_main = pd.concat([df_1, df_2])

        return df_main

    @staticmethod
    def save_df(df: pd.DataFrame, file_type: str, file_name_saved: str) -> None: # noqa
        """Salva o DataFrame no formato solicitado.

        Args:
            df (pd.DataFrame): recebe o DataFrame que será salvo.
            file_type (str): recebe o tipo de formato de arquivo que a
            pessoa deseja escolher para salvar o DataFrame
            file_name_saved (str): recebe o nome que ficará o nome do arquivo
        """
        file_type = file_type.lower()
        if (file_type == 'json'):
            df = df.to_json(orient="split")
            file = open(f"resultados/{file_name_saved}.{file_type}",
                        "w+", newline="",
                        encoding="utf-8"
                        )
            file.write(df)
            file.close()
            print(f'Arquivo salvo: resultados/{file_name_saved}.{file_type}')

        elif (file_type == 'csv'):
            df = df.to_csv()
            file = open(f"resultados/{file_name_saved}.{file_type}",
                        "w+", newline="",
                        encoding="utf-8"
                        )
            file.write(df)
            file.close()
            print(f'Arquivo salvo: resultados/{file_name_saved}.{file_type}')

        elif (file_type == 'yaml'):
            df = yaml.dump(
                df.reset_index().to_dict(orient='records'),
                sort_keys=False, width=72, indent=4,
                default_flow_style=None
            )
            file = open(f"resultados/{file_name_saved}.{file_type}",
                        "w+", newline="",
                        encoding="utf-8"
                        )
            file.write(df)
            file.close()
            print(f'Arquivo salvo: resultados/{file_name_saved}.{file_type}')

        elif (file_type == 'xml'):
            df = df.to_xml(root_name="result", row_name="paper")
            file = open(f"resultados/{file_name_saved}.{file_type}",
                        "w+", newline="",
                        encoding="utf-8"
                        )
            file.write(df)
            file.close()
            print(f'Arquivo salvo: resultados/{file_name_saved}.{file_type}')

        else:
            print('Opção não suportada! As opções suportadas são: CSV, XML, Json, YAML') # noqa

    @staticmethod
    def merge_dataframes(df_1: pd.DataFrame, df_2: pd.DataFrame, column_to_merge: str) -> pd.DataFrame: # noqa
        """Faz o merge de dois DataFrames pela coluna selecionada.

        Args:
            df_1 (pd.DataFrame): Primeiro DataFrame que será feito mergeado
            df_2 (pd.DataFrame): Segundo DataFrame que será feito mergeado
            column_to_merge (str): Coluna que será o filtro para
            realizar o merge

        Returns:
            pd.DataFrame: merge entre os DataFrames.
        """
        df_merged = pd.merge(df_1, df_2, on=column_to_merge)

        return df_merged

    @staticmethod
    def remove_duplicate(df: pd.DataFrame) -> pd.DataFrame:
        """Remove as duplicatas do DataFrame selecionado

        Args:
            df (pd.DataFrame): DataFrame selecionado

        Returns:
            pd.DataFrame: DataFrame sem as duplicações
        """
        df = df.drop_duplicates()

        return df

    @staticmethod
    def filter_column(df: pd.DataFrame, column_filter: dict) -> pd.DataFrame:
        """Realiza o filtro no DataFrame baseado no dict de coluna
        e valor que a pessoa deseja ver

        Args:
            df (pd.DataFrame): DataFrame que será feito o filtro.
            column_filter (dict): Dict de nome de coluna e o
            dado que será filtrado.

        Returns:
            pd.DataFrame: DataFrame apenas com os valores filtrados.
        """
        df_response = pd.DataFrame()

        for column in column_filter:
            if column['filter'] is not None:
                for filter in column['filter']:
                    if df[column['column']].dtypes == 'int64' or df[column['column']].dtypes == 'float64': # noqa
                        df_filter = df.query(
                            f"{column['column']} == {filter}"
                            )
                        df_response = pd.concat([df_response, df_filter])

                    else:
                        df_filter = df[df[column['column']].str.contains(filter, regex=True) == True] # noqa
                        df_response = pd.concat([df_response, df_filter])

        df_response = df_response.drop_duplicates()

        return df_response