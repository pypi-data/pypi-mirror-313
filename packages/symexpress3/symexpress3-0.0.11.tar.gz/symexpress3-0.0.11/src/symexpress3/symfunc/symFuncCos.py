#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Cos function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Sine_and_cosine
    https://en.wikipedia.org/wiki/Trigonometric_functions
"""

import cmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncTrigonoBase

class SymFuncCos( symFuncTrigonoBase.SymFuncTrigonoBase ):
  """
  Cos function
  """
  def __init__( self ):
    super().__init__()
    self._name         = "cos"
    self._desc         = "cos"
    self._minparams    = 1    # minimum number of parameters
    self._maxparams    = 1    # maximum number of parameters
    self._syntax       = "cos(<rad>)"


  def functionToValue( self, elem ):

    if self._checkCorrectFunction( elem ) != True:
      return None

    result = self._convertFuncSinCosTan( elem )
    if result != None:
      return result

    result = self._convertSinCosTanAtanSign( elem )
    if result != None:
      return result

    result = self._convertSinCosAtan( elem )
    if result != None:
      return result

    result = self._optimizeSinCosTan( elem )
    if result != None:
      # print( f"4: {str(elem)} - {str(result)}" )

      return result

    return None


  def _getValueSingle( self, dValue, dValue2 = None ):
    return cmath.cos( dValue )


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

  symTest = symexpress3.SymFormulaParser( 'cos( pi / 4 )' )
  symTest.optimize()
  testClass = SymFuncCos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "2^^(1/2) * 2^^-1", 0.7071067811865476 )


  symTest = symexpress3.SymFormulaParser( 'cos( -2 )' )
  symTest.optimize()
  testClass = SymFuncCos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "cos( 2 )", -0.4161468365471424 )


  symTest = symexpress3.SymFormulaParser( 'cos( atan( 2 ) )' )
  symTest.optimize()
  testClass = SymFuncCos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  # _Check( testClass, symTest, value, dValue, "5^^(-1/2)", 0.4472135955 )
  _Check( testClass, symTest, value, dValue, "(1/5) * 5^^(1/2)", 0.4472135955 )


  symTest = symexpress3.SymFormulaParser( 'cos( 7 pi )' )
  symTest.optimize()
  testClass = SymFuncCos()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "cos( 1 * pi )", -1 )


  # symTest = symexpress3.SymFormulaParser( 'cos(atan(x)/3)' )
  # symTest.optimize()
  # testClass = SymFuncCos()
  # value     = testClass.funcionToComplexValue( symTest.elements[ 0 ] )
  # dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  # _Check( testClass, symTest, value, dValue, "(1/2) * ( cos(  atan( x ) ) + i *  sin(  atan( x ) ))^^(1/3) + (1/2) * ( cos(  atan( x ) ) + (-1) * i *  sin(  atan( x ) ))^^(1/3)", None)


if __name__ == '__main__':
  Test( True )
