# sample_module_2.py

import math
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Item:
    sku: str
    name: str
    price: float
    quantity: int


def apply_discount(price: float, discount_pct: float) -> float:
    """Return price after applying a percentage discount.
    Ensures the final price is never negative.
    """
    discounted = price * (1 - max(0.0, min(discount_pct, 1.0)))
    return max(0.0, round(discounted, 2))


def compute_cart_totals(items: List[Item], discount_pct: float = 0.0) -> Dict[str, float]:
    """Compute totals for a cart, optionally applying a cart-wide discount."""
    subtotal = sum(i.price * i.quantity for i in items)
    discount = subtotal - sum(apply_discount(i.price, discount_pct) * i.quantity for i in items)
    total = subtotal - discount
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "total": round(total, 2),
    }


def format_usd(amount: float) -> str:
    """Format a float as USD currency."""
    return f"${amount:,.2f}"


def summarize_items(items: List[Item]) -> List[Dict[str, str]]:
    """Return a simple summary view for display purposes."""
    return [
        {
            "sku": i.sku,
            "name": i.name,
            "qty": str(i.quantity),
            "price": format_usd(i.price),
            "line_total": format_usd(i.price * i.quantity),
        }
        for i in items
    ]


class InventoryManager:
    """Manage inventory and simple lookups."""

    def __init__(self):
        self._stock: Dict[str, Item] = {}

    def add_item(self, item: Item) -> None:
        if item.sku in self._stock:
            existing = self._stock[item.sku]
            self._stock[item.sku] = Item(
                sku=existing.sku,
                name=existing.name,
                price=item.price,  # latest price wins
                quantity=existing.quantity + item.quantity,
            )
        else:
            self._stock[item.sku] = item

    def remove_item(self, sku: str, quantity: int) -> bool:
        if sku not in self._stock or quantity <= 0:
            return False
        current = self._stock[sku]
        if current.quantity < quantity:
            return False
        self._stock[sku] = Item(
            sku=current.sku,
            name=current.name,
            price=current.price,
            quantity=current.quantity - quantity,
        )
        return True

    def get(self, sku: str) -> Optional[Item]:
        return self._stock.get(sku)

    def list_items(self) -> List[Item]:
        return list(self._stock.values())


def estimate_shipping_weight(items: List[Item]) -> float:
    """Very rough estimate: weight grows sub-linearly with quantity.
    This is just a placeholder formula using sqrt for variety.
    """
    return round(sum(math.sqrt(max(0, i.quantity)) for i in items), 3)


def demo():
    items = [
        Item(sku="WID-001", name="Widget", price=9.99, quantity=3),
        Item(sku="GAD-002", name="Gadget", price=4.50, quantity=2),
        Item(sku="THG-003", name="Thing", price=19.99, quantity=1),
    ]

    totals = compute_cart_totals(items, discount_pct=0.1)
    print("Cart Totals:")
    print({k: format_usd(v) if k != "subtotal" and k != "discount" and k != "total" else v for k, v in totals.items()})

    print("\nItem Summary:")
    for row in summarize_items(items):
        print(row)

    inv = InventoryManager()
    for i in items:
        inv.add_item(i)

    # Remove one widget
    inv.remove_item("WID-001", 1)

    print("\nInventory:")
    for i in inv.list_items():
        print(i)

    print("\nEstimated shipping weight:", estimate_shipping_weight(items))


if __name__ == "__main__":
    demo()
