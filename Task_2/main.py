from datetime import date, timedelta, datetime
from urllib import error

from core.database import initial_db
from utils import utils


def main():
    initial_db()
    date_start = date(2023, 1, 1)
    date_end = date.today()
    delta = date_end - date_start
    for i in range(delta.days + 1):
        current_date = date_start + timedelta(days=i)
        date_str = current_date.strftime("%Y%m%d")
        try:
            file = utils.FileDownloader(
                f"https://spimex.com/upload/reports/oil_xls/oil_xls_{date_str}"
                f"162000.xls?r=9455"
            )
            data = utils.FileParser()
            data.insert_to_db()
            file.delete_file()
            print(f"Data save in database for {current_date}")
        except error.HTTPError:
            pass


if __name__ == "__main__":
    start = datetime.now()
    main()
    print(f"Время загрузки данных - {datetime.now() - start}")
