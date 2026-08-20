import unittest
import threading

from InventoryManagement import InventoryManagement


class InventoryQA(unittest.TestCase):

    def setUp(self):

        self.inventory = InventoryManagement()

        self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            50
        )

        self.inventory.add_product(
            "Warehouse B",
            "Laptop",
            30
        )

        self.inventory.add_product(
            "Warehouse C",
            "Laptop",
            20
        )

    # 1. Stock Availability
    def test_stock_availability(self):

        stock = self.inventory.get_stock(
            "Warehouse A",
            "Laptop"
        )

        self.assertEqual(stock, 50)

    # 2. Insufficient Inventory
    def test_insufficient_inventory(self):

        result = self.inventory.fulfill_order(
            "Laptop",
            200
        )

        self.assertEqual(
            result,
            "Insufficient inventory"
        )

    # 3. Warehouse Transfer
    def test_warehouse_transfer(self):

        result = self.inventory.transfer_stock(
            "Warehouse A",
            "Warehouse B",
            "Laptop",
            10
        )

        self.assertEqual(
            result,
            "Stock transferred successfully"
        )

        self.assertEqual(
            self.inventory.get_stock(
                "Warehouse A",
                "Laptop"
            ),
            40
        )

        self.assertEqual(
            self.inventory.get_stock(
                "Warehouse B",
                "Laptop"
            ),
            40
        )

    # 4. Concurrent Orders
    def test_concurrent_orders(self):

        results = []

        def place_order():

            result = self.inventory.fulfill_order(
                "Laptop",
                5
            )

            results.append(result)

        threads = []

        for i in range(5):

            thread = threading.Thread(
                target=place_order
            )

            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            len(results),
            5
        )

    # 5. Reorder Threshold
    def test_reorder_threshold(self):

        self.inventory.remove_product(
            "Warehouse A",
            "Laptop",
            45
        )

        low_stock = self.inventory.low_stock()

        self.assertIn(
            "Warehouse A",
            low_stock
        )

        self.assertIn(
            "Laptop",
            low_stock["Warehouse A"]
        )

    # 6. Invalid Product
    def test_invalid_product(self):

        result = self.inventory.remove_product(
            "Warehouse A",
            "Mobile",
            5
        )

        self.assertEqual(
            result,
            "Invalid product"
        )

    # 7. Negative Inventory
    def test_negative_inventory(self):

        result = self.inventory.remove_product(
            "Warehouse A",
            "Laptop",
            100
        )

        self.assertEqual(
            result,
            "Insufficient inventory"
        )

        stock = self.inventory.get_stock(
            "Warehouse A",
            "Laptop"
        )

        self.assertGreaterEqual(
            stock,
            0
        )

    # 8. Multiple Warehouses
    def test_multiple_warehouses(self):

        warehouse = self.inventory.select_warehouse(
            "Laptop",
            25
        )

        self.assertIsNotNone(warehouse)

        self.assertIn(
            warehouse,
            [
                "Warehouse A",
                "Warehouse B",
                "Warehouse C"
            ]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
