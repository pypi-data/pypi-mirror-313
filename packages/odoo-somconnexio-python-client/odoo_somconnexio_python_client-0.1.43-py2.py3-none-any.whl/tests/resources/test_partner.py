from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.exceptions import ResourceNotFound
from odoo_somconnexio_python_client.resources.partner import Partner


class PartnerTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(ResourceNotFound, Partner.search_by_vat, vat="")

    @pytest.mark.vcr()
    def test_search_by_vat(self):
        partner = Partner.search_by_vat(vat="55642302N")

        assert partner.ref == "1234"
        assert partner.vat == "ES55642302N"
        assert partner.name == "Felip Dara"

    @pytest.mark.vcr()
    def test_get_with_ref(self):
        ref = "1234"
        partner = Partner.get(ref)

        assert partner.ref == "1234"
        assert partner.vat == "ES55642302N"
        assert partner.name == "Felip Dara"
        assert partner.member
        assert partner.addresses[0].street == "Carrer del Penal, 2"
        assert "mobile_one_shot" in partner.banned_actions
        assert "mobile_tariff_change" in partner.banned_actions
        assert "new_service" in partner.banned_actions

    @pytest.mark.vcr()
    def test_check_sponsor_ok(self):
        sponsor_code = "cac3c"
        vat = "ES76230724F"
        result, message = Partner.check_sponsor(vat, sponsor_code)

        assert result
        assert message == "ok"

    @pytest.mark.vcr()
    def test_check_sponsor_ko_maximum_exceeded(self):
        sponsor_code = "ry12u"
        vat = "ES62308540E"
        result, message = Partner.check_sponsor(vat, sponsor_code)

        assert not result
        assert message == "maximum number of sponsees exceeded"

    @pytest.mark.vcr()
    def test_check_sponsor_ko_wrong_code(self):
        sponsor_code = "abc12"
        vat = "ES11673039X"
        result, message = Partner.check_sponsor(vat, sponsor_code)

        assert not result
        assert message == "invalid code or vat number"

    @pytest.mark.vcr()
    def test_get_sponsees_not_found(self):
        self.assertRaises(ResourceNotFound, Partner.sponsees, ref="NOT_EXISTS")

    @pytest.mark.vcr()
    def test_get_sponsees_ok(self):
        ref = "1234"
        sponsees = Partner.sponsees(ref)
        assert sponsees.sponsorship_code == "RYR6O"
        assert sponsees.sponsees_max == 5
        assert sponsees.sponsees_number == 1
        assert sponsees.sponsees_list == ["Joanau Basu"]
