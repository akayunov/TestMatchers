from requests import structures
from matchers import MatcherContainsKeyCaseInsensitive


class TestDict:
    def test_basic(self):
        expected = MatcherContainsKeyCaseInsensitive({'a': 1}, {}, {})
        got = structures.CaseInsensitiveDict({'A': 1})

        assert expected.match(got)

    def test_match_when_subset(self):
        expected = MatcherContainsKeyCaseInsensitive({'a': 1}, {}, {})

        got = structures.CaseInsensitiveDict({'a': 1, 'B': 2})

        assert expected.match(got)

    def test_match_when_not_subset(self):
        expected = MatcherContainsKeyCaseInsensitive(
            {'a': 2}, {}, {}
        )

        got = structures.CaseInsensitiveDict({'A': 1, 'b': 2})

        assert not expected.match(got)

    def test_match_empty_dict(self):
        expected = MatcherContainsKeyCaseInsensitive({}, {}, {})
        got = structures.CaseInsensitiveDict({})

        assert expected.match(got)
