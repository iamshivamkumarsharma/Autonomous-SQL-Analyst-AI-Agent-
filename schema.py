def get_schema():
    return """
customers(customer_id, name, city)
products(product_id, product_name, category)
orders(order_id, customer_id, order_date)
order_items(order_id, product_id, quantity, price)
"""
