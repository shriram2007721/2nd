import threading


class InventoryManagement:

    def __init__(self):

        self.warehouses = {
            "Warehouse A": {},
            "Warehouse B": {},
            "Warehouse C": {}
        }

        self.suppliers = {}

        self.reorder_threshold = 10

        self.lock = threading.Lock()

    # Add Product
    def add_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if quantity < 0:
            return "Invalid quantity"

        if product not in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] = 0

        self.warehouses[warehouse][product] += quantity

        return "Product added successfully"

    # Remove Product
    def remove_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if product not in self.warehouses[warehouse]:
            return "Invalid product"

        if quantity < 0:
            return "Invalid quantity"

        if self.warehouses[warehouse][product] < quantity:
            return "Insufficient inventory"

        self.warehouses[warehouse][product] -= quantity

        return "Product removed successfully"

    # Transfer Stock
    def transfer_stock(self, source, destination, product, quantity):

        if source not in self.warehouses:
            return "Invalid source warehouse"

        if destination not in self.warehouses:
            return "Invalid destination warehouse"

        if product not in self.warehouses[source]:
            return "Invalid product"

        if quantity <= 0:
            return "Invalid quantity"

        if self.warehouses[source][product] < quantity:
            return "Insufficient inventory"

        with self.lock:

            self.warehouses[source][product] -= quantity

            if product not in self.warehouses[destination]:
                self.warehouses[destination][product] = 0

            self.warehouses[destination][product] += quantity

        return "Stock transferred successfully"

    # Supplier Management
    def add_supplier(self, supplier_id, supplier_name):

        self.suppliers[supplier_id] = supplier_name

        return "Supplier added successfully"

    def remove_supplier(self, supplier_id):

        if supplier_id not in self.suppliers:
            return "Supplier not found"

        del self.suppliers[supplier_id]

        return "Supplier removed successfully"

    # Low Stock Detection
    def low_stock(self):

        result = {}

        for warehouse in self.warehouses:

            for product, quantity in self.warehouses[warehouse].items():

                if quantity <= self.reorder_threshold:

                    if warehouse not in result:
                        result[warehouse] = []

                    result[warehouse].append(product)

        return result

    # Reorder
    def reorder(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if quantity <= 0:
            return "Invalid quantity"

        if product not in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] = 0

        self.warehouses[warehouse][product] += quantity

        return "Stock reordered successfully"

    # Warehouse Selection
    def select_warehouse(self, product, quantity):

        for warehouse in self.warehouses:

            available = self.warehouses[warehouse].get(
                product, 0
            )

            if available >= quantity:
                return warehouse

        return None

    # Fulfill Order
    def fulfill_order(self, product, quantity):

        if quantity <= 0:
            return "Invalid quantity"

        warehouse = self.select_warehouse(
            product,
            quantity
        )

        if warehouse is None:
            return "Insufficient inventory"

        with self.lock:

            self.warehouses[warehouse][product] -= quantity

        return "Order fulfilled from " + warehouse

    # Get Stock
    def get_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return -1

        return self.warehouses[warehouse].get(
            product,
            0
        )


if __name__ == "__main__":

    inventory = InventoryManagement()

    print(inventory.add_product(
        "Warehouse A",
        "Laptop",
        50
    ))

    print(inventory.add_product(
        "Warehouse B",
        "Laptop",
        30
    ))

    print(inventory.add_product(
        "Warehouse C",
        "Laptop",
        20
    ))

    print(inventory.add_product(
        "Warehouse A",
        "Mouse",
        15
    ))

    print(inventory.add_supplier(
        "S001",
        "ABC Suppliers"
    ))

    print(inventory.transfer_stock(
        "Warehouse A",
        "Warehouse B",
        "Laptop",
        10
    ))

    print(inventory.fulfill_order(
        "Laptop",
        25
    ))

    print("Low Stock:")

    print(inventory.low_stock())

    print("Warehouse A Laptop:",
          inventory.get_stock(
              "Warehouse A",
              "Laptop"
          ))
