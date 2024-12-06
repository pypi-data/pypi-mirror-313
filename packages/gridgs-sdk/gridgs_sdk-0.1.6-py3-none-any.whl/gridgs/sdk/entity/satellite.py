#
#  Copyright (c) OKB Fifth Generation, 2021.
#

class Satellite:
    _id: int

    def __init__(self, id: int):
        if not id or not id > 0:
            raise ValueError('Satellite id should be more then 0')
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    def __eq__(self, other):
        return self.id == other.id


def satellite_from_dict(sat: dict) -> Satellite:
    return Satellite(id=sat['id'])
