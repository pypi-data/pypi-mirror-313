#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Factorial function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Factorial

"""

import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase


class SymFuncFactorial( symFuncBase.SymFuncBase ):
  """
  Factorial function, x!
  """
  def __init__( self ):
    super().__init__()
    self._name        = "factorial"
    self._desc        = "Factorial x!"
    self._minparams   = 1    # minimum number of parameters
    self._maxparams   = 1    # maximum number of parameters
    self._syntax      = "factorial(<n>)"
    self._synExplain  = "factorial(<n>) = n!"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""
    output += "<mfenced separators=''>"
    output += elem.elements[ 0 ].mathMl()
    output += "</mfenced>"
    output += '<mo>!</mo>'

    return [ '()' ], output

  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    elem2 = elem.elements[ 0 ]

    # x!
    if not isinstance ( elem2, symexpress3.SymNumber ):
      return None

    if elem2.power != 1:
      return None

    if elem2.factSign == -1:
      return None

    if elem2.factDenominator != 1:
      return None

    dValue  = math.factorial( elem2.getValue() )
    elemnew = symexpress3.SymFormulaParser( str( dValue ))

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew

  def _getValueSingle( self, dValue, dValue2 = None ):
    return math.factorial( dValue )

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    dValue     = round( dValue    , 10 )
    if dValueCalc != None:
      dValueCalc = round( dValueCalc, 10 )
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'factorial( 4 )' )
  symTest.optimize()
  testClass = SymFuncFactorial()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "24", 24 )

if __name__ == '__main__':
  Test( True )
