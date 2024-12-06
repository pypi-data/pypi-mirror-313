#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Acos function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
"""

import cmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncTrigonoBase

class SymFuncAcos( symFuncTrigonoBase.SymFuncTrigonoBase ):
  """
  Acos function
  """
  def __init__( self ):
    super().__init__()
    self._name      = "acos"
    self._desc      = "acos"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "acos(<x>)"


  def functionToValue( self, elem ):

    if self._checkCorrectFunction( elem ) != True:
      return None

    result = self._conversTableToArc( elem )
    if result != None:
      return result

    result = self._convertSinCosTanAtanSign( elem )
    if result != None:
      return result

    return None


  def _getValueSingle( self, dValue, dValue2 = None ):
    return cmath.acos( dValue )



#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check(  testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ) != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value}' )

  symTest = symexpress3.SymFormulaParser( 'acos( 1/2 )' )
  symTest.optimize()
  testClass = SymFuncAcos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, round( dValue, 10), "1 * 3^^-1 * pi", round( 1.0471975512, 10) )


  symTest = symexpress3.SymFormulaParser( 'acos( -1/2 )' )
  symTest.optimize()
  testClass = SymFuncAcos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, round( dValue, 10), "pi + (-1) *  acos( 1 * (1/2) )", round( 2.0943951024, 10) )


if __name__ == '__main__':
  Test( True )
