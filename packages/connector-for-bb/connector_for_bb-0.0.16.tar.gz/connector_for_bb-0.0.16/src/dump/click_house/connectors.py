import clickhouse_connect
from pandas import DataFrame as PandasDataFrame

from dump.config_utils import load_config


class ConnectorCH:
    def __init__(
        self,
        db_config_name: str = "click_house",
    ) -> None:
        self.db_config_name = db_config_name
        self.__config = load_config(section=self.db_config_name)

        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                self._client = clickhouse_connect.get_client(**self.__config)
                # print("Connected to the ClickHouse server.")
            except Exception as error:
                print(error)
        return self._client


class TableCH(ConnectorCH):
    def __init__(self, db_config_name: str = "click_house") -> None:
        super().__init__(db_config_name)

    def get_df(self, query: str) -> PandasDataFrame:
        return self.client.query_df(query)
