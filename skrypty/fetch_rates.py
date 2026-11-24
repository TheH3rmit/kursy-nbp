
import csv
import json

from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from io import StringIO
from datetime import date
from decimal import Decimal


API_URL = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"
CURRENCIES = ("EUR", "USD", "GBP")
DATA_PATH = Path(__file__).resolve().parents[1] / "dane"


def main():
    # Getting data from the NBP API
    try:
        with urlopen(API_URL, timeout=15) as response:
            table = json.load(response)[0]

    except HTTPError as error:
        if error.code == 404:
            print("Brak tabeli")
            return
        raise

    # Read and validate
    dzien = table["effectiveDate"]
    date.fromisoformat(dzien)

    rates = {
        rate["code"]: rate["mid"]
        for rate in table["rates"]
    }

    prepared = {}

    for currency in CURRENCIES:

        if currency not in rates:
            raise ValueError(f"Brak kursu: {currency}")

        value = Decimal(str(rates[currency]))

        if not value.is_finite() or value <= 0:
            raise ValueError(f"Niepoprawny kurs: {value}")

        file = DATA_PATH / f"{currency.lower()}.csv"
        history = {}

        # Read existing rates
        if file.exists():
            with file.open(
                "r", encoding="utf-8", newline=""
            ) as f:
                for row in csv.reader(f):
                    if len(row) != 2:
                        raise ValueError(
                            f"Niepoprawny wiersz: {file}"
                        )

                    history[row[0]] = row[1]

        # Add or update rate for the date
        history[dzien] = f"{value:.4f}"

        buffer = StringIO()
        save = csv.writer(buffer, lineterminator="\n")
        save.writerows(sorted(history.items()))

        prepared[file] = buffer.getvalue()

    # Write to CSV
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    for file, contents in prepared.items():

        if file.exists() and file.read_text(
            encoding="utf-8"
        ) == contents:
            print(f"{file.name}: brak zmian")
            continue

        file.write_text(contents, encoding="utf-8")
        print(f"{file.name}: zapisano dane z {dzien}")


if __name__ == "__main__":
    main()
