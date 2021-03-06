import datetime
from decimal import Decimal
import time
import logging

logger = logging.getLogger('django')
max_datetime = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
max_time_stamp = time.mktime(max_datetime.timetuple())


def sqlGenerateOrList(param_name, count, operation):
    index = 0
    sql_string = ''
    while index < count:
        sql_string += '{} {} %s'.format(param_name, operation)
        if index != count - 1:
            sql_string += ' OR '
        index += 1
    return sql_string


def extractInParams(request, equals_param, in_param):
    included_values = []
    equals = request.GET.get(equals_param, None)
    includes_raw = request.GET.get(in_param, None)
    if equals:
        included_values.append(equals)
    if includes_raw:
        includes = includes_raw.split(',')
        included_values = included_values + includes
    if len(included_values) == 0:
        return None
    return included_values


def getDateTimeFromTimestamp(timestamp):
    try:
        integer_stamp = int(timestamp)
    except ValueError:
        logger.error('Incorrect timestamp')
        return max_datetime

    if integer_stamp > max_time_stamp:
        logger.error('Timestamp greater than max')
        return max_datetime
    return datetime.datetime.fromtimestamp(integer_stamp)


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def calculate_token_value(value, decimals):
    return (Decimal(value) / Decimal(pow(10, decimals))).quantize(Decimal(10) ** -decimals)
