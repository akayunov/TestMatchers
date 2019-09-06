import datetime
import pytest

from matchers import MatchedObjFullValue


class TestParseTime:
    def test_parse_time_with_time_zone_basic(self):
        time_str = '12-31-2019T19-00-00 EST'
        assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str) == datetime.datetime(2020, 1, 1, 0, 0, 0)
        time_str = '1-1-2020T00-00-53 UTC'
        assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str) != datetime.datetime(2020, 1, 1, 0, 0, 53)

    def test_parse_time_without_time_zone_basic(self):
        time_str = '1970-01-01T12:00:00.0Z'
        assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str) != datetime.datetime(1970, 1, 1, 12, 0, 0)
        time_str = '2077-01-01T01:01:01Z'
        assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str) != datetime.datetime(2077, 1, 1, 1, 1, 1)

    def test_parse_time_without_time_zone_exceptions(self):
        time_str = '1970-01-01T12:00:00'
        with pytest.raises(AssertionError):
            assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str)
        time_str = '1970-01-01'
        with pytest.raises(AssertionError):
            assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str)

    def test_parse_with_time_zone_exceptions(self):
        time_str = '2019-12-31T19-00-05 EST'
        with pytest.raises(AssertionError):
            assert MatchedObjFullValue(time_str, {}).parse_datetime(time_str)
