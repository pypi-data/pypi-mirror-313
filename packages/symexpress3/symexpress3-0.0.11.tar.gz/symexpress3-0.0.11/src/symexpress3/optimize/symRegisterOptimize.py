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

from symexpress3          import symtables
from symexpress3.optimize import optimizeSinTwoCosTwo
from symexpress3.optimize import optimizeMultiply
from symexpress3.optimize import optimizeAdd
from symexpress3.optimize import optimizePower
from symexpress3.optimize import optimizeOnlyOneRoot
from symexpress3.optimize import optimizeSplitDenominator
from symexpress3.optimize import optimizeNestedRadicals
from symexpress3.optimize import optimizeImaginairDenominator
from symexpress3.optimize import optimizeExpandArrays
from symexpress3.optimize import optimizeUnnestingRadicals
from symexpress3.optimize import optimizeRootToPrincipalRoot
from symexpress3.optimize import optimizeRootOfImagNumToCosISin
from symexpress3.optimize import optimizePowerArrays
from symexpress3.optimize import optimizeUnnestingCubitRoot

#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterOptimize():
  """
  Register all the optimize action classes
  """
  symtables.RegisterTableEntry( 'optimize', optimizeSinTwoCosTwo.OptimizeSinTwoCosTwo()                     )
  symtables.RegisterTableEntry( 'optimize', optimizeMultiply.OptimizeMultiply()                             )
  symtables.RegisterTableEntry( 'optimize', optimizeAdd.OptimizeAdd()                                       )
  symtables.RegisterTableEntry( 'optimize', optimizePower.OptimizePower()                                   )
  symtables.RegisterTableEntry( 'optimize', optimizeOnlyOneRoot.OptimizeOnlyOneRoot()                       )
  symtables.RegisterTableEntry( 'optimize', optimizeSplitDenominator.OptimizeSplitDenominator()             )
  symtables.RegisterTableEntry( 'optimize', optimizeNestedRadicals.OptimizeNestedRadicals()                 )
  symtables.RegisterTableEntry( 'optimize', optimizeImaginairDenominator.OptimizeImaginairDenominator()     )
  symtables.RegisterTableEntry( 'optimize', optimizeExpandArrays.OptimizeExpandArrays()                     )
  symtables.RegisterTableEntry( 'optimize', optimizeUnnestingRadicals.OptimizeUnnestingRadicals()           )
  symtables.RegisterTableEntry( 'optimize', optimizeRootToPrincipalRoot.OptimizeRootToPrincipalRoot()       )
  symtables.RegisterTableEntry( 'optimize', optimizeRootOfImagNumToCosISin.OptimizeRootOfImagNumToCosISin() )
  symtables.RegisterTableEntry( 'optimize', optimizePowerArrays.OptimizePowerArrays()                       )
  symtables.RegisterTableEntry( 'optimize', optimizeUnnestingCubitRoot.OptimizeUnnestingCubitRoot()         )


#
# Get all the modules from the functions, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the optimize actions
  """

  symModules = []

  symModules.append( optimizeSinTwoCosTwo           )
  symModules.append( optimizeMultiply               )
  symModules.append( optimizeAdd                    )
  symModules.append( optimizePower                  )
  symModules.append( optimizeOnlyOneRoot            )
  symModules.append( optimizeSplitDenominator       )
  symModules.append( optimizeNestedRadicals         )
  symModules.append( optimizeImaginairDenominator   )
  symModules.append( optimizeExpandArrays           )
  symModules.append( optimizeUnnestingRadicals      )
  symModules.append( optimizeRootToPrincipalRoot    )
  symModules.append( optimizeRootOfImagNumToCosISin )
  symModules.append( optimizePowerArrays            )
  symModules.append( optimizeUnnestingCubitRoot     )


  return symModules

if __name__ == '__main__':
  SymRegisterOptimize()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
