from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.exceptions import (
    InvalidSortBy,
    InvalidSortOrder,
    ResourceNotFound,
)
from odoo_somconnexio_python_client.resources.contract import (
    Contract,
)


class ContractTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(
            ResourceNotFound, Contract.get_by_phone_number, phone_number="9999"
        )

    @pytest.mark.vcr()
    def test_get_contract_by_phone_number(self):
        contracts = Contract.get_by_phone_number(phone_number="654987654")
        contract = contracts[0]

        assert contract.code == "1"
        assert contract.customer_vat == "ES55642302N"
        assert contract.phone_number == "654987654"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_T_UNL_20552"

    @pytest.mark.vcr()
    def test_get_contract_by_code(self):
        contracts = Contract.get_by_code(code="1")
        contract = contracts[0]

        assert contract.code == "1"
        assert contract.customer_vat == "ES55642302N"
        assert contract.phone_number == "654987654"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_T_UNL_20552"

    @pytest.mark.vcr()
    def test_search_paginated_contracts_by_customer_ref(self):
        paging_contracts = Contract.search_by_customer_ref(
            customer_ref="1234",
            limit="5",
            offset="0",
            sortBy="code",
            sortOrder="DESCENDENT",
        )
        contract = paging_contracts.contracts[1]
        paging = paging_contracts.paging

        assert contract.customer_ref == "1234"
        assert contract.customer_vat == "ES55642302N"
        assert contract.phone_number == "654543432"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_2_SHARED_UNL_51200"
        assert paging.limit == 5
        assert paging.totalNumberOfRecords == 7
        assert paging.offset == 0
        assert paging.sortBy == "code"
        assert paging.sortOrder == "DESCENDENT"

    @pytest.mark.vcr()
    def test_search_filtering_contracts_by_customer_ref(self):
        paging_contracts = Contract.search_by_customer_ref(
            customer_ref="1234",
            phone_number="654987654",
            subscription_type="mobile",
        )
        contract = paging_contracts.contracts[0]
        paging = paging_contracts.paging

        assert contract.customer_ref == "1234"
        assert contract.customer_vat == "ES55642302N"
        assert contract.phone_number == "654987654"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_T_UNL_20552"
        assert paging.limit == 100
        assert paging.totalNumberOfRecords == 1
        assert paging.offset == 0
        assert paging.sortBy == "id"
        assert paging.sortOrder == "DESCENDENT"

    @pytest.mark.vcr()
    def test_search_paginated_contracts_by_vat(self):
        paging_contracts = Contract.search_by_customer_vat(
            vat="ES55642302N",
            limit="5",
            offset="0",
            sortBy="code",
            sortOrder="DESCENDENT",
        )
        paging = paging_contracts.paging
        first_contract = paging_contracts.contracts[0]
        second_contract = paging_contracts.contracts[1]

        assert first_contract.code == "7"
        assert first_contract.customer_vat == "ES55642302N"
        assert first_contract.phone_number == "654543432"
        assert (
            first_contract.current_tariff_product
            == "SE_SC_REC_MOBILE_2_SHARED_UNL_51200"
        )

        assert second_contract.code == "6"
        assert second_contract.customer_vat == "ES55642302N"
        assert second_contract.phone_number == "654543432"
        assert (
            second_contract.current_tariff_product
            == "SE_SC_REC_MOBILE_2_SHARED_UNL_51200"
        )

        assert paging.limit == 5
        assert paging.totalNumberOfRecords == 7
        assert paging.offset == 0
        assert paging.sortBy == "code"
        assert paging.sortOrder == "DESCENDENT"

    def test_search_contract_by_customer_ref_with_pagination_bad_limit(self):
        self.assertRaises(
            Exception,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit="XXX",
        )

    def test_search_contract_by_customer_ref_with_pagination_bad_offset(self):
        self.assertRaises(
            Exception,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit=5,
            offset="XXX",
        )

    def test_search_contract_by_customer_ref_with_pagination_bad_sort_order(self):
        self.assertRaises(
            InvalidSortOrder,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit="5",
            offset="0",
            sortBy="date_start",
            sortOrder="XXX",
        )

    @pytest.mark.vcr()
    def test_search_contract_by_customer_ref_with_pagination_bad_sort_by(self):
        self.assertRaises(
            InvalidSortBy,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit="5",
            offset="0",
            sortBy="XXX",
            sortOrder="DESCENDENT",
        )

    @pytest.mark.vcr()
    def test_terminate_contract(self):
        terminate_data = {
            "code": "1",
            "terminate_reason": "TR001",
            "terminate_comment": "Termination comment test",
            "terminate_date": "2023-10-04",
            "terminate_user_reason": "TUR001",
        }
        expected_response_data = {"result": "OK"}

        result = Contract.terminate(**terminate_data)

        assert result == expected_response_data

    @pytest.mark.vcr()
    def test_terminate_reasons(self):
        reasons = Contract.terminate_reasons()

        assert "terminate_reasons" in reasons
        assert "terminate_user_reasons" in reasons
