from sys import version_info as v


if v.minor >= 13:
    from re import PatternError
else:
    from re import error as PatternError

