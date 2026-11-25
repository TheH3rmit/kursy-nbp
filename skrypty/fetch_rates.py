
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

def fetch_rates():
    try:
        with urlopen(API_URL, timeout=15) as response:
            return json.load(response)[0]

    except HTTPError as error:
        if error.code == 404:
            print("Brak tabeli")
            return None
        raise

def validate_rate(rates, currency):
    if currency not in rates:
        raise ValueError(f"Brak kursu: {currency}")

    value = Decimal(str(rates[currency]))

    if not value.is_finite() or value <= 0:
        raise ValueError(f"Niepoprawny kurs: {value}")
    return value

def read_history(file):
    history = {}

    # Read existing rates
    if file.exists():
        with file.open(
            "r", encoding="utf-8", newline=""
        ) as f:
            for row in csv.reader(f):
                if len(row) != 2:
                    raise ValueError(f"Niepoprawny wiersz: {file}")
                history[row[0]] = row[1]
    return history

def prepare_rates(rates, date_time):
    prepared = {}

    for currency in CURRENCIES:
        value = validate_rate(rates, currency)

        file = DATA_PATH / f"{currency.lower()}.csv"

        history = read_history(file)

        # Add or update rate for the date
        history[date_time] = f"{value:.4f}"

        buffer = StringIO()
        save = csv.writer(buffer, lineterminator="\n")
        save.writerows(sorted(history.items()))

        prepared[file] = buffer.getvalue()
    return prepared

def save_rates(prepared, date_time):
    # Write to CSV
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    for file, contents in prepared.items():

        if file.exists() and file.read_text(
            encoding="utf-8"
        ) == contents:
            print(f"{file.name}: brak zmian")
            continue

        file.write_text(contents, encoding="utf-8")
        print(f"{file.name}: zapisano dane z {date_time}")


def main():
    # Getting data from the NBP API
    table = fetch_rates()

    if table is None:
        return

    # Read and validate
    date_time = table["effectiveDate"]
    date.fromisoformat(date_time)

    rates = {
        rate["code"]: rate["mid"]
        for rate in table["rates"]
    }

    prepared = prepare_rates(rates,date_time)

    # Write to CSV
    save_rates(prepared, date_time)


if __name__ == "__main__":
    main()
