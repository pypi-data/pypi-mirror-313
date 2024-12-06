#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Registration of function classes for symexpress3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from symexpress3 import symtables

from symexpress3.symfunc import symFuncCeilFloor
from symexpress3.symfunc import symFuncExp
from symexpress3.symfunc import symFuncAbs
from symexpress3.symfunc import symFuncFactorial
from symexpress3.symfunc import symFuncBinomial
from symexpress3.symfunc import symFuncAtan2
from symexpress3.symfunc import symFuncAtan
from symexpress3.symfunc import symFuncSin
from symexpress3.symfunc import symFuncCos
from symexpress3.symfunc import symFuncTan
from symexpress3.symfunc import symFuncSum
from symexpress3.symfunc import symFuncProduct
from symexpress3.symfunc import symFuncFallingFactorial
from symexpress3.symfunc import symFuncRisingFactorial
from symexpress3.symfunc import symFuncHypergeometric
from symexpress3.symfunc import symFuncLog
from symexpress3.symfunc import symFuncAsin
from symexpress3.symfunc import symFuncAcos

#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterFunctions():
  """
  Register all the function classes
  """
  symtables.RegisterTableEntry( 'function', symFuncCeilFloor.SymFuncCeil()      )
  symtables.RegisterTableEntry( 'function', symFuncCeilFloor.SymFuncFloor()     )
  symtables.RegisterTableEntry( 'function', symFuncExp.SymFuncExp()             )
  symtables.RegisterTableEntry( 'function', symFuncAbs.SymFuncAbs()             )
  symtables.RegisterTableEntry( 'function', symFuncFactorial.SymFuncFactorial() )
  symtables.RegisterTableEntry( 'function', symFuncBinomial.SymFuncBinomial()   )
  symtables.RegisterTableEntry( 'function', symFuncAtan2.SymFuncAtan2()         )
  symtables.RegisterTableEntry( 'function', symFuncAtan.SymFuncAtan()           )
  symtables.RegisterTableEntry( 'function', symFuncSin.SymFuncSin()             )
  symtables.RegisterTableEntry( 'function', symFuncCos.SymFuncCos()             )
  symtables.RegisterTableEntry( 'function', symFuncTan.SymFuncTan()             )
  symtables.RegisterTableEntry( 'function', symFuncSum.SymFuncSum()             )
  symtables.RegisterTableEntry( 'function', symFuncProduct.SymFuncProduct()     )
  symtables.RegisterTableEntry( 'function', symFuncFallingFactorial.SymFuncFallingFactorial() )
  symtables.RegisterTableEntry( 'function', symFuncRisingFactorial.SymFuncRisingFactorial()   )
  symtables.RegisterTableEntry( 'function', symFuncHypergeometric.SymFuncHypergeometric()     )
  symtables.RegisterTableEntry( 'function', symFuncLog.SymFuncLog()                           )
  symtables.RegisterTableEntry( 'function', symFuncAsin.SymFuncAsin()                         )
  symtables.RegisterTableEntry( 'function', symFuncAcos.SymFuncAcos()                         )


#
# Get all the modules from the functions, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the functions
  """

  symModules = []

  symModules.append( symFuncCeilFloor        )
  symModules.append( symFuncExp              )
  symModules.append( symFuncAbs              )
  symModules.append( symFuncFactorial        )
  symModules.append( symFuncBinomial         )
  symModules.append( symFuncAtan2            )
  symModules.append( symFuncAtan             )
  symModules.append( symFuncSin              )
  symModules.append( symFuncCos              )
  symModules.append( symFuncTan              )
  symModules.append( symFuncSum              )
  symModules.append( symFuncProduct          )
  symModules.append( symFuncFallingFactorial )
  symModules.append( symFuncRisingFactorial  )
  symModules.append( symFuncHypergeometric   )
  symModules.append( symFuncLog              )
  symModules.append( symFuncAsin             )
  symModules.append( symFuncAcos             )


  return symModules

if __name__ == '__main__':
  SymRegisterFunctions()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
