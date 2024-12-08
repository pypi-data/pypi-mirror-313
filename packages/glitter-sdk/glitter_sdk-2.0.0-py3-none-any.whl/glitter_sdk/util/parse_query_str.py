from attrs import asdict, define, make_class, Factory

_reserved_chars = {}
_reserved_chars[ord("+")] = "\\+"
_reserved_chars[ord("-")] = "\\-"
_reserved_chars[ord("=")] = "\\="
_reserved_chars[ord("&")] = "\\&"
_reserved_chars[ord("|")] = "\\|"
_reserved_chars[ord(">")] = "\\>"
_reserved_chars[ord("<")] = "\\<"
_reserved_chars[ord("!")] = "\\!"
_reserved_chars[ord("(")] = "\\("
_reserved_chars[ord(")")] = "\\)"
_reserved_chars[ord("{")] = "\\{"
_reserved_chars[ord("}")] = "\\}"
_reserved_chars[ord("[")] = "\\["
_reserved_chars[ord("]")] = "\\]"
_reserved_chars[ord("^")] = "\\^"
_reserved_chars[ord('"')] = "\\"
_reserved_chars[ord("~")] = "\\~"
_reserved_chars[ord("*")] = "\\*"
_reserved_chars[ord("?")] = "\\?"
_reserved_chars[ord(":")] = "\\:"
_reserved_chars[ord("\\")] = "\\\\"
_reserved_chars[ord("/")] = "\/"
_reserved_chars[ord(" ")] = "\ "

_escape_char = {}
_escape_char[ord("\\")] = "\\\\"


def reserve_query(value, mapping=None):
    """escapes *value* without adding quote.

    Value should be unicode
    """
    return value.translate(_reserved_chars)


def escape_query(value, mapping=None):
    """escapes *value* without adding quote.

    Value should be unicode
    """
    return value.translate(_escape_char)


def query_string_prepare(queries: list):
    query_string = []
    for query in queries:
        query_string.append(str(query))

    rst = " ".join(query_string)
    return rst


@define
class Query:
    def prepare_query(self):
        pass


@define
class MatchQuery:
    field: str
    query: str
    boost: float = 1.0

    def prepare_query(self):
        rst = "{}:{}^{}".format(self.field, reserve_query(self.query), self.boost)
        return rst

    def __str__(self):
        return self.prepare_query()


@define
class MatchPhraseQuery:
    field: str
    query: str
    boost: float = 1.0

    def prepare_query(self):
        if self.field:
            return "{}:{}^{}".format(self.field, "\"" + self.query + "\"", self.boost)
        else:
            return "{}^{}".format("\"" + self.query + "\"", self.boost)

    def __str__(self):
        return self.prepare_query()


@define
class RegexpQuery:
    field: str
    query: str
    boost: float = 1.0

    def prepare_query(self):
        return "{}:{}^{}".format(self.field, "/" + self.query + "/", self.boost)

    def __str__(self):
        return self.prepare_query()


@define
class NumericRangeQuery:
    field: str
    operator: str
    value: int
    boost: float = 1.0

    def prepare_query(self):
        return "{}:{}{}^{}".format(self.field, self.operator, self.value, self.boost)

    def __str__(self):
        return self.prepare_query()


@define
class DateRangeQuery:
    field: str
    operator: str
    value: str
    boost: float = 1.0

    def prepare_query(self):
        return "{}:{}\"{}\"^{}".format(self.field, self.operator, self.value, self.boost)

    def __str__(self):
        return self.prepare_query()
