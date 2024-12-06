#
#  Copyright (c) OKB Fifth Generation, 2021.
#

class HorizontalCoords:
    _azimuth: int
    _elevation: int

    MIN_AZ = -360
    MAX_AZ = 540
    MIN_EL = -90
    MAX_EL = 90

    def __init__(self, azimuth: int = 0, elevation: int = 0):

        azimuth = int(azimuth)
        elevation = int(elevation)

        if not (self.MIN_AZ <= azimuth <= self.MAX_AZ):
            raise ValueError(
                f"Trying to create coords with invalid azimuth: '{azimuth}'. Azimuth should be from '{self.MIN_AZ}' to '{self.MAX_AZ}'.")

        if not (self.MIN_EL <= elevation <= self.MAX_EL):
            raise ValueError(
                f"Trying to create coords with invalid elevation: '{elevation}'. Elevation should be from '{self.MIN_EL}' to '{self.MAX_EL}'.")

        self._azimuth = azimuth
        self._elevation = elevation

    @property
    def azimuth(self) -> int:
        return self._azimuth

    @property
    def elevation(self) -> int:
        return self._elevation

    def __composite_values__(self):
        return self.azimuth, self.elevation

    def __eq__(self, other):
        return self.azimuth == other.azimuth and self.elevation == other.elevation


def horizontal_coords_to_dict(coords: HorizontalCoords) -> dict:
    return {'azimuth': coords.azimuth, 'elevation': coords.elevation}


def horizontal_coords_from_dict(d: dict) -> HorizontalCoords:
    return HorizontalCoords(azimuth=d['azimuth'], elevation=d['elevation'])
