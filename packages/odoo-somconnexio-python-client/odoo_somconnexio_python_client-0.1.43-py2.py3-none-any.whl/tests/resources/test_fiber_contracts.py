import pytest
import unittest2 as unittest
from odoo_somconnexio_python_client.exceptions import ResourceNotFound

from odoo_somconnexio_python_client.resources.fiber_contracts import (
    FiberContractsToPack,
)


def assert_model(contracts):
    contract = contracts[0]

    assert contract.code == "2"
    assert contract.customer_vat == "ES55642302N"
    assert contract.phone_number == "939516001"
    assert contract.current_tariff_product == "SE_SC_REC_BA_F_600"


class FiberContractsToPackTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_by_partner_ref(self):
        assert_model(FiberContractsToPack.search_by_partner_ref(partner_ref=1234))

    @pytest.mark.vcr()
    def test_search_by_partner_ref_and_mobiles_sharing_data(self):
        assert_model(
            FiberContractsToPack.search_by_partner_ref(
                partner_ref=1234, mobiles_sharing_data="true"
            )
        )

    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(
            ResourceNotFound,
            FiberContractsToPack.search_by_partner_ref,
            partner_ref="xxx",
        )
