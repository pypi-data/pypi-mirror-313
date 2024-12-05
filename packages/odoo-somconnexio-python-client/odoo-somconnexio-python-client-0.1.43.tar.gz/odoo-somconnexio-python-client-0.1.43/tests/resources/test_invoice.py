from odoo_somconnexio_python_client.exceptions import (
    InvalidSortBy,
    InvalidSortOrder,
    ResourceNotFound,
)
from odoo_somconnexio_python_client.resources.invoice import Invoice

import unittest2 as unittest
import pytest


class InvoiceTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(ResourceNotFound, Invoice.get_by_id, id="9999")

    @pytest.mark.vcr()
    def test_get_invoice_by_id(self):
        invoice = Invoice.get_by_id(9)
        self._common_invoice_asserts(invoice)
        assert invoice.pdf

    @pytest.mark.vcr()
    def test_search_paginated_invoices_by_customer_ref(self):
        paging_invoices = Invoice.search_by_customer_ref(
            customer_ref="1234",
            limit="1",
            offset="0",
        )

        invoice = paging_invoices.invoices[0]
        self._common_invoice_asserts(invoice)
        assert not invoice.pdf

        paging = paging_invoices.paging
        self._common_paging_asserts(paging)
        assert paging.sortBy == "date_invoice"
        assert paging.sortOrder == "DESCENDENT"

    @pytest.mark.vcr()
    def test_search_paginated_invoices_by_customer_vat(self):
        paging_invoices = Invoice.search_by_customer_vat(
            vat="ES55642302N",
            limit="1",
            offset="0",
            sortBy="id",
            sortOrder="ASCENDENT",
        )

        invoice = paging_invoices.invoices[0]
        self._common_invoice_asserts(invoice)
        assert not invoice.pdf

        paging = paging_invoices.paging
        self._common_paging_asserts(paging)
        assert paging.sortBy == "id"
        assert paging.sortOrder == "ASCENDENT"

    def test_search_invoicesby_customer_ref_with_pagination_bad_limit(self):
        self.assertRaises(
            Exception,
            Invoice.search_by_customer_ref,
            customer_ref="123",
            limit="XXX",
        )

    def test_search_invoices_by_customer_ref_with_pagination_bad_offset(self):
        self.assertRaises(
            Exception,
            Invoice.search_by_customer_ref,
            customer_ref="123",
            limit=5,
            offset="XXX",
        )

    def test_search_invoices_by_customer_ref_with_pagination_bad_sort_order(self):
        self.assertRaises(
            InvalidSortOrder,
            Invoice.search_by_customer_ref,
            customer_ref="123",
            limit="5",
            offset="0",
            sortBy="date_start",
            sortOrder="XXX",
        )

    @pytest.mark.vcr()
    def test_search_invoices_by_customer_ref_with_pagination_bad_sort_by(self):
        self.assertRaises(
            InvalidSortBy,
            Invoice.search_by_customer_ref,
            customer_ref="123",
            limit="5",
            offset="0",
            sortBy="XXX",
            sortOrder="DESCENDENT",
        )

    def _common_invoice_asserts(self, invoice):
        assert invoice.id == 9
        assert invoice.name == "SO2024-0001"
        assert invoice.date == "2024-07-24"
        assert invoice.total_amount == 2.5
        assert invoice.tax_amount == 0.5
        assert invoice.base_amount == 2.0
        assert invoice.status == "paid"

    def _common_paging_asserts(self, paging):
        assert paging.limit == 1
        assert paging.totalNumberOfRecords == 1
        assert paging.offset == 0
