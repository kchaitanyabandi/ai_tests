# sample_module.py

import math
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_order(order_id, items, tax_rate):
    """Process a single order and compute totals."""
    subtotal = 0.0
    for item in items:
        subtotal += item["price"] * item["quantity"]

    tax = subtotal * tax_rate
    total = subtotal + tax
    return {
        "order_id": order_id,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }

def process_orders(orders, tax_rate):
    """Process multiple orders and return a summary."""
    logging.info("Starting to process orders.")
    results = []
    grand_total = 0.0

    for order in orders:
        result = process_order(order["order_id"], order["items"], tax_rate)
        results.append(result)
        grand_total += result["total"]
    
    logging.info("Finished processing orders. Summary computed.")
    
    return {
        "orders": results,
        "grand_total": grand_total,
        "count": len(results),
    }

def format_currency(value):
    """Format a float as USD currency."""
    return f"${value:,.2f}"

def print_report(summary):
    """Print a simple report for the processed orders."""
    print("=" * 40)
    print("ORDER SUMMARY REPORT")
    print("=" * 40)
    print(f"Number of orders: {summary['count']}")
    print(f"Grand total     : {format_currency(summary['grand_total'])}")
    print("=" * 40)

def demo():
    """Run a small demo."""
    orders = [
        {
            "order_id": "A100",
            "items": [
                {"name": "Widget", "price": 9.99, "quantity": 3},
                {"name": "Gadget", "price": 4.50, "quantity": 2},
            ],
        },
        {
            "order_id": "B200",
            "items": [
                {"name": "Thing", "price": 19.99, "quantity": 1},
                {"name": "Widget", "price": 9.99, "quantity": 5},
            ],
        },
    ]
    summary = process_orders(orders, tax_rate=0.1)
    print_report(summary)

# Some extra fluff to make the file longer and more realistic.

def slow_operation():
    """Pretend to do a slow operation."""
    total = 0
    for i in range(1000):
        total += math.sqrt(i)
    return total

def helper_one(value):
    return value * 2

def helper_two(value):
    return value + 10

def helper_three(value):
    return helper_two(helper_one(value))

class OrderProcessor:
    def __init__(self, tax_rate):
        self.tax_rate = tax_rate

    def run(self, orders):
        return process_orders(orders, self.tax_rate)

if __name__ == "__main__":
    demo()