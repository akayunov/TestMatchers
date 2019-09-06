from matchers import MatcherFullOrderInsensitive


class TestDict:
    def test_basic(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': 1,
                'b': [1, 2, {'a': 1, 'b': [1, 2]}]
            }, {}, {}
        )

        got = {
            'a': 1,
            'b': [2, {'b': [2, 1], 'a': 1}, 1]
        }

        assert expected.match(got)

    def test_not_match_when_subset(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 1}, {}, {}
        )

        got = {'a': 1,
               'b': 2}

        assert not expected.match(got)

    def test_not_match_by_value(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 1,
             'b': 3}, {}, {}
        )

        got = {'a': 1,
               'b': 2}

        assert not expected.match(got)

    def test_match_dict_with_null_values(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 1,
             'b': None}, {}, {}
        )

        got = {'a': 1,
               'b': None}

        assert expected.match(got)

    def test_not_match_dict_with_null_values(self):
        expected = MatcherFullOrderInsensitive(
            {'a': None,
             'b': None}, {}, {}
        )

        got = {'a': 1,
               'b': None}

        assert not expected.match(got)

    def test_match_dict_with_dummy_values(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 1,
             'b': 4}, {}, {}
        )

        got = {'a': 1,
               'b': 4}

        assert expected.match(got)

    def test_match_dict_with_bool_values(self):
        expected = MatcherFullOrderInsensitive(
            {'a': False,
             'b': True}, {}, {}
        )

        got = {'a': False,
               'b': True}

        assert expected.match(got)

    def test_not_match_dict_with_bool_values(self):
        expected = MatcherFullOrderInsensitive(
            {'a': False,
             'b': False}, {}, {}
        )

        got = {'a': False,
               'b': True}

        assert not expected.match(got)

    def test_match_empty_dict(self):
        expected = MatcherFullOrderInsensitive({}, {}, {})
        got = {}

        assert expected.match(got)

    def test_not_match_dict_inner_dict_subset(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': {
                    'bb': 11
                },
                'b': 42
            }, {}, {}
        )

        got = {
            'a': {
                'bb': 11
            },
            'b': 42,
            'c': 54
        }

        assert not expected.match(got)

    def test_match_dict_with_list_with_diff_order(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': [2, 3, 1]
            }, {}, {}
        )
        got = {
            'a': [1, 2, 3]
        }

        assert expected.match(got)

    def test_not_match_structure_1_subset(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': {
                    'b': [
                        {
                            'inner_1': 42,
                            'inner_2': {
                                'list': [
                                    {
                                        'sub': 1,
                                        'sub_1': [1, 2]
                                    }
                                ]
                            }
                        }
                    ]
                }
            }, {}, {}
        )

        got = {
            'a': {
                'b': [
                    {
                        'inner_1': 42,
                        'inner_2': {
                            'list': [
                                {
                                    'sub': 1,
                                    'sub_1': [1, 2],
                                    'sub_2': [1, 2]
                                }
                            ]
                        }
                    }
                ]
            },
            'b': {
                'z': 23
            },
            'sub_1': [1, 2]
        }

        assert not expected.match(got)

    def test_structure_1_when_not_subset(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': {
                    'b': [
                        {
                            'inner_1': 42,
                            'inner_2': {
                                'list': [
                                    {
                                        'sub': 1,
                                        'sub_1': [1, 2, 3]
                                    }
                                ]
                            }
                        }
                    ]
                },
                'sub_1': {'sub': 34}
            }, {}, {}
        )

        got = {
            'a': {
                'b': [
                    {
                        'inner_1': 42,
                        'inner_2': {
                            'list': [
                                {
                                    'sub': 1,
                                    'sub_1': [1, 2],
                                    'sub_2': [1, 2]
                                }
                            ]
                        }
                    }
                ]
            },
            'b': {
                'z': 23
            },
            'sub_1': [1, 2]
        }

        assert not expected.match(got)

    def test_match_when_contains(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 1}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_when_not_contains(self):
        expected = MatcherFullOrderInsensitive(
            {'a': 2}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_empty_dict_contains(self):
        expected = MatcherFullOrderInsensitive({}, {}, {})
        got = [{}]

        assert not expected.match(got)

    def test_match_empty_dict_not_contains(self):
        expected = MatcherFullOrderInsensitive([{}], {}, {})
        got = [[{}]]

        assert not expected.match(got)

    def test_not_match_dict_inner_dict_contains(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': {
                    'bb': 11
                },
                'b': 42
            }, {}, {}
        )

        got = [
            {
                'a': {
                    'bb': 11
                },
                'b': 42,
                'c': 54
            },
            1,
            2
        ]

        assert not expected.match(got)

    def test_match_dict_inner_dict_not_contains(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': {
                    'bb': 111
                },
                'b': 42
            }, {}, {}
        )

        got = [
            {
                'a': {
                    'bb': 11
                },
                'b': 42,
                'c': 54
            },
            1,
            2
        ]

        assert not expected.match(got)

    def test_not_match_dict_with_list_contains(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': [1, 2]
            }, {}, {}
        )

        got = [
            {
                'a': [2, 1, 3]
            },
            {
                'a': [1, 3, 9]
            }
        ]

        assert not expected.match(got)

    def test_match_dict_with_list_not_contains(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': [1, 2, 9]
            }, {}, {}
        )

        got = [
            {
                'a': [2, 1, 3]
            },
            {
                'a': [1, 3, 9]
            }
        ]

        assert not expected.match(got)

    def test_not_match_complicated_struct_dict_contains(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': 23,
                'b': {'bb': 2},
                'c': [1, 2],
                'expected': {
                    'dd': [
                        4, 6
                    ],
                    'ee': {'eee': 567}
                }
            }, {}, {}
        )

        got = [
            {
                'a': 23,
                'a1': 32,
                'b': {'bb': 2},
                'c': [2, 1],
                'expected': {
                    'dd': [
                        2, 4, 6, 8
                    ],
                    'ee': {'eee': 567, 'eeee': 765}
                }
            },
            {
                'a': [1, 2, 3]
            }
        ]

        assert not expected.match(got)

    def test_not_match_dict_complicated_struct(self):
        expected = MatcherFullOrderInsensitive(
            {
                'a': 23,
                'b': {'bb': 22},
                'c': [1, 2],
                'expected': {
                    'dd': [
                        4, 2, 8, 6
                    ],
                    'ee': {'eee': 567, 'c': []}
                },
                'cc': [5, 4, 3, 2, 1, 0, {}],
            }, {}, {}
        )

        got = [{
            'a': 23,
            'b': {'bb': 22},
            'c': [2, 1],
            'cc': [0, 1, 2, 3, 4, 5, {}],
            'expected': {
                'dd': [
                    2, 4, 6, 8
                ],
                'ee': {'eee': 567, 'c': []}
            }
        }]

        assert not expected.match(got)
