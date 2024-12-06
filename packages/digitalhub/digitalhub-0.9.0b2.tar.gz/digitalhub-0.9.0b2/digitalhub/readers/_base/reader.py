from __future__ import annotations

from abc import abstractmethod
from typing import Any


class DataframeReader:
    """
    Dataframe reader abstract class.
    """

    ##############################
    # Read methods
    ##############################

    @staticmethod
    @abstractmethod
    def read_df(path: str | list[str], extension: str, **kwargs) -> Any:
        """
        Read DataFrame from path.
        """

    ##############################
    # Write methods
    ##############################

    @abstractmethod
    def write_df(self, df: Any, dst: Any, extension: str | None = None, **kwargs) -> None:
        """
        Method to write a dataframe to a file.
        """

    @staticmethod
    @abstractmethod
    def write_csv(df: Any, *args, **kwargs) -> str:
        """
        Write DataFrame as csv.
        """

    @staticmethod
    @abstractmethod
    def write_parquet(df: Any, *args, **kwargs) -> str:
        """
        Write DataFrame as parquet.
        """

    @staticmethod
    @abstractmethod
    def write_table(df: Any, *args, **kwargs) -> str:
        """
        Write DataFrame as table.
        """

    ##############################
    # Utils
    ##############################

    @staticmethod
    @abstractmethod
    def get_schema(df: Any) -> Any:
        """
        Get schema.
        """

    @staticmethod
    @abstractmethod
    def get_preview(df: Any) -> Any:
        """
        Get preview.
        """
