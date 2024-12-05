from odoo_somconnexio_python_client.resources.odoo_paging import Paging
from odoo_somconnexio_python_client.client import Client
from ..exceptions import ResourceNotFound

default_offset = 0
default_limit = 500
default_sortOrder = "DESCENDENT"
default_sortBy = "date_invoice"


class PagingInvoices:
    def __init__(self, invoices, paging):
        self.invoices = invoices
        self.paging = paging


class Invoice:
    _url_path = "/invoice"

    def __init__(
        self, id, name, date, total_amount, tax_amount, base_amount, status, pdf=False
    ):
        self.id = id
        self.name = name
        self.date = date
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.base_amount = base_amount
        self.status = status
        self.pdf = pdf

    @classmethod
    def search_by_customer_ref(
        cls,
        customer_ref,
        limit=default_limit,
        offset=default_offset,
        sortOrder=default_sortOrder,
        sortBy=default_sortBy,
    ):
        """
        Search Invoices in Odoo by partner's ref and control paging params.

        :return: Invoices objects if exists and controls params to pagination
        """
        params = cls._get_search_params(
            limit, offset, sortBy, sortOrder, {"customer_ref": customer_ref}
        )
        return cls._get(
            params=params,
        )

    @classmethod
    def search_by_customer_vat(
        cls,
        vat,
        limit=default_limit,
        offset=default_offset,
        sortOrder=default_sortOrder,
        sortBy=default_sortBy,
    ):
        """
        Search Invoices in Odoo by partner's vat and control paging params.

        :return: Invoices objects if exists and controls params to pagination
        """
        params = cls._get_search_params(
            limit, offset, sortBy, sortOrder, {"partner_vat": vat}
        )
        return cls._get(
            params=params,
        )

    @classmethod
    def get_by_id(cls, id):
        """
        Search Invoice in Odoo by id.

        :return: Invoice object if exists
        """
        return cls._get(id=id)

    @classmethod
    def _get_search_params(cls, limit, offset, sortBy, sortOrder, ref):
        paging = Paging(
            limit=int(limit),
            offset=int(offset),
            sortBy=sortBy,
            sortOrder=sortOrder,
        )
        paging.validate_pagination()
        params = ref
        params.update(paging.__dict__)
        return params

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

        if id:
            response = cls(**response_data)
        else:
            invoices = [
                cls(**invoice_found) for invoice_found in response_data["invoices"]
            ]
            response = PagingInvoices(
                invoices,
                Paging(**response_data.get("paging", {})),
            )

        return response
