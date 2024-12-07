import datetime
import typing

from dateutil import parser

from ._functional import try_chain

import pytz


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


def now_tz(tz):
    return datetime.datetime.now(pytz.timezone(tz))


def now_pt():
    return now_tz("US/Pacific")


def date_pt(year, month, day):
    return pytz.timezone("US/Pacific").localize(
        datetime.datetime(year, month, day, 0, 0, 0, 0)
    )


def date_utc(year, month, day):
    return pytz.timezone("UTC").localize(
        datetime.datetime(year, month, day, 0, 0, 0, 0)
    )


def date_et(year, month, day):
    return pytz.timezone("US/Eastern").localize(
        datetime.datetime(year, month, day, 0, 0, 0, 0)
    )


def now_et():
    return now_tz("US/Eastern")


def strptime(format: str) -> typing.Callable[..., datetime.datetime]:
    def _strptime(value):
        return datetime.datetime.strptime(value, format)

    return _strptime


def parse_timestamp(
    timestamp: typing.Any,
    *formats,
    raise_error=False,
    timezone=datetime.UTC,
    as_date=False,
) -> typing.Optional[datetime.datetime]:
    if not timestamp:
        return None

    if isinstance(timestamp, datetime.datetime):
        return timestamp

    chain_fns = []

    if len(formats) > 0:
        for fmt in formats:
            chain_fns.append(strptime(fmt))

    chain_fns += [
        strptime("%Y-%m-%dT%H:%M:%S.%fZ"),
        strptime("%Y-%m-%d"),
        lambda x: parser.parse(x),
    ]

    output = try_chain(chain_fns, fail=raise_error)(timestamp)
    if output:
        output.replace(tzinfo=timezone)
        return output.date() if as_date else output
    return None


def parse_date(
    date: typing.Any, *formats, raise_error=False
) -> typing.Optional[datetime.date]:
    return parse_timestamp(
        date,
        *formats,
        raise_error=raise_error,
        as_date=True,
    )
