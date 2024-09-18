class Purchase:
    def __init__(self, datetime_purchase, company_name, total_items, payment_method, products):
        self.datetime_purchase = datetime_purchase
        self.company_name = company_name
        self.total_items = total_items
        self.payment_method = payment_method
        self.products = products
