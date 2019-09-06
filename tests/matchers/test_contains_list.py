from matchers import MatcherContains


class TestList:
    def test_empty_list_subset(self):
        expected = MatcherContains([], {}, {})
        got = []

        assert expected.match(got)

    def test_list_with_hashables_subset(self):
        expected = MatcherContains(
            [1, 2, '1', '2'], {}, {}
        )

        got = [1, 2, '1', '2']

        assert expected.match(got)

    def test_list_with_hashables_not_subset(self):
        expected = MatcherContains(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 3]

        assert not expected.match(got)

    def test_list_with_hashables_not_equal_when_different_len(self):
        expected = MatcherContains(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 1, 3]

        assert not expected.match(got)

    def test_convert_int_to_str(self):
        expected = MatcherContains([1, 2], {}, {})
        got = [1, 2, 3]

        assert expected.match(got)

    def test_list_with_inner_list_subset(self):
        expected = MatcherContains(
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

        assert expected.match(got)

    def test_list_with_inner_list_not_subset(self):
        expected = MatcherContains(
            [
                [1, 2],
                [3, 8]
            ], {}, {}
        )

        got = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]

        assert not expected.match(got)

    def test_list_with_empty_inner_list_subset(self):
        expected = MatcherContains(
            [[]], {}, {}
        )

        got = [[]]

        assert expected.match(got)

    def test_list_with_inner_dict_subset(self):
        expected = MatcherContains(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert expected.match(got)

    def test_list_with_inner_dict_not_subset(self):
        expected = MatcherContains(
            [
                {'a': 2}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_subset(self):
        expected = MatcherContains([
            [{'a': 1}],
            [{'b': 2}]
        ], {}, {})

        got = [
            [{'b': 2},
             {'a': 1}],
            [{'b': 2},
             {'s': 42}]
        ]

        assert expected.match(got)

    def test_list_with_list_of_dicts_not_subset(self):
        expected = MatcherContains([
            [{'a': 2}],
            [{'b': 2}]
        ], {}, {})

        got = [
            [{'b': 1},
             {'a': 1}],
            [{'a': 2},
             {'b': 2}]
        ]

        assert not expected.match(got)

    def test_list_with_hashables_contains(self):
        expected = MatcherContains(
            [3, 1], {}, {}
        )

        got = [[1, 2, 3],
               [3, 4, 5],
               [1, 3, 4]]

        assert not expected.match(got)

    def test_list_with_hashables_not_contains(self):
        expected = MatcherContains(
            [4, 1], {}, {}
        )

        got = [[1, 2, 3],
               [3, 4, 5],
               [1, 3]]

        assert not expected.match(got)

    def test_list_with_inner_list_contains(self):
        expected = MatcherContains(
            [1, 2], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_inner_list_not_contains(self):
        expected = MatcherContains(
            [9], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_empty_inner_list_contains(self):
        expected = MatcherContains(
            [], {}, {}
        )

        got = [[]]

        assert expected.match(got)

    def test_list_with_inner_dict_contains(self):
        expected = MatcherContains(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            [{'a': 1, 'b': 2}]
        ]

        assert not expected.match(got)

    def test_list_with_inner_dict_not_contains(self):
        expected = MatcherContains(
            [
                {'a': 2}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_contains(self):
        expected = MatcherContains([
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
        expected = MatcherContains([
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

    def test_match_list_with_str_value(self):
        expected = MatcherContains(['a'], {}, {})
        got = ['a', 'b', 'c']

        assert expected.match(got)

    def test_not_match_list_with_str_value(self):
        expected = MatcherContains(['a'], {}, {})
        got = ['aa', 'b', 'c']

        assert not expected.match(got)

    def test_match_list_with_bool_value(self):
        expected = MatcherContains([True], {}, {})
        got = [True, False, False]

        assert expected.match(got)

    def test_match_list_with_few_bool_value(self):
        expected = MatcherContains([True, False], {}, {})
        got = [True, True, False]

        assert expected.match(got)

    def test_not_match_list_with_bool_value(self):
        expected = MatcherContains([False], {}, {})
        got = [True, True]

        assert not expected.match(got)

    def test_not_match_list_compare_bool_with_empty_list(self):
        expected = MatcherContains([False], {}, {})
        got = []

        assert not expected.match(got)

    def test_not_match_list_compare_bool_with_int_1(self):
        expected = MatcherContains([False], {}, {})
        got = [0]

        assert not expected.match(got)

    def test_not_match_list_compare_bool_with_int_2(self):
        expected = MatcherContains([True], {}, {})
        got = [1]

        assert not expected.match(got)

    def test_not_match_list_compare_int_with_bool_1(self):
        expected = MatcherContains([1], {}, {})
        got = [True]

        assert not expected.match(got)

    def test_not_match_list_compare_int_with_bool_2(self):
        expected = MatcherContains([0], {}, {})
        got = [False]

        assert not expected.match(got)

    def test_match_list_with_none_value(self):
        expected = MatcherContains([None], {}, {})
        got = [None, 1, 2]

        assert expected.match(got)

    def test_not_match_list_compare_none_with_empty_list(self):
        expected = MatcherContains([None], {}, {})
        got = []

        assert not expected.match(got)

    def test_not_match_list_compare_none_with_bool(self):
        expected = MatcherContains([None], {}, {})
        got = [False]

        assert not expected.match(got)

    def test_not_match_list_compare_none_with_int(self):
        expected = MatcherContains([None], {}, {})
        got = [0]

        assert not expected.match(got)

    def test_not_match_list_compare_none_with_empty_dict(self):
        expected = MatcherContains([None], {}, {})
        got = [{}]

        assert not expected.match(got)

    def test_not_match_list_compare_float_with_int(self):
        expected = MatcherContains([1.0], {}, {})
        got = [1, 2]

        assert not expected.match(got)

    def test_not_match_list_compare_int_with_float(self):
        expected = MatcherContains([2], {}, {})
        got = [2.0, 1]

        assert not expected.match(got)
