from matchers import MatcherFull


class TestDict:
    def test_basic(self):
        expected = MatcherFull(
            {'a': 1}, {}, {}
        )

        got = {'a': 1}

        assert expected.match(got)

    def test_not_match_when_subset(self):
        expected = MatcherFull(
            {'a': 1}, {}, {}
        )

        got = {'a': 1,
               'b': 2}

        assert not expected.match(got)

    def test_not_match_when_not_subset(self):
        expected = MatcherFull(
            {'a': 2}, {}, {}
        )

        got = {'a': 1,
               'b': 2}

        assert not expected.match(got)

    def test_match_empty_dict(self):
        expected = MatcherFull({}, {}, {})
        got = {}

        assert expected.match(got)

    def test_not_match_dict_inner_dict_subset(self):
        expected = MatcherFull(
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

    def test_match_dict_inner_dict_when_not_subset(self):
        expected = MatcherFull(
            {
                'a': {
                    'bb': 11
                },
                'b': 42
            }, {}, {}
        )

        got = {
            'a': {
                'bb': 1
            },
            'b': 42,
            'c': 54
        }

        assert not expected.match(got)

    def test_not_match_dict_with_list_subset(self):
        expected = MatcherFull(
            [
                {
                    'b': [1, 3]
                }
            ], {}, {}
        )
        got = [{
            'b': [4, 3, 1, 1]
        }]

        assert not expected.match(got)

    def test_match_dict_with_list_when_not_subset(self):
        expected = MatcherFull(
            {
                'a': [1, 4]
            }, {}, {}
        )

        got = {
            'a': [1, 2, 3]
        }

        assert not expected.match(got)

    def test_not_match_structure_1_subset(self):
        expected = MatcherFull(
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
        expected = MatcherFull(
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
        expected = MatcherFull(
            {'a': 1}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_when_not_contains(self):
        expected = MatcherFull(
            {'a': 2}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_empty_dict_contains(self):
        expected = MatcherFull({}, {}, {})
        got = [{}]

        assert not expected.match(got)

    def test_match_empty_dict_not_contains(self):
        expected = MatcherFull([{}], {}, {})
        got = [[{}]]

        assert not expected.match(got)

    def test_not_match_dict_inner_dict_contains(self):
        expected = MatcherFull(
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
        expected = MatcherFull(
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
        expected = MatcherFull(
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
        expected = MatcherFull(
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
        expected = MatcherFull(
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

    def test_match_complicated_struct_dict_not_contains(self):
        expected = MatcherFull(
            {
                'a': 23,
                'b': {'bb': 22},
                'c': [1, 2],
                'expected': {
                    'dd': [
                        4, 6, 9
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
                    'ee': {'eeee': 765}
                }
            },
            {
                'a': [1, 2, 3]
            }
        ]

        assert not expected.match(got)


class TestListStrict:
    def test_empty_list_subset(self):
        expected = MatcherFull([], {}, {})
        got = []

        assert expected.match(got)

    def test_not_match_list_with_hashables_subset(self):
        expected = MatcherFull(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, '2']
        assert not expected.match(got)

    def test_list_with_hashables_not_subset(self):
        expected = MatcherFull(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 3]

        assert not expected.match(got)

    def test_list_with_hashables_not_equal_when_different_len(self):
        expected = MatcherFull(
            [1, 2, '1', '2'], {}, {}
        )

        got = ['1', 1, 2, 1, 3]

        assert not expected.match(got)

    def test_convert_int_to_str(self):
        expected = MatcherFull([1, 2], {}, {})
        got = ['1', '2', '3']

        assert not expected.match(got)

    def test_list_with_inner_list_subset(self):
        expected = MatcherFull(
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

    def test_list_with_inner_list_not_subset(self):
        expected = MatcherFull(
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
        expected = MatcherFull(
            [[]], {}, {}
        )

        got = [[]]

        assert expected.match(got)

    def test_list_with_inner_dict_subset(self):
        expected = MatcherFull(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_inner_dict_not_subset(self):
        expected = MatcherFull(
            [
                {'a': 2}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_subset(self):
        expected = MatcherFull([
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

    def test_list_with_list_of_dicts_not_subset(self):
        expected = MatcherFull([
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
        expected = MatcherFull(
            [3, 1], {}, {}
        )

        got = [[1, 2, 3],
               [3, 4, 5],
               [1, 3, 4]]

        assert not expected.match(got)

    def test_list_with_hashables_not_contains(self):
        expected = MatcherFull(
            [4, 1], {}, {}
        )

        got = [[1, 2, 3],
               [3, 4, 5],
               [1, 3]]

        assert not expected.match(got)

    def test_list_with_inner_list_contains(self):
        expected = MatcherFull(
            [1, 2], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_inner_list_not_contains(self):
        expected = MatcherFull(
            [9], {}, {}
        )

        got = [
            [2, 4, 1],
            [1],
            []
        ]

        assert not expected.match(got)

    def test_list_with_empty_inner_list_contains(self):
        expected = MatcherFull(
            [], {}, {}
        )

        got = [[]]

        assert not expected.match(got)

    def test_list_with_inner_dict_contains(self):
        expected = MatcherFull(
            [
                {'a': 1}
            ], {}, {}
        )

        got = [
            [{'a': 1, 'b': 2}]
        ]

        assert not expected.match(got)

    def test_list_with_inner_dict_not_contains(self):
        expected = MatcherFull(
            [
                {'a': 2}
            ], {}, {}
        )

        got = [
            {'a': 1, 'b': 2}
        ]

        assert not expected.match(got)

    def test_list_with_list_of_dicts_contains(self):
        expected = MatcherFull([
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
        expected = MatcherFull([
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
