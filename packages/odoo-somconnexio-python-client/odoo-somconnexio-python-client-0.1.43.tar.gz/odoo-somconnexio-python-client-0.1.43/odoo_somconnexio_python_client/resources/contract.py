from odoo_somconnexio_python_client.client import Client
from odoo_somconnexio_python_client.resources.address import Address
from odoo_somconnexio_python_client.resources.odoo_paging import Paging

from ..exceptions import ResourceNotFound

default_limit = 100
default_offset = 0
default_sortBy = "id"
default_sortOrder = "DESCENDENT"


class PagingContracts:
    def __init__(self, contracts, paging):
        self.contracts = contracts
        self.paging = paging


class Contract:
    _url_path = "/contract"

    # TODO: Add all the needed fields in the future...
    def __init__(
        self,
        id,
        code,
        customer_firstname,
        customer_lastname,
        customer_ref,
        customer_vat,
        phone_number,
        current_tariff_product,
        technology,
        supplier,
        iban,
        ticket_number,
        date_start,
        date_end,
        is_terminated,
        fiber_signal,
        description,
        email,
        subscription_type,
        subscription_technology,
        available_operations,
        address,
        parent_contract,
        shared_bond_id,
        price,
        has_landline_phone,
        bandwidth,
        data,
        minutes,
        **kwargs
    ):
        self.id = id
        self.code = code
        self.customer_firstname = customer_firstname
        self.customer_lastname = customer_lastname
        self.customer_ref = customer_ref
        self.customer_vat = customer_vat
        self.phone_number = phone_number
        self.current_tariff_product = current_tariff_product
        self.technology = technology
        self.supplier = supplier
        self.iban = iban
        self.ticket_number = ticket_number
        self.date_start = date_start
        self.date_end = date_end
        self.is_terminated = is_terminated
        self.fiber_signal = fiber_signal
        self.description = description
        self.email = email
        self.subscription_type = subscription_type
        self.subscription_technology = subscription_technology
        self.available_operations = available_operations
        self.address = Address(**address)
        self.parent_contract_code = parent_contract
        self.shared_bond_code = shared_bond_id
        self.has_landline_phone = has_landline_phone
        self.bandwidth = bandwidth
        self.price = price
        self.data = data
        self.minutes = minutes

    @classmethod
    def search_by_customer_ref(
        cls,
        customer_ref,
        limit=default_limit,
        offset=default_offset,
        sortBy=default_sortBy,
        sortOrder=default_sortOrder,
        phone_number=None,
        subscription_type=None,
    ):
        """
        Search Contracts in Odoo by partner's ref and control paging params.
        Can filtering found contracts by phone_number and subscription_type.

        :return: Contracts objects if exists and controls params to pagination
        """
        paging = Paging(
            limit=int(limit),
            offset=int(offset),
            sortBy=sortBy,
            sortOrder=sortOrder,
        )
        paging.validate_pagination()
        params = {"customer_ref": customer_ref}
        params.update(paging.__dict__)

        if phone_number:
            params.update({"phone_number": phone_number})

        if subscription_type:
            params.update({"subscription_type": subscription_type})

        return cls._get(
            params=params,
            is_paginated=True,
        )

    @classmethod
    def search_by_customer_vat(
        cls,
        vat,
        limit=default_limit,
        offset=default_offset,
        sortBy=default_sortBy,
        sortOrder=default_sortOrder,
    ):
        """
        Search Contracts in Odoo by partner's vat and control paging params.

        :return: Contracts objects if exists and controls params to pagination
        """
        paging = Paging(
            limit=int(limit),
            offset=int(offset),
            sortBy=sortBy,
            sortOrder=sortOrder,
        )
        paging.validate_pagination()
        params = {"partner_vat": vat}
        params.update(paging.__dict__)

        return cls._get(
            params=params,
            is_paginated=True,
        )

    @classmethod
    def get_by_phone_number(cls, phone_number):
        """
        Search Contract in Odoo by phone number.

        :return: Contract object if exists
        """
        return cls._get(
            params={
                "phone_number": phone_number,
            }
        )

    @classmethod
    def get_by_code(cls, code):
        """
        Search Contract in Odoo by code reference.

        :return: Contract object if exists
        """
        return cls._get(
            params={
                "code": code,
            }
        )

    @classmethod
    def _get(cls, id=None, params={}, is_paginated=False):
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

        contracts = [
            cls(**contract_found) for contract_found in response_data["contracts"]
        ]
        response = contracts

        if is_paginated:
            response = PagingContracts(
                contracts,
                Paging(**response_data.get("paging", {})),
            )

        return response

    @classmethod
    def terminate(cls, **kwargs):
        """
        Terminate a contract.

        :param kwargs:
        :return:
        """
        return Client().post(
            "{}/terminate".format(cls._url_path),
            kwargs,
        )

    @classmethod
    def terminate_reasons(cls):
        """
        Get termination reasons from the API.

        :return: Dictionary with 'terminate_reasons' and 'terminate_user_reasons'
        """
        return Client().get(
            "{}/terminate_reasons".format(cls._url_path),
        )
