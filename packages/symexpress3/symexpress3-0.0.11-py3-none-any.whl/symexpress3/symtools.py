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
import math

from symexpress3 import symtables
from symexpress3 import symexpress3

# pylint: disable=global-variable-not-assigned
globalVariableLetter  = "n"  # the letter for the generated unique variable
globalVariableCounter = 1    # the current unique number, rises every time a variable is get

def VariableGenerateGet():
  """
  Get a unique generated variable.
  Format is fixed letter with a unique number
  """
  # pylint: disable=global-statement
  global globalVariableLetter, globalVariableCounter

  varName = globalVariableLetter + str( globalVariableCounter )
  globalVariableCounter += 1
  return varName

def VariableGenerateReset():
  """
  Reset the variable counter.
  Is for test scripts
  """
  # pylint: disable=global-statement
  global globalVariableCounter
  globalVariableCounter = 1

def VariableGenerateSet( newCurrentNumber ):
  """
  Set the variable counter to the given number.
  Is for test scripts
  """
  # pylint: disable=global-statement
  global globalVariableCounter
  globalVariableCounter = newCurrentNumber



def GetAllOptimizeActions():
  """
  Get all the optimize actions in a dictionary [key]=description
  """
  result = {}
  for key, value  in symtables.optSymAnyTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymNumberTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymVariableTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymFunctionTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optimizeTable.items():
    result[ key ] = value.description

  for key, value  in symtables.functionTable.items():
    result[ "functionToValue_" + key ] = value.description

  # fixed values
  result[ "functionToValues" ] = 'Convert functions to values'
  result[ "setOnlyOne"       ] = "All radicals are principal"

  return result


def GetAllFunctions():
  """
  Get all the functions in a dictionary [key]=description
  """
  result = {}
  for objFunc in symtables.functionTable.values():
    key = objFunc.syntax
    if key == None:
      key = objFunc.name
    result[ key ] = objFunc.description

  return result


def GetFixedVariables():
  """
  Get dictionary of fixed defined variables ( [variable name] = description
  """
  if len( symtables.fixedVariables ) > 0:
    return symtables.fixedVariables

  symtables.fixedVariables[ "pi"       ] = "π"
  symtables.fixedVariables[ "i"        ] = "Imaginary number"
  symtables.fixedVariables[ "e"        ] = "Euler's number"
  symtables.fixedVariables[ "infinity" ] = "∞"

  return symtables.fixedVariables


def ConvertToSymexpress3String( varData ):
  """
  Convert given data into a symexpress3 string
  """

  # print( f"Start varData: {varData}" )

  if isinstance( varData, str ):
    if '.' in varData :
      try:
        varData = float( varData )
      except: # pylint: disable=bare-except)
        pass # so not a float

  if isinstance( varData, float ):
    frac, whole = math.modf( varData )

    frac = round( frac, 15 ) # python use 17 digits, 15 for correct rounding

    factStr = str( frac )
    iPoint  = factStr.find('.')
    if iPoint >= 0:
      factStr = factStr[ (iPoint + 1): ]
    else:
      factStr = ""

    varData = str( int(whole) )
    if len( factStr ) > 0:
      varData += factStr + "/1" + "0" * len( factStr )

  if isinstance( varData, int ):
    varData = str( varData )

  # check on correct symexpress3 string
  try:
    symexpress3.SymFormulaParser( varData )
  except Exception as exceptAll:
    # pylint: disable=raise-missing-from
    raise NameError( f"'{varData}' is not a valid symexpress3 string, error: {str(exceptAll)}" )


  # print( f"End varData: {varData}" )

  return varData
