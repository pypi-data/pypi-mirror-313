from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.resources.one_shot_catalog import (
    OneShot,
    OneShotCatalog,
)


class OneShotTariffTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_code(self):
        pricelists = OneShotCatalog.search(
            code="21IVA", product_code="SE_SC_REC_MOBILE_T_150_1024"
        )

        tariff_names = []
        tariff_codes = []

        pricelist_21IVA = pricelists[0]
        self.assertIsInstance(pricelist_21IVA, OneShotCatalog)
        self.assertEqual(pricelist_21IVA.code, "21IVA")
        for one_shot in pricelist_21IVA.one_shots:
            self.assertIsInstance(one_shot, OneShot)
            tariff_names.append(one_shot.name)
            tariff_codes.append(one_shot.code)

        self.assertIn("1 GB Addicionals", tariff_names)
        self.assertIn("CH_SC_OSO_1GB_ADDICIONAL", tariff_codes)

    @pytest.mark.vcr()
    def test_search_non_existant_product_code(self):
        pricelists = OneShotCatalog.search(product_code="BBBB")
        self.assertEqual(len(pricelists[0].one_shots), 0)
