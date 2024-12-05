from odoo_somconnexio_python_client.client import Client
from odoo_somconnexio_python_client.resources.address import Address

from .sponsees import Sponsees
from ..exceptions import ResourceNotFound


class Partner:
    _url_path = "/partner"

    # TODO: Add all the needed fields in the future...
    def __init__(
        self,
        id,
        name,
        firstname,
        lastname,
        ref,
        lang,
        vat,
        type,
        email,
        phone,
        mobile,
        cooperator_register_number,
        cooperator_end_date,
        coop_agreement_code,
        sponsor_ref,
        coop_candidate,
        member,
        addresses,
        banned_actions,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.firstname = firstname
        self.lastname = lastname
        self.ref = ref
        self.lang = lang
        self.vat = vat
        self.type = type
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.cooperator_register_number = cooperator_register_number
        self.cooperator_end_date = cooperator_end_date
        self.sponsor_ref = sponsor_ref
        self.coop_agreement_code = coop_agreement_code
        self.coop_candidate = coop_candidate
        self.member = member
        self.addresses = []
        for address in addresses:
            self.addresses.append(Address(**address))
        self.banned_actions = banned_actions

    @classmethod
    def get(cls, ref):
        """
        Get ResPartner using the ref param.

        :return: Partner object if exists
        """
        return cls._get(id=int(ref))

    @classmethod
    def search_by_vat(cls, vat):
        """
        Search ResPartner in Odoo by VAT number.

        :return: Partner object if exists
        """
        return cls._get(
            params={
                "vat": vat,
            }
        )

    @classmethod
    def check_sponsor(cls, vat, sponsor_code):
        """
        Check if partner can sponsor new partners.

        :return: True or False
        """
        if not vat or not sponsor_code:
            return False

        url = "{}/{}".format(cls._url_path, "check_sponsor")
        params = {
            "vat": vat,
            "sponsor_code": sponsor_code,
        }
        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)
        return response_data["result"] == "allowed", response_data["message"]

    @classmethod
    def sponsees(cls, ref):
        """
        Get sponsees info from a Partner using the ref param.

        :return: sponsees object if exists
        """
        url = Sponsees._url_path
        params = {"ref": ref}
        response_data = Client().get(url, params=params)
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter={})

        return Sponsees(**response_data)

    @classmethod
    def _get(cls, id=None, params={}):
        if id:
            url = "{}/{}".format(cls._url_path, id)
        else:
            url = cls._url_path

        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)

        return cls(**response_data)
