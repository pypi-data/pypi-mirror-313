import unittest

from cast_planet.data.filters.field import DateRangeConfig, DateRangeFilter
from datetime import datetime, timedelta


class TestDateRangeFilter(unittest.TestCase):
    def test_create_date_filter_from_datetime_object(self):
        now = datetime.now()
        later = now + timedelta(hours=1)
        x = DateRangeConfig(gte=now, lte=later)
        y = DateRangeFilter(field_name='acquired', config=x)
        assert y.config.lte == later

    def test_create_date_filter_from_str(self):
        start_time = '2022-01-01T13:00'
        end_time = '2022-01-01T12:00'
        x = DateRangeConfig(gte=start_time, lte=end_time)
        y = DateRangeFilter(field_name='acquired', config=x)
        assert y.config.gte == datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
