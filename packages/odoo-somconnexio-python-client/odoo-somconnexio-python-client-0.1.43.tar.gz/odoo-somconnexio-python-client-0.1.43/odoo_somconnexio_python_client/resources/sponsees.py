class Sponsees:
    _url_path = "/partner/sponsees"

    def __init__(
        self, sponsorship_code, sponsees_max, sponsees_number, sponsees, **kwargs
    ):
        self.sponsorship_code = sponsorship_code
        self.sponsees_max = sponsees_max
        self.sponsees_number = sponsees_number
        self.sponsees_list = sponsees
