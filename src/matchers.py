import difflib
import json
import re

from collections import UserDict, UserList
from datetime import datetime, timedelta
import copy

import requests
import pytz

DEFAULT_INITIAL_TIME = 1577836800  # default time in tests
TIME_DELTA_WITH_SERVER = timedelta(0)  # set to diff in time zone value
IS_FAKE_MODE = False  # mode in which fake time works


class MatcherJsonEnc(json.JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, (UserDict, UserList)):
            return o.data
        elif isinstance(o, (MatchedObjFullValue,)):
            return o.value
        else:
            return str(o)


class MatchedObjMixin:
    def format_diff(self, other):
        return '\n'.join(
            difflib.unified_diff(
                json.dumps(self, cls=MatcherJsonEnc, indent=4, sort_keys=True).split('\n'),
                # encode class need because for header "other" can be requests.structures.CaseInsensitiveDict type
                # or bytes in case GET file
                json.dumps(other, cls=MatcherJsonEnc, indent=4, sort_keys=True).split('\n'),
                n=1000)
        )


class MatchedObjContainsDict(UserDict, MatchedObjMixin):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        if type(other) is dict:  # pylint: disable=unidiomatic-typecheck
            return all(k in other and self[k] == other[k] for k in self)
        return False


class MatchedObjContainsList(UserList, MatchedObjMixin):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        if type(other) is not list:  # pylint: disable=unidiomatic-typecheck
            return False
        # 1) so complex because of next test case
        # [1, 1, 2] is contained in [3, 1, 2, 3, 1, 2] is true

        # 2) can't use set.issubset(another_set) because of multiple same object set([1,2,3]) == set([1,2])
        other_iter = iter(other)
        for self_item in self:
            for other_item in other_iter:
                if self_item == other_item:
                    break
            else:
                return False
        return True


class MatchedObjFullList(MatchedObjContainsList):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        if super().__eq__(other):
            return len(self) == len(other)
        return False


class MatchedObjFullDict(MatchedObjContainsDict):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        if super().__eq__(other):
            return len(self) == len(other)
        return False


class MatchedObjContainsOrderInsensitiveList(MatchedObjContainsList):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        # 1) we need copy.copy and remove item from "got" because of next test case, just run test for plugin
        # [1, 1, 2] is contained in [2, 1, 2, 3, 1, 3] is true

        # 2) can't use set.issubset(another_set) because of multiple same object: set([1,1,2]) -> set(1,2)

        # 3) It also possible that this code raise false positive in case using greedy matchers like MatchedObjInteger, for example
        # expected = MatcherContainsOrderInsensitive([{'a': MatchedObjInteger(0, 10)}, {'a': 10}], {}, {})
        # got = [{'a': 10}, {'a': 0}]
        # assert not expected.match(got) - not match because MatchedObjInteger(0, 10) can match with {'a': 10}
        # and it means that for {'a': 10} won't be suitable pair. But if we match {'a': 10} first,
        # then MatchedObjInteger(0, 10) can be matched with {'a': 0} and test will pass. Not a big problem for now.

        other = copy.copy(other)
        if type(other) is list:  # pylint: disable=unidiomatic-typecheck
            for s in self:
                for o in other:
                    if s == o:
                        del other[other.index(o)]
                        break
                else:
                    return False
            return True
        return False


class MatchedObjFullOrderInsensitiveList(MatchedObjContainsOrderInsensitiveList):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        if super().__eq__(other):
            return len(self) == len(other)
        return False


class MatchedObjContainsKeyCaseInsensitiveDict(MatchedObjContainsDict):  # pylint: disable=too-many-ancestors
    def __eq__(self, other):
        # only for headers comparision
        if type(other) is requests.structures.CaseInsensitiveDict:  # pylint: disable=unidiomatic-typecheck
            return all(k in other and self[k] == other[k] for k in self)
        return False


class MatchedObjFullValue(MatchedObjMixin):
    # strftime/strptime heavy load operation so do it once
    INITIAL_DATE_BY_FMTS = {
        fmt: datetime.utcfromtimestamp(DEFAULT_INITIAL_TIME).strftime(fmt) for fmt in
        ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.0Z', '%a, %d %b %Y %H:%M:%S GMT')
    }
    INITIAL_DATE_BY_FMTS_WITH_TZ = {
        '%m-%d-%YT%H-%M-%S EST': pytz.timezone('UTC').localize(
            datetime.utcfromtimestamp(DEFAULT_INITIAL_TIME)
        ).astimezone(pytz.timezone('EST')).replace(tzinfo=None).strftime('%m-%d-%YT%H-%M-%S EST')}

    # we don't have contains value matcher because right way is use matcher with more strict logic like regexp
    def __init__(self, value, context):
        self.value = value
        self.context = context

    def __eq__(self, other):
        # Need to check types because in python True == 1 and False == 0
        if type(self.value) is type(other) and self.value == other:
            return True
        else:
            # may be it's date in local mode
            if not IS_FAKE_MODE:
                if type(other) is str and 'test_start_time' in self.context and 'step_end_time' in self.context:  # pylint: disable=unidiomatic-typecheck
                    return self.is_date_in_interval(other, self.context['test_start_time'], self.context['step_end_time'])

    def __str__(self):
        return str(self.value)

    def is_date_in_interval(self, other, low, high):
        date = self.parse_datetime(other)
        if type(date) is not datetime:  # pylint: disable=unidiomatic-typecheck
            return False
        return low - TIME_DELTA_WITH_SERVER <= date <= high - TIME_DELTA_WITH_SERVER

    def parse_datetime(self, other):
        # try to parse date. In local server can't be any sleep so
        # it's means that self.value will always equal to conf.default_initial_time so just find out format string and validate date
        # to avoid this logic we can use something like "$func.validate_integer_as_string(0)" for date field in test,
        # but don't think that QA's will be happy about this
        # if you still want sleep in local server, then you also can compare self.value to conf.default_initial_time + sleep time
        # it's doesn't look hard
        for fmt in self.INITIAL_DATE_BY_FMTS:
            if self.value == self.INITIAL_DATE_BY_FMTS[fmt]:
                return datetime.strptime(other, fmt)

        if self.value == self.INITIAL_DATE_BY_FMTS_WITH_TZ['%m-%d-%YT%H-%M-%S EST']:
            _, zone = other.split(' ')
            dt = datetime.strptime(other, '%m-%d-%YT%H-%M-%S EST')
            tz = pytz.timezone(zone)
            target_tz = pytz.timezone('UTC')
            target_dt = tz.localize(dt).astimezone(target_tz)
            return target_dt.replace(tzinfo=None)


class MatchedObjExternalShareIdentity(MatchedObjFullValue):
    org_id_re = re.compile(r'\A[a-f\d]{8}\Z')

    def __init__(self, org_id):
        try:
            org_id = format(int(org_id), '08x').lower()
        except Exception:
            raise AssertionError(
                fr'You try to create grantee_identity object from string {org_id}, org_id should looks like HEX(\d+)'
            )

        if not self.org_id_re.match(org_id):
            raise AssertionError(
                fr'You try to create grantee_identity object from string {org_id}, org_id should looks like HEX(\d+)'
            )
        self.externalshare_regexp = re.compile(r'\Aexternalshare_[a-zA-Z\d]{22}' + org_id + r'\Z', re.S | re.X | re.M)
        super().__init__(self.externalshare_regexp.pattern, {})

    def __eq__(self, other):
        if type(other) is str:  # pylint: disable=unidiomatic-typecheck
            return bool(self.externalshare_regexp.match(other))
        return False


class MatchedObjKeyMaterial(MatchedObjFullValue):
    key_material_regexp = re.compile(r'\A[\da-f]{32}\Z', re.S | re.X | re.M)

    def __init__(self):
        super().__init__(self.key_material_regexp, {})

    def __eq__(self, other):
        if type(other) is str:  # pylint: disable=unidiomatic-typecheck
            return bool(self.key_material_regexp.match(other))
        return False


class MatchedObjAccessToken(MatchedObjFullValue):
    access_token_regexp = re.compile(r'\A[0-3][-\w]{1,120}\Z', re.S | re.X | re.M)

    def __init__(self, ):
        super().__init__(self.access_token_regexp.pattern, {})

    def __eq__(self, other):
        if isinstance(other, (str,)):
            return bool(self.access_token_regexp.match(other))
        else:
            return False


class MatchedObjGuid(MatchedObjFullValue):
    guid_regexp = re.compile(r'\A[a-f\d]{8}[-][a-f\d]{4}[-][a-f\d]{4}[-][a-f\d]{4}[-][a-f\d]{12}\Z', re.I | re.S | re.X | re.M)

    def __init__(self, ):
        super().__init__(self.guid_regexp, {})

    def __eq__(self, other):
        if isinstance(other, (str,)):
            return bool(self.guid_regexp.match(other))
        return False


class MatchedObjUrl(MatchedObjFullValue):
    def __init__(self, value):
        super().__init__(value, {})
        # TODO regexp should contain service and pod name
        self.url_regexp = re.compile(r'\A(https|wss)://.*\Z', re.I | re.S | re.X | re.M)

    def __eq__(self, other):
        if isinstance(other, (str,)):
            return bool(self.url_regexp.match(other))
        return False


class MatchedObjInteger(MatchedObjFullValue):
    def __init__(self, min_, max_=2 ** 32 - 1):
        super().__init__(f'[{min_}: {max_}]', {})
        self.min = min_
        self.max = max_

    def __eq__(self, other):
        if isinstance(other, (int,)):
            return self.min <= other <= self.max
        return False


class MatchedObjIntegerAsString(MatchedObjInteger):
    def __eq__(self, other):
        if isinstance(other, (str,)):
            return super().__eq__(int(other))
        return False


class MatchedObjSecuriSyncVersion(MatchedObjFullValue):
    re_version = re.compile(r'2[.]\d{2}[.]\d{1,2}(\s[-]\d+[-]\w+)?', re.I | re.S | re.X | re.M)

    def __init__(self):
        super().__init__(self.re_version, {})

    def __eq__(self, other):
        if isinstance(other, (str,)):
            return bool(self.re_version.match(other))
        return False


class MatchedObjStringPart(MatchedObjFullValue):
    def __eq__(self, other):
        if isinstance(other, (str,)):
            return self.value in other
        elif isinstance(other, (bytes,)):
            return self.value in other.decode()
        return False


# ======================================================================================================

class MatcherContains:
    list_matcher = MatchedObjContainsList
    dict_matcher = MatchedObjContainsDict
    value_matcher = MatchedObjFullValue

    def __init__(self, expected, env, context):
        self.context = context
        # expand_recursive - function to expand macros in tests
        # self.expected_matcher = self._convert(expand_recursive(expected, env))
        self.expected_matcher = self._convert(expected)

    def _convert(self, struct):
        if isinstance(struct, (MatchedObjMixin,)):
            # sometime we use validator obj in test file, something like "$func.validate_integer_as_string(0)"
            return struct

        elif isinstance(struct, dict):
            matcher_obj = self.dict_matcher(struct)
            for key in matcher_obj:
                matcher_obj[key] = self._convert(matcher_obj[key])
            return matcher_obj

        elif isinstance(struct, list):
            matcher_obj = self.list_matcher(struct)
            for index, _ in enumerate(matcher_obj):
                matcher_obj[index] = self._convert(matcher_obj[index])
            return matcher_obj

        else:
            return self.value_matcher(struct, context=self.context)

    def match(self, got):
        return self.expected_matcher == got

    def get_diff(self, got):
        return self.expected_matcher.format_diff(got)


class MatcherFull(MatcherContains):
    list_matcher = MatchedObjFullList
    dict_matcher = MatchedObjFullDict
    value_matcher = MatchedObjFullValue


class MatcherContainsOrderInsensitive(MatcherContains):
    list_matcher = MatchedObjContainsOrderInsensitiveList
    dict_matcher = MatchedObjContainsDict
    value_matcher = MatchedObjFullValue


class MatcherFullOrderInsensitive(MatcherFull):
    list_matcher = MatchedObjFullOrderInsensitiveList
    dict_matcher = MatchedObjFullDict
    value_matcher = MatchedObjFullValue


class MatcherNegative(MatcherFull):
    def match(self, got):
        return self.expected_matcher != got

    def get_diff(self, got):
        return 'Negative object are equals, so there is no any diff.'


class MatcherContainsKeyCaseInsensitive(MatcherFull):
    # only for headers comparision
    dict_matcher = MatchedObjContainsKeyCaseInsensitiveDict
