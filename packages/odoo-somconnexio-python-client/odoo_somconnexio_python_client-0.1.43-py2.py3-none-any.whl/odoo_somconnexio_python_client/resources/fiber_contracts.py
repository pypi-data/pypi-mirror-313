from odoo_somconnexio_python_client.client import Client
from odoo_somconnexio_python_client.resources.contract import Contract

from ..exceptions import ResourceNotFound


class FiberContractsToPack:
    _url_path = "/contract/available-fibers-to-link-with-mobile"

    @classmethod
    def search_by_partner_ref(cls, partner_ref, mobiles_sharing_data="false"):
        """
        Search available fiber contracts to pack by their partner reference.
        mobiles_sharing_data if true return fibers with offer mobile associated

        :return: Contract object if exists
        """
        return cls._get(
            params={
                "partner_ref": partner_ref,
                "mobiles_sharing_data": mobiles_sharing_data,
            }
        )

    @classmethod
    def _get(cls, params={}):
        url = cls._url_path

        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)

        return [Contract(**contract_found) for contract_found in response_data]
