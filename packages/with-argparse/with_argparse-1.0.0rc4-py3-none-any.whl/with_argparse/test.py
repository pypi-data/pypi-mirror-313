from dataclasses import dataclass

from configure_argparse import WithArgparse
from with_argparse.impl import with_dataclass


@dataclass
class ABCD:
    my_type2: int
    my_type: int = 3

@with_dataclass(dataclass=ABCD)
def func(inp: ABCD):
    return inp

print(func())
