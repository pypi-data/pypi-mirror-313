import pytest
import unittest2 as unittest
from odoo_somconnexio_python_client.exceptions import ResourceNotFound
from odoo_somconnexio_python_client.resources.coop_agreement import CoopAgreement


class CoopAgreementTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(ResourceNotFound, CoopAgreement.get, code="XX")

    @pytest.mark.vcr()
    def test_search_resource_found(self):
        result = CoopAgreement.get(code="ExampleCode")
        assert result.name == "Cooperativa Amiga"
        assert result.code == "ExampleCode"
        assert result.first_month_promotion
