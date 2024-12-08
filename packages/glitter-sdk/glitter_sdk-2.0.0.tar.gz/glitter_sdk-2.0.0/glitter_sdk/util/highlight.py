from typing import List
def highlight_prepare(fields: List[str]):
    place_hold = ",".join(["\"{}\""] * len(fields))
    option = """{"highlight":{ "style":"html","fields":[""" + place_hold.format(*fields) + """]}}"""
    option = option.translate({ord('"'): "\""})
    # return "{}{}{}".format("/*+ SET_VAR( bleve_option=", option, ")*/ ")
    return "/*+ SET_VAR(full_text_option='%s')*/" % option
