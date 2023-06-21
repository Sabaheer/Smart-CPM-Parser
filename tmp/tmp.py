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