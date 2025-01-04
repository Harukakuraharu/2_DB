import os
import urllib.request
from typing import Any

import pandas as pd

from core.database import Session
from crud import crud


class FileDownloader:
    """Class for work with file - download and delete"""

    def __init__(self, url) -> None:
        self.url: str = url
        self.file_name: str = "example.xls"
        self.download_file()

    def download_file(self) -> tuple[str, Any]:
        return urllib.request.urlretrieve(self.url, self.file_name)

    def delete_file(self) -> None:
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


class FileParser:
    def __init__(self, file_name="example.xls") -> None:
        self.session = Session
        self.data: pd.DataFrame = pd.read_excel(file_name)

    def update_table(self):
        date_data = self.data["Форма СЭТ-БТ"].iloc[2].split(": ")
        self.data.columns = list(range(15))
        self.data = self.data[[1, 2, 3, 4, 5, 14]][
            self.data[14] != "-"
        ].dropna()
        self.data.drop(5, inplace=True)
        return date_data[-1]

    def make_data_list(self, date_data: str) -> list:
        data_list = []
        for _, row in self.data.iterrows():
            data_list.append(
                {
                    "exchange_product_id": row[1],
                    "exchange_product_name": row[2],
                    "oil_id": row[1][:4],
                    "delivery_basis_id": row[1][4:7],
                    "delivery_basis_name": row[3],
                    "delivery_type_id": row[1][-1],
                    "volume": row[4],
                    "total": row[5],
                    "count": row[14],
                    "date": date_data,
                }
            )
        return data_list

    def insert_to_db(self) -> None:
        with self.session() as session:
            date = self.update_table()
            data = self.make_data_list(date)
            crud.BaseCrud(session).create_item(data)
            session.commit()
