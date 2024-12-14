import datetime


def now():
    "UTC 현재 시간"

    return datetime.datetime.now(datetime.UTC)
