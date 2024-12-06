#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ceil and Floor functions for Sym Express 3

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


    https://en.wikipedia.org/wiki/Floor_and_ceiling_functions
"""

import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase


class SymFuncCeil( symFuncBase.SymFuncBase ):
  """
  Ceil function, round to the highest integer
  """
  def __init__( self ):
    super().__init__()
    self._name      = "ceil"
    self._desc      = "Round to the highest integer"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "ceil(<x>)"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += "<mfenced  open='&lceil;' close='&rceil;'>"
    output += "<mtable>"

    output += "<mtr>"
    output += "<mtd>"
    output += elem.elements[ 0 ].mathMl()
    output += "</mtd>"
    output += "</mtr>"

    output += "</mtable>"
    output += "</mfenced>"

    return [], output

  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    # array not supported, use expandArray
    if isinstance ( elem, symexpress3.SymArray ):
      return None

    # round up to the first integer
    dVars = elem.getVariables()
    for key in dVars.items():
      # if (key != "e" and key != "pi" ):
      if not key in ("e", "pi"):
        return None

    try:
      dValue  = elem.elements[ 0 ].getValue()
    except: # pylint: disable=bare-except
      return None

    # array not supported, use expandArray
    if isinstance( dValue, list ):
      return None

    if isinstance( dValue, complex ):
      return None

    dValue  = math.ceil( dValue )
    elemnew = symexpress3.SymFormulaParser( str( dValue ))

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew

  def _getValueSingle( self, dValue, dValue2 = None ):
    return math.ceil( dValue )


class SymFuncFloor( symFuncBase.SymFuncBase ):
  """
  Floor function, round to the lowest integer
  """
  def __init__( self ):
    super().__init__()
    self._name      = "floor"
    self._desc      = "Round to the lowest integer"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "floor(<x>)"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += "<mfenced  open='&lfloor;' close='&rfloor;'>"
    output += "<mtable>"

    output += "<mtr>"
    output += "<mtd>"
    output += elem.elements[ 0 ].mathMl()
    output += "</mtd>"
    output += "</mtr>"

    output += "</mtable>"
    output += "</mfenced>"

    return [], output

  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    # array not supported, use expandArray
    if isinstance( elem, symexpress3.SymArray ):
      return None

    # round to the lowest integer
    dVars = elem.getVariables()
    for key in dVars.items():
      # if (key != "e" and key != "pi" ):
      if not key in ("e", "pi"):
        return None

    try:
      dValue  = elem.elements[ 0 ].getValue()
    except: # pylint: disable=bare-except
      return None

    # array not supported, use expandArray
    if isinstance( dValue, list ):
      return None

    if isinstance( dValue, complex ):
      return None

    dValue  = math.floor( dValue )
    elemnew = symexpress3.SymFormulaParser( str( dValue ))

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew

  def _getValueSingle( self, dValue, dValue2 = None ):
    return math.floor( dValue )

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    dValue     = round( dValue    , 10 )
    dValueCalc = round( dValueCalc, 10 )
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or dValue != dValueCalc :
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  # 5/3 = 1.666666
  symTest = symexpress3.SymFormulaParser( 'ceil( 5 /3' )
  symTest.optimize()
  testClass = SymFuncCeil()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "2", 2 )


  symTest = symexpress3.SymFormulaParser( 'floor( 5 /3' )
  symTest.optimize()

  floor  = SymFuncFloor()
  value  = floor.functionToValue( symTest.elements[ 0 ] )
  dValue = floor.getValue(        symTest.elements[ 0 ] )

  _Check( floor, symTest, value, dValue, "1", 1 )


if __name__ == '__main__':
  Test( True )
