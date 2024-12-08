import datetime
from decimal import Decimal
import re
import time
import base64
from glitter_sdk.core.msgs import Arguments
from glitter_proto.blockved.glitterchain.index import Argument as Argument_pb
from glitter_proto.blockved.glitterchain.index import *
from glitter_sdk.exceptions import SQLError, ParamError
from glitter_sdk.util.constants import FIELD_TYPE


def to_glitter_arguments(args: List) -> Arguments:
    """
    Convert a list of Python arguments to Glitter Arguments protobuf.

    Args:
    args: List of arguments

    Returns:
    Arguments protobuf message

    Raises:
    ValueError if args is empty or contains unsupported types
    """
    if len(args) == 0:
        raise ValueError("args is empty")

    rst = []
    for arg in args:
        if isinstance(arg, int):
            rst.append(Argument_pb(ArgumentVarType.INT, str(arg)))
            continue
        if isinstance(arg, float):
            rst.append(Argument_pb(ArgumentVarType.FLOAT, str(arg)))
            continue
        if isinstance(arg, bool):
            rst.append(Argument_pb(ArgumentVarType.BOOL, str(arg)))
            continue
        if isinstance(arg, str):
            rst.append(Argument_pb(type=ArgumentVarType.STRING, value=arg))
            continue
        if isinstance(arg, bytes):
            rst.append(Argument_pb(ArgumentVarType.BYTES, base64.standard_b64encode(arg).decode("ascii")))
            continue
        raise ValueError("type is not support")

    return Arguments(rst)

def build_batch_insert_statement(table: str, columns: List, row_values: List[List]):
    """
    Build a SQL statement for batch insertion.

    Args:
      table: Name of the table
      columns: List of column names
      row_values: List of rows, each row is a list of values

    Returns:
      SQL statement string and Arguments protobuf containing values

    Raises:
      ValueError if a row does not match columns length
    """
    sql = "INSERT INTO {} ({}) VALUES ".format(table, ",".join(columns))
    repeat = len(columns) - 1
    placeholder = " (?" + ",?" * repeat + ")"
    placeholder = placeholder + ("," + placeholder) * (len(row_values) - 1)
    sql = sql + placeholder
    values = Arguments()
    for row in row_values:
        if len(row) != len(columns):
            raise ValueError("length of value is not correct")
        value = to_glitter_arguments(row)
        values.append(value)

    return sql, values


def build_update_statement(database_name: str, table_name: str, columns: map = None, where_equal: map = None):
    """
    Build a SQL UPDATE statement where connected by and.

    Args:
      database_name: Database name
      table_name: Table name
      columns: Dict of column name to new value
      where_equal: Dict of column name to value for WHERE clause

    Returns:
      SQL statement string, Arguments protobuf with values
    """

    update = []
    cond_vals = []
    for col_name, col_val in columns.items():
        update.append("{}=?".format(col_name))
        cond_vals.append(col_val)

    where_cond = []
    if where_equal:
        for col_name, col_val in where_equal.items():
            where_cond.append("{}=?".format(col_name))
            cond_vals.append(col_val)
    cond_vals_args = to_glitter_arguments(cond_vals)

    sql = "UPDATE  {}.{} SET {} WHERE {} ".format(database_name, table_name, ",".join(update), " and ".join(where_cond))

    return sql, cond_vals_args


def build_delete_statement(database_name: str, table_name: str, where: map, order_by: str, asc: bool, limit: int):
    """Build a DELETE SQL statement.

    Args:
      database_name: Database name
      table_name: Table name
      where: Dict of column name to value for WHERE clause
      order_by: Column to order by
      asc: Ascending order if True, otherwise descending
      limit: Limit number of rows

    Returns:
      SQL string, Arguments protobuf with values
    """

    where_cond = []
    where_vals = []
    if where:
        for col_name, col_val in where.items():
            where_cond.append("{}=?".format(col_name))
            where_vals.append(col_val)
    where_val_args = to_glitter_arguments(where_vals)

    sql = "DELETE FROM {}.{} WHERE {} ".format(database_name, table_name, " AND ".join(where_cond))

    if order_by:
        sql += " ORDER BY {} {}".format(order_by, "ASC" if asc else "DESC")
    if limit > 0:
        sql += " LIMIT {}".format(limit)

    return sql, where_val_args


def prepare_sql(sql_tpl: str, args: (list, tuple)):
    return sql_tpl % escape_args(args)


def escape_args(args):
    # take example by  https://github.com/PyMySQL/PyMySQL, a pure python client
    if isinstance(args, (tuple, list)):
        return tuple(literal(arg) for arg in args)
    elif isinstance(args, dict):
        return {key: literal(val) for (key, val) in args.items()}
    else:
        # If it's not a dictionary let's try escaping it anyways.
        # Worst case it will throw a Value error
        return escape(args)

def literal(obj):
    """Alias for escape()

    Non-standard, for internal use; do not use this in your applications.
    """
    return escape(obj, encoders)

def escape(obj, mapping=None):
    """Escape whatever value you pass to it.

    Non-standard, for internal use; do not use this in your applications.
    """
    if isinstance(obj, str):
        return "'" + escape_string(obj) + "'"
    if isinstance(obj, (bytes, bytearray)):
        ret = escape_bytes(obj)
        return ret
    return escape_item(obj, "utf8mb4", mapping=mapping)

def escape_item(val, charset, mapping=None):
    if mapping is None:
        mapping = encoders
    encoder = mapping.get(type(val))

    # Fallback to default when no encoder found
    if not encoder:
        try:
            encoder = mapping[str]
        except KeyError:
            raise TypeError("no default type converter defined")

    if encoder in (escape_dict, escape_sequence):
        val = encoder(val, charset, mapping)
    else:
        val = encoder(val, mapping)
    return val


def escape_dict(val, charset, mapping=None):
    n = {}
    for k, v in val.items():
        quoted = escape_item(v, charset, mapping)
        n[k] = quoted
    return n


def escape_sequence(val, charset, mapping=None):
    n = []
    for item in val:
        quoted = escape_item(item, charset, mapping)
        n.append(quoted)
    return "(" + ",".join(n) + ")"


def escape_set(val, charset, mapping=None):
    return ",".join([escape_item(x, charset, mapping) for x in val])


def escape_bool(value, mapping=None):
    return str(int(value))


def escape_int(value, mapping=None):
    return str(value)


def escape_float(value, mapping=None):
    s = repr(value)
    if s in ("inf", "nan"):
        raise SQLError("%s can not be used with MySQL" % s)
    if "e" not in s:
        s += "e0"
    return s


_escape_table = [chr(x) for x in range(128)]
_escape_table[0] = "\\0"
_escape_table[ord("\\")] = "\\\\"
_escape_table[ord("\n")] = "\\n"
_escape_table[ord("\r")] = "\\r"
_escape_table[ord("\032")] = "\\Z"
_escape_table[ord('"')] = '\\"'
_escape_table[ord("'")] = "\\'"


def escape_string(value, mapping=None):
    """escapes *value* without adding quote.

    Value should be unicode
    """
    return value.translate(_escape_table)


def escape_bytes_prefixed(value, mapping=None):
    return "_binary'%s'" % value.decode("ascii", "surrogateescape").translate(
        _escape_table
    )


def escape_bytes(value, mapping=None):
    return "'%s'" % value.decode("ascii", "surrogateescape").translate(_escape_table)


def escape_str(value, mapping=None):
    return "'%s'" % escape_string(str(value), mapping)


def escape_None(value, mapping=None):
    return "NULL"


def escape_timedelta(obj, mapping=None):
    seconds = int(obj.seconds) % 60
    minutes = int(obj.seconds // 60) % 60
    hours = int(obj.seconds // 3600) % 24 + int(obj.days) * 24
    if obj.microseconds:
        fmt = "'{0:02d}:{1:02d}:{2:02d}.{3:06d}'"
    else:
        fmt = "'{0:02d}:{1:02d}:{2:02d}'"
    return fmt.format(hours, minutes, seconds, obj.microseconds)


def escape_time(obj, mapping=None):
    if obj.microsecond:
        fmt = "'{0.hour:02}:{0.minute:02}:{0.second:02}.{0.microsecond:06}'"
    else:
        fmt = "'{0.hour:02}:{0.minute:02}:{0.second:02}'"
    return fmt.format(obj)


def escape_datetime(obj, mapping=None):
    if obj.microsecond:
        fmt = "'{0.year:04}-{0.month:02}-{0.day:02} {0.hour:02}:{0.minute:02}:{0.second:02}.{0.microsecond:06}'"
    else:
        fmt = "'{0.year:04}-{0.month:02}-{0.day:02} {0.hour:02}:{0.minute:02}:{0.second:02}'"
    return fmt.format(obj)


def escape_date(obj, mapping=None):
    fmt = "'{0.year:04}-{0.month:02}-{0.day:02}'"
    return fmt.format(obj)


def escape_struct_time(obj, mapping=None):
    return escape_datetime(datetime.datetime(*obj[:6]))


def Decimal2Literal(o, d):
    return format(o, "f")


def _convert_second_fraction(s):
    if not s:
        return 0
    # Pad zeros to ensure the fraction length in microseconds
    s = s.ljust(6, "0")
    return int(s[:6])


DATETIME_RE = re.compile(
    r"(\d{1,4})-(\d{1,2})-(\d{1,2})[T ](\d{1,2}):(\d{1,2}):(\d{1,2})(?:.(\d{1,6}))?"
)


def convert_datetime(obj):
    """Returns a DATETIME or TIMESTAMP column value as a datetime object:

      >>> datetime_or_None('2007-02-25 23:06:20')
      datetime.datetime(2007, 2, 25, 23, 6, 20)
      >>> datetime_or_None('2007-02-25T23:06:20')
      datetime.datetime(2007, 2, 25, 23, 6, 20)

    Illegal values are returned as None:

      >>> datetime_or_None('2007-02-31T23:06:20') is None
      True
      >>> datetime_or_None('0000-00-00 00:00:00') is None
      True

    """
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode("ascii")

    m = DATETIME_RE.match(obj)
    if not m:
        return convert_date(obj)

    try:
        groups = list(m.groups())
        groups[-1] = _convert_second_fraction(groups[-1])
        return datetime.datetime(*[int(x) for x in groups])
    except ValueError:
        return convert_date(obj)


TIMEDELTA_RE = re.compile(r"(-)?(\d{1,3}):(\d{1,2}):(\d{1,2})(?:.(\d{1,6}))?")


def convert_timedelta(obj):
    """Returns a TIME column as a timedelta object:

      >>> timedelta_or_None('25:06:17')
      datetime.timedelta(1, 3977)
      >>> timedelta_or_None('-25:06:17')
      datetime.timedelta(-2, 83177)

    Illegal values are returned as None:

      >>> timedelta_or_None('random crap') is None
      True

    Note that MySQL always returns TIME columns as (+|-)HH:MM:SS, but
    can accept values as (+|-)DD HH:MM:SS. The latter format will not
    be parsed correctly by this function.
    """
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode("ascii")

    m = TIMEDELTA_RE.match(obj)
    if not m:
        return obj

    try:
        groups = list(m.groups())
        groups[-1] = _convert_second_fraction(groups[-1])
        negate = -1 if groups[0] else 1
        hours, minutes, seconds, microseconds = groups[1:]

        tdelta = (
                datetime.timedelta(
                    hours=int(hours),
                    minutes=int(minutes),
                    seconds=int(seconds),
                    microseconds=int(microseconds),
                )
                * negate
        )
        return tdelta
    except ValueError:
        return obj


TIME_RE = re.compile(r"(\d{1,2}):(\d{1,2}):(\d{1,2})(?:.(\d{1,6}))?")


def convert_time(obj):
    """Returns a TIME column as a time object:

      >>> time_or_None('15:06:17')
      datetime.time(15, 6, 17)

    Illegal values are returned as None:

      >>> time_or_None('-25:06:17') is None
      True
      >>> time_or_None('random crap') is None
      True

    Note that MySQL always returns TIME columns as (+|-)HH:MM:SS, but
    can accept values as (+|-)DD HH:MM:SS. The latter format will not
    be parsed correctly by this function.

    Also note that MySQL's TIME column corresponds more closely to
    Python's timedelta and not time. However if you want TIME columns
    to be treated as time-of-day and not a time offset, then you can
    use set this function as the converter for FIELD_TYPE.TIME.
    """
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode("ascii")

    m = TIME_RE.match(obj)
    if not m:
        return obj

    try:
        groups = list(m.groups())
        groups[-1] = _convert_second_fraction(groups[-1])
        hours, minutes, seconds, microseconds = groups
        return datetime.time(
            hour=int(hours),
            minute=int(minutes),
            second=int(seconds),
            microsecond=int(microseconds),
        )
    except ValueError:
        return obj


def convert_date(obj):
    """Returns a DATE column as a date object:

      >>> date_or_None('2007-02-26')
      datetime.date(2007, 2, 26)

    Illegal values are returned as None:

      >>> date_or_None('2007-02-31') is None
      True
      >>> date_or_None('0000-00-00') is None
      True

    """
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode("ascii")
    try:
        return datetime.date(*[int(x) for x in obj.split("-", 2)])
    except ValueError:
        return obj


def through(x):
    return x


convert_bit = through

encoders = {
    bool: escape_bool,
    int: escape_int,
    float: escape_float,
    str: escape_str,
    bytes: escape_bytes,
    tuple: escape_sequence,
    list: escape_sequence,
    set: escape_sequence,
    frozenset: escape_sequence,
    dict: escape_dict,
    type(None): escape_None,
    datetime.date: escape_date,
    datetime.datetime: escape_datetime,
    datetime.timedelta: escape_timedelta,
    datetime.time: escape_time,
    time.struct_time: escape_struct_time,
    Decimal: Decimal2Literal,
}

decoders = {
    FIELD_TYPE.BIT: convert_bit,
    FIELD_TYPE.TINY: int,
    FIELD_TYPE.SHORT: int,
    FIELD_TYPE.LONG: int,
    FIELD_TYPE.FLOAT: float,
    FIELD_TYPE.DOUBLE: float,
    FIELD_TYPE.LONGLONG: int,
    FIELD_TYPE.INT24: int,
    FIELD_TYPE.YEAR: int,
    FIELD_TYPE.TIMESTAMP: convert_datetime,
    FIELD_TYPE.DATETIME: convert_datetime,
    FIELD_TYPE.TIME: convert_timedelta,
    FIELD_TYPE.DATE: convert_date,
    FIELD_TYPE.BLOB: through,
    FIELD_TYPE.TINY_BLOB: through,
    FIELD_TYPE.MEDIUM_BLOB: through,
    FIELD_TYPE.LONG_BLOB: through,
    FIELD_TYPE.STRING: through,
    FIELD_TYPE.VAR_STRING: through,
    FIELD_TYPE.VARCHAR: through,
    FIELD_TYPE.DECIMAL: Decimal,
    FIELD_TYPE.NEWDECIMAL: Decimal,
}

# for MySQLdb compatibility
conversions = encoders.copy()
conversions.update(decoders)
Thing2Literal = escape_str

encoders = {k: v for (k, v) in conversions.items() if type(k) is not int}
