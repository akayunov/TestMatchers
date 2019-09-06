from matchers import MatcherNegative


class TestDict:
    def test_basic(self):
        expected = MatcherNegative(
            {'a': 1}, {}, {}
        )

        got = {'a': 1}

        assert not expected.match(got)
