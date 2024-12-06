from sys import exit
from types import FunctionType

from pybrary.command import parse_args
from pybrary import commands


def main():
    a, k = parse_args()

    try:
        f, *a = a
    except ValueError:
        f = ''

    try:
        cmd = getattr(commands, f)
    except AttributeError:
        print('Available Pybrary Commands :')
        for k, v in vars(commands).items():
            if isinstance(v, FunctionType):
                print('   ', k)
        exit()

    try:
        success, output = cmd(*a, **k)
    except Exception as x:
        success, output = False, str(x)

    if success:
        print(output)
    else:
        exit(f' ! {output}')
