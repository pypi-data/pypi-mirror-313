import pandas as pd
import pyarrow
import sqlalchemy
import sqlite3
import sqlparse
from sqlalchemy import create_engine
from datetime import datetime

from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    OutputPortModuleParameter, ScriptModuleParameter, ModuleParameters
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.studio.core.error import UserError
from azureml.studio.internal.error import ErrorMapping, InvalidSQLScriptError, InvalidDatasetError
from azureml.studio.core.utils.missing_value_utils import drop_na
from azureml.studio.core.logger import TimeProfile


SQLITE_MAX_COLUMN = 1000
MAX_COLUMN_MSG = 'too many'
# SQLite stores date-time in text type with the format of "YYYY-MM-DD HH:MM:SS.SSS".
# Refer to https://www.sqlite.org/datatype3.html.
ISO_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
NUMBER_TO_CHECK_FORMAT = 100


def check_column_names_ignore_case_sensitive(data: pd.DataFrame):
    """
    DataFrame.to_sql() is case insensitive for column names. So we need to check if there are duplicate column names
    before calling DataFrame.to_sql() method. Example: column a and column A are considered as duplicate columns.
    """
    orig_columns = data.columns
    dict_word_lower = {v: v.lower() for v in orig_columns}

    # group column name by ignoring case sensitive
    groups_words = {}
    for key, value in dict_word_lower.items():
        my_list = []
        if value in groups_words.keys():
            my_list = groups_words[value]
        my_list.append(key)
        groups_words[value] = my_list

    error_msg = ''
    for col_names in groups_words.values():
        if len(col_names) > 1:
            error_msg += str(col_names) + ', '
    if len(error_msg) > 0:
        hint_message = 'Failed when create table using SQLite. Input DataFrame has duplicate column names:'
        ErrorMapping.throw(UserError(hint_message + error_msg))
    return True


class ApplySqlTransModule(ModuleBase):
    def __init__(self):
        meta_data = ModuleMetaData(
            id="90381e80-67c3-4d99-8754-1db785b7ea37",
            name="Apply SQL Transformation",
            category="Data Transformation",
            description="Runs a SQLite query on input datasets to transform the data.")
        parameters = ModuleParameters(
            [
                InputPortModuleParameter(
                    name="t1",
                    friendly_name="t1",
                    is_optional=False),
                InputPortModuleParameter(
                    name="t2",
                    friendly_name="t2",
                    is_optional=True),
                InputPortModuleParameter(
                    name="t3",
                    friendly_name="t3",
                    is_optional=True),
                OutputPortModuleParameter(
                    name="dataset",
                    friendly_name="Result_dataset",
                    is_optional=False),
                ScriptModuleParameter(
                    name="sqlquery",
                    friendly_name="SQL query script",
                    is_optional=False,
                    default_value="select * from t1",
                    language="Sql")])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["t1"]),
            ModuleSpecNode.from_module_parameter(parameters["t2"], is_optional=True),
            ModuleSpecNode.from_module_parameter(parameters["t3"], is_optional=True),
            ModuleSpecNode.from_module_parameter(parameters["dataset"]),
            ModuleSpecNode.from_module_parameter(parameters["sqlquery"]),
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/apply_sql_trans_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        logger.info("Construct SQLite Server")
        engine = create_engine('sqlite://', echo=False)
        conn = engine.connect()

        # Fix bug 836347: validate the sql query before processing the entire dataset by insert empty input first
        self._transform_df_to_sql(engine, True)
        logger.info('Read SQL script query')
        sql_query = self.parameters["sqlquery"].value
        try:
            if sql_query:
                logger.info('Validate SQL script query')
                sql_query = sql_query.strip()
                sql_querys = [s.strip() for s in sqlparse.split(sql_query) if self._is_valid_sql_statement(s)]
                if len(sql_querys) > 1:
                    for query in sql_querys[:-1]:
                        conn.execute(query)
                    sql_query = sql_querys[-1]

            _ = pd.read_sql_query(sql_query, con=engine)
        except sqlalchemy.exc.ResourceClosedError as noselectex:
            ErrorMapping.rethrow(noselectex, UserError(str(noselectex)))
        except sqlalchemy.exc.SQLAlchemyError as sqlalchemyex:
            ErrorMapping.rethrow(
                sqlalchemyex, InvalidSQLScriptError(
                    sql_query, sqlalchemyex))
        except (sqlite3.Warning, sqlite3.Error) as ex:
            ErrorMapping.rethrow(
                ex, InvalidSQLScriptError(
                    sql_query, ex))

        except ValueError as ex:
            if "query contains a null character" in str(ex):
                ErrorMapping.rethrow(
                    ex, InvalidSQLScriptError(
                        sql_query, ex))
        except Exception as err:
            raise err
        finally:
            conn.close()

        # runs the valid sql query on input datasets to transform the data
        engine = create_engine('sqlite://', echo=False)
        conn = engine.connect()
        logger.info('Insert data to SQLite Server')
        self._transform_df_to_sql(engine)
        try:
            if sql_query:
                if len(sql_querys) > 1:
                    for query in sql_querys[:-1]:
                        conn.execute(query)
                    sql_query = sql_querys[-1]

            output = None
            logger.info('Generate SQL query result from SQLite Server')
            output = pd.read_sql_query(sql_query, con=engine)
        except (sqlalchemy.exc.SQLAlchemyError, sqlite3.Error) as noselectex:
            ErrorMapping.rethrow(noselectex, UserError(str(noselectex)))
        except Exception as err:
            raise err
        finally:
            conn.close()

        output = self.handle_output_same_column_name(output)
        with TimeProfile(f"Convert to date time"):
            output = self.handle_output_datetime_column(output)
        try:
            self._handle_output("dataset", output)
        except pyarrow.lib.ArrowNotImplementedError as output_ex:
            error_message = 'Output Dataset has data types not supported by pyarrow. ' + str(output_ex)
            ErrorMapping.rethrow(UserError(error_message))

    def handle_output_datetime_column(self, data: pd.DataFrame):
        for column_index in range(len(data.columns)):
            if _is_datetime_column(data.iloc[:, column_index]):
                try:
                    data.iloc[:, column_index] = pd.to_datetime(
                        data.iloc[:, column_index],
                        format=ISO_DATETIME_FORMAT,
                        errors="ignore")
                except Exception:
                    pass
        return data

    def handle_output_same_column_name(self, data: pd.DataFrame):
        new_column_names = []
        exist_column_name = {}
        for column_index in range(len(data.columns)):
            column = data.iloc[:, column_index]
            column_name = column.name
            if column_name in exist_column_name:
                new_name = column_name

                while new_name in data.columns:
                    exist_column_name[column_name] = exist_column_name[column_name] + 1
                    new_name = f'{column_name} ({exist_column_name[column_name]})'

                new_column_names.append(new_name)
            else:
                exist_column_name[column_name] = 1
                new_column_names.append(column_name)
        data.columns = new_column_names
        return data

    def _is_valid_sql_statement(self, statement: str):
        if not statement or not statement.strip():
            return False
        import sqlparse
        for token in sqlparse.parse(statement)[0].flatten():
            if "Token.Comment" not in str(token.ttype) and "Token.Text.Whitespace" not in str(token.ttype):
                return True
        return False

    def _transform_df_to_sql(self, engine, validate_sql=False):
        input_parameter_list = ['t1', 't2', 't3']
        for input_parameter in input_parameter_list:
            t = self._get_empty_input(input_parameter) if validate_sql else self._get_input(input_parameter)
            if t is not None:
                if len(t.columns) == 0:
                    ErrorMapping.throw(UserError(f'{input_parameter} is empty dataframe.'))
                hint_message = f"Insert {input_parameter} with only column names" if validate_sql else \
                               f"Insert {input_parameter}"
                logger.info(hint_message)
                try:
                    if check_column_names_ignore_case_sensitive(t):
                        t.to_sql(input_parameter, con=engine, index=False)
                except sqlalchemy.exc.OperationalError as sqlalchemyex:
                    if len(sqlalchemyex.args) > 0 and MAX_COLUMN_MSG in sqlalchemyex.args[0]:
                        err_message = f"Number of columns in the dataset " \
                                      f"in {input_parameter} exceeds allowed maximum of {SQLITE_MAX_COLUMN}."
                        ErrorMapping.rethrow(sqlalchemyex, UserError(err_message))
                    else:
                        raise
                except MemoryError as memerr:
                    hint_message = 'Out of memory, please try upgrade compute. ' + str(memerr)
                    ErrorMapping.rethrow(memerr, UserError(hint_message))

                except ValueError as ex:
                    if "query contains a null character" in str(ex):
                        ErrorMapping.rethrow(ex, InvalidDatasetError(reason="Column name in input datasets contains"
                                                                            " a null character."))

    def _get_empty_input(self, name: str) -> pd.DataFrame:
        # retrieve empty input data which only contain the dataframe's column names to validate sql scripts
        param = self.parameters[name]
        if isinstance(param, InputPortModuleParameter):
            if param.data is not None:
                return param.data.data.iloc[0:0].copy()
        return None


def _is_datetime_iso_pattern(date_str: str) -> bool:
    """Checks if a string follows the date-time format of %Y-%m-%d %H:%M:%S.%f"""
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str, ISO_DATETIME_FORMAT)
        return True
    except Exception:
        return False


def _is_datetime_column(series: pd.Series) -> bool:
    """Checks if a column should be converted to date-time type."""
    s = drop_na(series)
    if len(s) == 0:
        return False
    elif len(s) <= NUMBER_TO_CHECK_FORMAT:
        return all(_is_datetime_iso_pattern(i) for i in s)
    # For long columns (length>100), randomly select 100 values to check.
    return _is_datetime_column(s.sample(NUMBER_TO_CHECK_FORMAT))
