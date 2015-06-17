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
        self._ephem.time = date,
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


LUMINARIES_PARTS = (
    (1,
     'A Sphere within a Sphere',
     datetime.date(1866,  1, 27)),
    (2,
     'Auguries',
     datetime.date(1866,  2, 18)),
    (3,
     'The House of Self-undoing',
     datetime.date(1866,  3, 20)),
    (4,
     'Paenga-wha-wha',
     datetime.date(1866,  4, 27)),
    (5,
     'Weight and Lucre',
     datetime.date(1865,  5, 12)),
    (6,
     'The Widow and the Weeds',
     datetime.date(1865,  6, 18)),
    (7,
     'Domicile',
     datetime.date(1865,  7, 28)),
    (8,
     'The Truth About Aurora',
     datetime.date(1865,  8, 22)),
    (9,
     'Mutable Earth',
     datetime.date(1866,  9, 20)),
    (10,
     'Masters of Succession',
     datetime.date(1866, 11, 11)),
    (11,
     'Orion Sets When Scorpio Rises',
     datetime.date(1865, 12, 3)),
    (12,
     'The Old Moon in the Young Moon\'s Arms',
     datetime.date(1866,  1, 14)))


class Luminaries():
    def __init__(self):
        self._parts = [Part(*p) for p in sorted(LUMINARIES_PARTS, key=lambda part: part[0])]

    def __getitem__(self, index):
        print(index)
        if not isinstance(index, int):
            raise Exception('Non-int index: {}'.format(index))
        if 0 > index > len(self._parts):
            raise KeyError('Book doesn\'t have a part number {}'.format(index))
        return self._parts[index-1]
