#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (C) 2021 Gien van den Enden - swvandenenden@gmail.com

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

# Different between functionTable and optSymFunction is functionTable can calculate a value from a function, optSymFunction cannot
functionTable       = {} # dictionary of functions of type SymFuncBase     , see symexpress3.symfunc.symRegisterFunctions
optimizeTable       = {} # dictionary of optimize classes for SymExpress   , see symexpress3.optimize.symRegisterOptimze
optSymNumberTable   = {} # dictionary of optimize classes for SymNumber
optSymVariableTable = {} # dictionary of optimize classes for SymVariable
optSymFunctionTable = {} # dictionary of optimize classes for SymFunction
optSymAnyTable      = {} # dictionary of optimize classes for any type, last resort if the optimize not fit in 1 of the above

fixedVariables      = {} # dictionary of fixed variables, see symtools.py


def RegisterTableEntry( cType, oEntry ):
  """
  Register the given optimize class
  """

  # pylint: disable=multiple-statements
  if   cType == "optSymNumber"   :  optSymNumberTable[   oEntry.name ] = oEntry
  elif cType == "optSymVariable" :  optSymVariableTable[ oEntry.name ] = oEntry
  elif cType == "optSymFunction" :  optSymFunctionTable[ oEntry.name ] = oEntry
  elif cType == "optimize"       :  optimizeTable[       oEntry.name ] = oEntry
  elif cType == "function"       :  functionTable[       oEntry.name ] = oEntry
  elif cType == "optSymAny"      :  optSymAnyTable[      oEntry.name ] = oEntry
  else:
    raise NameError( f'RegisterTableEntry, unknown type: {cType}' )
