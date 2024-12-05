from ..exceptions import (
    InvalidSortOrder,
    NotNumericLimit,
    NotNumericOffset,
)


class Paging:
    def __init__(self, limit, offset, sortBy, sortOrder, **kwargs):
        self.limit = limit
        self.offset = offset
        self.sortBy = sortBy
        self.sortOrder = sortOrder
        try:
            self.totalNumberOfRecords = kwargs["totalNumberOfRecords"]
        except KeyError:
            pass

    def validate_pagination(self):
        if not type(self.limit) == int:
            raise NotNumericLimit(limit=self.limit)
        if not type(self.offset) == int:
            raise NotNumericOffset(offset=self.offset)
        if self.sortOrder not in ["DESCENDENT", "ASCENDENT"]:
            raise InvalidSortOrder
