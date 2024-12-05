import os
from typing import Dict
import pandas as pd


def gen_empty_table(schema: Dict[str, str],
                    output_path: str = None) -> pd.DataFrame:
    df = pd.DataFrame({s[0]: pd.Series([], dtype=s[1])
                       for s in schema.items()})
    if output_path is not None:
        df.to_parquet(output_path)
    return df


def convert_csv(
        input_path: str,
        header: int = 0,
        output_path: str = None) -> pd.DataFrame:
    if input_path.startswith('./'):
        input_path = os.path.join(os.getcwd(), input_path)
    df = pd.read_csv(input_path, header=header, index_col=None)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if output_path is not None:
        df.to_parquet(output_path)
    return df


# data = gen_empty_table({'col1': 'int'},output_path='D:\\Temp\\empty.parquet')
# print(data)
if __name__ == "__main__":
    data = convert_csv(
        input_path='D:\\Git\\AzureML\\ModuleX\\azureml\\custommodules\\testdata\\data.csv',
        output_path='D:\\Git\\AzureML\\ModuleX\\azureml\\custommodules\\testdata\\data.parquet')
