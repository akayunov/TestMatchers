from matchers import MatcherContains


class TestDict:
    def test_basic(self):
        expected = MatcherContains({'a': 1}, {}, {})
        got = {'a': 1}

        assert expected.match(got)

    def test_match_when_subset(self):
        expected = MatcherContains({'a': 1}, {}, {})

        got = {'a': 1, 'b': 2}

        assert expected.match(got)

    def test_match_when_not_subset(self):
        expected = MatcherContains(
            {'a': 2}, {}, {}
        )

        got = {'a': 1, 'b': 2}

        assert not expected.match(got)

    def test_match_empty_dict(self):
        expected = MatcherContains({}, {}, {})
        got = {}

        assert expected.match(got)

    def test_match_dict_inner_dict_subset(self):
        expected = MatcherContains(
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

        assert expected.match(got)

    def test_match_dict_inner_dict_when_not_subset(self):
        expected = MatcherContains(
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

    def test_match_dict_with_list_subset(self):
        expected = MatcherContains(
            [
                {
                    'b': [1, 3]
                }
            ], {}, {}
        )

        got = [{
            'b': [4, 3, 1, 3]
        }]

        assert expected.match(got)

    def test_match_dict_with_list_when_not_subset(self):
        expected = MatcherContains(
            {
                'a': [1, 4]
            }, {}, {}
        )

        got = {
            'a': [1, 2, 3]
        }

        assert not expected.match(got)

    def test_structure_1_subset(self):
        expected = MatcherContains(
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
        assert expected.match(got)

    def test_structure_1_when_not_subset(self):
        expected = MatcherContains(
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
        expected = MatcherContains(
            {'a': 1}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_when_not_contains(self):
        expected = MatcherContains(
            {'a': 2}, {}, {}
        )

        got = [{'a': 1}]

        assert not expected.match(got)

    def test_match_empty_dict_contains(self):
        expected = MatcherContains({}, {}, {})
        got = [{}]

        assert not expected.match(got)

    def test_match_empty_dict_not_contains(self):
        expected = MatcherContains([{}], {}, {})
        got = [[{}]]

        assert not expected.match(got)

    def test_match_dict_inner_dict_contains(self):
        expected = MatcherContains(
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
        expected = MatcherContains(
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

    def test_match_dict_with_list_contains(self):
        expected = MatcherContains(
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
        expected = MatcherContains(
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

    def test_match_complicated_struct_dict_contains(self):
        expected = MatcherContains(
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
        expected = MatcherContains(
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

    def test_match_dict_with_string_values(self):
        expected = MatcherContains({'a': 'b'}, {}, {})
        got = {'a': 'b', 'b': 'c'}

        assert expected.match(got)

    def test_not_match_dict_with_string_values(self):
        expected = MatcherContains({'a': 'c'}, {}, {})
        got = {'a': 'b', 'b': 'c'}

        assert not expected.match(got)

    def test_not_match_dict_with_bool_values(self):
        expected = MatcherContains({'a': True}, {}, {})
        got = {'a': False, 'b': 'c'}

        assert not expected.match(got)

    def test_match_dict_with_bool_values(self):
        expected = MatcherContains({'a': True}, {}, {})
        got = {'a': True, 'b': 'c'}

        assert expected.match(got)

    def test_not_match_dict_compare_bool_with_int(self):
        expected = MatcherContains({'a': True}, {}, {})
        got = {'a': 1, 'b': 'c'}

        assert not expected.match(got)

    def test_not_match_dict_compare_int_with_bool(self):
        expected = MatcherContains({'a': 1}, {}, {})
        got = {'a': True, 'b': 'c'}

        assert not expected.match(got)

    def test_match_dict_with_none_value(self):
        expected = MatcherContains({'a': None}, {}, {})
        got = {'a': None, 'b': 'c'}

        assert expected.match(got)

    def test_not_match_dict_compare_none_with_empty_dict(self):
        expected = MatcherContains({'a': None}, {}, {})
        got = {}

        assert not expected.match(got)

    def test_not_match_dict_compare_none_with_bool(self):
        expected = MatcherContains({'a': None}, {}, {})
        got = {'a': False}

        assert not expected.match(got)

    def test_not_match_dict_compare_bool_with_none(self):
        expected = MatcherContains({'a': False}, {}, {})
        got = {'a': None}

        assert not expected.match(got)

    def test_not_match_dict_compare_none_with_int(self):
        expected = MatcherContains({'a': None}, {}, {})
        got = {'a': 0}

        assert not expected.match(got)

    def test_not_match_dict_compare_int_with_none(self):
        expected = MatcherContains({'a': 0}, {}, {})
        got = {'a': None}

        assert not expected.match(got)

    def test_match_dict_with_float_value(self):
        expected = MatcherContains({'a': 0.1}, {}, {})
        got = {'a': 0.1, 'c': 2}

        assert expected.match(got)

    def test_not_match_dict_with_float_value(self):
        expected = MatcherContains({'a': 0.1}, {}, {})
        got = {'a': 0.11, 'c': 0.1}

        assert not expected.match(got)

    def test_not_match_dict_compare_float_with_int_1(self):
        expected = MatcherContains({'a': 1.1}, {}, {})
        got = {'a': 1, 'c': 1.1}

        assert not expected.match(got)

    def test_not_match_dict_compare_float_with_int_2(self):
        expected = MatcherContains({'a': 1.0}, {}, {})
        got = {'a': 1, 'c': 1.1}

        assert not expected.match(got)

    def test_not_match_dict_compare_int_with_float(self):
        expected = MatcherContains({'a': 2}, {}, {})
        got = {'a': 2.0, 'c': 1.1}

        assert not expected.match(got)
