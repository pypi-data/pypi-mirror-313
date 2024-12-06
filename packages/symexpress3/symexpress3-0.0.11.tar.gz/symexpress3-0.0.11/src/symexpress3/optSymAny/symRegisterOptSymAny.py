#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Registration any optimize for symexpress3

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

from symexpress3           import symtables
from symexpress3.optSymAny import optSymAnyArrayPower
from symexpress3.optSymAny import optSymAnyExpandArray
from symexpress3.optSymAny import optSymAnyRootToPrincipalRoot

#
# automatic called from symepxress3
#
def SymRegisterOptimize():
  """
  Register all the any optimize classes
  """
  symtables.RegisterTableEntry( 'optSymAny', optSymAnyArrayPower.OptSymAnyArrayPower()                   )
  symtables.RegisterTableEntry( 'optSymAny', optSymAnyExpandArray.OptSymAnyExpandArray()                 )
  symtables.RegisterTableEntry( 'optSymAny', optSymAnyRootToPrincipalRoot.OptSymAnyRootToPrincipalRoot() )

#
# Get all the modules from the optSymVariable, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the any optimizes
  """

  symModules = []

  symModules.append( optSymAnyArrayPower             )
  symModules.append( optSymAnyExpandArray            )
  symModules.append( optSymAnyRootToPrincipalRoot    )

  return symModules

if __name__ == '__main__':
  SymRegisterOptimize()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
