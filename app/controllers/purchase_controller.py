from flask import jsonify, request
from app.services.purchase_service import scrape_purchase_details

def scrape():
    data = request.get_json()
    url = data.get('url')
    if url:
        result = scrape_purchase_details(url)
        return jsonify(result)
    else:
        return jsonify({"error": "No URL provided"}), 400
