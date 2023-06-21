import json
import string

from GrammarDesc import GrammarDesc
from parser.MatchField import MatchField
from parser.Rule import Rule


def createRule(fields):
    res = []
    for field_item in fields:

        res += [MatchField(field_item[0], field_item[1], field_item[2], precede_separator=field_item[3], depends_on=field_item[4])]
    return Rule(GrammarDesc("dummy", res))

def testEquals(expected, actual):
    if expected == actual:
        return True

    if expected is None and actual is not None or expected is not None and actual is None:
        return False

    if len(expected) != len(actual):
        return False

    for key in expected:
        if key not in actual:
            return False
        if actual[key] != expected[key]:
            return False

    return True

def getjson(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data

def savejson(filename, data:string):
    f = open(filename, "w")
    f.write(data)
    f.close()