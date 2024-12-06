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

from symexpress3                import symtables
from symexpress3.optSymVariable import optSymVariableI
from symexpress3.optSymVariable import optSymVariableRootIToSinCos

#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterOptimize():
  """
  Register all the variable optimize classes
  """
  symtables.RegisterTableEntry( 'optSymVariable', optSymVariableI.OptSymVariableI()                         )
  symtables.RegisterTableEntry( 'optSymVariable', optSymVariableRootIToSinCos.OptSymVariableRootIToSinCos() )

#
# Get all the modules from the optSymVariable, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the variable optimizes
  """

  symModules = []

  symModules.append( optSymVariableI             )
  symModules.append( optSymVariableRootIToSinCos )

  return symModules

if __name__ == '__main__':
  SymRegisterOptimize()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
