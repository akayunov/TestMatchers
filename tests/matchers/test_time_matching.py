from datetime import datetime, timedelta

from matchers import MatcherFull

INITIAL_TIME = '2020-01-01T00:00:00Z'


def build_step_context(start_date, end_date):
    return {
        'test_start_time': start_date,
        'test_start_time_str': start_date.strftime('%Y.%m.%d %X'),
        'step_end_time': end_date,
        'step_end_time_str': end_date.strftime('%Y.%m.%d %X'),
        'pod': 'dev0'
    }


def fmt_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def test_time_between_start_end():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull({'creation_date': INITIAL_TIME}, {}, context=context)

    got = {'creation_date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}

    assert expected.match(got)


def test_time_between_start_end_contains():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull({'creation_date': INITIAL_TIME}, {}, context=context)

    got = [{'creation_date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}]

    assert not expected.match(got)


def test_time_between_start_end_list_of_dicts():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull([{'date': INITIAL_TIME}], {}, context=context)

    got = [{'date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}]
    assert expected.match(got)


def test_time_between_start_end_list_of_dicts_contains():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull([{'date': INITIAL_TIME}], {}, context=context)

    got = [[{'date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}]]

    assert not expected.match(got)


def test_time_between_start_end_dict_of_lists():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull([{'events': [{'date': INITIAL_TIME}]}], {}, context=context
                           )

    got = [{'events': [{'date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}]}]
    assert expected.match(got)


def test_time_between_start_end_dict_of_lists_contains():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull({'events': [{'date': INITIAL_TIME}]}, {}, context=context)

    got = [{'events': [{'date': fmt_date(datetime.utcnow() - timedelta(seconds=2))}]}]
    assert not expected.match(got)


def test_time_is_less_than_test_start_time():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull({'creation_date': INITIAL_TIME, }, {}, context=context)

    got = {'creation_date': fmt_date(datetime.utcnow() - timedelta(seconds=6))}
    assert not expected.match(got)


def test_time_is_greater_than_step_end_time():
    context = build_step_context(
        datetime.utcnow() - timedelta(seconds=5),
        datetime.utcnow()
    )

    expected = MatcherFull({'creation_date': INITIAL_TIME, }, {}, context=context)

    got = {'creation_date': fmt_date(datetime.utcnow() + timedelta(seconds=1))}
    assert not expected.match(got)
