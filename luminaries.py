import datetime
import ephem
from collections import namedtuple, OrderedDict

Location = namedtuple('Location',
                      ['lat',
                       'lon'])

LUMINARIES_LOCATION = Location(lat=-45.8667,
                               lon=170.5000)


Constellation = namedtuple('Constellation',
                           ['symbol',
                            'element',
                            'character'])


class Constellation():
    ZODIAC = {'Aries': ('♈', 'Fire', 'Te Rau Tauwhare'),
              'Taurus': ('♉', 'Earth', 'Charlie Frost'),
              'Gemini': ('♊', 'Air', 'Benjamin Lowenthal'),
              'Cancer': ('♋', 'Water', 'Edgar Clinch'),
              'Leo': ('♌', 'Fire', 'Dick Mannering'),
              'Virgo': ('♍', 'Earth', 'Quee Long'),
              'Libra': ('♎', 'Air', 'Harald Nilssen'),
              'Scorpius': ('♏', 'Water', 'Joseph Pritchar'),
              'Sagittarius': ('♐', 'Fire', 'Thomas Balfour'),
              'Capricornus': ('♑', 'Earth', 'Aubert Gascoigne'),
              'Aquarius': ('♒', 'Air', 'Sook Yongsheng'),
              'Pisces': ('♓', 'Water', 'Cowell Devlin')}

    CONSTELLATION_MAPPING = {'Ophiuchus': 'Sagittarius',
                             'Sextans': 'Leo'}

    @classmethod
    def from_name(cls, name):
        constellation_name = cls.CONSTELLATION_MAPPING.get(name, name)
        symbol, element, character = cls.ZODIAC[constellation_name]
        return cls(constellation_name, symbol, element, character)

    def __init__(self, name, symbol, element, character):
        self.name = name
        self.symbol = symbol
        self.element = element
        self.character = character

    def __str__(self):
        return self.name


class Planet():
    PLANET_CHARACTERS = OrderedDict(Mercury='Walter Moody',
                                    Venus='Lydia Carver',
                                    Mars='Francis Carver',
                                    Jupiter='Alistair Lauderback',
                                    Saturn='George Shepard',
                                    Moon='Anna Wetherell',
                                    Sun='Emery Staines')

    @classmethod
    def from_name_and_date(cls, name, date):
        constructor = getattr(ephem, name)
        planet = constructor()
        planet.compute(date)
        return cls(planet, cls.PLANET_CHARACTERS[name])

    def __init__(self, ephem_planet, character):
        self._ephem_planet = ephem_planet
        self.character = character

    @property
    def name(self):
        return self._ephem_planet.name

    @property
    def mag(self):
        return self._ephem_planet.mag

    @property
    def constellation(self):
        return Constellation.from_name(ephem.constellation(self._ephem_planet)[1])

    @property
    def phase(self):
        return int(self._ephem_planet.phase)


class Sky():
    def __init__(self, date):
        self.date = date
        self._ephem = ephem.Observer()
        self._ephem.date = "{}/{}/{}".format(date.year, date.month, date.day)
        self._ephem.lat = LUMINARIES_LOCATION.lat
        self._ephem.lon = LUMINARIES_LOCATION.lon
        self.planets = [Planet.from_name_and_date(name, self._ephem.date) for name in Planet.PLANET_CHARACTERS]


class Part():
    def __init__(self, number, title, date):
        self.number = number
        self.title = title
        self.date = date
        self.sky = Sky(self.date)

    def __str__(self):
        s = 'Part {}: "{}", {}\n'.format(self.number, self.title, self.date)
        for planet in self.sky.planets:
            s += '\t{}: ({}%, {}) in {}\n'.format(planet.name,
                                                  planet.phase,
                                                  planet.mag,
                                                  planet.constellation)
            s += '\t{} and {} ({})\n\n'.format(planet.character,
                                               planet.constellation.character,
                                               planet.constellation.element)
        s += '\n\n'
        return s


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
        if not isinstance(index, int):
            raise Exception('Non-int index: {}'.format(index))
        if 0 > index > len(self._parts):
            raise KeyError('Book doesn\'t have a part number {}'.format(index))
        return self._parts[index-1]


if __name__ == "__main__":
    for part in Luminaries():
        print(part)
