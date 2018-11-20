from time import strptime

from skyfield import almanac
from skyfield import api
from skyfield import constants
from skyfield.api import load

PLANETS = load('de421.bsp')


class AlmanacService(object):
    timescale = None

    def __init__(self):
        self.timescale = api.load.timescale()

    def search_seasons(self, from_date_string=None, to_date_string=None):
        from_time = self.parse_date_time(from_date_string)
        to_time = self.parse_date_time(to_date_string)
        t, y = almanac.find_discrete(from_time, to_time, almanac.seasons(PLANETS))
        return t, y

    def search_moon_phases(self, from_date_string=None, to_date_string=None):
        from_time = self.parse_date_time(from_date_string)
        to_time = self.parse_date_time(to_date_string)
        t, y = almanac.find_discrete(from_time, to_time, almanac.moon_phases(PLANETS))
        return t, y

    def search_zodiacs(self, planet, from_date_string=None, to_date_string=None):
        from_time = self.parse_date_time(from_date_string)
        to_time = self.parse_date_time(to_date_string)
        t, y = almanac.find_discrete(from_time, to_time, self.get_find_zodiacs_function(planet))
        return t, y

    def parse_date_time(self, date_string):
        t = strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        return self.timescale.utc(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    def get_find_zodiacs_function(self, planet):
        earth = PLANETS['earth']
        body = PLANETS[planet]

        def find_zodiac_at(t):
            bt = body.at(t)
            _, mlon, _ = bt.observe(earth).apparent().ecliptic_latlon('date')
            # Aries should start with longitude 0 until 30°, vernal equinox, then taurus...
            return (mlon.radians // (constants.tau / 12) % 12).astype(int)

        find_zodiac_at.rough_period = 28  # one zodiak change per month
        return find_zodiac_at


if __name__ == '__main__':
    service = AlmanacService()
    t, y = service.search_zodiacs('moon', from_date_string="2019-11-12T12:12:12", to_date_string="2020-11-12T12:12:12")
    for yi, ti in zip(y, t):
        print(yi, ti.utc_iso(' '))
