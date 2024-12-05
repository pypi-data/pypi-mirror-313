class HTTPError(Exception):
    message = "Network problem accessing Odoo API. Exception: \n {}"

    def __init__(self, error_msg):
        self.message = self.message.format(error_msg)
        super(HTTPError, self).__init__(self.message)


class BadRequestError(Exception):
    message = "BadRequest with the next body: \n {}"

    def __init__(self, body):
        self.message = self.message.format(body)
        super(HTTPError, self).__init__(self.message)


class ResourceNotFound(Exception):
    message = "ResourceNotFound. Resource: {} and filter: {}"

    def __init__(self, resource, filter):
        self.message = self.message.format(resource, filter)
        super(ResourceNotFound, self).__init__(self.message)


class NotNumericLimit(Exception):
    message = "NotNumericLimit. Limit {}"

    def __init__(self, limit):
        self.message = self.message.format(limit)
        super(NotNumericLimit, self).__init__(self.message)


class NotNumericOffset(Exception):
    message = "NotNumericOffset. Limit {}"

    def __init__(self, offset):
        self.message = self.message.format(offset)
        super(NotNumericOffset, self).__init__(self.message)


class InvalidSortBy(Exception):
    message = "Invalid field to sort by. field {}"

    def __init__(self, sort_by):
        self.message = self.message.format(sort_by)
        super(InvalidSortBy, self).__init__(self.message)


class InvalidSortOrder(Exception):
    message = "Invalid sort order. It must be ASCENDENT or DESCENDENT"

    def __init__(self):
        super(InvalidSortOrder, self).__init__(self.message)
