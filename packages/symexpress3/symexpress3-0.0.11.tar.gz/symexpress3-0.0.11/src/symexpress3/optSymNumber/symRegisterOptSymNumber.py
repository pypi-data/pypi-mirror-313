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

from symexpress3              import symtables
from symexpress3.optSymNumber import optSymNumberPower
from symexpress3.optSymNumber import optSymNumberNegRootToI
from symexpress3.optSymNumber import optSymNumberRadicalDenominatorToCounter
from symexpress3.optSymNumber import optSymNumberOnlyOneRoot

#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterOptimize():
  """
  Register all the number optimize classes
  """

  symtables.RegisterTableEntry( 'optSymNumber', optSymNumberPower.OptSymNumberPower()           )
  symtables.RegisterTableEntry( 'optSymNumber', optSymNumberNegRootToI.OptSymNumberNegRootToI() )
  symtables.RegisterTableEntry( 'optSymNumber', optSymNumberRadicalDenominatorToCounter.OptSymNumberRadicalDenominatorToCounter() )
  symtables.RegisterTableEntry( 'optSymNumber', optSymNumberOnlyOneRoot.OptSymNumberOnlyOneRoot() )


#
# Get all the modules from the optSymNumber, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the number optimizes
  """
  symModules = []

  symModules.append( optSymNumberPower                       )
  symModules.append( optSymNumberNegRootToI                  )
  symModules.append( optSymNumberRadicalDenominatorToCounter )
  symModules.append( optSymNumberOnlyOneRoot                 )

  return symModules

if __name__ == '__main__':
  SymRegisterOptimize()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
