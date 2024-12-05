from typing import Final

from colt import ColtBuilder

from harbory.constants import COLT_ARGSKEY, COLT_TYPEKEY

COLT_BUILDER: Final = ColtBuilder(typekey=COLT_TYPEKEY, argskey=COLT_ARGSKEY)
