"""Module creates views generate_student and bitcoin converter currency."""

from flask import Flask, Response, jsonify
from faker import Faker
import csv
import io
import requests
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)

bitcoin_args = {
    "currency": fields.Str(load_default="USD"),
    "count": fields.Int(load_default=1)
}


@app.route('/generate_students', methods=['GET'])
def generate_students():
    # Read count parameter from GET, default to 10 and cap at 1000
    from flask import request
    count = request.args.get('count', default=10, type=int)
    count = min(count, 1000)

    fake = Faker()
    students = []

    # Generate student records using Faker
    for _ in range(count):
        student = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "birthday": fake.date_of_birth(minimum_age=18, maximum_age=60)
        }
        students.append(student)

    # Write records to CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["first_name", "last_name", "email", "password", "birthday"]
    )
    writer.writeheader()
    for student in students:
        student['birthday'] = student['birthday'].isoformat()
        writer.writerow(student)

    csv_data = output.getvalue()

    # Save CSV to a file on the server
    with open("students.csv", "w", newline="", encoding="utf-8") as f:
        f.write(csv_data)

    # Display CSV content on the web page within a <pre> tag
    return Response(f"<pre>{csv_data}</pre>", mimetype="text/html")


@app.route('/bitcoin_rate', methods=['GET'])
@use_args(bitcoin_args, location="query")
def get_bitcoin_value(args):
    # Get query parameters: currency code (default USD) and count (default 1)
    currency = args.get("currency", "USD").upper()
    count = args.get("count", 1)

    url = f"https://bitpay.com/api/rates/{currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching btc rates: {str(e)}"}), 500

    rate = data.get("rate")
    if rate is None:
        return jsonify({"error": f"Currency code {currency} not found."}), 400

    # Multiply the bitcoin rate by the count provided
    total_value = rate * count

    # Mapping from currency codes to symbols (if API doesn't provide it)
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "UAH": "₴",
        "GBP": "£",
    }
    symbol = currency_symbols.get(currency, currency)

    result = {
        "currency": currency,
        "count": count,
        "bitcoin_rate": rate,
        "total_value": total_value,
        "symbol": symbol
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
