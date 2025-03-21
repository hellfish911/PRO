"""Module retrieves data from the database and displays it as webview."""

from flask import Flask, request, jsonify
from database_handler import execute_query

app = Flask(__name__)


@app.route('/order_price', methods=['GET'])
def order_price():
    """Get the optional country parameter from the query string"""
    country = request.args.get('country', None)

    # Build the SQL query depending on whether a country is provided
    if country:
        query = """
            SELECT i.BillingCountry,
                   SUM(il.UnitPrice * il.Quantity) AS total_sales
            FROM invoice_items il
            JOIN Invoices i ON i.InvoiceId = il.InvoiceId
            WHERE i.BillingCountry = ?
            GROUP BY i.BillingCountry
        """
        records = execute_query(query, (country,))
    else:
        query = """
            SELECT i.BillingCountry,
                   SUM(il.UnitPrice * il.Quantity) AS total_sales
            FROM invoice_items il
            JOIN Invoices i ON i.InvoiceId = il.InvoiceId
            GROUP BY i.BillingCountry
        """
        records = execute_query(query)

    # Format the results as a list of dictionaries
    data = []
    for row in records:
        data.append({
            "BillingCountry": row[0],
            "TotalSales": row[1]
        })

    # Return JSON response
    return jsonify(data)


@app.route('/track_info', methods=['GET'])
def get_all_info_about_track():
    """
    Return detailed information about a track by joining all relevant tables.
    Require a track ID as input (e.g., /track_info?track_id=1).
    """
    track_id = request.args.get('track_id')
    if not track_id:
        return jsonify({"error": "track_id is required"}), 400

    query = """
        SELECT t.TrackId,
               t.Name AS TrackName,
               t.Composer,
               t.Milliseconds,
               t.Bytes,
               t.UnitPrice,
               a.AlbumId,
               a.Title AS AlbumTitle,
               ar.ArtistId,
               ar.Name AS ArtistName,
               g.GenreId,
               g.Name AS GenreName,
               mt.MediaTypeId,
               mt.Name AS MediaTypeName
        FROM tracks t
        LEFT JOIN albums a ON t.AlbumId = a.AlbumId
        LEFT JOIN artists ar ON a.ArtistId = ar.ArtistId
        LEFT JOIN genres g ON t.GenreId = g.GenreId
        LEFT JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
        WHERE t.TrackId = ?
    """

    records = execute_query(query, (track_id,))
    if not records:
        return jsonify({"error": "No track found for the given track_id"}), 404

    row = records[0]
    result = {
        "TrackId": row[0],
        "TrackName": row[1],
        "Composer": row[2],
        "Milliseconds": row[3],
        "Bytes": row[4],
        "UnitPrice": row[5],
        "AlbumId": row[6],
        "AlbumTitle": row[7],
        "ArtistId": row[8],
        "ArtistName": row[9],
        "GenreId": row[10],
        "GenreName": row[11],
        "MediaTypeId": row[12],
        "MediaTypeName": row[13]
    }
    return jsonify(result)


@app.route('/tracks_time', methods=['GET'])
def get_tracks_time_in_hours():
    """
    Show the total play time (in hours) of all tracks for each album.
    Join the tracks and albums tables, groups by album, and convert
    the sum of track durations (milliseconds) to hours.
    """
    query = """
        SELECT a.AlbumId,
               a.Title AS AlbumTitle,
               SUM(t.Milliseconds) AS TotalMilliseconds,
               ROUND(SUM(t.Milliseconds) / 3600000.0, 2) AS TotalHours
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        GROUP BY a.AlbumId, a.Title
    """
    records = execute_query(query)
    data = []
    for row in records:
        data.append({
            "AlbumId": row[0],
            "AlbumTitle": row[1],
            "TotalMilliseconds": row[2],
            "TotalHours": row[3]
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
