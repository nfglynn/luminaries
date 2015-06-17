import datetime
import astral
import ephem
from collections import namedtuple

Location = namedtuple('Location',
                      ['astral_name',
                       'lat',
                       'lon'])

LUMINARIES_LOCATION = Location(astral_name='Wellington',
                               lat=-45.8667,
                               lon=170.5000)


class Sky():
    def __init__(self, date):
        self.date = date
        self._astral = astral.Astral()[LUMINARIES_LOCATION.astral_name]
        self._ephem = ephem.Observer()
        self._ephem.time=date,
        self._ephem.lat = LUMINARIES_LOCATION.lat,
        self._ephem.lon = LUMINARIES_LOCATION.lon


    @property
    def moon_phase(self):
        return self._astral.moon_phase(self.date)

    @property
    def mars_mag(self):
        
        pass

    @property
    def jupiter_mag(self):
        pass

    @property
    def saturn_mag(self):
        pass


class Part():
    def __init__(self, number, title, date):
        self.number = number
        self.title = title
        self.date = date
        self.sky = Sky(self.date)


LUMINARIES_PARTS= (
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()),
    ('',
     datetime.date()))


class Luminaries():
    def __init__(self):
        self._parts = LUMINARIES_PARTS
