import unittest
import threading

from InventoryManagement import InventoryManagement


class InventoryQA(unittest.TestCase):

    def setUp(self):

        self.inventory = InventoryManagement()

        # Warehouse A
        self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            50
        )

        # Warehouse B
        self.inventory.add_product(
            "Warehouse B",
            "Laptop",
            30
        )

        # Warehouse C
        self.inventory.add_product(
            "Warehouse C",
            "Phone",
            20
        )

    # 1. Stock Availability
    def test_stock_availability(self):

        stock = self.inventory.check_stock(
            "Warehouse A",
            "Laptop"
        )

        self.assertEqual(stock, 50)

    # 2. Insufficient Inventory
    def test_insufficient_inventory(self):

        result = self.inventory.fulfill_order(
            "Laptop",
            100
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
            self.inventory.check_stock(
                "Warehouse A",
                "Laptop"
            ),
            40
        )

        self.assertEqual(
            self.inventory.check_stock(
                "Warehouse B",
                "Laptop"
            ),
            40
        )

    # 4. Concurrent Orders
    def test_concurrent_orders(self):

        results = []

        def order():

            result = self.inventory.fulfill_order(
                "Laptop",
                10
            )

            results.append(result)

        threads = []

        for i in range(3):

            thread = threading.Thread(
                target=order
            )

            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            len(results),
            3
        )

        # Total laptop stock = 80
        # Three orders × 10 = 30
        # Remaining = 50
        total_stock = (
            self.inventory.check_stock(
                "Warehouse A",
                "Laptop"
            )
            +
            self.inventory.check_stock(
                "Warehouse B",
                "Laptop"
            )
        )

        self.assertEqual(total_stock, 50)

    # 5. Reorder Threshold
    def test_reorder_threshold(self):

        self.inventory.remove_product(
            "Warehouse A",
            "Laptop",
            45
        )

        stock = self.inventory.check_stock(
            "Warehouse A",
            "Laptop"
        )

        self.assertEqual(stock, 5)

        result = self.inventory.reorder(
            "Warehouse A",
            "Laptop",
            20
        )

        self.assertEqual(
            result,
            "Reorder completed"
        )

        self.assertEqual(
            self.inventory.check_stock(
                "Warehouse A",
                "Laptop"
            ),
            25
        )

    # 6. Invalid Product
    def test_invalid_product(self):

        result = self.inventory.fulfill_order(
            "Tablet",
            5
        )

        self.assertEqual(
            result,
            "Insufficient inventory"
        )

    # 7. Negative Inventory
    def test_negative_inventory(self):

        result = self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            -10
        )

        self.assertEqual(
            result,
            "Invalid quantity"
        )

    # 8. Multiple Warehouses
    def test_multiple_warehouses(self):

        self.assertEqual(
            len(self.inventory.warehouses),
            3
        )

        self.assertIn(
            "Warehouse A",
            self.inventory.warehouses
        )

        self.assertIn(
            "Warehouse B",
            self.inventory.warehouses
        )

        self.assertIn(
            "Warehouse C",
            self.inventory.warehouses
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
