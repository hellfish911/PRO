"""Module returns webview of retrieved statistics from the database."""

from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from database_handler import execute_query

app = Flask(__name__)

stats_args = {
    'genre': fields.Str(required=True,
                        error_messages={'required': 'genre is required'})
}


@app.route('/stats_by_city', methods=['GET'])
@use_args(stats_args, location='query')
def stats_by_city(args):
    """
    Accept a genre as input and display the city or cities in which
    this genre is most listened to. If there is no data for the given genre,
    display a message.
    The genre is a required parameter (e.g., /stats_by_city?genre=Metal).
    """
    genre = args['genre']

    query = """
        SELECT i.BillingCity, COUNT(*) AS listens
        FROM invoice_items il
        JOIN Invoices i ON i.InvoiceId = il.InvoiceId
        JOIN tracks t ON t.TrackId = il.TrackId
        JOIN genres g ON t.GenreId = g.GenreId
        WHERE g.Name = ?
        GROUP BY i.BillingCity
        ORDER BY listens DESC
    """
    records = execute_query(query, (genre,))

    if not records:
        return jsonify({'message': f'No data for genre {genre}'}), 404

    max_listens = records[0][1]
    top_cities = [row[0] for row in records if row[1] == max_listens]

    return jsonify({
        'genre': genre,
        'top_cities': top_cities,
        'listen_count': max_listens
    })


if __name__ == '__main__':
    app.run(debug=True)
