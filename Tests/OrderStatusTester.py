import unittest
import datetime
from Backend.Logic.QBlOrderStatusEngine import OrderStatusHandler
from mock import patch


class TestOrderStatusHandler(unittest.TestCase):
    def test_order_status_updates(self):
        order_id = '12345'
        order_time = datetime.datetime.now()
        order_status = 'Order Received'

        # Create an instance of the OrderStatusHandler class
        order_handler = OrderStatusHandler()

        # Test status updates for each stage
        for status in ['Order Accepted', 'Preparing Order', 'Driver Assigned', 'Out for Delivery', 'Delivered']:
            with self.subTest(status=status):
                # Mock the print function to capture output for testing
                with patch('builtins.print') as mocked_print:
                    # Call the DefineOrderStatus method to simulate status updates
                    order_handler.DefineOrderStatus(order_id, order_time, order_status)
                    # Check if the print function was called with the expected status
                    mocked_print.assert_called_with(f"Order ID: {order_id}, Status: {status}, Timestamp: ")

    def test_order_cancellation(self):
        order_id = '12345'
        order_time = datetime.datetime.now()
        order_status = 'Order Received'

        # Create an instance of the OrderStatusHandler class
        order_handler = OrderStatusHandler()

        # Test cancellation when order is not yet out for delivery or delivered
        with self.subTest(status='Cancellation before Out for Delivery'):
            # Mock the print function to capture output for testing
            with patch('builtins.print') as mocked_print:
                # Call the DefineOrderStatus method to simulate status updates until Preparing Order
                order_handler.DefineOrderStatus(order_id, order_time, order_status)
                # Call the DefineOrderStatus method to simulate cancellation
                order_handler.DefineOrderStatus(order_id, order_time, 'Cancelled')
                # Check if the print function was called with the correct cancellation message
                mocked_print.assert_called_with(
                    "Order cannot be updated further as it is already out for delivery or delivered.")

        # Test cancellation when order is out for delivery
        order_status = 'Out for Delivery'
        with self.subTest(status='Cancellation at Out for Delivery'):
            # Mock the print function to capture output for testing
            with patch('builtins.print') as mocked_print:
                # Call the DefineOrderStatus method to simulate cancellation
                order_handler.DefineOrderStatus(order_id, order_time, 'Cancelled')
                # Check if the print function was called with the correct cancellation message
                mocked_print.assert_called_with(
                    "Order cannot be updated further as it is already out for delivery or delivered.")


if __name__ == '__main__':
    unittest.main()
