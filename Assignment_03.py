"""Assignment 03: object-oriented refactoring of the store system."""

import contextlib
import io


# Legacy behaviour lock: this section is retained as the exact reference.
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]
TAXRATE = 0.07
foodtax = 0.0
ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(order):
    name, tier, items = order
    subtotal = tax = 0.0
    print("Receipt for " + name + " (" + tier + ")")
    print("-" * 40)
    for product_index, quantity in items:
        product = PRODUCTS[product_index]
        line = product[1] * quantity
        subtotal += line
        tax += line * (foodtax if product[2] == "food" else TAXRATE)
        print(product[0] + " x" + str(quantity) + " = " + str(line))
    discount = 0.0
    if tier == "silver":
        discount = subtotal * (0.05 if subtotal > 100 else 0.02)
    elif tier == "gold":
        discount = subtotal * (0.10 if subtotal > 100 else 0.05)
    elif tier == "platinum":
        discount = subtotal * (0.15 if subtotal > 100 else 0.10)
    if sum(item[1] for item in items) >= 10:
        discount += subtotal * 0.03
    total = subtotal - discount + tax
    multiplier = {"none": 1, "silver": 2, "gold": 3, "platinum": 5}[tier]
    points = int(total // 10) * multiplier
    print("-" * 40)
    print("Subtotal: " + str(round(subtotal, 2)))
    print("Discount: " + str(round(discount, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(points))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for order in ORDERS:
        grand += calc(order)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


TAX_RATE = 0.07
FOOD_TAX_RATE = 0.0
ELECTRONICS_CATEGORY = "electronics"
STATIONERY_CATEGORY = "stationery"
DISCOUNT_THRESHOLD = 100
BULK_QTY_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.03
POINTS_DIVISOR = 10
SEPARATOR = "-" * 40


class Product:
    def __init__(self, name, price, category):
        if not name or price < 0 or not category:
            raise ValueError("Invalid product state")
        self.name = name
        self.price = float(price)
        self.category = category

    def tax_rate(self):
        return FOOD_TAX_RATE if self.category == "food" else TAX_RATE


class OrderItem:
    def __init__(self, product, quantity):
        if not isinstance(product, Product) or quantity < 1:
            raise ValueError("Invalid order item state")
        self.product = product
        self.quantity = quantity

    def line_total(self):
        return self.product.price * self.quantity

    def tax(self):
        return self.line_total() * self.product.tax_rate()


class Customer:
    discount_rates = (0.0, 0.0)
    points_multiplier = 1
    tier = "none"

    def __init__(self, name):
        if not name:
            raise ValueError("Customer name is required")
        self.name = name

    def discount_rate(self, subtotal):
        return self.discount_rates[subtotal > DISCOUNT_THRESHOLD]

    def discount(self, subtotal):
        return subtotal * self.discount_rate(subtotal)

    def points(self, total):
        return int(total // POINTS_DIVISOR) * self.points_multiplier


class NoneCustomer(Customer):
    tier = "none"


class SilverCustomer(Customer):
    tier = "silver"
    discount_rates = (0.02, 0.05)
    points_multiplier = 2


class GoldCustomer(Customer):
    tier = "gold"
    discount_rates = (0.05, 0.10)
    points_multiplier = 3


class PlatinumCustomer(Customer):
    tier = "platinum"
    discount_rates = (0.10, 0.15)
    points_multiplier = 5


CUSTOMER_TYPES = {
    "none": NoneCustomer,
    "silver": SilverCustomer,
    "gold": GoldCustomer,
    "platinum": PlatinumCustomer,
}


class Order:
    def __init__(self, customer, items):
        if not isinstance(customer, Customer) or not items:
            raise ValueError("Invalid order state")
        self.customer = customer
        self.items = tuple(items)

    def subtotal(self):
        return sum(item.line_total() for item in self.items)

    def discount(self):
        subtotal = self.subtotal()
        bulk_discount = subtotal * BULK_DISCOUNT_RATE if self.quantity() >= BULK_QTY_THRESHOLD else 0.0
        return self.customer.discount(subtotal) + bulk_discount

    def tax(self):
        return sum(item.tax() for item in self.items)

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return self.customer.points(self.total())

    def quantity(self):
        return sum(item.quantity for item in self.items)

    def receipt(self):
        lines = ["Receipt for " + self.customer.name + " (" + self.customer.tier + ")", SEPARATOR]
        lines.extend(item.product.name + " x" + str(item.quantity) + " = " + str(item.line_total()) for item in self.items)
        lines.extend([
            SEPARATOR,
            "Subtotal: " + str(round(self.subtotal(), 2)),
            "Discount: " + str(round(self.discount(), 2)),
            "Tax: " + str(round(self.tax(), 2)),
            "Total: " + str(round(self.total(), 2)),
            "Points earned: " + str(self.points()),
            "",
        ])
        return "\n".join(lines)


def build_orders():
    products = [Product(*product) for product in PRODUCTS]
    orders = []
    for name, tier, raw_items in ORDERS:
        customer = CUSTOMER_TYPES[tier](name)
        items = [OrderItem(products[index], quantity) for index, quantity in raw_items]
        orders.append(Order(customer, items))
    return orders


def refactored_main():
    orders = build_orders()
    for order in orders:
        print(order.receipt())
    print("GRAND TOTAL (all orders): " + str(round(sum(order.total() for order in orders), 2)))


def capture(function):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


def _check():
    output = capture(refactored_main)
    if output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        expected = GOLDEN_OUTPUT.splitlines()
        actual = output.splitlines()
        for index in range(max(len(expected), len(actual))):
            expected_line = expected[index] if index < len(expected) else "<no line>"
            actual_line = actual[index] if index < len(actual) else "<no line>"
            if expected_line != actual_line:
                print("First difference at line " + str(index + 1) + ":")
                print("  expected: " + repr(expected_line))
                print("  yours:    " + repr(actual_line))
                break


if __name__ == "__main__":
    _check()
