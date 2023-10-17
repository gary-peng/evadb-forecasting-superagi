from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import Type, List
from evadb_forecasting_tool import EvaDBForecastingTool


class EvaDBForecastingToolkit(BaseToolkit, ABC):
    name: str = "EvaDB Forecasting Toolkit"
    description: str = "EvaDB Forecasting Tool kit contains all tools related to EvaDB Forecasting"

    def get_tools(self) -> List[BaseTool]:
        return [EvaDBForecastingTool()]
    
    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            # Add more config keys specific to your project
        ]