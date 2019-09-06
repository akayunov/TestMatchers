from matchers import MatcherFullOrderInsensitive, MatchedObjInteger


import pytest


class TestList:
    def test_list_basic(self):
        expected = MatcherFullOrderInsensitive(
            [1, '2', ['r', 'q'], {'a': 1, 'b': [1, 2, 3]}], {}, {}
        )
        got = [['q', 'r'], 1, {'b': [3, 1, 2], 'a': 1, }, '2']

        assert expected.match(got)

    def test_empty_list_subset(self):
        expected = MatcherFullOrderInsensitive([], {}, {})
        got = []

        assert expected.match(got)

    def test_not_match_empty_list(self):
        expected = MatcherFullOrderInsensitive([], {}, {})
        got = [12]

        assert not expected.match(got)

    def test_not_match_list_with_two_same_values(self):
        expected = MatcherFullOrderInsensitive(
            [[1, 2, 3, 8], [1, 2, 3, 8]], {}, {}
        )
        got = [[1, 2, 8, 3], [1, 2, 4, 3]]

        assert not expected.match(got)

    def test_match_list_with_hashables_subset(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, '2']

        assert expected.match(got)

    def test_match_list_with_null_values(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2, '1', None], {}, {}
        )

        got = ['1', 1, 2, None]

        assert expected.match(got)

    def test_match_list_of_lists(self):
        expected = MatcherFullOrderInsensitive(
            [[1, 8], [9, 5, 4], [0, 0, 1]], {}, {}
        )

        got = [[4, 5, 9], [1, 0, 0], [1, 8]]

        assert expected.match(got)

    def test_not_match_list_of_lists_child_len(self):
        expected = MatcherFullOrderInsensitive(
            [[1, 8], [9, 5, 4], [0, 0, 1]], {}, {}
        )

        got = [[4, 5, 9, 0], [1, 0, 0], [1, 8]]

        assert not expected.match(got)

    def test_not_match_list_of_lists_value(self):
        expected = MatcherFullOrderInsensitive(
            [[1, 8], [9, 5, 4], [0, 0, 1]], {}, {}
        )

        got = [[4, 5, 9], [1, 0, 0], [1, 9]]

        assert not expected.match(got)

    def test_match_list_of_dicts(self):
        expected = MatcherFullOrderInsensitive(
            [{'a': 1, 'b': 2}, {'a': 1}, {'qw': 0, '45': 'rt'}], {}, {}
        )

        got = [{'qw': 0, '45': 'rt'}, {'a': 1, 'b': 2}, {'a': 1}]

        assert expected.match(got)

    def test_not_match_list_of_dicts_value(self):
        expected = MatcherFullOrderInsensitive(
            [{'a': 1, 'b': '4'}, {'a': 1}, {'qw': 0, '45': 'rt'}], {}, {}
        )

        got = [{'qw': 0, '45': 'rt'}, {'a': 1, 'b': 2}, {'a': 1}]

        assert not expected.match(got)

    def test_match_list_with_dict_with_null_values(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2, '1', {'a': None, 'b': 1}], {}, {}
        )

        got = ['1', 1, 2, {'a': None, 'b': 1}]

        assert expected.match(got)

    def test_list_with_hashables_not_subset(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 3]

        assert not expected.match(got)

    def test_list_with_hashables_not_equal_when_different_len(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 1, '2']

        assert not expected.match(got)

    def test_convert_int_to_str(self):
        expected = MatcherFullOrderInsensitive([1, 2, 3], {}, {})
        got = ['1', '2', '3']

        assert not expected.match(got)

    def test_list_with_inner_list_subset(self):
        expected = MatcherFullOrderInsensitive(
            [
                [1, 2],
                [3, 4]
            ], {}, {}
        )

        got = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]

        assert not expected.match(got)

    def test_list_with_empty_inner_list_subset(self):
        expected = MatcherFullOrderInsensitive(
            [[]], {}, {}
        )

        got = [[]]

        assert expected.match(got)

    def test_list_with_inner_dict_subset(self):
        expected = MatcherFullOrderInsensitive(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_subset(self):
        expected = MatcherFullOrderInsensitive([
            [{'a': 1}],
            [{'b': 2}]
        ], {}, {})

        got = [
            [{'b': 2},
             {'a': 1}],
            [{'b': 2},
             {'s': 42}]
        ]

        assert not expected.match(got)

    def test_list_with_hashables_contains(self):
        expected = MatcherFullOrderInsensitive(
            [3, 1], {}, {}
        )

        got = [[1, 2, 3],
               [3, 4, 5],
               [1, 3, 4]]

        assert not expected.match(got)

    def test_list_with_inner_list_contains(self):
        expected = MatcherFullOrderInsensitive(
            [1, 2], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_inner_list_not_contains(self):
        expected = MatcherFullOrderInsensitive(
            [9], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_empty_inner_list_contains(self):
        expected = MatcherFullOrderInsensitive(
            [], {}, {}
        )

        got = [[]]

        assert not expected.match(got)

    def test_list_with_inner_dict_contains(self):
        expected = MatcherFullOrderInsensitive(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            [{'a': 1, 'b': 2}]
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_contains(self):
        expected = MatcherFullOrderInsensitive([
            [{'a': 1}]
        ], {}, {})

        got = [
            [
                [
                    {'b': 2},
                    {'a': 1}
                ],
                [
                    {'b': 2},
                    {'s': 42}
                ]
            ]
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_not_not_contains(self):
        expected = MatcherFullOrderInsensitive([
            [{'a': 1}]
        ], {}, {})

        got = [
            [
                [
                    {'b': 2},
                    {'a': [1]}
                ],
                [
                    {'b': 2},
                    {'s': 42}
                ]
            ]
        ]

        assert not expected.match(got)

    @pytest.mark.xfail(
        reason='__eq__ function of MatchedObjContainsOrderInsensitiveList not completed. Will be fixed in future')
    def test_match_with_greedy_matcher(self):
        expected = MatcherFullOrderInsensitive(
            [{'a': MatchedObjInteger(0, 10)},
             {'a': 10}
             ], {}, {}
        )
        got = [{'a': 10}, {'a': 0}]
        assert expected.match(got)
