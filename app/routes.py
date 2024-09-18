from app.controllers.purchase_controller import scrape

def init_routes(app):
    app.route('/api/scrape_purchase', methods=['POST'])(scrape)
