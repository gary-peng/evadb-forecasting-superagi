from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type

import sqlite3
import pandas
import evadb

class EvaDBForecastingInput(BaseModel):
    csv_file_path: str = Field(..., description="The path to the CSV file containing the dataset")
    time_col_name: str = Field(..., description="The name of the CSV column that contains the datestamp")
    forecasted_col_name: str = Field(..., description="The name of the CSV column we wish to forecast")
    horizon: str = Field(..., description="The number of steps we want to forecast in the future")


class EvaDBForecastingTool(BaseTool):
    """
    EvaDB Forecasting Tool
    """
    name: str = "EvaDB Forecasting Tool"
    args_schema: Type[BaseModel] = EvaDBForecastingInput
    description: str = "Forecast a time series dataset"

    def _execute(self, csv_file_path: str, time_col_name: str, forecasted_col_name: str, horizon: str):
        conn = sqlite3.connect('sqlite.db')
        df = pandas.read_csv(csv_file_path)
        df.to_sql('data', conn, if_exists='replace')

        cursor = evadb.connect().cursor()

        params = {
            "database": "sqlite.db",
        }
        query = f"CREATE DATABASE IF NOT EXISTS sqlite WITH ENGINE = 'sqlite', PARAMETERS = {params};"
        cursor.query(query).df()

        cursor.query(f"""
        CREATE OR REPLACE FUNCTION Forecast FROM
            (
            SELECT {time_col_name}, {forecasted_col_name}
            FROM sqlite.data
            )
        TYPE Forecasting
        PREDICT '{forecasted_col_name}'
        TIME '{time_col_name}'
        FREQUENCY 'D'
        """).df()

        prediction = cursor.query(f"SELECT Forecast({horizon});").df()
        conn.close()
        return prediction.to_string()
