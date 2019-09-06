from datetime import datetime

import pytest

from matchers import MatchedObjExternalShareIdentity, MatchedObjKeyMaterial, MatchedObjIntegerAsString, \
    MatchedObjInteger, MatchedObjUrl, MatchedObjGuid, MatchedObjAccessToken, MatchedObjFullValue


def test_external_id_validator():
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) == 'externalshare_' + 'x' * 22 + 'ffffffff'
    assert MatchedObjExternalShareIdentity(0) == 'externalshare_' + 'x' * 22 + '00000000'

    with pytest.raises(AssertionError):
        MatchedObjExternalShareIdentity('qwe')
    with pytest.raises(AssertionError):
        MatchedObjExternalShareIdentity(None)
    assert MatchedObjExternalShareIdentity(1231) == 'externalshare_' + 'x' * 22 + '000004cf'
    with pytest.raises(AssertionError):
        MatchedObjExternalShareIdentity(['FFFFFFFF'])

    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != ''
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != None  # noqa: E711
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != {}
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != []

    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'qweqwe'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_' + 'x' * 21 + 'FFFFFFFF'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_' + 'x' * 22 + 'FFFF'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_' + 'x' * 22 + 'FFFFFFFFF'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_' + 'x' * 22 + 'AACC1141'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare' + 'x' * 22 + 'FFFFFFFF'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare' + 'x' * 22 + '000004cf'
    assert MatchedObjExternalShareIdentity(2 ** 32 - 1) != 'externalshare_' + 'x' * 22 + 'fffffffff'


def test_key_material_validator():
    assert MatchedObjKeyMaterial() != ''
    assert MatchedObjKeyMaterial() != None  # noqa: E711
    assert MatchedObjKeyMaterial() != []
    assert MatchedObjKeyMaterial() != {}
    assert MatchedObjKeyMaterial() != 12414
    assert MatchedObjKeyMaterial() != '1' * 31
    assert MatchedObjKeyMaterial() != '1' * 33
    assert MatchedObjKeyMaterial() != 'j' * 32
    assert MatchedObjKeyMaterial() != 'F' * 32
    assert MatchedObjKeyMaterial() == '1' * 32
    assert MatchedObjKeyMaterial() == '0' * 32
    assert MatchedObjKeyMaterial() == '9' * 32
    assert MatchedObjKeyMaterial() == 'a' * 32
    assert MatchedObjKeyMaterial() == 'f' * 32


def test_integer_as_str():
    assert MatchedObjIntegerAsString(0, 10) == '0'
    assert MatchedObjIntegerAsString(0, 10) == '1'
    assert MatchedObjIntegerAsString(0, 10) == '9'
    assert MatchedObjIntegerAsString(0, 10) == '10'
    assert MatchedObjIntegerAsString(0, 10) != '11'
    assert MatchedObjIntegerAsString(0, 10) != '-1'
    assert MatchedObjIntegerAsString(0, 0) != '1'
    assert MatchedObjIntegerAsString(0, 0) == '0'
    assert MatchedObjIntegerAsString(0, 10) != 2
    assert MatchedObjIntegerAsString(-2, 0) == '-1'
    with pytest.raises(ValueError):
        assert MatchedObjIntegerAsString(0, 20) != 'a'
    with pytest.raises(ValueError):
        assert MatchedObjIntegerAsString(0, 0) != '1.1'


def test_integer():
    assert MatchedObjInteger(0, 10) == 0
    assert MatchedObjInteger(0, 10) == 10
    assert MatchedObjInteger(0, 10) != -1
    assert MatchedObjInteger(0, 10) != 11
    assert MatchedObjInteger(0, 0) != 1
    assert MatchedObjInteger(0, 0) == 0
    assert MatchedObjInteger(-5, -1) == -3
    assert MatchedObjInteger(-5, -1) != 1
    assert MatchedObjInteger(0, 10) != '2'
    assert MatchedObjInteger(0, 10) != 2.2


def test_url():
    assert MatchedObjUrl('') == 'https://trataat.com'
    assert MatchedObjUrl('') == 'wss://trataat.com'
    assert MatchedObjUrl('') != 'http://trataat.com'
    assert MatchedObjUrl('') != 'wsss://trataat.com'
    assert MatchedObjUrl('') != 'asdas://trataat.com'


def test_guid():
    assert MatchedObjGuid() == '62c1a358-535d-4a37-ba9e-27c09b115832'
    assert MatchedObjGuid() != ''
    assert MatchedObjGuid() != 0
    assert MatchedObjGuid() != '62c1a358-535d-4a37-ba9e-27c09b11583_'
    assert MatchedObjGuid() != '62c1a358-535d-4a37-ba9e-27c09b11583j'


def test_access_token():
    assert MatchedObjAccessToken() == '0wqfewgegklfgkldsfg'
    assert MatchedObjAccessToken() == '2wqfewgegklfgkldsfg'
    assert MatchedObjAccessToken() == '3wqfewgegklfgkldsfg'
    assert MatchedObjAccessToken() != '5wqfewgegklfgkldsfg'
    assert MatchedObjAccessToken() == '3' + 'x' * 120
    assert MatchedObjAccessToken() != '3' + 'x' * 121
    assert MatchedObjAccessToken() != '3'


def test_full_value():
    assert MatchedObjFullValue(None, {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) == None  # noqa: E711
    assert MatchedObjFullValue(1, {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) == 1
    assert MatchedObjFullValue('qwe', {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) == 'qwe'
    assert MatchedObjFullValue(1, {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) != '1'
    assert MatchedObjFullValue(True, {}) != 1
    assert MatchedObjFullValue(False, {}) != 0


def test_date():
    assert MatchedObjFullValue(
        '2020-01-01T00:00:00Z',
        {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) == '2020-01-17T00:00:00Z'
    assert MatchedObjFullValue(
        '2020-01-01T00:00:00Z',
        {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2021, 1, 1, 0, 0, 0)}) != 42
    assert MatchedObjFullValue(
        '2020-01-01T00:00:00Z',
        {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2000, 1, 1, 0, 0, 2)}) == '2000-01-01T00:00:01Z'
    assert MatchedObjFullValue(
        '2020-01-01T00:00:00Z',
        {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2000, 1, 1, 0, 0, 2)}) != '2222-01-01T00:00:01Z'
    assert MatchedObjFullValue(
        '2020-01-01T00:00:00Z',
        {'test_start_time': datetime(2000, 1, 1, 0, 0, 0), 'step_end_time': datetime(2000, 1, 1, 0, 0, 2)}) != '1999-01-01T00:00:01Z'
