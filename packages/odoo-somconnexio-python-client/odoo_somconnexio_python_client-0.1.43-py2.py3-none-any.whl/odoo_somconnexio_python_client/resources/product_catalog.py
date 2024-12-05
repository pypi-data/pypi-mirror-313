from odoo_somconnexio_python_client.client import Client


class Offer:
    def __init__(self, code, price, name):
        self.name = name
        self.code = code
        self.price = price


class Product:
    def __init__(
        self,
        name,
        code,
        price,
        category="",
        minutes="",
        data="",
        bandwidth="",
        available_for=[],
        has_landline_phone=False,
        offer=None,
        **kwargs
    ):
        self.code = code
        self.name = name
        self.price = price
        self.category = category
        self.minutes = minutes
        self.data = data
        self.bandwidth = bandwidth
        self.available_for = available_for
        self.has_landline_phone = has_landline_phone
        if offer is not None:
            self.offer = Offer(**offer)
        else:
            self.offer = None


class Pack:
    def __init__(
        self,
        name,
        code,
        price,
        category,
        products,
        mobiles_in_pack,
        fiber_bandwidth="",
        has_land_line=False,
        available_for=[],
        **kwargs
    ):
        self.code = code
        self.name = name
        self.price = price
        self.category = category
        self.available_for = available_for
        self.mobiles_in_pack = mobiles_in_pack
        self.fiber_bandwidth = fiber_bandwidth
        self.has_landline_phone = has_land_line
        self.products = [Product(**product) for product in products]


class ProductCatalog:
    _url_path = "/product-catalog"

    def __init__(self, code, products, packs, **kwargs):
        self.code = code
        self.products = [Product(**product) for product in products]
        self.packs = [Pack(**pack) for pack in packs]

    @classmethod
    def search(cls, code="", category="", lang="ca", product_code=""):
        headers = {"Accept-Language": lang}
        response_data = Client().get(
            cls._url_path,
            params={"code": code, "categ": category, "product_code": product_code},
            extra_headers=headers,
        )

        pricelists = []
        for pricelist in response_data.get("pricelists"):
            pricelists.append(cls(**pricelist))
        return pricelists
