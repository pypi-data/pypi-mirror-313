from odoo_somconnexio_python_client.client import Client


class OneShot:
    def __init__(self, name, code, price, minutes="", data="", **kwargs):
        self.code = code
        self.name = name
        self.price = price
        self.minutes = minutes
        self.data = data


class OneShotCatalog:
    _url_path = "/one-shot-catalog"

    def __init__(self, code, one_shots, **kwargs):
        self.code = code
        self.one_shots = [OneShot(**product) for product in one_shots]

    @classmethod
    def search(cls, code="21IVA", product_code="", lang="ca"):
        headers = {"Accept-Language": lang}
        response_data = Client().get(
            cls._url_path,
            params={"code": code, "product_code": product_code},
            extra_headers=headers,
        )

        pricelists = []
        for pricelist in response_data.get("pricelists"):
            pricelists.append(cls(**pricelist))
        return pricelists
