# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.api.orders_api import OrdersApi


class TestOrdersApi(unittest.TestCase):
    """OrdersApi unit test stubs"""

    def setUp(self) -> None:
        self.api = OrdersApi()

    def tearDown(self) -> None:
        pass

    def test_orders_all_list(self) -> None:
        """Test case for orders_all_list

        Get All Orders
        """
        pass

    def test_orders_current_list(self) -> None:
        """Test case for orders_current_list

        Get Current Order
        """
        pass

    def test_orders_delete(self) -> None:
        """Test case for orders_delete

        Delete Order
        """
        pass

    def test_orders_edit_patch(self) -> None:
        """Test case for orders_edit_patch

        Edit Order
        """
        pass

    def test_orders_get(self) -> None:
        """Test case for orders_get

        Get Order
        """
        pass

    def test_orders_invoice_get(self) -> None:
        """Test case for orders_invoice_get

        Generate Invoice
        """
        pass

    def test_orders_item_patch(self) -> None:
        """Test case for orders_item_patch

        Delete Order Item
        """
        pass

    def test_orders_offer_get(self) -> None:
        """Test case for orders_offer_get

        Generate Offer
        """
        pass

    def test_orders_post(self) -> None:
        """Test case for orders_post

        Add Order Items
        """
        pass

    def test_orders_put(self) -> None:
        """Test case for orders_put

        Update Order Items
        """
        pass


if __name__ == '__main__':
    unittest.main()
