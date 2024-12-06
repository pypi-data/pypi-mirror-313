"""
Initialization of the functions and modules symexpress3
"""

from .symexpress3 import *
from .symtools    import *
from .version     import __version__,__author__,__copyright__,__credits__,__license__,__maintainer__,__email__,__status__


from .symfunc.symRegisterFunctions              import SymRegisterFunctions
from .optimize.symRegisterOptimize              import SymRegisterOptimize
from .optSymNumber.symRegisterOptSymNumber      import SymRegisterOptimize as SymRegisterOptSymNumber
from .optSymVariable.symRegisterOptSymVariable  import SymRegisterOptimize as SymRegisterOptSymVariable
from .optSymFunction.symRegisterOptSymFunction  import SymRegisterOptimize as SymRegisterOptSymFunction
from .optSymAny.symRegisterOptSymAny            import SymRegisterOptimize as SymRegisterOptSymAny


SymRegisterFunctions()
SymRegisterOptimize()
SymRegisterOptSymNumber()
SymRegisterOptSymVariable()
SymRegisterOptSymFunction()
SymRegisterOptSymAny()

# print( "Symexpress3.__init__ name: " + __name__ )
